import streamlit as st
import pandas as pd
import plotly.express as px

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(page_title="Mis Inversiones", layout="wide", page_icon="💰")
st.title("📊 Dashboard Avanzado de Inversiones")
st.write("---")

# 2. ALMACENAMIENTO DE DATOS EN MEMORIA (Con tus datos reales y categorías)
if "mis_datos" not in st.session_state:
    st.session_state.mis_datos = pd.DataFrame([
        {"Activo": "microsoft", "Tipo": "Acciones", "Cantidad": 2.8494, "Precio compra": 370.51, "Precio actual": 380.95},
        {"Activo": "xiaomi", "Tipo": "Acciones", "Cantidad": 162.06, "Precio compra": 4.65, "Precio actual": 3.23},
        {"Activo": "amazon", "Tipo": "Acciones", "Cantidad": 2.3191, "Precio compra": 181.02, "Precio actual": 221.35},
        {"Activo": "oro", "Tipo": "Liquidez", "Cantidad": 6.7741, "Precio compra": 74.90, "Precio actual": 74.69},
        {"Activo": "nvidia", "Tipo": "Acciones", "Cantidad": 1.2594, "Precio compra": 159.59, "Precio actual": 191.94},
        {"Activo": "fondo msci world", "Tipo": "Fondos", "Cantidad": 400.33, "Precio compra": 24.53, "Precio actual": 27.866},
        {"Activo": "palm harbour", "Tipo": "Fondos", "Cantidad": 33.4737, "Precio compra": 20.01, "Precio actual": 20.72},
        {"Activo": "emerging", "Tipo": "Fondos", "Cantidad": 43.36, "Precio compra": 11.99, "Precio actual": 14.274},
        {"Activo": "abaco", "Tipo": "Fondos", "Cantidad": 109.1889, "Precio compra": 9.16, "Precio actual": 9.2189}
    ])

# 3. PANEL DE CONTROL LATERAL
st.sidebar.header("➕ Añadir / Modificar")
nuevo_activo = st.sidebar.text_input("Nombre de la inversión", placeholder="Ej: Apple, Bitcoin...")
nuevo_tipo = st.sidebar.selectbox("Clasificación de Activo", ["Acciones", "Fondos", "Liquidez"])
nueva_cantidad = st.sidebar.number_input("Cantidad", min_value=0.0000, value=1.0000, step=0.1000, format="%.4f")
nuevo_p_compra = st.sidebar.number_input("Precio de Compra (€)", min_value=0.00, value=10.00, step=1.00)
nuevo_p_actual = st.sidebar.number_input("Precio Actual (€)", min_value=0.00, value=10.00, step=1.00)

if st.sidebar.button("💾 Guardar en la Cartera"):
    if nuevo_activo:
        nueva_fila = {
            "Activo": nuevo_activo.lower(),
            "Tipo": nuevo_tipo,
            "Cantidad": nueva_cantidad,
            "Precio compra": nuevo_p_compra,
            "Precio actual": nuevo_p_actual
        }
        df_temporal = st.session_state.mis_datos
        df_temporal = df_temporal[df_temporal["Activo"] != nuevo_activo.lower()]
        st.session_state.mis_datos = pd.concat([df_temporal, pd.DataFrame([nueva_fila])], ignore_index=True)
        st.sidebar.success(f"¡{nuevo_activo} actualizado!")
        st.rerun()

# 4. CÁLCULOS MATEMÁTICOS
df = st.session_state.mis_datos.copy()

if not df.empty:
    df["Valor inversión"] = df["Cantidad"] * df["Precio compra"]
    df["Valor actual"] = df["Cantidad"] * df["Precio actual"]
    df["Ganancia"] = df["Valor actual"] - df["Valor inversión"]
    
    total_invertido = df["Valor inversión"].sum()
    total_actual = df["Valor actual"].sum()
    total_ganancia = df["Ganancia"].sum()
    
    # INDICADORES PRINCIPALES
    c1, c2, c3 = st.columns(3)
    c1.metric("Capital Invertido", f"{total_invertido:,.2f} €")
    c2.metric("Valor Neto Actual", f"{total_actual:,.2f} €")
    c3.metric("Plusvalía / Minusvalía Total", f"{total_ganancia:,.2f} €", delta=f"{total_ganancia:,.2f} €")
    
    st.write("---")
    st.subheader("📝 Desglose de Posiciones Abiertas")
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    st.write("---")
    
    # 5. GRÁFICOS DE CÍRCULOS INTERACTIVOS
    st.subheader("📊 Distribución Estructural de Capital")
    col_tarta1, col_tarta2 = st.columns(2)
    
    with col_tarta1:
        fig_tipo = px.pie(df, values="Valor actual", names="Tipo", title="Reparto por Categoría (Liquidez vs Acciones vs Fondos)", hole=0.4)
        st.plotly_chart(fig_tipo, use_container_width=True)
        
    with col_tarta2:
        fig_activo = px.pie(df, values="Valor actual", names="Activo", title="Concentración por Activos Individuales", hole=0.2)
        st.plotly_chart(fig_activo, use_container_width=True)
        
    st.write("---")
    
    # 6. OBJETIVOS DE PATRIMONIO (40k, 50k, 70k, 100k)
    st.subheader("🎯 Camino hacia la Libertad Financiera (Objetivos)")
    metas = [40000, 50000, 70000, 100000]
    columnas_metas = st.columns(4)
    
    for idx, meta in enumerate(metas):
        with columnas_metas[idx]:
            pct = (total_actual / meta) * 100
            pct_progreso = min(pct / 100, 1.0)
            st.metric(label=f"Objetivo {meta:,} €", value=f"{pct:.1f} %", delta=f"Faltan {(meta - total_actual):,.2f} €" if total_actual < meta else "¡Logrado! 🎉")
            st.progress(pct_progreso)
            
    st.write("---")
    
    # 7. PROYECCIÓN DE RENTABILIDAD
    st.subheader("🔮 Estimación de Rendimiento Pasivo Anualizado (Próximos 12 meses)")
    
    def rendimiento_teorico(row):
        if row["Tipo"] == "Acciones": return row["Valor actual"] * 0.08
        elif row["Tipo"] == "Fondos": return row["Valor actual"] * 0.06
        else: return row["Valor actual"] * 0.025

    df["Rendimiento Anual Esperado"] = df.apply(rendimiento_teorico, axis=1)
    anual_total = df["Rendimiento Anual Esperado"].sum()
    mensual_total = anual_total / 12
    
    col_r1, col_r2 = st.columns(2)
    col_r1.metric("Ingreso Estimado Promedio Mensual", f"+ {mensual_total:,.2f} € / mes")
    col_r2.metric("Retorno Estimado Total 12 Meses", f"+ {anual_total:,.2f} € / año", delta="Crecimiento Compuesto")