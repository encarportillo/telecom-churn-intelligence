import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from dotenv import load_dotenv

st.set_page_config(page_title="Resumen Ejecutivo | Telecom Churn", page_icon="📊", layout="wide")

st.title("📊 Resumen Ejecutivo & Impacto Financiero")
st.markdown("Diagnóstico de cartera, ingresos recurrentes en riesgo y simulación de rentabilidad de campañas.")

# -------------------------------------------------------------
# Carga de Datos con Caché
# -------------------------------------------------------------
@st.cache_data
def load_data():
    load_dotenv(Path(__file__).resolve().parent.parent.parent / ".env")
    
    # Intentar conexión directa a BigQuery
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

    # Fallback si se ejecuta offline o sin credenciales BQ
    raw_path = Path(__file__).resolve().parent.parent.parent / "data/raw/Telco_customer_churn.xlsx"
    if raw_path.exists():
        df_raw = pd.read_excel(raw_path)
        df_raw["monthly_charges"] = pd.to_numeric(df_raw["Monthly Charges"], errors="coerce")
        df_raw["churn_target"] = df_raw["Churn Value"]
        df_raw["contract"] = df_raw["Contract"]
        return df_raw
        
    return pd.DataFrame()

df = load_data()

if df.empty:
    st.error("No se pudo cargar la información de clientes. Verifica la conexión a BigQuery o los datos locales.")
    st.stop()

# -------------------------------------------------------------
# Métricas Clave de Negocio (KPIs)
# -------------------------------------------------------------
total_clientes = len(df)
clientes_churn = (df["churn_target"] == 1).sum()
tasa_churn = clientes_churn / total_clientes

mrr_total = df["monthly_charges"].sum()
mrr_riesgo = df[df["churn_target"] == 1]["monthly_charges"].sum()
arr_riesgo = mrr_riesgo * 12

arpu_retenido = df[df["churn_target"] == 0]["monthly_charges"].mean()
arpu_churn = df[df["churn_target"] == 1]["monthly_charges"].mean()

kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("Cartera de Clientes", f"{total_clientes:,}", help="Total de contratos activos auditados")
kpi2.metric("Tasa de Churn Global", f"{tasa_churn:.2%}", f"-{clientes_churn:,} bajas", delta_color="inverse")
kpi3.metric("MRR en Riesgo Mensual", f"${mrr_riesgo:,.0f} USD", f"{(mrr_riesgo/mrr_total):.1%} del MRR total", delta_color="inverse")
kpi4.metric("ARR en Riesgo Proyectado", f"${arr_riesgo:,.0f} USD", "Impacto anualizado (12 meses)", delta_color="inverse")

st.divider()

# -------------------------------------------------------------
# Gráficos de Facturación y Asimetría
# -------------------------------------------------------------
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.subheader("Distribución de Clientes vs. Ingresos Facturados")
    fig_donut = go.Figure(data=[
        go.Pie(
            labels=["MRR Retenido", "MRR Perdido (Churn)"],
            values=[mrr_total - mrr_riesgo, mrr_riesgo],
            hole=0.45,
            marker_colors=["#1f77b4", "#d62728"]
        )
    ])
    fig_donut.update_layout(height=350, margin=dict(l=20, r=20, t=30, b=20))
    st.plotly_chart(fig_donut, use_container_width=True)

with col_chart2:
    st.subheader("Gasto Promedio Mensual (ARPU)")
    df_arpu = pd.DataFrame({
        "Segmento": ["Cliente Retenido", "Cliente Fugado (Churn)"],
        "ARPU (USD)": [arpu_retenido, arpu_churn]
    })
    fig_bar = px.bar(
        df_arpu, 
        x="Segmento", 
        y="ARPU (USD)", 
        text_auto=".2f",
        color="Segmento",
        color_discrete_map={"Cliente Retenido": "#1f77b4", "Cliente Fugado (Churn)": "#d62728"}
    )
    fig_bar.update_layout(height=350, showlegend=False, margin=dict(l=20, r=20, t=30, b=20))
    st.plotly_chart(fig_bar, use_container_width=True)

st.divider()

# -------------------------------------------------------------
# Simulador Financiero de Campaña de Retención (P&L / ROI)
# -------------------------------------------------------------
st.subheader("🧮 Simulador de ROI de la Estrategia de Retención")
st.markdown("Modela el impacto financiero neto de una campaña preventiva basada en el score del modelo predictivo.")

sim_col1, sim_col2, sim_col3 = st.columns(3)

with sim_col1:
    cobertura_campana = st.slider(
        "Porcentaje de clientes críticos a intervenir (%)",
        min_value=5, max_value=50, value=20, step=5
    ) / 100.0

with sim_col2:
    tasa_efectividad = st.slider(
        "Efectividad estimada de la oferta de retención (%)",
        min_value=10, max_value=60, value=30, step=5
    ) / 100.0

with sim_col3:
    costo_contacto = st.number_input(
        "Costo unitario por intervención (USD)",
        min_value=5.0, max_value=100.0, value=15.0, step=5.0
    )

# Cálculos de negocio
clientes_intervenidos = int(total_clientes * cobertura_campana)
costo_total_campana = clientes_intervenidos * costo_contacto

# Con el modelo calibrado, la concentración de fugados en el top decil es muy alta (precision ~70%)
precision_esperada = 0.70
churners_alcanzados = clientes_intervenidos * precision_esperada
clientes_rescatados = churners_alcanzados * tasa_efectividad

# Valor LTV rescatado (12 meses de permanencia adicional al ARPU de churners)
ingreso_anual_rescatado = clientes_rescatados * (arpu_churn * 12)
beneficio_neto = ingreso_anual_rescatado - costo_total_campana
roi_porcentaje = (beneficio_neto / costo_total_campana) * 100.0 if costo_total_campana > 0 else 0

st.write("")
res_col1, res_col2, res_col3, res_col4 = st.columns(4)
res_col1.metric("Clientes Contactados", f"{clientes_intervenidos:,}")
res_col2.metric("Clientes Salvados", f"{int(clientes_rescatados):,}")
res_col3.metric("Beneficio Neto (1 año)", f"${beneficio_neto:,.0f} USD")
res_col4.metric("ROI de la Campaña", f"{roi_porcentaje:.1f}%")