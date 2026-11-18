import streamlit as st

st.set_page_config(
    page_title="Telecom Churn Intelligence",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("📡 Telecom Churn Intelligence & Revenue Retention Platform")
st.markdown(
    """
    Bienvenido a la plataforma analítica integral de **Retención de Clientes y Gestión de Ingresos**.
    Esta solución aborda el ciclo de vida analítico completo: desde la ingesta en almacenes de datos cloud 
    hasta la prescripción de campañas de retención en tiempo real mediante algoritmos de Machine Learning.
    """
)

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("📊 1. Resumen Ejecutivo")
    st.markdown(
        """
        - Visión holística de la cartera y facturación recurrente (**MRR / ARR**).
        - Cuantificación del volumen económico expuesto a fuga.
        - **Simulador de ROI de Retención**: modelo financiero interactivo para estimar 
          el beneficio neto de contactar clientes según su nivel de riesgo.
        """
    )

with col2:
    st.subheader("🔍 2. Diagnóstico & Factores")
    st.markdown(
        """
        - Exploración analítica de causas raíz de cancelación.
        - Desglose por contratos, tipo de conectividad y canales de soporte.
        - Explicabilidad global y local del modelo mediante **valores SHAP (Explainable AI)**.
        """
    )

with col3:
    st.subheader("⚡ 3. Simulador en Vivo")
    st.markdown(
        """
        - Herramienta de scoring individual para agentes de atención y retención.
        - Conexión vía REST API al microservicio contenerizado (**FastAPI + XGBoost**).
        - Prescripción automática de tácticas de mitigación según el nivel de riesgo.
        """
    )

st.divider()

st.markdown(
    """
    **Origen de los datos:** para este proyecto se utilizaron datos públicos alojados en
    [Kaggle: Telco customer churn: IBM dataset](https://www.kaggle.com/datasets/yeanzc/telco-customer-churn-ibm-dataset).
    """
)

st.divider()

st.info(
    "👈 **Selecciona una sección en el menú lateral izquierdo** para comenzar la navegación interactiva."
)