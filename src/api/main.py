import os
from pathlib import Path
from contextlib import asynccontextmanager
import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from src.api.schemas import (
    CustomerInput,
    PredictionResponse,
    BatchCustomerInput,
    BatchPredictionResponse,
    HealthCheck,
)

# Estado global para almacenar el pipeline en memoria
ml_models = {}

MODEL_PATH = Path(os.getenv("MODEL_PATH", "outputs/models/telecom_churn_pipeline.joblib"))


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Carga el modelo serializado al iniciar y libera memoria al apagar."""
    # Obtenemos la raíz del proyecto de forma absoluta a partir de este archivo
    base_dir = Path(__file__).resolve().parent.parent.parent  # telecom-churn-intelligence/
    
    candidate_paths = [
        base_dir / "outputs" / "models" / "telecom_churn_pipeline.joblib",
        Path("outputs/models/telecom_churn_pipeline.joblib").resolve(),
        Path("../outputs/models/telecom_churn_pipeline.joblib").resolve(),
    ]
    
    resolved_path = None
    for p in candidate_paths:
        if p.exists():
            resolved_path = p
            break

    if resolved_path is None:
        print(f"Advertencia: No se encontró el artefacto del modelo en: {candidate_paths}")
        ml_models["pipeline"] = None
    else:
        print(f"Cargando pipeline de inferencia desde: {resolved_path}")
        ml_models["pipeline"] = joblib.load(resolved_path)
        print("Pipeline cargado exitosamente en memoria.")

    yield
    ml_models.clear()


app = FastAPI(
    title="Telecom Churn Prediction API",
    description="Microservicio de inferencia en tiempo real para detección temprana y retención de clientes.",
    version="1.0.0",
    lifespan=lifespan,
)

# Configuración básica de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def compute_derived_features(customer: CustomerInput) -> dict:
    """Calcula las variables de ingeniería de características requeridas por el pipeline."""
    data = customer.model_dump()

    # Si total_charges no viene, se aproxima con mensualidad * antigüedad
    if data["total_charges"] is None or data["total_charges"] == 0:
        data["total_charges"] = max(data["monthly_charges"] * max(data["tenure_months"], 1), 0.0)

    # 1. Flag de contrato mes a mes
    data["is_month_to_month"] = 1 if data["contract"] == "Month-to-month" else 0

    # 2. Conteo de servicios de valor agregado (VAS)
    vas_services = [
        "online_security", "online_backup", "device_protection",
        "tech_support", "streaming_tv", "streaming_movies"
    ]
    data["total_vas_services"] = sum(1 for s in vas_services if data.get(s) == "Yes")

    # 3. Riesgo tecnológico: Fibra óptica sin soporte
    data["high_risk_fiber_no_support"] = 1 if (
        data["internet_service"] == "Fiber optic" and data["tech_support"] == "No"
    ) else 0

    # 4. Cohorte de antigüedad
    tenure = data["tenure_months"]
    if tenure <= 12:
        data["tenure_cohort"] = "0-12_months"
    elif tenure <= 24:
        data["tenure_cohort"] = "13-24_months"
    elif tenure <= 48:
        data["tenure_cohort"] = "25-48_months"
    else:
        data["tenure_cohort"] = "49+_months"

    return data


def assign_risk_and_action(prob: float, customer: CustomerInput) -> tuple[str, str]:
    """Asigna el segmento de riesgo operativo y la acción de retención prescrita."""
    if prob >= 0.75:
        tier = "Crítico"
        if customer.contract == "Month-to-month" and customer.internet_service == "Fiber optic":
            action = "Ofrecer migración prioritaria a plan anual con 25% desc. y soporte técnico premium bonificado."
        elif customer.contract == "Month-to-month":
            action = "Ofrecer upgrade de velocidad condicionado a contrato anual de fidelización."
        else:
            action = "Contacto telefónico ejecutivo directo y descuento en los próximos 3 ciclos de facturación."
    elif prob >= 0.50:
        tier = "Alto"
        if customer.tech_support == "No":
            action = "Ofrecer paquete de valor agregado (Soporte Técnico + Seguridad) gratuito por 6 meses."
        else:
            action = "Invitar a cambio de método de pago a PAC/PAT con descuento recurrente en factura."
    elif prob >= 0.25:
        tier = "Medio"
        action = "Cross-selling preventivo de servicios digitales (streaming o cloud backup)."
    else:
        tier = "Bajo"
        action = "Mantener comunicación estándar. No intervenir comercialmente."

    return tier, action


@app.get("/", tags=["General"])
def root():
    return {
        "service": "Telecom Churn Prediction API",
        "status": "online",
        "docs_url": "/docs",
    }


@app.get("/health", response_model=HealthCheck, tags=["Monitor"])
def health_check():
    return HealthCheck(
        status="healthy",
        model_loaded=ml_models.get("pipeline") is not None,
        version="1.0.0",
    )


@app.post("/predict", response_model=PredictionResponse, tags=["Inferencia"])
def predict_single_customer(customer: CustomerInput):
    pipeline = ml_models.get("pipeline")
    if pipeline is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="El modelo predictivo no se encuentra disponible o no fue cargado correctamente.",
        )

    # 1. Transformar datos y calcular variables derivadas
    enriched_data = compute_derived_features(customer)
    df_single = pd.DataFrame([enriched_data])

    # 2. Inferencia con el pipeline serializado
    try:
        probability = float(pipeline.predict_proba(df_single)[:, 1][0])
        prediction = int(probability >= 0.50)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error durante el procesamiento del pipeline: {str(e)}",
        )

    # 3. Asignar reglas de negocio
    tier, action = assign_risk_and_action(probability, customer)

    return PredictionResponse(
        churn_prediction=prediction,
        churn_probability=round(probability, 4),
        risk_tier=tier,
        retention_strategy=action,
    )


@app.post("/predict/batch", response_model=BatchPredictionResponse, tags=["Inferencia"])
def predict_batch_customers(batch: BatchCustomerInput):
    pipeline = ml_models.get("pipeline")
    if pipeline is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="El modelo predictivo no se encuentra disponible.",
        )

    if not batch.customers:
        return BatchPredictionResponse(total_records=0, critical_risk_count=0, predictions=[])

    enriched_records = [compute_derived_features(c) for c in batch.customers]
    df_batch = pd.DataFrame(enriched_records)

    try:
        probabilities = pipeline.predict_proba(df_batch)[:, 1]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error procesando el lote: {str(e)}",
        )

    responses = []
    critical_count = 0
    for prob, customer in zip(probabilities, batch.customers):
        p_float = float(prob)
        tier, action = assign_risk_and_action(p_float, customer)
        if tier == "Crítico":
            critical_count += 1
        responses.append(
            PredictionResponse(
                churn_prediction=int(p_float >= 0.50),
                churn_probability=round(p_float, 4),
                risk_tier=tier,
                retention_strategy=action,
            )
        )

    return BatchPredictionResponse(
        total_records=len(responses),
        critical_risk_count=critical_count,
        predictions=responses,
    )