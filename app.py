import streamlit as st
import pandas as pd
import numpy as np
import os

st.set_page_config(
    page_title="SYNCRET - Pórticos Planos | Jara Aguila Nilo (0202313022)", 
    page_icon="🏛️", 
    layout="wide"
)

st.markdown("""
<style>
    /* Margen superior corregido para que el badge del autor no se corte */
    .block-container { padding-top: 3.5rem !important; padding-bottom: 3rem !important; }
    .stApp { 
        background: linear-gradient(rgba(9, 13, 22, 0.94), rgba(20, 27, 45, 0.96)), 
                    url('https://images.unsplash.com/photo-1541888946425-d0fbb18f248e?q=80&w=1920&auto=format&fit=crop');
        background-size: cover; background-position: center; background-attachment: fixed;
        color: #f7fafc;
    }
    /* Estilo para los botones principales y de navegación */
    .stButton button {
        background: linear-gradient(135deg, #1d4ed8, #3b82f6) !important;
        color: white !important; font-weight: 700 !important; font-size: 16px !important;
        border-radius: 14px !important; height: 58px !important; width: 100% !important; 
        border: 2px solid rgba(255,255,255,0.25) !important;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.35);
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.55);
        border-color: rgba(255,255,255,0.5) !important;
    }
    /* Tarjeta de Enunciado Mejorada */
    .enunciado-card {
        background: rgba(30, 41, 59, 0.85);
        padding: 20px 25px;
        border-left: 6px solid #3b82f6;
        border-radius: 12px;
        font-size: 16px;
        font-weight: 500;
        color: #f1f5f9;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        margin-bottom: 25px;
        line-height: 1.5;
        word-wrap: break-word;
    }
    /* Pestañas (Tabs) grandes y visibles */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        justify-content: center;
        background-color: rgba(15, 23, 42, 0.7);
        padding: 12px;
        border-radius: 14px;
        box-shadow: inset 0 2px 8px rgba(0,0,0,0.4);
    }
    .stTabs [data-baseweb="tab"] {
        height: 55px;
        background-color: #1e293b !important;
        border-radius: 10px !important;
        padding: 0 22px;
        font-size: 16px !important;
        font-weight: 700 !important;
        color: #cbd5e1 !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #1d4ed8, #3b82f6) !important;
        color: white !important;
        font-size: 17px !important;
        border: 1px solid rgba(255,255,255,0.4) !important;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.5);
    }
    /* Tablas más limpias y legibles */
    table { font-size: 14px !important; background-color: rgba(15, 23, 42, 0.6) !important; }
</style>
""", unsafe_allow_html=True)

# --- CONTROL DE NAVEGACIÓN POR ESTADOS ---
if 'pagina' not in st.session_state:
    st.session_state.pagina = 'home'

def ir_a(menu):
    st.session_state.pagina = menu

# ==========================================
# PÁGINA PRINCIPAL (Estilo Armaduras 3D)
# ==========================================
if st.session_state.pagina == 'home':
    st.markdown("""
        <div style="display: flex; justify-content: center; margin-top: 10px; margin-bottom: 20px;">
            <div style="background: linear-gradient(135deg, #1e3a8a, #3b82f6); padding: 10px 28px; border-radius: 30px; border: 1px solid rgba(255,255,255,0.3); box-shadow: 0 4px 12px rgba(0,0,0,0.3);">
                <span style="color: #f8fafc; font-weight: 600; font-size: 15px;">👤 Autor: Jara Aguila Nilo (0202313022) • UNS</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("<h1 style='text-align: center; color: #f7fafc; font-size: 2.7rem; margin-bottom: 5px;'>📈 Sistematización del método de Rigidez</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #93c5fd; font-size: 1.25rem; margin-bottom: 25px;'>Procedimiento para Pórticos Planos</p>", unsafe_allow_html=True)
    
    st.markdown("<p style='text-align: center; color: #cbd5e1; font-size: 1.1rem; font-weight: 500; margin-bottom: 25px;'>🎯 Selecciona una Opción o Ejercicio a Evaluar</p>", unsafe_allow_html=True)

    col_m1, col_m2, col_m3 = st.columns([1, 1.4, 1])
    with col_m2:
        if st.button("🔷 EJERCICIO 1", use_container_width=True):
            ir_a('ej_1')
            st.session_state.calc_ej1 = False
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🟢 EJERCICIO 2", use_container_width=True):
            ir_a('ej_2')
            st.session_state.calc_ej2 = False
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔶 EJERCICIO 3", use_container_width=True):
            ir_a('ej_3')
            st.session_state.calc_ej3 = False
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("📑 CONCLUSIONES DEL TRABAJO", use_container_width=True):
            ir_a('conclusiones')

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 13px;'>Universidad Nacional del Santa • Análisis Estructural II • Desarrollado por Jara Aguila Nilo (0202313022)</p>", unsafe_allow_html=True)

# ==========================================
# VISTA: CONCLUSIONES DEL TRABAJO (6 Conclusiones)
# ==========================================
elif st.session_state.pagina == 'conclusiones':
    col_b1, col_b2, col_b3 = st.columns([1, 2, 1])
    with col_b2:
        if st.button("⬅️ Volver al Menú Principal", use_container_width=True):
            ir_a('home')
            st.rerun()

    st.markdown("<h1 style='text-align: center; color: #f7fafc;'>📑 Conclusiones del Trabajo</h1>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("""
    <div style="background: rgba(30, 41, 59, 0.85); padding: 30px; border-radius: 12px; font-size: 16px; color: #f1f5f9; line-height: 1.8; box-shadow: 0 4px 20px rgba(0,0,0,0.4);">
        <ol style="margin: 0; padding-left: 20px;">
            <li style="margin-bottom: 15px;"><b>Sistematización Eficiente:</b> La sistematización del método matricial de rigideces desarrollada en la plataforma permite optimizar el análisis estructural de pórticos planos, automatizando el armado de matrices y reduciendo los márgenes de error operativo frente a los métodos manuales tradicionales.</li>
            <li style="margin-bottom: 15px;"><b>Transformación de Coordenadas:</b> La correcta implementación de las matrices de transformación global y local demostró ser indispensable para modelar con precisión elementos con orientaciones geométricas específicas, tales como columnas inclinadas y voladizos, asegurando la correcta transmisión de grados de libertad.</li>
            <li style="margin-bottom: 15px;"><b>Condiciones de Contorno y Apoyos:</b> El planteamiento riguroso de restricciones nodales y apoyos (empotrados, fijos y móviles) resulta fundamental para reflejar de forma realista el comportamiento físico de la estructura y garantizar la estabilidad estática del sistema global.</li>
            <li style="margin-bottom: 15px;"><b>Efecto de Cargas Distribuidas y Triangulares:</b> El uso adecuado de vectores de cargas equivalentes y de empotramiento perfecto permitió incorporar con alta fidelidad tanto estados de carga uniformes como distribuciones triangulares a lo largo de las vigas y columnas del pórtico.</li>
            <li style="margin-bottom: 15px;"><b>Equilibrio Estático y Fuerzas Internas:</b> El cálculo de las fuerzas internas (axiales, cortantes y momentos flectores) cumplió cabalmente con las leyes del equilibrio estático global, validando la consistencia matemática de los desplazamientos nodales y las reacciones en los apoyos.</li>
            <li><b>Aporte Académico y Profesional:</b> La herramienta desarrollada consolida los fundamentos teóricos del Análisis Estructural II, constituyendo un valioso soporte didáctico y técnico para la evaluación, diseño y comprensión del comportamiento elástico en edificaciones aporticadas.</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# VISTA: EJERCICIO 01
# ==========================================
elif st.session_state.pagina == 'ej_1':
    col_b1, col_b2, col_b3 = st.columns([1, 2, 1])
    with col_b2:
        if st.button("⬅️ Volver al Menú Principal", use_container_width=True):
            ir_a('home')
            st.rerun()
            
    st.markdown("<h1 style='text-align: center; color: #f7fafc;'>🏛 EJERCICIO 01</h1>", unsafe_allow_html=True)
    st.markdown("""
        <div class="enunciado-card">
            <b>ENUNCIADO:</b> HALLAR LAS REACCIONES, FUERZAS AXIALES, ESFUERZOS DE CORTE, MOMENTOS FLECTORES Y DESPLAZAMIENTOS.
        </div>
    """, unsafe_allow_html=True)

    if os.path.exists("enunciado_1.jpg"):
        col_e1, col_e2, col_e3 = st.columns([1, 2, 1])
        with col_e2:
            st.image("enunciado_1.jpg", caption="Esquema del Pórtico - Ejercicio 01", use_container_width=True)

    st.markdown("---")
    st.subheader("📍 Coordenadas Nodales y Restricciones")
    nodos_default = pd.DataFrame({
        "Nodo": [1, 2, 3, 4], "X (m)": [0.0, 0.0, 5.0, 7.5], "Y (m)": [0.0, 3.0, 3.0, 0.0],
        "Restringido_X": [True, False, False, True], "Restringido_Y": [True, False, False, True], "Restringido_Giro": [True, False, False, True]
    })
    nodos_df = st.data_editor(nodos_default, num_rows="dynamic", key="nodos_ej1", use_container_width=True)

    st.subheader("🔗 Conectividad y Propiedades de Elementos")
    barras_default = pd.DataFrame({
        "Barra": [1, 2, 3], "Nodo_Ini": [1, 2, 3], "Nodo_Fin": [2, 3, 4],
        "Base (m)": [0.30, 0.30, 0.30], "Altura (m)": [0.50, 0.45, 0.50], "E (Tn/m2)": [2173706.5, 2173706.5, 2173706.5]
    })
    barras_df = st.data_editor(barras_default, num_rows="dynamic", key="barras_ej1", use_container_width=True)

    st.markdown("---")

    if st.button("🚀 INICIAR CÁLCULO MATRICIAL - EJERCICIO 01", key="btn_ej1"):
        st.session_state.calc_ej1 = True

    if st.session_state.get("calc_ej1", False):
        nodos_clean = nodos_df.dropna(subset=["Nodo", "X (m)", "Y (m)"])
        barras_clean = barras_df.dropna(subset=["Barra", "Nodo_Ini", "Nodo_Fin"])
        
        n_nodos = len(nodos_clean)
        n_gdl = 3 * n_nodos
        nodo_idx = {int(row["Nodo"]): i for i, row in nodos_clean.iterrows()}
        
        gdl_restringidos = []
        for i, row in nodos_clean.iterrows():
            idx = nodo_idx[row["Nodo"]]
            if row["Restringido_X"]: gdl_restringidos.append(3*idx)
            if row["Restringido_Y"]: gdl_restringidos.append(3*idx + 1)
            if row["Restringido_Giro"]: gdl_restringidos.append(3*idx + 2)
            
        gdl_libres = [i for i in range(n_gdl) if i not in gdl_restringidos]
        
        K_global = np.zeros((n_gdl, n_gdl))
        matrices_locales = {}
        matrices_globales = {}
        angulos_elementos = {}
        conexiones_elementos = {}
        
        for _, barra in barras_clean.iterrows():
            b_id = int(barra["Barra"])
            n1_id = int(barra["Nodo_Ini"])
            n2_id = int(barra["Nodo_Fin"])
            n1 = nodos_clean[nodos_clean["Nodo"] == n1_id].iloc[0]
            n2 = nodos_clean[nodos_clean["Nodo"] == n2_id].iloc[0]
            dx, dy = n2["X (m)"] - n1["X (m)"], n2["Y (m)"] - n1["Y (m)"]
            L = np.sqrt(dx**2 + dy**2)
            ang = round(np.degrees(np.arctan2(dy, dx)), 2)
            angulos_elementos[b_id] = ang
            conexiones_elementos[b_id] = (n1_id, n2_id)
            
            c, s = dx / L, dy / L
            b, h, E = barra["Base (m)"], barra["Altura (m)"], barra["E (Tn/m2)"]
            A, I = b * h, (b * h**3) / 12.0
            ae_l, ei = (A * E) / L, E * I
            
            K_L = np.zeros((6, 6))
            K_L[0,0] = ae_l; K_L[0,3] = -ae_l; K_L[3,0] = -ae_l; K_L[3,3] = ae_l
            K_L[1,1] = 12.0*ei/L**3; K_L[1,2] = 6.0*ei/L**2; K_L[1,4] = -12.0*ei/L**3; K_L[1,5] = 6.0*ei/L**2
            K_L[2,1] = 6.0*ei/L**2; K_L[2,2] = 4.0*ei/L; K_L[2,4] = -6.0*ei/L**2; K_L[2,5] = 2.0*ei/L
            K_L[4,1] = -12.0*ei/L**3; K_L[4,2] = -6.0*ei/L**2; K_L[4,4] = 12.0*ei/L**3; K_L[4,5] = -6.0*ei/L**2
            K_L[5,1] = 6.0*ei/L**2; K_L[5,2] = 2.0*ei/L; K_L[5,4] = -6.0*ei/L**2; K_L[5,5] = 4.0*ei/L
            matrices_locales[b_id] = K_L.copy()
            
            Tg = np.array([[c, s, 0, 0, 0, 0], [-s, c, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0], [0, 0, 0, c, s, 0], [0, 0, 0, -s, c, 0], [0, 0, 0, 0, 0, 1]])
            K_g_elem = Tg.T @ K_L @ Tg
            matrices_globales[b_id] = K_g_elem.copy()
            
            idx1, idx2 = nodo_idx[n1_id], nodo_idx[n2_id]
            gdl_elem = [3*idx1, 3*idx1+1, 3*idx1+2, 3*idx2, 3*idx2+1, 3*idx2+2]
            for i in range(6):
                for j in range(6):
                    K_global[gdl_elem[i], gdl_elem[j]] += K_g_elem[i, j]

        st.balloons()
        st.success("¡Cálculo estructural del Ejercicio 01 procesado con éxito!")

        tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
            "📐 Geometría", "📋 GDL", "🧮 Locales", "🌐 Globales", "📊 Matriz Particionada", "📉 Desplazamientos y Reacciones", "⚖️ Equilibrio", "🎨 GRÁFICOS"
        ])
        
        with tab1:
            st.subheader("📐 Resumen
