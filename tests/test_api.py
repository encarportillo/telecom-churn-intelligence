import pytest
from fastapi.testclient import TestClient
from src.api.main import app


@pytest.fixture(scope="module")
def client():
    # El context manager 'with' fuerza la ejecución del evento lifespan (inicio y apagado)
    with TestClient(app) as test_client:
        yield test_client


def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["model_loaded"] is True


def test_predict_high_risk_customer(client):
    # Perfil análogo al cliente crítico de SHAP (Fibra, mes a mes, sin soporte, alta tarifa)
    payload = {
        "gender": "Female",
        "senior_citizen": 0,
        "partner": "No",
        "dependents": "No",
        "tenure_months": 2,
        "contract": "Month-to-month",
        "paperless_billing": "Yes",
        "payment_method": "Electronic check",
        "phone_service": "Yes",
        "multiple_lines": "No",
        "internet_service": "Fiber optic",
        "online_security": "No",
        "online_backup": "No",
        "device_protection": "No",
        "tech_support": "No",
        "streaming_tv": "No",
        "streaming_movies": "No",
        "monthly_charges": 95.0,
        "total_charges": 190.0,
    }

    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["churn_prediction"] == 1
    assert data["churn_probability"] >= 0.50
    assert data["risk_tier"] in ["Alto", "Crítico"]


def test_predict_loyal_customer(client):
    # Perfil fidelizado: 2 años de contrato, DSL, soporte técnico, baja tarifa
    payload = {
        "gender": "Male",
        "senior_citizen": 0,
        "partner": "Yes",
        "dependents": "Yes",
        "tenure_months": 60,
        "contract": "Two year",
        "paperless_billing": "No",
        "payment_method": "Credit card (automatic)",
        "phone_service": "Yes",
        "multiple_lines": "Yes",
        "internet_service": "DSL",
        "online_security": "Yes",
        "online_backup": "Yes",
        "device_protection": "Yes",
        "tech_support": "Yes",
        "streaming_tv": "No",
        "streaming_movies": "No",
        "monthly_charges": 45.0,
        "total_charges": 2700.0,
    }

    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["churn_prediction"] == 0
    assert data["churn_probability"] < 0.50
    assert data["risk_tier"] == "Bajo"


def test_predict_validation_error(client):
    payload = {
        "gender": "Male",
        "senior_citizen": 0,
        "partner": "Yes",
        "dependents": "No",
        "tenure_months": 12,
        "contract": "Contrato_Invalido",  # Error intencional
        "paperless_billing": "No",
        "payment_method": "Mailed check",
        "phone_service": "Yes",
        "internet_service": "DSL",
        "monthly_charges": 50.0,
    }

    response = client.post("/predict", json=payload)
    assert response.status_code == 422