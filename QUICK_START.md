# ⚡ Quick Start Guide - Telecom Churn Intelligence

Guía rápida para iniciar el proyecto en **5 minutos**.

---

## 🎯 Opción 1: Inicio Local (Desarrollo)

### Paso 1: Preparar entorno
```powershell
# Clonar o descargar el proyecto
cd telecom-churn-intelligence

# Crear entorno virtual
python -m venv .venv

# Activar (Windows)
.\.venv\Scripts\Activate.ps1

# Instalar dependencias
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### Paso 2: Iniciar API
```powershell
# Terminal 1: API REST en puerto 8000
python -m uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

Verifica en: `http://localhost:8000/docs` (Swagger UI interactivo)

### Paso 3: Iniciar Dashboard
```powershell
# Terminal 2: Dashboard Streamlit en puerto 8501
python -m streamlit run dashboard/app.py
```

Abre: `http://localhost:8501`

### ✅ ¡Listo! 
Ahora puedes:
- ✅ Hacer predicciones con la API
- ✅ Explorar el dashboard interactivo
- ✅ Ver análisis de churn

---

## 🐳 Opción 2: Docker (Recomendado)

### Paso 1: Build & Run
```powershell
cd telecom-churn-intelligence
docker compose -f docker/docker-compose.yml up --build
```

### Paso 2: Verifica servicios
- **API**: `http://localhost:8000`
- **Docs**: `http://localhost:8000/docs`
- **Health**: `http://localhost:8000/health`

### ✅ ¡Listo!
El contenedor incluye todas las dependencias.

---

## 🧪 Ejecutar Pruebas

```powershell
# Tests completos
python -m pytest -v

# Con cobertura
python -m pytest --cov=src

# Linting
python -m ruff check .
```

---

## 📊 Entrenar Modelo

### Requisito: CSV con columnas
```
customer_id, tenure_months, monthly_charges, contract, internet_service, 
tech_support, online_security, online_backup, device_protection, 
streaming_tv, streaming_movies, total_charges, churn
```

### Comando
```powershell
python -m src.models.train --input data/customers.csv --output outputs/models/telecom_churn_pipeline.joblib
```

---

## 🔮 Hacer Predicción Individual (cURL)

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "C001",
    "tenure_months": 12,
    "monthly_charges": 75.0,
    "contract": "Month-to-month",
    "internet_service": "Fiber optic",
    "tech_support": "No",
    "online_security": "No",
    "online_backup": "No",
    "device_protection": "No",
    "streaming_tv": "No",
    "streaming_movies": "No",
    "total_charges": 900.0
  }'
```

**Response:**
```json
{
  "churn_prediction": 1,
  "churn_probability": 0.8234,
  "risk_tier": "Crítico",
  "retention_strategy": "Contacto ejecutivo directo..."
}
```

---

## 🔑 Configurar BigQuery (Opcional)

### Paso 1: Credenciales GCP
```bash
# Descarga JSON desde Google Cloud Console
# Coloca en: config/gcp_credentials.json
```

### Paso 2: Variables de Entorno
```env
GCP_PROJECT_ID=tu-proyecto
GCP_DATASET_ID=tu-dataset
GCP_TABLE_NAME=tu-tabla
GOOGLE_APPLICATION_CREDENTIALS=config/gcp_credentials.json
```

### Paso 3: Ejecutar ETL
```powershell
python -m src.etl.ingest_to_bq
```

---

## 📁 Estructura Mínima Entendida

```
src/
  ├─ api/           → FastAPI endpoints
  ├─ models/        → ML pipeline
  └─ etl/           → Transformaciones de datos

dashboard/          → Streamlit app
tests/              → pytest tests
docker/             → Docker config
requirements.txt    → Dependencias
```

---

## 🚨 Troubleshooting

| Problema | Solución |
|----------|----------|
| **ModuleNotFoundError: No module named 'src'** | Activa venv: `.\.venv\Scripts\Activate.ps1` |
| **Port 8000 ya en uso** | Cambia puerto: `--port 8001` o mata proceso |
| **Modelo no encontrado (503)** | Entrena primero: `python -m src.models.train ...` |
| **CORS error desde dashboard** | API tiene CORS habilitado (`allow_origins=["*"]`) |
| **Docker build falló** | Limpia: `docker system prune -a` y reinenta |

---

## 📚 Documentación Completa

- **README.md** - Documentación exhaustiva
- **PROJECT_ANALYSIS.md** - Análisis técnico profundo
- **`/docs`** - Swagger UI (cuando API esté running)

---

## ✅ Checklist de Verificación

- [ ] Python 3.11+ instalado (`python --version`)
- [ ] Entorno virtual activado (prompt muestra `.venv`)
- [ ] Dependencias instaladas (`pip list | grep fastapi`)
- [ ] API respondiendo (`curl http://localhost:8000/health`)
- [ ] Dashboard accesible (`http://localhost:8501`)
- [ ] Tests pasando (`pytest`)

---

## 🎯 Siguientes Pasos

1. **Explorar API**: Abre `http://localhost:8000/docs` y prueba endpoints
2. **Navegar Dashboard**: Ve a `http://localhost:8501` y explora páginas
3. **Entrenar Modelo**: Usa tu CSV con datos reales
4. **Personalizar**: Modifica reglas de negocio en `src/api/main.py`
5. **Desplegar**: Sube a Cloud Run, AKS, ECS, etc.

---

**¡Estás listo! 🚀**

Cualquier duda, consulta `README.md` o `PROJECT_ANALYSIS.md`.
