# 📡 Telecom Churn Intelligence & Revenue Retention Platform

Una solución de **Machine Learning empresarial** integrada y completa para predecir, entender y prevenir la cancelación de clientes en el sector de telecomunicaciones. Combina ingeniería de datos cloud-native, modelos interpretables, APIs de scoring en tiempo real y un dashboard interactivo de análisis y simulación.

---

## Origen de los datos

Para este proyecto se utilizaron datos públicos alojados en Kaggle: [Telco customer churn: IBM dataset](https://www.kaggle.com/datasets/yeanzc/telco-customer-churn-ibm-dataset).

---

## 🎯 Propósito y Valor

- **Predicción Temprana**: Identifica clientes con alto riesgo de cancelación mediante XGBoost/Logistic Regression.
- **Explainabilidad Operativa**: Desglose de factores críticos mediante SHAP y exploración visual.
- **Prescripción de Tácticas**: Reglas de negocio automáticas que asignan estrategias de retención según el perfil de riesgo.
- **Operacionalización**: Microservicio REST containerizado para integración con sistemas CRM/BPM.
- **Revenue Analytics**: Simulador de ROI interactivo para cuantificar el impacto financiero de campañas de retención.

---

## 🏗️ Arquitectura y Componentes

```
telecom-churn-intelligence/
│
├── src/
│   ├── etl/                          # Ingesta y transformación de datos
│   │   ├── ingest_to_bq.py          # Conexión y carga a BigQuery (Google Cloud)
│   │   ├── transform_raw_data.py    # Limpieza, ingeniería de características
│   │   ├── sql/                      # Scripts SQL parametrizados
│   │   └── __init__.py
│   │
│   ├── models/                       # Modelado y entrenamiento
│   │   ├── pipeline.py              # Definición de la tubería ML (Scaler + Classifier)
│   │   ├── train.py                 # Entrada de entrenamiento desde CSV
│   │   ├── explain.py               # Interpretabilidad local (SHAP values)
│   │   └── __init__.py
│   │
│   └── api/                          # Microservicio de inferencia REST
│       ├── main.py                  # FastAPI: endpoints de predicción y health
│       ├── schemas.py               # Pydantic models (request/response)
│       └── __init__.py
│
├── dashboard/                        # Aplicación Streamlit multipágina
│   ├── app.py                       # Página de inicio e índice
│   └── pages/
│       ├── 1_Resumen_Ejecutivo.py   # KPIs, MRR/ARR, exposición económica
│       ├── 2_Analisis_Causas.py     # EDA, desglose de factores de churn
│       └── 3_Simulador_Churn.py     # Scoring individual en vivo
│
├── notebooks/                        # Flujo exploratorio y experimentación
│   ├── 1_data_exploration.ipynb
│   ├── 2_etl_pipeline.ipynb
│   └── 3_model_training.ipynb
│
├── tests/                            # Suite de pruebas unitarias e integración
│   ├── test_api.py                  # Tests de endpoints REST
│   ├── test_credentials.py          # Tests de seguridad (sin secretos en código)
│   └── __init__.py
│
├── docker/                           # Containerización
│   ├── Dockerfile                   # Imagen Python + dependencias
│   └── docker-compose.yml           # Orquestación API + stack local
│
├── config/                           # Archivos de configuración
│   └── gcp_credentials.json         # (⚠️ NO COMMITAR) Credenciales BigQuery
│
├── outputs/                          # Artefactos generados (modelos, métricas)
│   ├── models/
│   │   └── telecom_churn_pipeline.joblib
│   └── metrics/
│
├── requirements.txt                  # Dependencias Python
├── pytest.ini                        # Configuración de pytest
├── .env                              # Variables de entorno (plantilla)
└── .gitignore                        # Exclusiones (secretos, venv, caché)
```

### Componentes Principales

| Módulo | Responsabilidad | Tecnología |
|--------|-----------------|-----------|
| **ETL** | Ingesta BigQuery, limpieza, feature engineering | pandas, Google Cloud BigQuery SDK |
| **Models** | Entrenamiento, serialización, explainabilidad | scikit-learn, XGBoost, SHAP |
| **API** | Microservicio de scoring real-time, reglas de retención | FastAPI, Pydantic, Uvicorn |
| **Dashboard** | Analítica interactiva, simulador, exploración visual | Streamlit, Plotly, pandas, SHAP |
| **Tests** | Cobertura de API, validación de datos, seguridad | pytest, httpx |
| **Docker** | Containerización y orquestación local | Docker, Docker Compose |

---

## ⚡ Inicio Rápido

### Requisitos

- **Python** ≥ 3.11
- **pip** o **conda** para manejo de dependencias
- **Docker Desktop** (opcional, para containerización)
- Credenciales de **Google Cloud** (opcional, solo si usas BigQuery)

### Instalación Local

```bash
# 1. Clonar el repositorio
git clone https://github.com/encarportillo/telecom-churn-intelligence.git
cd telecom-churn-intelligence

# 2. Crear entorno virtual
python -m venv .venv

# 3. Activar entorno (Windows)
.\.venv\Scripts\Activate.ps1

# 4. Instalar dependencias
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# 5. Configurar variables de entorno (opcional para BigQuery)
# Copiar .env.example a .env y completar
# export GOOGLE_APPLICATION_CREDENTIALS=config/gcp_credentials.json
```

### API REST

```bash
# Iniciar servidor de desarrollo con auto-reload
python -m uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

**Endpoints disponibles:**

- `GET /` — Estado del servicio
- `GET /health` — Health check con estado del modelo
- `POST /predict` — Predicción individual de churn + estrategia de retención
- `POST /predict/batch` — Predicción por lote (100+ clientes)
- `GET /docs` — Documentación interactiva (Swagger UI)

**Ejemplo de request:**

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "CUST_001",
    "tenure_months": 6,
    "monthly_charges": 85.5,
    "contract": "Month-to-month",
    "internet_service": "Fiber optic",
    "tech_support": "No",
    "online_security": "No",
    "online_backup": "No",
    "device_protection": "No",
    "streaming_tv": "No",
    "streaming_movies": "No",
    "total_charges": 513.0
  }'
```

### Dashboard Streamlit

```bash
# En otra terminal, asegúrate que el entorno virtual esté activado
python -m streamlit run dashboard/app.py
```

El dashboard se abre en `http://localhost:8501` y proporciona:
- **Resumen Ejecutivo**: KPIs de cartera, MRR/ARR, exposición de ingresos
- **Análisis de Causas**: Factores de riesgo, distribuciones, correlaciones
- **Simulador en Vivo**: Scoring individual con prescripción de tácticas

---

## 📊 Datos y Modelo

### Fuente de Datos

El ETL soporta dos modos:

1. **BigQuery** (producción):
   - Configura `GOOGLE_APPLICATION_CREDENTIALS` con credenciales JSON
   - Define tabla en variables `GCP_PROJECT_ID`, `GCP_DATASET_ID`, `GCP_TABLE_NAME`
   - Ejecuta: `python -m src.etl.ingest_to_bq`

2. **CSV Local** (desarrollo):
   - Requiere columnas: `customer_id`, `tenure_months`, `monthly_charges`, `churn`, etc.
   - Ejecuta: `python -m src.etl.transform_raw_data --input data.csv`

### Esquema de Cliente

Columnas esperadas y transformaciones:

```python
ENTRADA:
  - customer_id: str
  - tenure_months: int
  - monthly_charges: float
  - total_charges: float (opcional, aproximado si falta)
  - contract: str ["Month-to-month", "One year", "Two year"]
  - internet_service: str ["Fiber optic", "DSL", "No"]
  - tech_support: str ["Yes", "No"]
  - online_security, online_backup, device_protection, 
    streaming_tv, streaming_movies: str ["Yes", "No"]

CARACTERÍSTICAS DERIVADAS (en API):
  - is_month_to_month: int [0, 1]
  - total_vas_services: int [0, 6] (servicios de valor agregado)
  - high_risk_fiber_no_support: int [0, 1]
  - tenure_cohort: str ["0-12_months", "13-24_months", "25-48_months", "49+_months"]
```

### Entrenamiento

```bash
# Entrenar desde CSV local
python -m src.models.train \
  --input data/processed/customers.csv \
  --output outputs/models/telecom_churn_pipeline.joblib
```

**Modelo Base:**
- **Pipeline**: StandardScaler → LogisticRegression (class_weight="balanced")
- **Features**: tenure_months, monthly_charges (extensible)
- **Objetivo**: Predicción binaria de churn (0/1)

**Notas de Producción:**
- Valida calidad de datos, imbalance de clases y métricas de negocio antes de desplegar
- Este modelo inicial es una plantilla técnica, no una recomendación de producción
- Implementa monitoreo de data drift y model decay

### Explainabilidad

```bash
python -m src.models.explain --model outputs/models/telecom_churn_pipeline.joblib
```

Genera valores SHAP para interpretación global y local del modelo.

---

## 🧪 Pruebas y Calidad de Código

### Ejecutar Pruebas

```bash
# Tests unitarios e integración
python -m pytest -v

# Con cobertura
python -m pytest --cov=src --cov-report=html

# Tests específicos
python -m pytest tests/test_api.py::test_predict_single_customer -v
```

### Linting y Formateo

```bash
# Análisis estático con Ruff
python -m ruff check .

# Formateo automático
python -m ruff format .

# Validación de tipos (opcional, si añades type hints)
python -m mypy src/
```

**CI/CD:**
- GitHub Actions ejecuta `pytest` + `ruff check` en cada push y pull request
- Workflow en `.github/workflows/` (si está configurado)

---

## 🐳 Ejecución con Docker

### Build y Run Local

```bash
# Desde la raíz del proyecto
docker compose -f docker/docker-compose.yml up --build

# O detach
docker compose -f docker/docker-compose.yml up --build -d

# Logs
docker compose -f docker/docker-compose.yml logs -f churn-api
```

**Servicios disponibles:**
- API: `http://localhost:8000`
- Docs: `http://localhost:8000/docs`

### Dockerfile

La imagen se construye desde la raíz (`context: ..`, `dockerfile: docker/Dockerfile`) e incluye:
- Python 3.11 slim base
- Instalación de dependencias desde `requirements.txt`
- Health check configurado

### Variables de Entorno en Container

```yaml
environment:
  - PORT=8000
  - MODEL_PATH=outputs/models/telecom_churn_pipeline.joblib
  # Opcionales para BigQuery:
  # - GOOGLE_APPLICATION_CREDENTIALS=config/gcp_credentials.json
```

---

## 🔐 Seguridad y Configuración

### Variables de Entorno (`.env`)

**Plantilla:**

```env
# Google Cloud (opcional)
GCP_PROJECT_ID=tu-proyecto-gcp
GCP_DATASET_ID=tu-dataset
GCP_TABLE_NAME=tu-tabla
GOOGLE_APPLICATION_CREDENTIALS=config/gcp_credentials.json

# API
MODEL_PATH=outputs/models/telecom_churn_pipeline.joblib
PORT=8000
```

**⚠️ IMPORTANTE:**
- Nunca comitas `.env`, `gcp_credentials.json` o secretos en el repositorio
- Usa `.env.example` como plantilla documentada
- En producción, inyecta secrets mediante orchestrador (Kubernetes, Cloud Run, etc.)

### Credenciales GCP

1. Crea un _Service Account_ en Google Cloud Console
2. Descarga JSON de credenciales
3. Coloca en `config/gcp_credentials.json` (ya excluido en `.gitignore`)
4. Configura variable: `export GOOGLE_APPLICATION_CREDENTIALS=config/gcp_credentials.json`

---

## 📈 Reglas de Negocio: Estrategias de Retención

La API asigna automáticamente un **risk tier** y una **acción de retención** según la probabilidad de churn:

| Riesgo | Rango Prob. | Acción |
|--------|------------|--------|
| **Crítico** | ≥ 75% | Contacto ejecutivo directo, descuentos agresivos, ofertas premium |
| **Alto** | 50–74% | Paquetes de valor agregado, cambios de método de pago |
| **Medio** | 25–49% | Cross-selling preventivo de servicios |
| **Bajo** | < 25% | Comunicación estándar, sin intervención comercial |

**Personalización por Segmento:**
- Contrato mes a mes + Fibra óptica → Migración prioritaria a plan anual
- Contrato mes a mes → Upgrade de velocidad + fidelización
- Sin Soporte Técnico → Oferta de paquete premium bonificado

Personaliza en [src/api/main.py](src/api/main.py) función `assign_risk_and_action()`.

---

## 📁 Estructura de Salidas

```
outputs/
├── models/
│   └── telecom_churn_pipeline.joblib     # Artefacto del modelo entrenado
├── metrics/
│   ├── confusion_matrix.png
│   ├── roc_curve.png
│   └── feature_importance.csv
└── reports/
    └── explainability_report.html        # SHAP summary plot
```

---

## 🚀 Flujo de Trabajo Típico

### 1. **Exploración y Preparación** (Notebooks)
```bash
# Ejecutar notebooks en orden
# 1_data_exploration.ipynb → EDA inicial
# 2_etl_pipeline.ipynb → Limpieza y feature engineering
# 3_model_training.ipynb → Entrenamiento y validación
```

### 2. **Entrenamiento y Validación**
```bash
python -m src.models.train --input data/processed/customers.csv \
  --output outputs/models/telecom_churn_pipeline.joblib
```

### 3. **Despliegue Local**
```bash
# API
python -m uvicorn src.api.main:app --reload

# Dashboard (otra terminal)
python -m streamlit run dashboard/app.py
```

### 4. **Pruebas**
```bash
python -m pytest -v
python -m ruff check .
```

### 5. **Containerización**
```bash
docker compose -f docker/docker-compose.yml up --build
```

### 6. **Despliegue en Producción**
- Usa **Google Cloud Run**, **Azure Container Instances**, **AWS ECS**, etc.
- Inyecta credenciales y configuración vía _environment variables_ o _secrets management_
- Implementa monitoring, logging y alertas

---

## 📚 Dependencias Principales

| Librería | Versión | Uso |
|----------|---------|-----|
| **FastAPI** | 0.143.0 | Framework REST API |
| **Streamlit** | 1.65.0 | Dashboard interactivo |
| **scikit-learn** | 1.9.1 | ML pipeline (scaler, LR) |
| **XGBoost** | 3.4.1 | Modelo alternativo (extensible) |
| **pandas** | 2.3.3 | Manipulación de datos |
| **numpy** | 2.5.4 | Cálculos numéricos |
| **SHAP** | 0.53.0 | Explainabilidad |
| **google-cloud-bigquery** | 3.46.1 | Integración BigQuery |
| **pytest** | 8.4.2 | Testing |
| **ruff** | 0.17.0 | Linting / Formateo |
| **uvicorn** | 0.54.0 | ASGI server |

Ver `requirements.txt` completo con versiones pinned.

---

## 🔗 Integración con Sistemas Externos

### CRM / Sistema de Retención
```bash
# El endpoint POST /predict/batch acepta 100+ clientes simultáneamente
POST http://api.example.com:8000/predict/batch
Content-Type: application/json

{
  "customers": [
    { "customer_id": "C001", "tenure_months": 6, ... },
    { "customer_id": "C002", "tenure_months": 24, ... }
  ]
}
```

### Data Warehouse
- ETL extrae datos de BigQuery, aplica transformaciones
- Modelo entrenado se serializa como artefacto joblib
- Predicciones pueden reintegrarse en warehouse para análisis

### Observabilidad
- Añade logging estructurado (python-json-logger)
- Configura tracing distribuido (OpenTelemetry)
- Monitorea latencia de API, precisión del modelo, distribución de probabilidades

---

## 🛠️ Desarrollo y Contribución

### Añadir una Nueva Feature

1. **Exploración**: Experimenta en notebook
2. **Código**: Implementa en `src/etl/transform.py` o `src/models/pipeline.py`
3. **Tests**: Escribe tests en `tests/`
4. **Validación**: Ejecuta `pytest` + `ruff`
5. **PR**: Envía pull request

### Actualizar Dependencias

```bash
# Verifica vulnerabilidades
python -m pip list --outdated

# Actualiza requirements.txt manualmente o:
pip-audit

# Reinstala
python -m pip install -r requirements.txt
```

---

## 📝 Licencia

Este proyecto está bajo licencia [MIT / Apache 2.0 / Tu licencia]. Incluye datos de ejemplo y plantillas técnicas. No se proporciona garantía de rendimiento en producción.

---

## 📧 Contacto y Soporte

- **Autor(es)**: Equipo de Ciencia de Datos
- **Repositorio**: [GitHub Link]
- **Issues**: [GitHub Issues]
- **Documentación**: Consulta [wiki] o docstrings en código

---

## ✅ Checklist de Producción

Antes de desplegar a producción, valida:

- [ ] Modelo entrenado y guardado en `outputs/models/`
- [ ] Pruebas ejecutadas sin errores (`pytest -v`)
- [ ] Linting pasó (`ruff check .`)
- [ ] Credenciales GCP configuradas (sin hardcoding)
- [ ] Health check respondiendo correctamente
- [ ] Dashboard funciona sin modelo (modo demo)
- [ ] Docker image construida y probada
- [ ] Logging y monitoreo configurados
- [ ] Data drift y model decay monitoreados
- [ ] Documentación actualizada

---

**Última actualización**: 2026-11-08 | Versión: 1.0.0
