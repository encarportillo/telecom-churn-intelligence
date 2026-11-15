# 📑 Índice de Documentación y Referencias

**Proyecto:** Telecom Churn Intelligence  
**Versión:** 1.0.0  
**Fecha de Análisis:** 8 de Noviembre de 2026  
**Estado:** ✅ Completo y Funcional

---

## 📚 Documentos Disponibles

### 1. **QUICK_START.md** ⚡
**Para:** Iniciar rápidamente (5 minutos)  
**Contiene:**
- Instalación paso a paso
- Inicio local vs Docker
- Comandos básicos de testing
- Troubleshooting común
- Checklist de verificación

**Cuándo usarlo:** Primera vez usando el proyecto

---

### 2. **README.md** 📖
**Para:** Documentación completa y detallada  
**Contiene:**
- Propósito y valor del proyecto
- Arquitectura y componentes
- Inicio rápido (desarrollo y Docker)
- Datos y entrenamiento de modelos
- Pruebas y calidad de código
- Seguridad y configuración
- Reglas de negocio (Risk Tiers)
- Integración con sistemas externos
- Workflow de desarrollo
- Checklist de producción

**Cuándo usarlo:** Documentación de referencia general

---

### 3. **PROJECT_ANALYSIS.md** 🔍
**Para:** Análisis técnico profundo  
**Contiene:**
- Resumen ejecutivo
- Análisis detallado de cada componente:
  - ETL (ingesta y transformación)
  - Models (entrenamiento y explicabilidad)
  - API REST (endpoints y esquemas)
  - Dashboard (páginas y visualizaciones)
  - Testing (pytest, ruff, cobertura)
  - Docker (Dockerfile, docker-compose)
  - Configuración y secretos
  - Notebooks de exploración
  - CI/CD
- Flujo de datos end-to-end
- Dependencias principales
- Checklist de completitud
- Estado de despliegue
- Recomendaciones futuras

**Cuándo usarlo:** Entender arquitectura profundamente, planificar mejoras

---

### 4. **INDEX.md** (este archivo) 📑
**Para:** Navegar la documentación  
**Contiene:**
- Índice de todos los documentos
- Estructura de directorios
- Mapa de funcionalidades
- Referencias rápidas
- Guía de contribución

**Cuándo usarlo:** Buscar dónde está la información que necesitas

---

## 🗂️ Estructura del Proyecto

```
telecom-churn-intelligence/
│
├── 📄 README.md                    ← Documentación completa
├── 📄 PROJECT_ANALYSIS.md          ← Análisis técnico
├── 📄 QUICK_START.md               ← Inicio rápido
├── 📄 INDEX.md                     ← Este archivo
│
├── src/                            ← Código principal
│   ├── api/                        ← API REST (FastAPI)
│   │   ├── main.py                 ← Endpoints principal
│   │   └── schemas.py              ← Modelos Pydantic
│   ├── models/                     ← ML Pipeline
│   │   ├── pipeline.py             ← Definición del modelo
│   │   ├── train.py                ← Entrenamiento
│   │   └── explain.py              ← Explainability (SHAP)
│   └── etl/                        ← Ingesta y transformación
│       ├── ingest_to_bq.py         ← BigQuery
│       ├── transform_raw_data.py   ← Transformaciones
│       └── sql/                    ← Queries SQL
│
├── dashboard/                      ← Streamlit App
│   ├── app.py                      ← Página de inicio
│   └── pages/
│       ├── 1_Resumen_Ejecutivo.py  ← KPIs
│       ├── 2_Analisis_Causas.py    ← EDA
│       └── 3_Simulador_Churn.py    ← Predicción
│
├── tests/                          ← Suite de pruebas
│   ├── test_api.py                 ← Tests de API
│   └── test_credentials.py         ← Tests de seguridad
│
├── docker/                         ← Containerización
│   ├── Dockerfile                  ← Imagen Python
│   └── docker-compose.yml          ← Orquestación
│
├── notebooks/                      ← Exploración
│   ├── 1_data_exploration.ipynb
│   ├── 2_etl_pipeline.ipynb
│   └── 3_model_training.ipynb
│
├── config/                         ← Configuración
│   └── gcp_credentials.json        ← (NO COMMITAR)
│
├── outputs/                        ← Artefactos generados
│   ├── models/
│   │   └── telecom_churn_pipeline.joblib
│   └── metrics/
│
├── requirements.txt                ← Dependencias Python
├── .env                            ← Variables de entorno
├── .gitignore                      ← Exclusiones Git
└── pytest.ini                      ← Config pytest
```

---

## 🎯 Mapa de Funcionalidades

| Funcionalidad | Archivo Principal | Documentación |
|---------------|-------------------|---------------|
| **Predicción Individual** | src/api/main.py | README.md "API REST" |
| **Predicción Batch** | src/api/main.py | README.md "Batch Processing" |
| **Health Check** | src/api/main.py | README.md "Endpoints" |
| **Entrenamiento** | src/models/train.py | README.md "Training" |
| **Explainability** | src/models/explain.py | PROJECT_ANALYSIS.md "Models" |
| **Ingesta BigQuery** | src/etl/ingest_to_bq.py | README.md "Datos" |
| **Transformación** | src/etl/transform_raw_data.py | PROJECT_ANALYSIS.md "ETL" |
| **Dashboard Ejecutivo** | dashboard/pages/1_*.py | PROJECT_ANALYSIS.md "Dashboard" |
| **Análisis de Causas** | dashboard/pages/2_*.py | README.md "Dashboard" |
| **Simulador** | dashboard/pages/3_*.py | README.md "Simulador" |
| **Testing** | tests/ | README.md "Testing" |
| **Docker** | docker/docker-compose.yml | QUICK_START.md "Docker" |

---

## ⚡ Referencia Rápida de Comandos

### Desarrollo Local
```bash
# Configuración
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# API
python -m uvicorn src.api.main:app --reload

# Dashboard
python -m streamlit run dashboard/app.py

# Tests
python -m pytest -v
python -m ruff check .
```

### Docker
```bash
docker compose -f docker/docker-compose.yml up --build
```

### Entrenar Modelo
```bash
python -m src.models.train --input data.csv --output model.joblib
```

### API Request (cURL)
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"customer_id": "C001", "tenure_months": 12, ...}'
```

---

## 🔍 Buscar Información

### ¿Dónde está...?

| Busco... | Mira en… | Sección |
|---------|----------|---------|
| Cómo instalar | QUICK_START.md | "Paso 1: Preparar entorno" |
| Cómo usar la API | README.md | "API REST" |
| Cómo entrenar modelo | README.md | "Datos y modelo" |
| Arquitectura del sistema | PROJECT_ANALYSIS.md | "Flujo de datos end-to-end" |
| Seguridad | README.md | "Seguridad y configuración" |
| Docker | QUICK_START.md | "Opción 2: Docker" |
| Testing | README.md | "Pruebas y calidad" |
| Troubleshooting | QUICK_START.md | "Troubleshooting" |
| Endpoints API | README.md | "API REST" |
| Risk Tiers | README.md | "Reglas de Negocio" |
| Dependencias | PROJECT_ANALYSIS.md | "Dependencias principales" |
| Estructura de código | PROJECT_ANALYSIS.md | "Análisis de componentes" |

---

## 🚀 Flujos Típicos de Trabajo

### 1. **Iniciar desarrollo**
1. Lee: QUICK_START.md
2. Ejecuta: `.\.venv\Scripts\Activate.ps1`
3. Ejecuta: `pip install -r requirements.txt`
4. Inicia: `python -m uvicorn src.api.main:app --reload`

### 2. **Entrenar modelo nuevo**
1. Prepara: CSV con columnas requeridas
2. Ejecuta: `python -m src.models.train --input data.csv --output model.joblib`
3. Verifica: API responde predicciones en `/predict`

### 3. **Explorar datos**
1. Abre: `notebooks/1_data_exploration.ipynb`
2. Ejecuta: Celdas en orden
3. Modifica: Personaliza análisis

### 4. **Desplegar a producción**
1. Lee: README.md "Checklist de producción"
2. Lee: PROJECT_ANALYSIS.md "Estado de despliegue"
3. Configura: Secrets, logging, monitoring
4. Despliega: Cloud Run / AKS / ECS

---

## 📊 Estadísticas del Proyecto

| Métrica | Valor |
|---------|-------|
| Archivos Python (.py) | ~15-20 |
| Líneas de código | ~3,000-4,000 |
| Dependencias principales | ~40 |
| Endpoints API | 5 |
| Páginas Dashboard | 3 |
| Archivos documentación | 4 (README, ANALYSIS, QUICK_START, INDEX) |
| Cobertura testing | Completa (API, credenciales) |

---

## ✅ Checklist de Orientación

Cuando empieces a trabajar:

- [ ] Leo **QUICK_START.md** (5 min)
- [ ] Leo la sección relevante de **README.md** (10-20 min)
- [ ] Ejecuto comandos de prueba (5 min)
- [ ] Consulto **PROJECT_ANALYSIS.md** para detalles (si necesito)
- [ ] Refiero a este **INDEX.md** para buscar información (siempre)

---

## 🔗 Relaciones entre Documentos

```
QUICK_START.md  ←→  README.md  ←→  PROJECT_ANALYSIS.md
      ↓               ↓               ↓
   (5 min)      (referencia)     (profundo)
      ↓               ↓               ↓
     Inicio        General        Técnico
   Fácil          Completo        Detallado

                    ↓
                INDEX.md
                (Navegación)
```

---

## 📞 Guía de Contribución

### Para añadir una feature:
1. Consulta: README.md "Desarrollo y Contribución"
2. Crea branch: `git checkout -b feature/nombre`
3. Implementa: Sigue estructura en PROJECT_ANALYSIS.md
4. Testa: `pytest -v`
5. Linting: `ruff check .`
6. PR: Describe cambios

### Para actualizar documentación:
1. Edita el .md relevante
2. Mantén referencia cruzada a otros docs
3. Actualiza INDEX.md si es necesario

---

## 🎓 Recursos de Aprendizaje

### Para entender cada componente:
- **ETL**: PROJECT_ANALYSIS.md "ETL (Extract, Transform, Load)"
- **ML**: PROJECT_ANALYSIS.md "Modelado (Models)"
- **API**: PROJECT_ANALYSIS.md "API REST (FastAPI)"
- **Dashboard**: PROJECT_ANALYSIS.md "Dashboard (Streamlit)"
- **Docker**: README.md "Ejecución con Docker"
- **Testing**: README.md "Pruebas y calidad"

---

## 📝 Notas Importantes

1. **Nunca** commits `.env`, `gcp_credentials.json` o secretos
2. **Siempre** usa `.env.example` como plantilla
3. **Testing** antes de push: `pytest && ruff check .`
4. **Documentación** se actualiza con cada cambio
5. **Docker** es la forma recomendada para producción

---

## 🎯 Próximas Acciones

Según tu rol:

### Data Engineer
→ README.md "Datos y modelo" + PROJECT_ANALYSIS.md "ETL"

### ML Engineer
→ PROJECT_ANALYSIS.md "Modelado" + README.md "Training"

### Backend Developer
→ README.md "API REST" + PROJECT_ANALYSIS.md "API REST"

### Frontend Developer
→ PROJECT_ANALYSIS.md "Dashboard" + README.md "Dashboard"

### DevOps Engineer
→ QUICK_START.md "Docker" + README.md "Docker"

### QA Engineer
→ README.md "Testing" + PROJECT_ANALYSIS.md "Testing"

---

**Última actualización:** 2026-11-08  
**Versión:** 1.0.0  
**Mantenedor:** Equipo de Proyecto

---

## 📍 Ubicación de Archivos

Todos los documentos están en la **raíz del proyecto**:

```
C:\Users\encar\Desktop\...\telecom-churn-intelligence\
  ├─ README.md
  ├─ PROJECT_ANALYSIS.md
  ├─ QUICK_START.md
  └─ INDEX.md (este archivo)
```

**¡Estás listo para empezar! 🚀**
