import streamlit as st
import pandas as pd
import random
import time

# 1. Configuración de la página
st.set_page_config(page_title="Simulador de Dados", layout="centered")
st.title("Distribución Estadística: Lanzamiento de Dados 🎲")
st.markdown("Demostración en vivo de la convergencia hacia el número 7.")

# 2. Inicializar la "Base de Datos" temporal (El Estado)
# Si es la primera vez que se abre la app, creamos un diccionario con ceros.
if 'frecuencias' not in st.session_state:
    st.session_state.frecuencias = {i: 0 for i in range(2, 13)}  # Posibles sumas: del 2 al 12

# 3. Interfaz de Usuario: Contenedores y Botones
col1, col2 = st.columns([1, 2])

with col1:
    lanzar_btn = st.button("🎲 Lanzar Dados", use_container_width=True)

with col2:
    # st.empty() crea un contenedor que podemos sobrescribir para hacer la animación
    dado_placeholder = st.empty()

# 4. Lógica del Botón y Animación
if lanzar_btn:
    # Animación rápida simulando que se agitan los dados
    for _ in range(10):
        d1, d2 = random.randint(1, 6), random.randint(1, 6)
        dado_placeholder.markdown(f"<h2 style='text-align: center; color: gray;'>Agitando... {d1} - {d2}</h2>",
                                  unsafe_allow_html=True)
        time.sleep(0.05)  # Pausa de milisegundos

    # Resultado real final
    final_d1 = random.randint(1, 6)
    final_d2 = random.randint(1, 6)
    suma = final_d1 + final_d2

    # Mostrar el resultado final en grande
    dado_placeholder.markdown(
        f"<h2 style='text-align: center; color: #007AFF;'>Resultado: {final_d1} + {final_d2} = {suma}</h2>",
        unsafe_allow_html=True)

    # Actualizar la persistencia de datos
    st.session_state.frecuencias[suma] += 1

# 5. Visualización Dinámica de Datos
st.divider()
st.subheader("Gráfica de Frecuencias (Eje Y: Cantidad, Eje X: Suma)")

# Convertir nuestro diccionario a un DataFrame de Pandas para que Streamlit lo grafique
df = pd.DataFrame({
    "Suma de Dados": list(st.session_state.frecuencias.keys()),
    "Apariciones": list(st.session_state.frecuencias.values())
}).set_index("Suma de Dados")

# Gráfico de barras nativo
st.bar_chart(df, y="Apariciones")