import streamlit as st
import pandas as pd
import random
import time

# 1. Configuración de la página
st.set_page_config(page_title="Simulador Estadístico", layout="centered")
# --- OCULTAR MARCA DE AGUA Y MENÚ ---
ocultar_menu_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """
st.markdown(ocultar_menu_style, unsafe_allow_html=True)
# ------------------------------------
st.title("La Ley de los Grandes Números 🎲")
st.markdown("Observa cómo la suma de dos dados converge hacia una distribución normal (Campana de Gauss). El 7 es matemáticamente el resultado más probable.")

# 2. Inicializar el Estado (Nuestra "Base de Datos" en memoria)
if 'frecuencias' not in st.session_state:
    st.session_state.frecuencias = {i: 0 for i in range(2, 13)} # Sumas del 2 al 12
if 'total_lanzamientos' not in st.session_state:
    st.session_state.total_lanzamientos = 0

# 3. Lógica de Negocio (Función reutilizable)
def lanzar_lote(cantidad):
    """Calcula n lanzamientos instantáneamente y actualiza el estado"""
    for _ in range(cantidad):
        suma = random.randint(1, 6) + random.randint(1, 6)
        st.session_state.frecuencias[suma] += 1
    st.session_state.total_lanzamientos += cantidad

# 4. Interfaz de Usuario: Panel de Control
st.subheader("Control de Simulación")

# Usamos columnas para alinear los botones como un panel de control profesional
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    if st.button("🎲 1 Vez", use_container_width=True):
        # La animación visual solo tiene sentido cuando es 1 solo lanzamiento
        placeholder = st.empty()
        for _ in range(5):
            d1, d2 = random.randint(1, 6), random.randint(1, 6)
            placeholder.markdown(f"<p style='text-align: center; color: gray;'>{d1} - {d2}</p>", unsafe_allow_html=True)
            time.sleep(0.05)
        placeholder.empty() # Limpiamos la animación
        lanzar_lote(1)

with col2:
    if st.button("🚀 +50", use_container_width=True):
        lanzar_lote(50)

with col3:
    if st.button("🔥 +100", use_container_width=True):
        lanzar_lote(100)

with col4:
    if st.button("⚡ +1000", use_container_width=True):
        lanzar_lote(1000)

with col5:
    if st.button("🗑️ Reset", use_container_width=True, type="primary"):
        st.session_state.frecuencias = {i: 0 for i in range(2, 13)}
        st.session_state.total_lanzamientos = 0

# 5. Métricas en vivo
st.metric(label="Total de Lanzamientos Acumulados", value=f"{st.session_state.total_lanzamientos:,}")

# 6. Visualización Dinámica de Datos
st.divider()

# Convertimos el diccionario a DataFrame para graficar
df = pd.DataFrame({
    "Suma de Dados": list(st.session_state.frecuencias.keys()),
    "Frecuencia": list(st.session_state.frecuencias.values())
}).set_index("Suma de Dados")

# Gráfico de barras
st.bar_chart(df, y="Frecuencia", color="#007AFF")