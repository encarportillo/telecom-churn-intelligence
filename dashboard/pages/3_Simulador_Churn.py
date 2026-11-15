import os
import joblib
import requests
import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
import plotly.graph_objects as go

st.set_page_config(
    page_title="Simulador de Churn | Telecom Intelligence",
    page_icon="⚡",
    layout="wide"
)

st.title("⚡ Simulador de Fuga en Tiempo Real & Prescripción de Acciones")
st.markdown(
    """
    Evalúa la probabilidad de deserción de un cliente en vivo consumiendo el microservicio 
    **FastAPI + XGBoost Tuned** y obtén la estrategia de retención comercial personalizada.
    """
)

# -------------------------------------------------------------
# Configuración y Monitoreo del Endpoint
# -------------------------------------------------------------
API_URL = os.getenv("API_URL", "http://localhost:8000")
BASE_DIR = Path(__file__).resolve().parent.parent.parent

@st.cache_resource
def get_local_pipeline():
    candidate_paths = [
        BASE_DIR / "outputs/models/telecom_churn_pipeline.joblib",
        Path("outputs/models/telecom_churn_pipeline.joblib").resolve(),
    ]
    path = next((p for p in candidate_paths if p.exists()), None)
    return joblib.load(path) if path else None

# Verificar salud del backend
api_online = False
try:
    resp = requests.get(f"{API_URL}/health", timeout=1.5)
    if resp.status_code == 200 and resp.json().get("model_loaded"):
        api_online = True
except Exception:
    api_online = False

status_col1, status_col2 = st.columns([1, 4])
with status_col1:
    if api_online:
        st.success("🟢 API FastAPI Online (Puerto 8000)")
    else:
        st.warning("🟡 API Offline (Modo Local Fallback)")
with status_col2:
    st.caption(
        "Modo de inferencia: " + 
        ("Microservicio REST vía Docker / Uvicorn" if api_online else "Carga directa del pipeline serializado en disco (.joblib)")
    )

st.divider()

# -------------------------------------------------------------
# Perfiles de Prueba Rápidos (Presets)
# -------------------------------------------------------------
st.subheader("📋 Cargar Perfil de Prueba Rápido")
preset = st.radio(
    "Selecciona una plantilla para autocompletar el formulario:",
    options=["Personalizado", "🚨 Caso Crítico (Fibra Óptica / Mes a Mes)", "🛡️ Caso Fidelizado (2 Años / DSL)"],
    horizontal=True
)

# Valores por defecto según preset seleccionado
if preset == "🚨 Caso Crítico (Fibra Óptica / Mes a Mes)":
    default_gender = "Female"
    default_senior = 0
    default_partner = "No"
    default_dependents = "No"
    default_tenure = 2
    default_contract = "Month-to-month"
    default_paperless = "Yes"
    default_payment = "Electronic check"
    default_phone = "Yes"
    default_multilines = "No"
    default_internet = "Fiber optic"
    default_security = "No"
    default_backup = "No"
    default_device = "No"
    default_support = "No"
    default_tv = "No"
    default_movies = "No"
    default_monthly = 95.0
    default_total = 190.0
elif preset == "🛡️ Caso Fidelizado (2 Años / DSL)":
    default_gender = "Male"
    default_senior = 0
    default_partner = "Yes"
    default_dependents = "Yes"
    default_tenure = 60
    default_contract = "Two year"
    default_paperless = "No"
    default_payment = "Credit card (automatic)"
    default_phone = "Yes"
    default_multilines = "Yes"
    default_internet = "DSL"
    default_security = "Yes"
    default_backup = "Yes"
    default_device = "Yes"
    default_support = "Yes"
    default_tv = "No"
    default_movies = "No"
    default_monthly = 45.0
    default_total = 2700.0
else:
    default_gender = "Female"
    default_senior = 0
    default_partner = "Yes"
    default_dependents = "No"
    default_tenure = 12
    default_contract = "Month-to-month"
    default_paperless = "Yes"
    default_payment = "Electronic check"
    default_phone = "Yes"
    default_multilines = "No"
    default_internet = "Fiber optic"
    default_security = "No"
    default_backup = "Yes"
    default_device = "No"
    default_support = "No"
    default_tv = "Yes"
    default_movies = "No"
    default_monthly = 80.0
    default_total = 960.0

# -------------------------------------------------------------
# Formulario de Captura de Cliente
# -------------------------------------------------------------
with st.form("form_simulador"):
    st.subheader("👤 Datos del Cliente y Configuración del Servicio")
    
    col_demo, col_plan, col_serv = st.columns(3)
    
    with col_demo:
        st.markdown("**Información Demográfica**")
        gender = st.selectbox("Género", options=["Female", "Male"], index=0 if default_gender == "Female" else 1)
        senior_citizen = st.selectbox("Adulto Mayor (Senior Citizen)", options=[0, 1], format_func=lambda x: "Sí" if x == 1 else "No", index=default_senior)
        partner = st.selectbox("Tiene Pareja", options=["Yes", "No"], index=0 if default_partner == "Yes" else 1)
        dependents = st.selectbox("Tiene Cargas / Dependientes", options=["Yes", "No"], index=0 if default_dependents == "Yes" else 1)
    
    with col_plan:
        st.markdown("**Contrato y Facturación**")
        tenure_months = st.slider("Meses de Antigüedad (Tenure)", min_value=0, max_value=72, value=default_tenure)
        contract = st.selectbox("Tipo de Contrato", options=["Month-to-month", "One year", "Two year"], index=["Month-to-month", "One year", "Two year"].index(default_contract))
        payment_method = st.selectbox(
            "Método de Pago", 
            options=["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"],
            index=["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"].index(default_payment)
        )
        paperless_billing = st.selectbox("Facturación Digital (Paperless)", options=["Yes", "No"], index=0 if default_paperless == "Yes" else 1)
        monthly_charges = st.number_input("Cargo Mensual (USD)", min_value=15.0, max_value=150.0, value=float(default_monthly), step=5.0)
        total_charges = st.number_input("Total Histórico Facturado (USD)", min_value=0.0, max_value=10000.0, value=float(default_total), step=50.0)

    with col_serv:
        st.markdown("**Servicios y Conectividad**")
        internet_service = st.selectbox("Servicio de Internet", options=["Fiber optic", "DSL", "No"], index=["Fiber optic", "DSL", "No"].index(default_internet))
        tech_support = st.selectbox("Soporte Técnico", options=["No", "Yes", "No internet service"], index=["No", "Yes", "No internet service"].index(default_support))
        online_security = st.selectbox("Seguridad en Línea", options=["No", "Yes", "No internet service"], index=["No", "Yes", "No internet service"].index(default_security))
        online_backup = st.selectbox("Copia de Respaldo", options=["No", "Yes", "No internet service"], index=["No", "Yes", "No internet service"].index(default_backup))
        device_protection = st.selectbox("Protección de Dispositivo", options=["No", "Yes", "No internet service"], index=["No", "Yes", "No internet service"].index(default_device))
        streaming_tv = st.selectbox("Streaming TV", options=["No", "Yes", "No internet service"], index=["No", "Yes", "No internet service"].index(default_tv))
        streaming_movies = st.selectbox("Streaming Películas", options=["No", "Yes", "No internet service"], index=["No", "Yes", "No internet service"].index(default_movies))
        phone_service = st.selectbox("Telefonía Fija", options=["Yes", "No"], index=0 if default_phone == "Yes" else 1)
        multiple_lines = st.selectbox("Múltiples Líneas", options=["No", "Yes", "No phone service"], index=["No", "Yes", "No phone service"].index(default_multilines))

    submitted = st.form_submit_button("🚀 Calcular Scoring y Estrategia de Retención", use_container_width=True)

# -------------------------------------------------------------
# Procesamiento de la Predicción
# -------------------------------------------------------------
if submitted:
    payload = {
        "gender": gender,
        "senior_citizen": senior_citizen,
        "partner": partner,
        "dependents": dependents,
        "tenure_months": tenure_months,
        "contract": contract,
        "paperless_billing": paperless_billing,
        "payment_method": payment_method,
        "phone_service": phone_service,
        "multiple_lines": multiple_lines,
        "internet_service": internet_service,
        "online_security": online_security,
        "online_backup": online_backup,
        "device_protection": device_protection,
        "tech_support": tech_support,
        "streaming_tv": streaming_tv,
        "streaming_movies": streaming_movies,
        "monthly_charges": monthly_charges,
        "total_charges": total_charges if total_charges > 0 else (monthly_charges * max(tenure_months, 1))
    }

    probabilidad = None
    prediccion = None
    tier = None
    estrategia = None

    if api_online:
        try:
            res = requests.post(f"{API_URL}/predict", json=payload, timeout=3.0)
            if res.status_code == 200:
                data_resp = res.json()
                probabilidad = data_resp["churn_probability"]
                prediccion = data_resp["churn_prediction"]
                tier = data_resp["risk_tier"]
                estrategia = data_resp["retention_strategy"]
        except Exception as e:
            st.warning(f"Error consultando API: {e}. Activando motor local.")

    # Inferencia local si API falló o está offline
    if probabilidad is None:
        local_pipe = get_local_pipeline()
        if local_pipe is not None:
            # Calcular variables de ingeniería
            calc_data = payload.copy()
            calc_data["is_month_to_month"] = 1 if contract == "Month-to-month" else 0
            vas_list = [online_security, online_backup, device_protection, tech_support, streaming_tv, streaming_movies]
            calc_data["total_vas_services"] = sum(1 for v in vas_list if v == "Yes")
            calc_data["high_risk_fiber_no_support"] = 1 if (internet_service == "Fiber optic" and tech_support == "No") else 0
            if tenure_months <= 12:
                calc_data["tenure_cohort"] = "0-12_months"
            elif tenure_months <= 24:
                calc_data["tenure_cohort"] = "13-24_months"
            elif tenure_months <= 48:
                calc_data["tenure_cohort"] = "25-48_months"
            else:
                calc_data["tenure_cohort"] = "49+_months"
            
            df_calc = pd.DataFrame([calc_data])
            probabilidad = float(local_pipe.predict_proba(df_calc)[:, 1][0])
            prediccion = int(probabilidad >= 0.50)

            # Reglas de negocio
            if probabilidad >= 0.75:
                tier = "Crítico"
                estrategia = "Ofrecer migración prioritaria a plan anual con 25% desc. y soporte técnico premium bonificado."
            elif probabilidad >= 0.50:
                tier = "Alto"
                estrategia = "Ofrecer paquete de valor agregado (Soporte + Seguridad) gratuito por 6 meses."
            elif probabilidad >= 0.25:
                tier = "Medio"
                estrategia = "Cross-selling preventivo de servicios digitales o streaming."
            else:
                tier = "Bajo"
                estrategia = "Mantener comunicación estándar. No intervenir comercialmente."

    # -------------------------------------------------------------
    # Visualización de Resultados
    # -------------------------------------------------------------
    st.divider()
    st.subheader("🎯 Diagnóstico de Retención")

    col_res1, col_res2 = st.columns([1, 2])

    color_map = {
        "Crítico": "#d62728",
        "Alto": "#ff7f0e",
        "Medio": "#bcbd22",
        "Bajo": "#2ca02c"
    }
    tier_color = color_map.get(tier, "#1f77b4")

    with col_res1:
        # Gráfico Gauge / Medidor de Probabilidad
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=probabilidad * 100,
            number={"suffix": "%", "valueformat": ".1f"},
            title={"text": "Probabilidad de Churn", "font": {"size": 18}},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": tier_color},
                "steps": [
                    {"range": [0, 25], "color": "#e8f5e9"},
                    {"range": [25, 50], "color": "#fffde7"},
                    {"range": [50, 75], "color": "#fff3e0"},
                    {"range": [75, 100], "color": "#ffebee"},
                ],
                "threshold": {
                    "line": {"color": "black", "width": 3},
                    "thickness": 0.75,
                    "value": 50
                }
            }
        ))
        fig_gauge.update_layout(height=260, margin=dict(l=20, r=20, t=30, b=10))
        st.plotly_chart(fig_gauge, use_container_width=True)

    with col_res2:
        st.markdown(f"### Nivel de Riesgo: <span style='color:{tier_color}'>{tier.upper()}</span>", unsafe_allow_html=True)
        st.markdown(f"**Estado de Predicción:** {'⚠️ Cliente en Peligro de Fuga' if prediccion == 1 else '✅ Cliente Estable en Cartera'}")
        
        st.info(f"💡 **Estrategia Prescrita:** {estrategia}")

        # Impacto financiero individual estimado
        perdida_anual_estimada = monthly_charges * 12
        st.caption(f"💵 **Valor en Riesgo Anualizado (ARR):** ${perdida_anual_estimada:,.2f} USD")