-- ====================================================================
-- PROYECTO: Telecom Churn Intelligence
-- CAPA: Feature Store / Matriz de Entrenamiento
-- TABLA DESTINO: `portafolio-511501.CUSTOMER_CHURN.telco_churn_features`
-- ====================================================================


CREATE OR REPLACE TABLE `portafolio-511501.CUSTOMER_CHURN.telco_churn_features` AS

WITH raw_cleaned AS (
  SELECT
    customerid AS customer_id,
    
    -- Demografía
    gender,
    CASE TRIM(LOWER(senior_citizen))
      WHEN 'yes' THEN 1
      WHEN 'no' THEN 0
      ELSE NULL
      END AS senior_citizen,
    partner,
    dependents,
    
    -- Antigüedad y Ubicación
    SAFE_CAST(tenure_months AS INT64) AS tenure_months,
    COALESCE(country, 'United States') AS country,
    COALESCE(`state`, 'California') AS state,
    COALESCE(city, 'Unknown') AS city,
    zip_code,
    CAST(latitude AS FLOAT64) AS latitude,
    CAST(longitude AS FLOAT64) AS longitude,
    
    -- Servicios Contratados
    phone_service,
    multiple_lines,
    internet_service,
    online_security,
    online_backup,
    device_protection,
    tech_support,
    streaming_tv,
    streaming_movies,
    
    -- Contrato y Facturación
    contract,
    paperless_billing,
    payment_method,
    
    -- Cargos Financieros (Manejo de nulos y espacios en blanco)
    CAST(monthly_charges AS FLOAT64) AS monthly_charges,
    CASE 
      WHEN TRIM(total_charges) = '' OR total_charges IS NULL THEN 0.0
      ELSE SAFE_CAST(TRIM(total_charges) AS FLOAT64)
    END AS total_charges,
    
    -- Valor del Cliente (CLTV)
    SAFE_CAST(cltv AS FLOAT64) AS cltv,
    
    -- Variable Objetivo (Target)
    -- En IBM dataset: 'churn_value' es 1 o 0 (o 'churn_label' Yes/No)
    CASE 
      WHEN churn_value = '1' OR LOWER(churn_label) = 'yes' THEN 1 
      ELSE 0 
    END AS churn_target

  FROM `portafolio-511501.CUSTOMER_CHURN.telco_customer_churn_raw`
),

engineered_features AS (
  SELECT
    *,
    
    -- 1. Ratio Financiero: Relación entre cargo actual y el promedio histórico mensual
    CASE 
      WHEN tenure_months > 0 THEN ROUND(monthly_charges / (total_charges / tenure_months), 4)
      ELSE 1.0 
    END AS monthly_to_avg_charge_ratio,
    
    -- 2. Conteo de Servicios de Valor Agregado (VAS Bundle Count)
    (
      CASE WHEN online_security = 'Yes' THEN 1 ELSE 0 END +
      CASE WHEN online_backup = 'Yes' THEN 1 ELSE 0 END +
      CASE WHEN device_protection = 'Yes' THEN 1 ELSE 0 END +
      CASE WHEN tech_support = 'Yes' THEN 1 ELSE 0 END +
      CASE WHEN streaming_tv = 'Yes' THEN 1 ELSE 0 END +
      CASE WHEN streaming_movies = 'Yes' THEN 1 ELSE 0 END
    ) AS total_vas_services,
    
    -- 3. Flag de Riesgo Contractual (Month-to-month tiene 4x probabilidad de fuga)
    CASE WHEN contract = 'Month-to-month' THEN 1 ELSE 0 END AS is_month_to_month,
    
    -- 4. Flag de Dependencia Tecnológica (Fibra óptica sin soporte técnico suele generar churn alto)
    CASE 
      WHEN internet_service = 'Fiber optic' AND tech_support = 'No' THEN 1 
      ELSE 0 
    END AS high_risk_fiber_no_support,

    -- 5. Segmento de Antigüedad (Cohort Tenures)
    CASE 
      WHEN tenure_months <= 12 THEN '0-12_months'
      WHEN tenure_months <= 24 THEN '13-24_months'
      WHEN tenure_months <= 48 THEN '25-48_months'
      ELSE '49+_months'
    END AS tenure_cohort

  FROM raw_cleaned
)

SELECT * FROM engineered_features;