import os
from pathlib import Path
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import joblib
import shap
from dotenv import load_dotenv

st.set_page_config(
    page_title="Diagnóstico & Causas | Telecom Churn",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 Diagnóstico Operativo & Explicabilidad de Fuga")
st.markdown(
    """
    Identificación de causas raíz de cancelación mediante análisis multivariable 
    y explicabilidad algorítmica (**Explainable AI - SHAP**).
    """
)

# -------------------------------------------------------------
# Carga de Datos y Artefactos con Caché
# -------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent.parent

@st.cache_data
def load_dataset():
    load_dotenv(BASE_DIR / ".env")
    try:
        from google.cloud import bigquery
        project_id = os.getenv("GCP_PROJECT_ID")
        dataset_id = os.getenv("GCP_DATASET_ID")
        if project_id and dataset_id:
            client = bigquery.Client(project=project_id)
            query = f"SELECT * FROM `{project_id}.{dataset_id}.telco_churn_features`"
            return client.query(query).to_dataframe()
    except Exception:
        pass

    raw_path = BASE_DIR / "data/raw/Telco_customer_churn.xlsx"
    if raw_path.exists():
        df_raw = pd.read_excel(raw_path)
        df_raw["monthly_charges"] = pd.to_numeric(df_raw["Monthly Charges"], errors="coerce")
        df_raw["total_charges"] = pd.to_numeric(df_raw["Total Charges"], errors="coerce").fillna(0)
        df_raw["tenure_months"] = df_raw["Tenure Months"]
        df_raw["churn_target"] = df_raw["Churn Value"]
        df_raw["contract"] = df_raw["Contract"]
        df_raw["internet_service"] = df_raw["Internet Service"]
        df_raw["tech_support"] = df_raw["Tech Support"]
        df_raw["payment_method"] = df_raw["Payment Method"]
        return df_raw

    return pd.DataFrame()

@st.cache_resource
def load_model_and_explainer():
    candidate_paths = [
        BASE_DIR / "outputs/models/telecom_churn_pipeline.joblib",
        Path("outputs/models/telecom_churn_pipeline.joblib").resolve(),
    ]
    model_path = next((p for p in candidate_paths if p.exists()), None)
    if not model_path:
        return None, None, None, None

    pipeline = joblib.load(model_path)
    preprocessor = pipeline.named_steps["preprocessor"]
    xgb_model = pipeline.named_steps["classifier"]
    explainer = shap.TreeExplainer(xgb_model)
    
    feature_names = [
        f.replace("num__", "").replace("cat__", "") 
        for f in preprocessor.get_feature_names_out()
    ]
    return pipeline, preprocessor, explainer, feature_names

df = load_dataset()
pipeline, preprocessor, explainer, feature_names = load_model_and_explainer()

if df.empty:
    st.error("No se pudo cargar la matriz de clientes. Verifica la conexión a BigQuery.")
    st.stop()

# -------------------------------------------------------------
# Pestañas de Navegación
# -------------------------------------------------------------
tab_eda, tab_shap_global, tab_shap_local = st.tabs([
    "📊 Factores Operativos (EDA)", 
    "🌐 Drivers Globales (SHAP Beeswarm)", 
    "🎯 Diagnóstico Individual (Waterfall)"
])

# -------------------------------------------------------------
# TAB 1: Factores Operativos de Cartera
# -------------------------------------------------------------
with tab_eda:
    st.subheader("Vulnerabilidades Críticas en el Viaje del Cliente")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Tasa de Churn por Contrato
        df_contract = df.groupby("contract")["churn_target"].agg(
            total_clientes="count",
            tasa_churn="mean"
        ).reset_index()
        
        fig_contract = px.bar(
            df_contract,
            x="contract",
            y="tasa_churn",
            text=df_contract["tasa_churn"].apply(lambda x: f"{x:.1%}"),
            title="Tasa de Cancelación según Tipo de Contrato",
            labels={"contract": "Tipo de Contrato", "tasa_churn": "Tasa de Churn"},
            color="tasa_churn",
            color_continuous_scale="Reds"
        )
        fig_contract.update_layout(height=380, showlegend=False, yaxis_tickformat=".0%")
        st.plotly_chart(fig_contract, use_container_width=True)
        st.caption("Los contratos Mes a Mes concentran una fuga superior al 42%, frente al <3% en contratos a 2 años.")

    with col2:
        # Cruce Crítico: Internet vs Soporte Técnico
        df_tech = df.groupby(["internet_service", "tech_support"])["churn_target"].mean().reset_index()
        
        fig_tech = px.bar(
            df_tech,
            x="internet_service",
            y="churn_target",
            color="tech_support",
            barmode="group",
            text=df_tech["churn_target"].apply(lambda x: f"{x:.1%}"),
            title="Efecto Protector del Soporte Técnico por Tecnología",
            labels={"internet_service": "Tecnología", "churn_target": "Tasa de Churn", "tech_support": "Soporte Técnico"},
            color_discrete_sequence=["#d62728", "#1f77b4", "#7f7f7f"]
        )
        fig_tech.update_layout(height=380, yaxis_tickformat=".0%")
        st.plotly_chart(fig_tech, use_container_width=True)
        st.caption("La Fibra Óptica sin soporte técnico alcanza casi 50% de fuga; con soporte, cae al ~22%.")

    col3, col4 = st.columns(2)
    
    with col3:
        # Cohorte de Antigüedad
        if "tenure_cohort" in df.columns:
            order_cohort = ["0-12_months", "13-24_months", "25-48_months", "49+_months"]
            df_cohort = df.groupby("tenure_cohort")["churn_target"].mean().reindex(order_cohort).reset_index()
            fig_cohort = px.line(
                df_cohort,
                x="tenure_cohort",
                y="churn_target",
                markers=True,
                title="Tasa de Fuga por Cohorte de Antigüedad",
                labels={"tenure_cohort": "Antigüedad", "churn_target": "Tasa de Churn"}
            )
            fig_cohort.update_traces(line_color="#e377c2", line_width=3, marker_size=8)
            fig_cohort.update_layout(height=350, yaxis_tickformat=".0%")
            st.plotly_chart(fig_cohort, use_container_width=True)
            st.caption("Casi el 48% de clientes en su primer año abandonan el servicio; luego la inercia estabiliza la cartera.")

    with col4:
        # Método de Pago
        df_pay = df.groupby("payment_method")["churn_target"].mean().sort_values(ascending=False).reset_index()
        fig_pay = px.bar(
            df_pay,
            x="payment_method",
            y="churn_target",
            text=df_pay["churn_target"].apply(lambda x: f"{x:.1%}"),
            title="Tasa de Fuga por Método de Pago",
            labels={"payment_method": "Método de Pago", "churn_target": "Tasa de Churn"},
            color="churn_target",
            color_continuous_scale="Purples"
        )
        fig_pay.update_layout(height=350, showlegend=False, yaxis_tickformat=".0%")
        st.plotly_chart(fig_pay, use_container_width=True)
        st.caption("Cheque electrónico presenta la mayor deserción (~45%) por fricción manual; PAC/PAT reducen la salida a la mitad.")

# -------------------------------------------------------------
# TAB 2: Explicabilidad Global con SHAP
# -------------------------------------------------------------
with tab_shap_global:
    st.subheader("Distribución Global de Importancia e Impacto (SHAP Beeswarm)")
    st.markdown(
        """
        Cada punto representa un cliente. La posición horizontal (**SHAP value**) indica si la variable 
        aumenta el riesgo de fuga (> 0) o blinda la retención (< 0). El color denota el valor de la variable.
        """
    )
    
    if explainer is None:
        st.warning("El modelo no está disponible para calcular valores SHAP.")
    else:
        with st.spinner("Generando análisis SHAP sobre la muestra de prueba..."):
            drop_cols = [
                "customer_id", "country", "state", "city", "zip_code",
                "latitude", "longitude", "cltv", "monthly_to_avg_charge_ratio", "churn_target"
            ]
            X = df.drop(columns=[c for c in drop_cols if c in df.columns])
            
            # Muestra representativa para agilidad de renderizado
            sample_size = min(600, len(X))
            X_sample = X.sample(n=sample_size, random_state=42)
            
            X_sample_proc = preprocessor.transform(X_sample)
            X_sample_df = pd.DataFrame(X_sample_proc, columns=feature_names)
            shap_vals_sample = explainer(X_sample_df)
            
            fig_shap, ax = plt.subplots(figsize=(10, 7))
            shap.summary_plot(shap_vals_sample, X_sample_df, max_display=12, show=False)
            plt.title("Drivers de Churn: Impacto y Dirección", fontsize=12, pad=15)
            st.pyplot(fig_shap, use_container_width=True)
            plt.close()

        st.markdown(
            """
            #### 📌 Principales Conclusiones Algorítmicas:
            1. **`is_month_to_month` (Rojo a la derecha):** Es el acelerador número uno de churn.
            2. **`dependents_Yes` (Rojo a la izquierda):** Las cargas familiares representan el ancla de retención más fuerte (SHAP < -1.0).
            3. **`high_risk_fiber_no_support`:** Los clientes con alta velocidad sin soporte técnico son fuertemente empujados hacia la salida.
            4. **`tenure_months` (Valores altos a la izquierda):** La antigüedad acumulada actúa como escudo orgánico contra la deserción.
            """
        )

# -------------------------------------------------------------
# TAB 3: Diagnóstico Local (Waterfall Individual)
# -------------------------------------------------------------
with tab_shap_local:
    st.subheader("Auditoría Individual de Riesgo de un Cliente")
    st.markdown("Inspecciona la descomposición aditiva de factores que explican la predicción de un caso concreto.")
    
    if explainer is not None:
        col_sel1, col_sel2 = st.columns([1, 2])
        
        with col_sel1:
            idx_cliente = st.number_input(
                "Selecciona el índice del cliente a auditar:",
                min_value=0, max_value=len(X_sample_df)-1, value=0, step=1
            )
            
            cliente_proc = X_sample_df.iloc[[idx_cliente]]
            prob_churn = pipeline.predict_proba(X_sample.iloc[[idx_cliente]])[0][1]
            pred_clase = "Fugado (Riesgo)" if prob_churn >= 0.50 else "Retenido (Seguro)"
            
            st.metric("Probabilidad Estimada de Churn", f"{prob_churn:.2%}")
            st.metric("Predicción del Modelo", pred_clase)
        
        with col_sel2:
            fig_waterfall, ax_wf = plt.subplots(figsize=(9, 5))
            shap.plots.waterfall(shap_vals_sample[idx_cliente], max_display=8, show=False)
            st.pyplot(fig_waterfall, use_container_width=True)
            plt.close()