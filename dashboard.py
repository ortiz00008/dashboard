import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Mis Inversiones", layout="wide")

st.title("💰 Dashboard de Inversiones")

# -------------------------
# DATOS (puedes cambiarlos)
# -------------------------
data = {
    "Activo": ["Acciones Apple", "Bitcoin", "ETF S&P500", "Ethereum", "Tesla"],
    "Invertido": [1000, 500, 1500, 800, 1200],
    "Valor_actual": [1300, 700, 1800, 650, 1100]
}

df = pd.DataFrame(data)

# -------------------------
# CÁLCULOS
# -------------------------
df["Ganancia"] = df["Valor_actual"] - df["Invertido"]
df["% Rentabilidad"] = (df["Ganancia"] / df["Invertido"]) * 100

# -------------------------
# MÉTRICAS
# -------------------------
col1, col2, col3 = st.columns(3)

col1.metric("Total invertido", f"{df['Invertido'].sum()} €")
col2.metric("Valor actual", f"{df['Valor_actual'].sum()} €")
col3.metric("Ganancia total", f"{df['Ganancia'].sum()} €")

st.divider()

# -------------------------
# TABLA
# -------------------------
st.subheader("📋 Detalle de inversiones")
st.dataframe(df)

# -------------------------
# GRÁFICA
# -------------------------
fig = px.bar(df, x="Activo", y="Ganancia", color="Ganancia",
             title="Ganancias por activo")

st.plotly_chart(fig, use_container_width=True)