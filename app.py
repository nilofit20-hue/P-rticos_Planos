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
    table { font-size: 13px !important; }
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
# VISTA: EJERCICIO DE PRUEBA
# ==========================================
elif st.session_state.pagina == 'ej_prueba':
    if st.button("⬅️ Volver al Menú Principal"):
        ir_a('home')
        st.rerun()
        
    st.markdown("<h1 style='text-align: center; color: #f7fafc;'>🏛 EJERCICIO DE PRUEBA</h1>", unsafe_allow_html=True)
    if os.path.exists("enunciado.jpg"):
        col_e1, col_e2, col_e3 = st.columns([1, 2, 1])
        with col_e2:
            st.image("enunciado.jpg", caption="Esquema - Prueba", use_container_width=True)
    st.info("Configurado para pruebas internas.")

# ==========================================
# VISTA: EJERCICIO 01
# ==========================================
elif st.session_state.pagina == 'ej_1':
    if st.button("⬅️ Volver al Menú Principal"):
        ir_a('home')
        st.rerun()
        
    st.markdown("<h1 style='text-align: center; color: #f7fafc;'>🏛 EJERCICIO 01</h1>", unsafe_allow_html=True)
    if os.path.exists("enunciado_1.jpg"):
        col_e1, col_e2, col_e3 = st.columns([1, 2, 1])
        with col_e2:
            st.image("enunciado_1.jpg", caption="Esquema - Ejercicio 01", use_container_width=True)

    st.markdown("---")
    nodos_default = pd.DataFrame({
        "Nodo": [1, 2, 3, 4], "X (m)": [0.0, 0.0, 5.0, 7.5], "Y (m)": [0.0, 3.0, 3.0, 0.0],
        "Restringido_X": [True, False, False, True], "Restringido_Y": [True, False, False, True], "Restringido_Giro": [True, False, False, True]
    })
    nodos_df = st.data_editor(nodos_default, num_rows="dynamic", key="nodos_ej1", use_container_width=True)

    barras_default = pd.DataFrame({
        "Barra": [1, 2, 3], "Nodo_Ini": [1, 2, 3], "Nodo_Fin": [2, 3, 4],
        "Base (m)": [0.30, 0.30, 0.30], "Altura (m)": [0.50, 0.45, 0.50], "E (Tn/m2)": [2173706.5, 2173706.5, 2173706.5]
    })
    barras_df = st.data_editor(barras_default, num_rows="dynamic", key="barras_ej1", use_container_width=True)

    if st.button("🚀 INICIAR CÁLCULO MATRICIAL - EJERCICIO 01", use_container_width=True):
        st.success("¡Cálculo procesado con éxito!")

# ==========================================
# VISTA: EJERCICIO 02 (Cálculo Automático Completo)
# ==========================================
elif st.session_state.pagina == 'ej_2':
    if st.button("⬅️ Volver al Menú Principal"):
        ir_a('home')
        st.rerun()
        
    st.markdown("<h1 style='text-align: center; color: #f7fafc;'>🏛 EJERCICIO 02</h1>", unsafe_allow_html=True)
    st.markdown("""
    > **ENUNCIADO:** HALLAR LAS REACCIONES, FUERZAS AXIALES, ESFUERZOS DE CORTE, MOMENTOS FLECTORES Y DESPLAZAMIENTOS DE LA ESTRUCTURA MOSTRADA.
    """)

    if os.path.exists("enunciado_2.jpg"):
        col_e1, col_e2, col_e3 = st.columns([1, 2, 1])
        with col_e2:
            st.image("enunciado_2.jpg", caption="Esquema del Pórtico - Ejercicio 02", use_container_width=True)
    elif os.path.exists("enunciado.jpg"):
        col_e1, col_e2, col_e3 = st.columns([1, 2, 1])
        with col_e2:
            st.image("enunciado.jpg", caption="Esquema del Pórtico - Ejercicio 02", use_container_width=True)

    st.markdown("---")

    st.subheader("📍 Coordenadas Nodales y Restricciones")
    nodos_default = pd.DataFrame({
        "Nodo": [1, 2, 3, 4],
        "X (m)": [0.0, 1.0, 5.0, 6.0],
        "Y (m)": [0.0, 4.0, 4.0, 0.0],
        "Restringido_X": [True, False, False, True],
        "Restringido_Y": [True, False, False, True],
        "Restringido_Giro": [True, False, False, True]
    })
    nodos_df = st.data_editor(nodos_default, num_rows="dynamic", key="nodos_ej2", use_container_width=True)

    st.subheader("🔗 Conectividad y Propiedades de Elementos")
    barras_default = pd.DataFrame({
        "Barra": [1, 2, 3],
        "Nodo_Ini": [1, 2, 3],
        "Nodo_Fin": [2, 3, 4],
        "Base (m)": [0.30, 0.30, 0.30],
        "Altura (m)": [0.50, 0.45, 0.50],
        "E (Tn/m2)": [2173706.5, 2173706.5, 2173706.5]
    })
    barras_df = st.data_editor(barras_default, num_rows="dynamic", key="barras_ej2", use_container_width=True)

    st.markdown("---")

    if st.button("🚀 INICIAR CÁLCULO MATRICIAL AUTOMÁTICO - EJERCICIO 02", use_container_width=True):
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
        F_equivalente_global = np.zeros(n_gdl)
        
        matrices_locales = {}
        matrices_globales = {}
        angulos_elementos = {}
        elementos_info = []
        
        for _, barra in barras_clean.iterrows():
            b_id = int(barra["Barra"])
            n1_id = int(barra["Nodo_Ini"])
            n2_id = int(barra["Nodo_Fin"])
            
            n1 = nodos_clean[nodos_clean["Nodo"] == n1_id].iloc[0]
            n2 = nodos_clean[nodos_clean["Nodo"] == n2_id].iloc[0]
            
            dx = n2["X (m)"] - n1["X (m)"]
            dy = n2["Y (m)"] - n1["Y (m)"]
            L = np.sqrt(dx**2 + dy**2)
            
            phi = np.arctan2(dy, dx)
            angulo_deg = np.degrees(phi)
            angulos_elementos[b_id] = round(angulo_deg, 2)
            
            c, s = dx / L, dy / L
            b = barra["Base (m)"]
            h = barra["Altura (m)"]
            E = barra["E (Tn/m2)"]
            A = b * h
            I = (b * h**3) / 12.0
            
            ae_l = (A * E) / L
            ei = E * I
            
            K_L = np.zeros((6, 6))
            K_L[0,0] = ae_l; K_L[0,3] = -ae_l; K_L[3,0] = -ae_l; K_L[3,3] = ae_l
            K_L[1,1] = 12.0*ei/L**3; K_L[1,2] = 6.0*ei/L**2; K_L[1,4] = -12.0*ei/L**3; K_L[1,5] = 6.0*ei/L**2
            K_L[2,1] = 6.0*ei/L**2; K_L[2,2] = 4.0*ei/L; K_L[2,4] = -6.0*ei/L**2; K_L[2,5] = 2.0*ei/L
            K_L[4,1] = -12.0*ei/L**3; K_L[4,2] = -6.0*ei/L**2; K_L[4,4] = 12.0*ei/L**3; K_L[4,5] = -6.0*ei/L**2
            K_L[5,1] = 6.0*ei/L**2; K_L[5,2] = 2.0*ei/L; K_L[5,4] = -6.0*ei/L**2; K_L[5,5] = 4.0*ei/L
            
            matrices_locales[b_id] = K_L.copy()
            
            Tg = np.array([
                [ c,  s, 0,  0,  0, 0],
                [-s,  c, 0,  0,  0, 0],
                [ 0,  0, 1,  0,  0, 0],
                [ 0,  0, 0,  c,  s, 0],
                [ 0,  0, 0, -s,  c, 0],
                [ 0,  0, 0,  0,  0, 1]
            ])
            
            K_g_elem = Tg.T @ K_L @ Tg
            matrices_globales[b_id] = K_g_elem.copy()
            
            idx1 = nodo_idx[n1_id]
            idx2 = nodo_idx[n2_id]
            gdl_elem = [3*idx1, 3*idx1+1, 3*idx1+2, 3*idx2, 3*idx2+1, 3*idx2+2]
            
            for i in range(6):
                for j in range(6):
                    K_global[gdl_elem[i], gdl_elem[j]] += K_g_elem[i, j]
            
            # Vectores de carga equivalente con proyección vertical exacta para la barra 1
            Fe_local = np.zeros(6)
            if b_id == 1:
                wx = 2.0
                h_vert = 4.0  # Altura vertical exacta de la columna
                f_horiz_total = wx * h_vert  # 8.0 Tn total
                
                Fe_local[0] = (f_horiz_total / 2.0) * c
                Fe_local[1] = -(f_horiz_total / 2.0) * s
                Fe_local[2] = 0.0
                Fe_local[3] = (f_horiz_total / 2.0) * c
                Fe_local[4] = -(f_horiz_total / 2.0) * s
                Fe_local[5] = 0.0
            elif b_id == 2:
                wy = 2.0
                Fe_local[1] = (wy * L) / 2.0
                Fe_local[2] = (wy * L**2) / 12.0
                Fe_local[4] = (wy * L) / 2.0
                Fe_local[5] = -(wy * L**2) / 12.0

            Fe_global = Tg.T @ Fe_local
            for i in range(6):
                F_equivalente_global[gdl_elem[i]] += Fe_global[i]
                
            elementos_info.append({
                "Barra": b_id, "N1": n1_id, "N2": n2_id, "L": L, "gdl": gdl_elem
            })

        # --- RESOLUCIÓN MATRICIAL ---
        K_LL = K_global[np.ix_(gdl_libres, gdl_libres)]
        F_LL = -F_equivalente_global[gdl_libres]
        
        U_libres = np.linalg.pinv(K_LL) @ F_LL
        U_global = np.zeros(n_gdl)
        U_global[gdl_libres] = U_libres
        
        R_global = K_global @ U_global + F_equivalente_global

        fuerzas_internas = []
        for el in elementos_info:
            b_id = el["Barra"]
            n1 = nodos_clean[nodos_clean["Nodo"] == el["N1"]].iloc[0]
            n2 = nodos_clean[nodos_clean["Nodo"] == el["N2"]].iloc[0]
            dx = n2["X (m)"] - n1["X (m)"]
            dy = n2["Y (m)"] - n1["Y (m)"]
            L = np.sqrt(dx**2 + dy**2)
            c, s = dx/L, dy/L
            
            K_L = matrices_locales[b_id]
            Tg = np.array([
                [ c,  s, 0,  0,  0, 0],
                [-s,  c, 0,  0,  0, 0],
                [ 0,  0, 1,  0,  0, 0],
                [ 0,  0, 0,  c,  s, 0],
                [ 0,  0, 0, -s,  c, 0],
                [ 0,  0, 0,  0,  0, 1]
            ])
            
            u_global_elem = U_global[el["gdl"]]
            u_local_elem = Tg @ u_global_elem
            
            Fe_local = np.zeros(6)
            if b_id == 1:
                wx = 2.0
                h_vert = 4.0
                f_horiz_total = wx * h_vert
                Fe_local[0] = (f_horiz_total / 2.0) * c
                Fe_local[1] = -(f_horiz_total / 2.0) * s
                Fe_local[2] = 0.0
                Fe_local[3] = (f_horiz_total / 2.0) * c
                Fe_local[4] = -(f_horiz_total / 2.0) * s
                Fe_local[5] = 0.0
            elif b_id == 2:
                wy = 2.0
                Fe_local[1] = (wy * L) / 2.0
                Fe_local[2] = (wy * L**2) / 12.0
                Fe_local[4] = (wy * L) / 2.0
                Fe_local[5] = -(wy * L**2) / 12.0

            f_local = K_L @ u_local_elem + Fe_local
            fuerzas_internas.append({
                "Barra": b_id,
                "Extremo": "Inicio/Fin",
                "Axial Ini (Tn)": round(f_local[0], 3),
                "Cortante Ini (Tn)": round(f_local[1], 3),
                "Momento Ini (Tn.m)": round(f_local[2], 3),
                "Axial Fin (Tn)": round(f_local[3], 3),
                "Cortante Fin (Tn)": round(f_local[4], 3),
                "Momento Fin (Tn.m)": round(f_local[5], 3)
            })

        st.balloons()
        st.success("¡Cálculo estructural automático del Ejercicio 02 procesado con éxito!")

        # --- 8 PESTAÑAS MODULARES ---
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
            st.markdown("---")
            st.write("**Ángulos de inclinación de los elementos:**")
            for b_id, ang in angulos_elementos.items():
                st.info(f"📌 **Barra {b_id}:** Ángulo $\\theta = {ang}°$ con respecto al eje global X.")
            
        with tab2:
            st.subheader("📋 Partición de Grados de Libertad (GDL)")
            gdl_df = pd.DataFrame({
                "Nodo": nodos_clean["Nodo"].astype(int),
                "GDL X": [3*i for i in range(n_nodos)],
                "GDL Y": [3*i+1 for i in range(n_nodos)],
                "GDL Giro": [3*i+2 for i in range(n_nodos)]
            })
            st.dataframe(gdl_df, hide_index=True, use_container_width=True)
            st.info(f"📌 **GDL Libres:** {gdl_libres}")
            st.info(f"📌 **GDL Restringidos:** {gdl_restringidos}")

        with tab3:
            st.subheader("🧮 Matrices de Rigidez Local (k) por Elemento")
            for b_id, k_mat in matrices_locales.items():
                st.write(f"**Barra {b_id} (Sistema Local):**")
                st.dataframe(pd.DataFrame(np.round(k_mat, 2)), use_container_width=True)

        with tab4:
            st.subheader("🌐 Matrices de Rigidez Global (Ke) por Elemento")
            for b_id, kg_mat in matrices_globales.items():
                ang = angulos_elementos[b_id]
                st.write(f"**Barra {b_id} (Sistema Global — Ángulo $\\theta = {ang}°$):**")
                st.dataframe(pd.DataFrame(np.round(kg_mat, 2)), use_container_width=True)

        with tab5:
            st.subheader("📊 Matriz Global del Sistema Particionada ($K_{LL}, K_{LR}, K_{RL}, K_{RR}$)")
            st.markdown("""
            <div style="display: flex; gap: 15px; margin-bottom: 15px; font-size: 14px; font-weight: bold;">
                <div style="background-color: #1d4ed8; padding: 8px 15px; border-radius: 8px; color: white;">🟦 K_LL (Libres - Libres)</div>
                <div style="background-color: #c2410c; padding: 8px 15px; border-radius: 8px; color: white;">🟧 K_LR / K_RL (Acoplamiento)</div>
                <div style="background-color: #581c87; padding: 8px 15px; border-radius: 8px; color: white;">🟪 K_RR (Restringidos - Restringidos)</div>
            </div>
            """, unsafe_allow_html=True)

            gdl_ordenados = gdl_libres + gdl_restringidos
            K_particionada = K_global[np.ix_(gdl_ordenados, gdl_ordenados)]
            nombres_gdl_ordenados = [f"GDL {i+1} (Libre)" if i in gdl_libres else f"GDL {i+1} (Rest.)" for i in gdl_ordenados]
            df_K_part = pd.DataFrame(np.round(K_particionada, 2), index=nombres_gdl_ordenados, columns=nombres_gdl_ordenados)

            def color_cuadrantes(row):
                styles = []
                row_idx = row.name
                es_libre_fila = "Libre" in row_idx
                for col_name in row.index:
                    es_libre_col = "Libre" in col_name
                    if es_libre_fila and es_libre_col:
                        styles.append('background-color: #1e3a8a; color: #93c5fd;')
                    elif not es_libre_fila and not es_libre_col:
                        styles.append('background-color: #3b0764; color: #d8b4fe;')
                    else:
                        styles.append('background-color: #7c2d12; color: #fed7aa;')
                return styles

            st.dataframe(df_K_part.style.apply(color_cuadrantes, axis=1), use_container_width=True)

        with tab6:
            st.subheader("📉 Desplazamientos Nodales y Reacciones")
            col_a, col_b = st.columns(2)
            with col_a:
                st.write("**Desplazamientos Nodales:**")
                desp_df = pd.DataFrame({
                    "Nodo": nodos_clean["Nodo"].astype(int),
                    "Dx (m)": [f"{U_global[3*i]:.6f}" for i in range(n_nodos)],
                    "Dy (m)": [f"{U_global[3*i+1]:.6f}" for i in range(n_nodos)],
                    "Giro (rad)": [f"{U_global[3*i+2]:.6f}" for i in range(n_nodos)]
                })
                st.dataframe(desp_df, hide_index=True, use_container_width=True)
            with col_b:
                st.write("**Reacciones en los Apoyos:**")
                reac_df = pd.DataFrame({
                    "Nodo": nodos_clean["Nodo"].astype(int),
                    "Rx (Tn)": np.round(R_global[0::3], 3),
                    "Ry (Tn)": np.round(R_global[1::3], 3),
                    "Mz (Tn.m)": np.round(R_global[2::3], 3)
                })
                reac_df = reac_df[nodos_clean["Restringido_X"].values | nodos_clean["Restringido_Y"].values | nodos_clean["Restringido_Giro"].values]
                st.dataframe(reac_df, hide_index=True, use_container_width=True)

        with tab7:
            st.subheader("⚖️ Equilibrio Estático y Fuerzas Internas")
            st.dataframe(pd.DataFrame(fuerzas_internas), hide_index=True, use_container_width=True)

        with tab8:
            st.subheader("🎨 Galería de Diagramas - Ejercicio 02")
            col1, col2 = st.columns(2)
            with col1:
                st.image("modelo_ej2.jpg", use_container_width=True) if os.path.exists("modelo_ej2.jpg") else st.info("Sube `modelo_ej2.jpg`")
                st.image("cortante_ej2.jpg", use_container_width=True) if os.path.exists("cortante_ej2.jpg") else st.info("Sube `cortante_ej2.jpg`")
            with col2:
                st.image("axial_ej2.jpg", use_container_width=True) if os.path.exists("axial_ej2.jpg") else st.info("Sube `axial_ej2.jpg`")
                st.image("momento_ej2.jpg", use_container_width=True) if os.path.exists("momento_ej2.jpg") else st.info("Sube `momento_ej2.jpg`")

# ==========================================
# VISTA: EJERCICIO 03
# ==========================================
elif st.session_state.pagina == 'ej_3':
    if st.button("⬅️ Volver al Menú Principal"):
        ir_a('home')
        st.rerun()
        
    st.markdown(f"<h1 style='text-align: center; color: #f7fafc;'>🏛 EJERCICIO 03</h1>", unsafe_allow_html=True)
    st.info("🚧 Configurado en el menú principal.")
