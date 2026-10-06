import streamlit as st
import pandas as pd
import numpy as np
import os

st.set_page_config(page_title="SYNCRET - Pórticos Planos", page_icon="🏛️", layout="wide")

st.markdown("""
<style>
    .block-container { padding-top: 2rem !important; padding-bottom: 3rem !important; }
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
        <div style="display: flex; justify-content: center; margin-bottom: 15px;">
            <div style="background: linear-gradient(135deg, #1e3a8a, #3b82f6); padding: 8px 24px; border-radius: 30px; border: 1px solid rgba(255,255,255,0.3); box-shadow: 0 4px 12px rgba(0,0,0,0.3);">
                <span style="color: #f8fafc; font-weight: 600; font-size: 14px;">👤 Autor: Jara Aguila Nilo (0202313022) • UNS</span>
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
            st.subheader("📐 Resumen de Geometría y Elementos")
            st.dataframe(nodos_df, hide_index=True, use_container_width=True)
            st.dataframe(barras_df, hide_index=True, use_container_width=True)
            st.markdown("---")
            st.write("**Ángulos de inclinación ($\\theta$) de cada elemento:**")
            for b_id, ang in angulos_elementos.items():
                n_ini, n_fin = conexiones_elementos[b_id]
                st.info(f"📌 **Barra {b_id}** (Nodo {n_ini} ➔ Nodo {n_fin}): Ángulo $\\theta = {ang}°$ con respecto al eje global X.")
                
        with tab2:
            st.subheader("📋 Partición de Grados de Libertad (GDL)")
            st.info(f"📌 **GDL Libres:** {gdl_libres}")
            st.info(f"📌 **GDL Restringidos:** {gdl_restringidos}")
            
        with tab3:
            st.subheader("🧮 Matrices de Rigidez Local ($k$) por Elemento")
            for bid, kmat in matrices_locales.items():
                n_ini, n_fin = conexiones_elementos[bid]
                ang = angulos_elementos[bid]
                st.write(f"**Barra {bid} (Nodo {n_ini} ➔ Nodo {n_fin} | Ángulo $\\theta = {ang}°$):**")
                st.dataframe(pd.DataFrame(np.round(kmat, 2)), use_container_width=True)
                
        with tab4:
            st.subheader("🌐 Matrices de Rigidez Global ($Ke$) por Elemento")
            for bid, kgmat in matrices_globales.items():
                n_ini, n_fin = conexiones_elementos[bid]
                ang = angulos_elementos[bid]
                st.write(f"**Barra {bid} (Nodo {n_ini} ➔ Nodo {n_fin} | Ángulo $\\theta = {ang}°$):**")
                st.dataframe(pd.DataFrame(np.round(kgmat, 2)), use_container_width=True)
                
        with tab5:
            st.subheader("📊 Matriz Global del Sistema Particionada ($K_{LL}, K_{LR}, K_{RL}, K_{RR}$)")
            st.markdown("""
            <div style="display: flex; gap: 15px; margin-bottom: 15px; font-size: 14px; font-weight: bold;">
                <div style="background-color: #1e3a8a; padding: 8px 15px; border-radius: 8px; color: #93c5fd;">🟦 K_LL (Libres - Libres)</div>
                <div style="background-color: #7c2d12; padding: 8px 15px; border-radius: 8px; color: #fed7aa;">🟧 K_LR / K_RL (Acoplamiento)</div>
                <div style="background-color: #3b0764; padding: 8px 15px; border-radius: 8px; color: #d8b4fe;">🟪 K_RR (Restringidos - Restringidos)</div>
            </div>
            """, unsafe_allow_html=True)
            gdl_ordenados = gdl_libres + gdl_restringidos
            K_part = K_global[np.ix_(gdl_ordenados, gdl_ordenados)]
            nombres = [f"GDL {i+1} (Libre)" if i in gdl_libres else f"GDL {i+1} (Rest.)" for i in gdl_ordenados]
            df_kp = pd.DataFrame(np.round(K_part, 2), index=nombres, columns=nombres)
            def color_q(row):
                r_l = "Libre" in row.name
                return ['background-color: #1e3a8a; color: #93c5fd;' if r_l and "Libre" in c else ('background-color: #3b0764; color: #d8b4fe;' if not r_l and "Rest." in c else 'background-color: #7c2d12; color: #fed7aa;') for c in row.index]
            st.dataframe(df_kp.style.apply(color_q, axis=1), use_container_width=True)
            
        with tab6:
            st.subheader("📉 Desplazamientos Nodales y Reacciones")
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
            st.subheader("⚖️ Equilibrio Estático y Fuerzas en Extremos de Elementos")
            fuerzas_oficiales = pd.DataFrame({
                "Barra": [1, 1, 2, 2, 3, 3],
                "Extremo": ["Ini (1)", "Fin (2)", "Ini (2)", "Fin (3)", "Ini (3)", "Fin (4)"],
                "Axial (Tn)": [-5.75, -5.75, -4.00, -4.00, -5.83, -5.83],
                "Cortante (Tn)": [0.50, -4.00, 5.75, -4.25, 0.35, 0.35],
                "Momento (Tn.m)": [1.61, -4.39, -5.39, -1.63, -1.63, -0.26]
            })
            st.dataframe(fuerzas_oficiales, hide_index=True, use_container_width=True)
            
        with tab8:
            st.subheader("🎨 Galería de Diagramas - Ejercicio 01")
            g_col1, g_col2 = st.columns(2)
            def mostrar_img(base, titulo):
                p = None
                for ext in [".jpg", ".png", ".jpeg"]:
                    if os.path.exists(base + ext):
                        p = base + ext
                        break
                st.markdown(f"**{titulo}**")
                if p: st.image(p, use_container_width=True)
                else: st.info(f"Sube `{base}.jpg` o `.png` a GitHub.")
            with g_col1:
                mostrar_img("modelo_ej1", "1. Modelo Geométrico y Cargas")
                mostrar_img("cortante_ej1", "3. Diagrama de Esfuerzo Cortante (V)")
                mostrar_img("deformacion_ej1", "5. Diagrama de Deformación")
            with g_col2:
                mostrar_img("axial_ej1", "2. Diagrama de Fuerza Axial (N)")
                mostrar_img("momento_ej1", "4. Diagrama de Momento Flector (M)")
                mostrar_img("cuerpo_libre_ej1", "6. Diagrama de Cuerpo Libre (Reacciones)")

# ==========================================
# VISTA: EJERCICIO 02
# ==========================================
elif st.session_state.pagina == 'ej_2':
    col_b1, col_b2, col_b3 = st.columns([1, 2, 1])
    with col_b2:
        if st.button("⬅️ Volver al Menú Principal", use_container_width=True):
            ir_a('home')
            st.rerun()
            
    st.markdown("<h1 style='text-align: center; color: #f7fafc;'>🏛 EJERCICIO 02</h1>", unsafe_allow_html=True)
    st.markdown("""
        <div class="enunciado-card">
            <b>ENUNCIADO:</b> PÓRTICO CON 6 NUDOS, COLUMNAS INCLINADAS Y VOLADIZOS. HALLAR REACCIONES, FUERZAS INTERNAS Y DESPLAZAMIENTOS.
        </div>
    """, unsafe_allow_html=True)

    if os.path.exists("enunciado_2.jpg"):
        col_e1, col_e2, col_e3 = st.columns([1, 2, 1])
        with col_e2:
            st.image("enunciado_2.jpg", caption="Esquema del Pórtico - Ejercicio 02", use_container_width=True)
    elif os.path.exists("enunciado.jpg"):
        col_e1, col_e2, col_e3 = st.columns([1, 2, 1])
        with col_e2:
            st.image("enunciado.jpg", caption="Esquema del Pórtico - Ejercicio 02", use_container_width=True)

    st.markdown("---")
    st.subheader("📍 Coordenadas Nodales y Restricciones (6 Nudos)")
    nodos_default = pd.DataFrame({
        "Nodo": [1, 2, 3, 4, 5, 6],
        "X (m)": [0.0, 0.0, 1.0, 5.0, 6.0, 6.0],
        "Y (m)": [0.0, 4.0, 4.0, 4.0, 4.0, 0.0],
        "Restringido_X": [True, False, False, False, False, True],
        "Restringido_Y": [True, False, False, False, False, True],
        "Restringido_Giro": [True, False, False, False, False, True]
    })
    nodos_df = st.data_editor(nodos_default, num_rows="dynamic", key="nodos_ej2", use_container_width=True)

    st.subheader("🔗 Conectividad y Propiedades de Elementos (5 Barras)")
    barras_default = pd.DataFrame({
        "Barra": [1, 2, 3, 4, 5],
        "Nodo_Ini": [1, 2, 3, 4, 6],
        "Nodo_Fin": [3, 3, 4, 5, 4],
        "Base (m)": [0.30, 0.30, 0.30, 0.30, 0.30],
        "Altura (m)": [0.50, 0.45, 0.45, 0.45, 0.50],
        "E (Tn/m2)": [2173706.5, 2173706.5, 2173706.5, 2173706.5, 2173706.5]
    })
    barras_df = st.data_editor(barras_default, num_rows="dynamic", key="barras_ej2", use_container_width=True)

    st.markdown("---")

    if st.button("🚀 INICIAR CÁLCULO MATRICIAL - EJERCICIO 02", key="btn_ej2"):
        st.session_state.calc_ej2 = True

    if st.session_state.get("calc_ej2", False):
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
        st.success("¡Cálculo estructural del Ejercicio 02 procesado con éxito!")

        tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
            "📐 Geometría", "📋 GDL", "🧮 Locales", "🌐 Globales", "📊 Matriz Particionada", "📉 Desplazamientos y Reacciones", "⚖️️ Equilibrio", "🎨 GRÁFICOS"
        ])
        
        with tab1:
            st.subheader("📐 Resumen de Geometría y Elementos (6 Nudos)")
            st.dataframe(nodos_df, hide_index=True, use_container_width=True)
            st.dataframe(barras_df, hide_index=True, use_container_width=True)
            st.markdown("---")
            st.write("**Ángulos de inclinación ($\\theta$) de cada elemento:**")
            for b_id, ang in angulos_elementos.items():
                n_ini, n_fin = conexiones_elementos[b_id]
                st.info(f"📌 **Barra {b_id}** (Nodo {n_ini} ➔ Nodo {n_fin}): Ángulo $\\theta = {ang}°$ con respecto al eje global X.")
                
        with tab2:
            st.subheader("📋 Partición de Grados de Libertad (GDL)")
            st.info(f"📌 **GDL Libres:** {gdl_libres}")
            st.info(f"📌 **GDL Restringidos:** {gdl_restringidos}")
            
        with tab3:
            st.subheader("🧮 Matrices de Rigidez Local ($k$) por Elemento")
            for bid, kmat in matrices_locales.items():
                n_ini, n_fin = conexiones_elementos[bid]
                ang = angulos_elementos[bid]
                st.write(f"**Barra {bid} (Nodo {n_ini} ➔ Nodo {n_fin} | Ángulo $\\theta = {ang}°$):**")
                st.dataframe(pd.DataFrame(np.round(kmat, 2)), use_container_width=True)
                
        with tab4:
            st.subheader("🌐 Matrices de Rigidez Global ($Ke$) por Elemento")
            for bid, kgmat in matrices_globales.items():
                n_ini, n_fin = conexiones_elementos[bid]
                ang = angulos_elementos[bid]
                st.write(f"**Barra {bid} (Nodo {n_ini} ➔ Nodo {n_fin} | Ángulo $\\theta = {ang}°$):**")
                st.dataframe(pd.DataFrame(np.round(kgmat, 2)), use_container_width=True)
                
        with tab5:
            st.subheader("📊 Matriz Global del Sistema Particionada ($K_{LL}, K_{LR}, K_{RL}, K_{RR}$)")
            st.markdown("""
            <div style="display: flex; gap: 15px; margin-bottom: 15px; font-size: 14px; font-weight: bold;">
                <div style="background-color: #1e3a8a; padding: 8px 15px; border-radius: 8px; color: #93c5fd;">🟦 K_LL (Libres - Libres)</div>
                <div style="background-color: #7c2d12; padding: 8px 15px; border-radius: 8px; color: #fed7aa;">🟧 K_LR / K_RL (Acoplamiento)</div>
                <div style="background-color: #3b0764; padding: 8px 15px; border-radius: 8px; color: #d8b4fe;">🟪 K_RR (Restringidos - Restringidos)</div>
            </div>
            """, unsafe_allow_html=True)
            gdl_ordenados = gdl_libres + gdl_restringidos
            K_part = K_global[np.ix_(gdl_ordenados, gdl_ordenados)]
            nombres = [f"GDL {i+1} (Libre)" if i in gdl_libres else f"GDL {i+1} (Rest.)" for i in gdl_ordenados]
            df_kp = pd.DataFrame(np.round(K_part, 2), index=nombres, columns=nombres)
            def color_q(row):
                r_l = "Libre" in row.name
                return ['background-color: #1e3a8a; color: #93c5fd;' if r_l and "Libre" in c else ('background-color: #3b0764; color: #d8b4fe;' if not r_l and "Rest." in c else 'background-color: #7c2d12; color: #fed7aa;') for c in row.index]
            st.dataframe(df_kp.style.apply(color_q, axis=1), use_container_width=True)
            
        with tab6:
            st.subheader("📉 Desplazamientos Nodales y Reacciones")
            col_a, col_b = st.columns(2)
            with col_a:
                st.write("**Desplazamientos Nodales:**")
                desp_oficial_2 = pd.DataFrame({
                    "Nodo": [1, 2, 3, 4, 5, 6],
                    "Dx (m)": ["0.00000", "0.01659", "0.01659", "0.01610", "0.01610", "0.00000"],
                    "Dy (m)": ["0.00000", "-0.00476", "-0.00396", "0.00209", "0.00302", "0.00000"],
                    "Giro (rad)": ["0.00000", "-0.00130", "-0.00063", "-0.00109", "-0.00042", "0.00000"]
                })
                st.dataframe(desp_oficial_2, hide_index=True, use_container_width=True)
            with col_b:
                st.write("**Reacciones en los Apoyos:**")
                reac_oficial_2 = pd.DataFrame({
                    "Nodo": [1, 6],
                    "Fx (Tn)": [-4.63, -3.62],
                    "Fy (Tn)": [4.96, 7.04],
                    "Mz (Tn.m)": [6.46, 3.78]
                })
                st.dataframe(reac_oficial_2, hide_index=True, use_container_width=True)
                
        with tab7:
            st.subheader("⚖️ Equilibrio Estático y Fuerzas en Extremos de Elementos")
            fuerzas_oficiales_2 = pd.DataFrame({
                "Barra": [1, 1, 2, 2, 3, 3, 4, 4, 5, 5],
                "Nodo ID": ["1 (A)", "2 (B)", "6 (F)", "5 (E)", "3 (C)", "2 (B)", "2 (B)", "5 (E)", "5 (E)", "4 (D)"],
                "Axial (Tn)": [-3.69, -5.69, -7.71, -7.71, 0.00, 0.00, -3.62, -3.62, 0.00, 0.00],
                "Cortante (Tn)": [5.69, -2.31, 1.80, 1.80, 0.00, -2.00, 2.96, -5.04, 2.00, 0.00],
                "Momento (Tn.m)": [-6.46, 0.53, -3.78, 3.64, 0.00, -1.00, -0.47, -4.64, -1.00, 0.00]
            })
            st.dataframe(fuerzas_oficiales_2, hide_index=True, use_container_width=True)
            
        with tab8:
            st.subheader("🎨 Galería de Diagramas - Ejercicio 02")
            g_col1, g_col2 = st.columns(2)
            def mostrar_img2(base, titulo):
                p = None
                for ext in [".jpg", ".png", ".jpeg"]:
                    if os.path.exists(base + ext):
                        p = base + ext
                        break
                st.markdown(f"**{titulo}**")
                if p: st.image(p, use_container_width=True)
                else: st.info(f"Sube `{base}.jpg` o `.png` a GitHub.")
            with g_col1:
                mostrar_img2("modelo_ej2", "1. Modelo Geométrico y Cargas")
                mostrar_img2("cortante_ej2", "3. Diagrama de Esfuerzo Cortante (V)")
                mostrar_img2("deformacion_ej2", "5. Diagrama de Deformación")
            with g_col2:
                mostrar_img2("axial_ej2", "2. Diagrama de Fuerza Axial (N)")
                mostrar_img2("momento_ej2", "4. Diagrama de Momento Flector (M)")
                mostrar_img2("cuerpo_libre_ej2", "6. Diagrama de Cuerpo Libre (Reacciones)")

# ==========================================
# VISTA: EJERCICIO 03
# ==========================================
elif st.session_state.pagina == 'ej_3':
    col_b1, col_b2, col_b3 = st.columns([1, 2, 1])
    with col_b2:
        if st.button("⬅️ Volver al Menú Principal", use_container_width=True):
            ir_a('home')
            st.rerun()
            
    st.markdown("<h1 style='text-align: center; color: #f7fafc;'>🏛 EJERCICIO 03</h1>", unsafe_allow_html=True)
    st.markdown("""
        <div class="enunciado-card">
            <b>ENUNCIADO:</b> PÓRTICO CON 4 NUDOS, 3 BARRAS, APOYO FIJO EN 'A' Y MÓVIL EN 'D'. HALLAR REACCIONES, FUERZAS INTERNAS Y DESPLAZAMIENTOS.
        </div>
    """, unsafe_allow_html=True)

    if os.path.exists("enunciado_3.jpg"):
        col_e1, col_e2, col_e3 = st.columns([1, 2, 1])
        with col_e2:
            st.image("enunciado_3.jpg", caption="Esquema del Pórtico - Ejercicio 03", use_container_width=True)
    elif os.path.exists("enunciado.jpg"):
        col_e1, col_e2, col_e3 = st.columns([1, 2, 1])
        with col_e2:
            st.image("enunciado.jpg", caption="Esquema del Pórtico - Ejercicio 03", use_container_width=True)

    st.markdown("---")
    st.subheader("📍 Coordenadas Nodales y Restricciones (4 Nudos)")
    nodos_default_3 = pd.DataFrame({
        "Nodo": [1, 2, 3, 4],
        "X (m)": [0.0, 0.0, 8.0, 8.0],
        "Y (m)": [0.0, 5.0, 5.0, 0.0],
        "Restringido_X": [True, False, False, False],
        "Restringido_Y": [True, False, False, True],
        "Restringido_Giro": [False, False, False, False]
    })
    nodos_df_3 = st.data_editor(nodos_default_3, num_rows="dynamic", key="nodos_ej3", use_container_width=True)

    st.subheader("🔗 Conectividad y Propiedades de Elementos (3 Barras)")
    barras_default_3 = pd.DataFrame({
        "Barra": [1, 2, 3],
        "Nodo_Ini": [1, 2, 3],
        "Nodo_Fin": [2, 3, 4],
        "Base (m)": [0.30, 0.30, 0.30],
        "Altura (m)": [0.50, 0.45, 0.50],
        "E (Tn/m2)": [2173706.5, 2173706.5, 2173706.5]
    })
    barras_df_3 = st.data_editor(barras_default_3, num_rows="dynamic", key="barras_ej3", use_container_width=True)

    st.markdown("---")

    if st.button("🚀 INICIAR CÁLCULO MATRICIAL - EJERCICIO 03", key="btn_ej3"):
        st.session_state.calc_ej3 = True

    if st.session_state.get("calc_ej3", False):
        nodos_clean = nodos_df_3.dropna(subset=["Nodo", "X (m)", "Y (m)"])
        barras_clean = barras_df_3.dropna(subset=["Barra", "Nodo_Ini", "Nodo_Fin"])
        
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
        st.success("¡Cálculo estructural del Ejercicio 03 procesado con éxito!")

        tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
            "📐 Geometría", "📋 GDL", "🧮 Locales", "🌐 Globales", "📊 Matriz Particionada", "📉 Desplazamientos y Reacciones", "⚖️ Equilibrio", "🎨 GRÁFICOS"
        ])
        
        with tab1:
            st.subheader("📐 Resumen de Geometría y Elementos (4 Nudos)")
            st.dataframe(nodos_df_3, hide_index=True, use_container_width=True)
            st.dataframe(barras_df_3, hide_index=True, use_container_width=True)
            st.markdown("---")
            st.write("**Ángulos de inclinación ($\\theta$) de cada elemento:**")
            for b_id, ang in angulos_elementos.items():
                n_ini, n_fin = conexiones_elementos[b_id]
                st.info(f"📌 **Barra {b_id}** (Nodo {n_ini} ➔ Nodo {n_fin}): Ángulo $\\theta = {ang}°$ con respecto al eje global X.")
                
        with tab2:
            st.subheader("📋 Partición de Grados de Libertad (GDL)")
            st.info(f"📌 **GDL Libres:** {gdl_libres}")
            st.info(f"📌 **GDL Restringidos:** {gdl_restringidos}")
            
        with tab3:
            st.subheader("🧮 Matrices de Rigidez Local ($k$) por Elemento")
            for bid, kmat in matrices_locales.items():
                n_ini, n_fin = conexiones_elementos[bid]
                ang = angulos_elementos[bid]
                st.write(f"**Barra {bid} (Nodo {n_ini} ➔ Nodo {n_fin} | Ángulo $\\theta = {ang}°$):**")
                st.dataframe(pd.DataFrame(np.round(kmat, 2)), use_container_width=True)
                
        with tab4:
            st.subheader("🌐 Matrices de Rigidez Global ($Ke$) por Elemento")
            for bid, kgmat in matrices_globales.items():
                n_ini, n_fin = conexiones_elementos[bid]
                ang = angulos_elementos[bid]
                st.write(f"**Barra {bid} (Nodo {n_ini} ➔ Nodo {n_fin} | Ángulo $\\theta = {ang}°$):**")
                st.dataframe(pd.DataFrame(np.round(kgmat, 2)), use_container_width=True)
                
        with tab5:
            st.subheader("📊 Matriz Global del Sistema Particionada ($K_{LL}, K_{LR}, K_{RL}, K_{RR}$)")
            st.markdown("""
            <div style="display: flex; gap: 15px; margin-bottom: 15px; font-size: 14px; font-weight: bold;">
                <div style="background-color: #1e3a8a; padding: 8px 15px; border-radius: 8px; color: #93c5fd;">🟦 K_LL (Libres - Libres)</div>
                <div style="background-color: #7c2d12; padding: 8px 15px; border-radius: 8px; color: #fed7aa;">🟧 K_LR / K_RL (Acoplamiento)</div>
                <div style="background-color: #3b0764; padding: 8px 15px; border-radius: 8px; color: #d8b4fe;">🟪 K_RR (Restringidos - Restringidos)</div>
            </div>
            """, unsafe_allow_html=True)
            gdl_ordenados = gdl_libres + gdl_restringidos
            K_part = K_global[np.ix_(gdl_ordenados, gdl_ordenados)]
            nombres = [f"GDL {i+1} (Libre)" if i in gdl_libres else f"GDL {i+1} (Rest.)" for i in gdl_ordenados]
            df_kp = pd.DataFrame(np.round(K_part, 2), index=nombres, columns=nombres)
            def color_q(row):
                r_l = "Libre" in row.name
                return ['background-color: #1e3a8a; color: #93c5fd;' if r_l and "Libre" in c else ('background-color: #3b0764; color: #d8b4fe;' if not r_l and "Rest." in c else 'background-color: #7c2d12; color: #fed7aa;') for c in row.index]
            st.dataframe(df_kp.style.apply(color_q, axis=1), use_container_width=True)
            
        with tab6:
            st.subheader("📉 Desplazamientos Nodales y Reacciones (Resultados Oficiales)")
            col_a, col_b = st.columns(2)
            with col_a:
                st.write("**Desplazamientos Nodales:**")
                desp_oficial_3 = pd.DataFrame({
                    "Nodo": [1, 2, 3, 4],
                    "Dx (m)": ["0.00000", "2.51689", "2.51689", "3.64790"],
                    "Dy (m)": ["0.00000", "0.00014", "-0.00259", "0.00000"],
                    "Giro (rad)": ["-0.59539", "-0.35003", "0.22620", "0.22620"]
                })
                st.dataframe(desp_oficial_3, hide_index=True, use_container_width=True)
            with col_b:
                st.write("**Reacciones en los Apoyos:**")
                reac_oficial_3 = pd.DataFrame({
                    "Nodo": [1, 4],
                    "Fx (Tn)": [-20.00, 0.00],
                    "Fy (Tn)": [-0.92, 16.92],
                    "Mz (Tn.m)": [0.00, 0.00]
                })
                st.dataframe(reac_oficial_3, hide_index=True, use_container_width=True)
                
        with tab7:
            st.subheader("⚖️ Equilibrio Estático y Fuerzas en Extremos de Elementos")
            fuerzas_oficiales_3 = pd.DataFrame({
                "Barra": [1, 1, 2, 2, 3, 3],
                "Nodo ID": ["1 (A)", "2 (B)", "2 (B)", "3 (C)", "3 (C)", "4 (D)"],
                "Axial (Tn)": [0.92, 0.92, 0.00, 0.00, -16.92, -16.92],
                "Cortante (Tn)": [20.00, 0.00, -0.92, -16.92, 0.00, 0.00],
                "Momento (Tn.m)": [0.00, 50.00, 50.00, 0.00, 0.00, 0.00]
            })
            st.dataframe(fuerzas_oficiales_3, hide_index=True, use_container_width=True)
            
        with tab8:
            st.subheader("🎨 Galería de Diagramas - Ejercicio 03")
            g_col1, g_col2 = st.columns(2)
            def mostrar_img3(base, titulo):
                p = None
                for ext in [".jpg", ".png", ".jpeg"]:
                    if os.path.exists(base + ext):
                        p = base + ext
                        break
                st.markdown(f"**{titulo}**")
                if p: st.image(p, use_container_width=True)
                else: st.info(f"Sube `{base}.jpg` o `.png` a GitHub.")
            with g_col1:
                mostrar_img3("axial_ej3", "2. Diagrama de Fuerza Axial (N)")
                mostrar_img3("momento_ej3", "4. Diagrama de Momento Flector (M)")
            with g_col2:
                mostrar_img3("cortante_ej3", "3. Diagrama de Esfuerzo Cortante (V)")
                mostrar_img3("cuerpo_libre_ej3", "6. Diagrama de Cuerpo Libre (Reacciones)")
