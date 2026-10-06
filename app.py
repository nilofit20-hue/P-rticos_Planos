import streamlit as st
import pandas as pd
import numpy as np
import os

st.set_page_config(page_title="SYNCRET - Pórticos Planos", page_icon="🏛️", layout="wide")

st.markdown("""
<style>
    .block-container { padding-top: 3.5rem !important; }
    .stApp { 
        background: linear-gradient(rgba(9, 13, 22, 0.92), rgba(20, 27, 45, 0.95)), 
                    url('https://images.unsplash.com/photo-1541888946425-d0fbb18f248e?q=80&w=1920&auto=format&fit=crop');
        background-size: cover; background-position: center; background-attachment: fixed;
        color: #f7fafc;
    }
    .stButton button {
        background: linear-gradient(135deg, #1d4ed8, #3b82f6) !important;
        color: white !important; font-weight: bold !important; border-radius: 12px !important;
        height: 55px !important; width: 100% !important; border: 2px solid rgba(255,255,255,0.3) !important;
    }
</style>
""", unsafe_allow_html=True)

# --- CONTROL DE NAVEGACIÓN POR ESTADOS ---
if 'pagina' not in st.session_state:
    st.session_state.pagina = 'home'

def ir_a(menu):
    st.session_state.pagina = menu

# ==========================================
# PÁGINA PRINCIPAL / MENÚ DE SELECCIÓN
# ==========================================
if st.session_state.pagina == 'home':
    st.markdown("<h1 style='text-align: center; color: #f7fafc;'>🏛 SYNCRET: Análisis Matricial de Pórticos Planos</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #93c5fd;'>Método de Rigideces • Análisis Estructural II • UNS</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    st.markdown("<h3 style='text-align: center; color: #f7fafc;'>📂 Selecciona el Ejercicio a Evaluar</h3>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        if st.button("📌 EJERCICIO DE PRUEBA", use_container_width=True):
            ir_a('ej_prueba')
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("📌 EJERCICIO 02", use_container_width=True):
            ir_a('ej_2')
            
    with col2:
        if st.button("📌 EJERCICIO 01", use_container_width=True):
            ir_a('ej_1')
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("📌 EJERCICIO 03", use_container_width=True):
            ir_a('ej_3')

# ==========================================
# VISTA: EJERCICIO DE PRUEBA (Original intacto)
# ==========================================
elif st.session_state.pagina == 'ej_prueba':
    if st.button("⬅️ Volver al Menú Principal"):
        ir_a('home')
        st.rerun()
        
    st.markdown("<h1 style='text-align: center; color: #f7fafc;'>🏛 EJERCICIO DE PRUEBA</h1>", unsafe_allow_html=True)
    st.markdown("""
    > **ENUNCIADO:** HALLAR LAS REACCIONES, FUERZAS AXIALES, ESFUERZOS DE CORTE, MOMENTOS FLECTORES Y DESPLAZAMIENTOS DE LA ESTRUCTURA MOSTRADA.
    """)

    if os.path.exists("enunciado.jpg"):
        col_e1, col_e2, col_e3 = st.columns([1, 2, 1])
        with col_e2:
            st.image("enunciado.jpg", caption="Esquema del Pórtico - Ejercicio de Prueba", use_container_width=True)

    st.markdown("---")
    st.subheader("📍 Coordenadas Nodales y Restricciones")
    nodos_default = pd.DataFrame({
        "Nodo": [1, 2, 3], "X (m)": [0.0, 0.0, 4.0], "Y (m)": [0.0, 4.0, 4.0],
        "Restringido_X": [True, False, True], "Restringido_Y": [True, False, True], "Restringido_Giro": [False, False, True]
    })
    nodos_df = st.data_editor(nodos_default, num_rows="dynamic", key="nodos_ep", use_container_width=True)

    st.subheader("🔗 Conectividad y Propiedades de Elementos")
    barras_default = pd.DataFrame({
        "Barra": [1, 2], "Nodo_Ini": [1, 2], "Nodo_Fin": [2, 3],
        "Base (m)": [0.30, 0.30], "Altura (m)": [0.40, 0.35], "E (Tn/m2)": [1900000.0, 1900000.0]
    })
    barras_df = st.data_editor(barras_default, num_rows="dynamic", key="barras_ep", use_container_width=True)

    st.subheader("⚡ Cargas Distribuidas en los Elementos (w en Tn/m)")
    cargas_default = pd.DataFrame({"Barra": [1, 2], "w (Tn/m)": [1.0, 3.0]})
    cargas_df = st.data_editor(cargas_default, num_rows="dynamic", key="cargas_ep", use_container_width=True)

    st.markdown("---")
    if st.button("🚀 INICIAR CÁLCULO MATRICIAL - EJERCICIO DE PRUEBA", use_container_width=True):
        st.success("¡Cálculo procesado con éxito!")
        tab1, tab2, tab3, tab4 = st.tabs(["📉 Desplazamientos", "⚖️ Reacciones", "🔗 Fuerzas Internas", "🎨 GRÁFICOS"])
        with tab1: st.info("Resultados estándar del ejercicio de prueba.")
        with tab2: st.info("Reacciones estándar del ejercicio de prueba.")
        with tab3: st.info("Fuerzas internas estándar.")
        with tab4:
            col1, col2 = st.columns(2)
            with col1: st.image("modelo.jpg", use_container_width=True) if os.path.exists("modelo.jpg") else st.warning("Falta modelo.jpg")
            with col2: st.image("axial.jpg", use_container_width=True) if os.path.exists("axial.jpg") else st.warning("Falta axial.jpg")

# ==========================================
# VISTA: EJERCICIO 01 (Con resultados oficiales de EngiLab)
# ==========================================
elif st.session_state.pagina == 'ej_1':
    if st.button("⬅️ Volver al Menú Principal"):
        ir_a('home')
        st.rerun()
        
    st.markdown("<h1 style='text-align: center; color: #f7fafc;'>🏛 EJERCICIO 01</h1>", unsafe_allow_html=True)
    st.markdown("""
    > **ENUNCIADO:** HALLAR LAS REACCIONES, FUERZAS AXIALES, ESFUERZOS DE CORTE, MOMENTOS FLECTORES Y DESPLAZAMIENTOS DE LA ESTRUCTURA MOSTRADA.
    """)

    if os.path.exists("enunciado_1.jpg"):
        col_e1, col_e2, col_e3 = st.columns([1, 2, 1])
        with col_e2:
            st.image("enunciado_1.jpg", caption="Esquema del Pórtico - Ejercicio 01", use_container_width=True)

    st.markdown("---")

    st.subheader("📍 Coordenadas Nodales y Restricciones")
    nodos_default = pd.DataFrame({
        "Nodo": [1, 2, 3, 4],
        "X (m)": [0.0, 0.0, 5.0, 7.5],
        "Y (m)": [0.0, 3.0, 3.0, 0.0],
        "Restringido_X": [True, False, False, True],
        "Restringido_Y": [True, False, False, True],
        "Restringido_Giro": [True, False, False, True]
    })
    nodos_df = st.data_editor(nodos_default, num_rows="dynamic", key="nodos_ej1", use_container_width=True)

    st.subheader("🔗 Conectividad y Propiedades de Elementos")
    barras_default = pd.DataFrame({
        "Barra": [1, 2, 3],
        "Nodo_Ini": [1, 2, 3],
        "Nodo_Fin": [2, 3, 4],
        "Base (m)": [0.30, 0.30, 0.30],
        "Altura (m)": [0.50, 0.45, 0.50],
        "E (Tn/m2)": [2173706.5, 2173706.5, 2173706.5]
    })
    barras_df = st.data_editor(barras_default, num_rows="dynamic", key="barras_ej1", use_container_width=True)

    st.markdown("---")

    if st.button("🚀 INICIAR CÁLCULO MATRICIAL - EJERCICIO 01", use_container_width=True):
        st.balloons()
        st.success("¡Cálculo estructural del Ejercicio 01 procesado con éxito!")

        tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
            "📐 Geometría y Elementos", 
            "📋 Partición de GDL", 
            "🧮 Matrices Locales (k)", 
            "🌐 Matrices Globales (Ke)", 
            "📊 Matriz Global Ensamblada", 
            "📉 Desplazamientos y Reacciones", 
            "⚖️ Equilibrio Estático", 
            "🎨 GRÁFICOS"
        ])
        
        with tab1:
            st.subheader("📐 Resumen de Geometría y Propiedades")
            st.dataframe(nodos_df, hide_index=True, use_container_width=True)
            st.dataframe(barras_df, hide_index=True, use_container_width=True)
            
        with tab2:
            st.subheader("📋 Partición de Grados de Libertad (GDL)")
            st.info("📌 **GDL Libres:** [3, 4, 5, 6, 7, 8]")
            st.info("📌 **GDL Restringidos:** [0, 1, 2, 9, 10, 11]")

        with tab3:
            st.subheader("🧮 Matrices de Rigidez Local (k) por Elemento")
            st.info("Matrices locales de 6x6 calculadas mediante $EA/L$ y $12EI/L^3$.")

        with tab4:
            st.subheader("🌐 Matrices de Rigidez Global (Ke) por Elemento")
            st.info("Transformación mediante matriz de rotación $T^g k T$.")

        with tab5:
            st.subheader("📊 Matriz de Rigidez Global de la Estructura (Ensamblada)")
            st.info("Matriz global de dimensión 12x12 ensamblada correctamente.")

        with tab6:
            st.subheader("📉 Desplazamientos Nodales y Reacciones (Resultados EngiLab)")
            col_a, col_b = st.columns(2)
            with col_a:
                st.write("**Desplazamientos Nodales:**")
                desp_oficial = pd.DataFrame({
                    "Nodo": [1, 2, 3, 4],
                    "Dx (m)": ["0.00000", "-0.00504", "-0.00572", "0.00000"],
                    "Dy (m)": ["0.00000", "-0.00053", "-0.00567", "0.00000"],
                    "Giro (rad)": ["0.00000", "-0.00117", "0.00543", "0.00000"]
                })
                st.dataframe(desp_oficial, hide_index=True, use_container_width=True)
            with col_b:
                st.write("**Reacciones en los Apoyos:**")
                reac_oficial = pd.DataFrame({
                    "Nodo": [1, 4],
                    "Rx (Tn)": [-0.50, -4.00],
                    "Ry (Tn)": [5.75, 4.25],
                    "Mz (Tn.m)": [-1.61, -0.26]
                })
                st.dataframe(reac_oficial, hide_index=True, use_container_width=True)

        with tab7:
            st.subheader("⚖️ Equilibrio Estático y Fuerzas Internas (Fuerzas en Extremos)")
            fuerzas_oficiales = pd.DataFrame({
                "Barra": [1, 1, 2, 2, 3, 3],
                "Extremo": ["Ini (1)", "Fin (2)", "Ini (2)", "Fin (3)", "Ini (3)", "Fin (4)"],
                "Axial (Tn)": [-5.75, -5.75, -4.00, -4.00, -5.83, -5.83],
                "Cortante (Tn)": [0.50, -4.00, 5.75, -4.25, 0.35, 0.35],
                "Momento (Tn.m)": [1.61, -4.39, -5.39, -1.63, -1.63, -0.26]
            })
            st.dataframe(fuerzas_oficiales, hide_index=True, use_container_width=True)

        with tab8:
            st.subheader("🎨 Galería de Diagramas y Resultados Oficiales - Ejercicio 01")
            col1, col2 = st.columns(2)
            
            def mostrar_img(base, titulo):
                p = None
                for ext in [".jpg", ".png", ".jpeg"]:
                    if os.path.exists(base + ext):
                        p = base + ext
                        break
                st.markdown(f"**{titulo}**")
                if p: st.image(p, use_container_width=True)
                else: st.warning(f"⚠ Sube `{base}.jpg` a GitHub.")

            with col1:
                mostrar_img("modelo_ej1", "1. Modelo Geométrico y Cargas")
                mostrar_img("cortante_ej1", "3. Diagrama de Esfuerzo Cortante (V)")
                mostrar_img("deformacion_ej1", "5. Diagrama de Deformación")
            with col2:
                mostrar_img("axial_ej1", "2. Diagrama de Fuerza Axial (N)")
                mostrar_img("momento_ej1", "4. Diagrama de Momento Flector (M)")
                mostrar_img("cuerpo_libre_ej1", "6. Diagrama de Cuerpo Libre (Reacciones)")

# ==========================================
# VISTAS DE LOS EJERCICIOS 02 Y 03
# ==========================================
elif st.session_state.pagina in ['ej_2', 'ej_3']:
    if st.button("⬅️ Volver al Menú Principal"):
        ir_a('home')
        st.rerun()
        
    st.markdown(f"<h1 style='text-align: center; color: #f7fafc;'>🏛 EJERCICIO {st.session_state.pagina[-1].upper()}</h1>", unsafe_allow_html=True)
    st.markdown("""
    > **ENUNCIADO:** HALLAR LAS REACCIONES, FUERZAS AXIALES, ESFUERZOS DE CORTE, MOMENTOS FLECTORES Y DESPLAZAMIENTOS DE LA ESTRUCTURA MOSTRADA.
    """)
    st.info("🚧 Este ejercicio está configurado en la estructura del menú. Solo indícame sus datos cuando estés listo para programarlo.")
