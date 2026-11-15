from typing import Optional, List
from pydantic import BaseModel, Field, field_validator


class CustomerInput(BaseModel):
    # Demografía
    gender: str = Field(..., description="Género del cliente ('Male', 'Female')", examples=["Female"])
    senior_citizen: int = Field(0, description="Adulto mayor (1: Sí, 0: No)", ge=0, le=1, examples=[0])
    partner: str = Field(..., description="Tiene pareja ('Yes', 'No')", examples=["Yes"])
    dependents: str = Field(..., description="Tiene dependientes/cargas ('Yes', 'No')", examples=["No"])

    # Antigüedad y Contrato
    tenure_months: int = Field(..., description="Meses de permanencia en la compañía", ge=0, examples=[2])
    contract: str = Field(..., description="Tipo de contrato ('Month-to-month', 'One year', 'Two year')", examples=["Month-to-month"])
    paperless_billing: str = Field(..., description="Facturación digital ('Yes', 'No')", examples=["Yes"])
    payment_method: str = Field(
        ...,
        description="Método de pago ('Electronic check', 'Mailed check', 'Bank transfer (automatic)', 'Credit card (automatic)')",
        examples=["Electronic check"]
    )

    # Servicios Contratados
    phone_service: str = Field(..., description="Servicio telefónico ('Yes', 'No')", examples=["Yes"])
    multiple_lines: str = Field("No", description="Múltiples líneas ('Yes', 'No', 'No phone service')", examples=["No"])
    internet_service: str = Field(..., description="Tipo de internet ('DSL', 'Fiber optic', 'No')", examples=["Fiber optic"])
    online_security: str = Field("No", description="Seguridad en línea ('Yes', 'No', 'No internet service')", examples=["No"])
    online_backup: str = Field("No", description="Copia de respaldo ('Yes', 'No', 'No internet service')", examples=["No"])
    device_protection: str = Field("No", description="Protección de dispositivo ('Yes', 'No', 'No internet service')", examples=["No"])
    tech_support: str = Field("No", description="Soporte técnico ('Yes', 'No', 'No internet service')", examples=["No"])
    streaming_tv: str = Field("No", description="Streaming de TV ('Yes', 'No', 'No internet service')", examples=["No"])
    streaming_movies: str = Field("No", description="Streaming de películas ('Yes', 'No', 'No internet service')", examples=["No"])

    # Facturación
    monthly_charges: float = Field(..., description="Cargo mensual facturado en USD", gt=0, examples=[85.5])
    total_charges: Optional[float] = Field(None, description="Total histórico facturado en USD (si es None, se calcula automáticamente)", examples=[171.0])

    @field_validator("contract")
    @classmethod
    def validate_contract(cls, v: str) -> str:
        valid = ["Month-to-month", "One year", "Two year"]
        if v not in valid:
            raise ValueError(f"Contrato inválido. Debe ser uno de: {valid}")
        return v

    @field_validator("internet_service")
    @classmethod
    def validate_internet(cls, v: str) -> str:
        valid = ["DSL", "Fiber optic", "No"]
        if v not in valid:
            raise ValueError(f"Servicio de internet inválido. Debe ser uno de: {valid}")
        return v


class PredictionResponse(BaseModel):
    churn_prediction: int = Field(..., description="0: Cliente Retenido, 1: Propenso a Fuga")
    churn_probability: float = Field(..., description="Probabilidad de deserción estimada (0.0 a 1.0)")
    risk_tier: str = Field(..., description="Nivel de riesgo ('Bajo', 'Medio', 'Alto', 'Crítico')")
    retention_strategy: str = Field(..., description="Acción de retención comercial recomendada")


class BatchCustomerInput(BaseModel):
    customers: List[CustomerInput]


class BatchPredictionResponse(BaseModel):
    total_records: int
    critical_risk_count: int
    predictions: List[PredictionResponse]


class HealthCheck(BaseModel):
    status: str
    model_loaded: bool
    version: str