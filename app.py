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
        "Nodo": [1, 2, 3],
        "X (m)": [0.0, 0.0, 4.0],
        "Y (m)": [0.0, 4.0, 4.0],
        "Restringido_X": [True, False, True],
        "Restringido_Y": [True, False, True],
        "Restringido_Giro": [False, False, True]
    })
    nodos_df = st.data_editor(nodos_default, num_rows="dynamic", key="nodos_ep", use_container_width=True)

    st.subheader("🔗 Conectividad y Propiedades de Elementos")
    barras_default = pd.DataFrame({
        "Barra": [1, 2],
        "Nodo_Ini": [1, 2],
        "Nodo_Fin": [2, 3],
        "Base (m)": [0.30, 0.30],
        "Altura (m)": [0.40, 0.35],
        "E (Tn/m2)": [1900000.0, 1900000.0]
    })
    barras_df = st.data_editor(barras_default, num_rows="dynamic", key="barras_ep", use_container_width=True)

    st.subheader("⚡ Cargas Distribuidas en los Elementos (w en Tn/m)")
    cargas_default = pd.DataFrame({
        "Barra": [1, 2],
        "w (Tn/m)": [1.0, 3.0]
    })
    cargas_df = st.data_editor(cargas_default, num_rows="dynamic", key="cargas_ep", use_container_width=True)

    st.markdown("---")

    if st.button("🚀 INICIAR CÁLCULO MATRICIAL - EJERCICIO DE PRUEBA", use_container_width=True):
        try:
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
            
            elementos_info = []
            fuerzas_internas = []
            matrices_locales = {}
            matrices_globales = {}
            
            for _, barra in barras_clean.iterrows():
                b_id = int(barra["Barra"])
                n1_id = int(barra["Nodo_Ini"])
                n2_id = int(barra["Nodo_Fin"])
                
                n1 = nodos_clean[nodos_clean["Nodo"] == n1_id].iloc[0]
                n2 = nodos_clean[nodos_clean["Nodo"] == n2_id].iloc[0]
                
                dx = n2["X (m)"] - n1["X (m)"]
                dy = n2["Y (m)"] - n1["Y (m)"]
                L = np.sqrt(dx**2 + dy**2)
                
                cos_phi = dx / L
                sin_phi = dy / L
                
                b = barra["Base (m)"]
                h = barra["Altura (m)"]
                E = barra["E (Tn/m2)"]
                A = b * h
                I = (b * h**3) / 12.0
                
                ae_l = (A * E) / L
                ei = E * I
                
                k11 = ae_l
                k22 = 12.0 * ei / L**3
                k23 = 6.0 * ei / L**2
                k33 = 4.0 * ei / L
                k36 = 2.0 * ei / L
                
                K_L = np.zeros((6, 6))
                K_L[0,0] = k11; K_L[0,3] = -k11; K_L[3,0] = -k11; K_L[3,3] = k11
                K_L[1,1] = k22; K_L[1,2] = k23; K_L[1,4] = -k22; K_L[1,5] = k23
                K_L[2,1] = k23; K_L[2,2] = k33; K_L[2,4] = -k23; K_L[2,5] = k36
                K_L[4,1] = -k22; K_L[4,2] = -k23; K_L[4,4] = k22; K_L[4,5] = -k23
                K_L[5,1] = k23; K_L[5,2] = k36; K_L[5,4] = -k23; K_L[5,5] = k33
                
                matrices_locales[b_id] = K_L.copy()
                
                c = cos_phi
                s = sin_phi
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
                        
                w_val = cargas_df[cargas_df["Barra"] == b_id]["w (Tn/m)"].values[0]
                Fe_local = np.array([
                    0.0,
                    (w_val * L) / 2.0,
                    (w_val * L**2) / 12.0,
                    0.0,
                    (w_val * L) / 2.0,
                    -(w_val * L**2) / 12.0
                ])
                
                Fe_global = Tg.T @ Fe_local
                for i in range(6):
                    F_equivalente_global[gdl_elem[i]] += Fe_global[i]
                    
                elementos_info.append({
                    "Barra": b_id, "N1": n1_id, "N2": n2_id, "L": L, "w": w_val, "gdl": gdl_elem
                })

            K_LL = K_global[np.ix_(gdl_libres, gdl_libres)]
            F_LL = -F_equivalente_global[gdl_libres]
            
            U_libres = np.linalg.pinv(K_LL) @ F_LL
            U_global = np.zeros(n_gdl)
            U_global[gdl_libres] = U_libres
            
            R_global = K_global @ U_global + F_equivalente_global

            for el in elementos_info:
                b_id = el["Barra"]
                n1 = nodos_clean[nodos_clean["Nodo"] == el["N1"]].iloc[0]
                n2 = nodos_clean[nodos_clean["Nodo"] == el["N2"]].iloc[0]
                dx = n2["X (m)"] - n1["X (m)"]
                dy = n2["Y (m)"] - n1["Y (m)"]
                L = np.sqrt(dx**2 + dy**2)
                c, s = dx/L, dy/L
                
                b_row = barras_clean[barras_clean["Barra"] == b_id].iloc[0]
                A = b_row["Base (m)"] * b_row["Altura (m)"]
                I = (b_row["Base (m)"] * b_row["Altura (m)"]**3) / 12.0
                E = b_row["E (Tn/m2)"]
                ae_l, ei = (A * E) / L, E * I
                
                k11 = ae_l
                k22 = 12.0 * ei / L**3
                k23 = 6.0 * ei / L**2
                k33 = 4.0 * ei / L
                k36 = 2.0 * ei / L
                
                K_L = np.zeros((6, 6))
                K_L[0,0] = k11; K_L[0,3] = -k11; K_L[3,0] = -k11; K_L[3,3] = k11
                K_L[1,1] = k22; K_L[1,2] = k23; K_L[1,4] = -k22; K_L[1,5] = k23
                K_L[2,1] = k23; K_L[2,2] = k33; K_L[2,4] = -k23; K_L[2,5] = k36
                K_L[4,1] = -k22; K_L[4,2] = -k23; K_L[4,4] = k22; K_L[4,5] = -k23
                K_L[5,1] = k23; K_L[5,2] = k36; K_L[5,4] = -k23; K_L[5,5] = k33
                
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
                Fe_local = np.array([0.0, (el["w"] * L)/2.0, (el["w"] * L**2)/12.0, 0.0, (el["w"] * L)/2.0, -(el["w"] * L**2)/12.0])
                f_local = K_L @ u_local_elem + Fe_local
                
                fuerzas_internas.append({
                    "Barra": b_id,
                    "Axial Ini (Tn)": round(f_local[0], 3),
                    "Cortante Ini (Tn)": round(f_local[1], 3),
                    "Momento Ini (Tn.m)": round(f_local[2], 3),
                    "Axial Fin (Tn)": round(f_local[3], 3),
                    "Cortante Fin (Tn)": round(f_local[4], 3),
                    "Momento Fin (Tn.m)": round(f_local[5], 3)
                })

            st.balloons()
            st.success("¡Cálculo matricial procesado con éxito!")

            tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
                "📐 Geometría y Elementos", "📋 Partición de GDL", "🧮 Matrices Locales (k)", 
                "🌐 Matrices Globales (Ke)", "📊 Matriz Global Ensamblada", "📉 Desplazamientos y Reacciones", 
                "⚖️ Equilibrio Estático", "🎨 GRÁFICOS"
            ])
            
            with tab1:
                st.subheader("📐 Resumen de Geometría y Propiedades")
                st.dataframe(nodos_clean, hide_index=True, use_container_width=True)
                st.dataframe(barras_clean, hide_index=True, use_container_width=True)
            with tab2:
                st.subheader("📋 Partición de Grados de Libertad (GDL)")
                st.info(f"📌 **GDL Libres:** {gdl_libres}")
                st.info(f"📌 **GDL Restringidos:** {gdl_restringidos}")
            with tab3:
                st.subheader("🧮 Matrices de Rigidez Local (k)")
                for b_id, k_mat in matrices_locales.items():
                    st.write(f"**Barra {b_id}:**")
                    st.dataframe(pd.DataFrame(np.round(k_mat, 2)), use_container_width=True)
            with tab4:
                st.subheader("🌐 Matrices de Rigidez Global (Ke)")
                for b_id, kg_mat in matrices_globales.items():
                    st.write(f"**Barra {b_id}:**")
                    st.dataframe(pd.DataFrame(np.round(kg_mat, 2)), use_container_width=True)
            with tab5:
                st.subheader("📊 Matriz Global Ensamblada")
                st.dataframe(pd.DataFrame(np.round(K_global, 2)), use_container_width=True)
            with tab6:
                st.subheader("📉 Desplazamientos y Reacciones")
                col_a, col_b = st.columns(2)
                with col_a:
                    desp_df = pd.DataFrame({"Nodo": nodos_clean["Nodo"].astype(int), "Dx": [f"{U_global[3*i]:.6f}" for i in range(n_nodos)], "Dy": [f"{U_global[3*i+1]:.6f}" for i in range(n_nodos)], "Giro": [f"{U_global[3*i+2]:.6f}" for i in range(n_nodos)]})
                    st.dataframe(desp_df, hide_index=True, use_container_width=True)
                with col_b:
                    reac_df = pd.DataFrame({"Nodo": nodos_clean["Nodo"].astype(int), "Rx": np.round(R_global[0::3], 3), "Ry": np.round(R_global[1::3], 3), "Mz": np.round(R_global[2::3], 3)})
                    reac_df = reac_df[nodos_clean["Restringido_X"].values | nodos_clean["Restringido_Y"].values | nodos_clean["Restringido_Giro"].values]
                    st.dataframe(reac_df, hide_index=True, use_container_width=True)
            with tab7:
                st.subheader("⚖️ Equilibrio Estático y Fuerzas Internas")
                st.dataframe(pd.DataFrame(fuerzas_internas), hide_index=True, use_container_width=True)
            with tab8:
                st.subheader("🎨 Galería de Diagramas")
                col1, col2 = st.columns(2)
                with col1:
                    st.image("modelo.jpg", use_container_width=True) if os.path.exists("modelo.jpg") else st.warning("Falta modelo.jpg")
                with col2:
                    st.image("axial.jpg", use_container_width=True) if os.path.exists("axial.jpg") else st.warning("Falta axial.jpg")

        except Exception as e:
            st.error(f"❌ Error en el cálculo estructural: {e}")

# ==========================================
# VISTA: EJERCICIO 01 (Nuevo pórtico real con columna inclinada)
# ==========================================
elif st.session_state.pagina == 'ej_1':
    if st.button("⬅️ Volver al Menú Principal"):
        ir_a('home')
        st.rerun()
        
    st.markdown("<h1 style='text-align: center; color: #f7fafc;'>🏛 EJERCICIO 01</h1>", unsafe_allow_html=True)
    st.markdown("""
    > **ENUNCIADO:** HALLAR LAS REACCIONES, FUERZAS AXIALES, ESFUERZOS DE CORTE, MOMENTOS FLECTORES Y DESPLAZAMIENTOS DE LA ESTRUCTURA MOSTRADA.
    """)

    # No se cargan imágenes de gráficos ni enunciado todavía para el Ejercicio 01, como pediste.
    st.info("ℹ️ Datos geométricos y de cargas configurados para el Ejercicio 01 (Pórtico con columna inclinada).")
    st.markdown("---")

    # --- DATOS REALES DEL EJERCICIO 01 ---
    # Nodos: 1(0,0), 2(0,3), 3(5,3), 4(7.5,0) - Ambos empotrados en 1 y 4
    st.subheader("📍 Coordenadas Nodales y Restricciones")
    nodos_default = pd.DataFrame({
        "Nodo": [1, 2, 3, 4],
        "X (m)": [0.0, 0.0, 5.0, 7.5],
        "Y (m)": [0.0, 3.0, 3.0, 0.0],
        "Restringido_X": [True, False, False, True],
        "Restringido_Y": [True, False, False, True],
        "Restringido_Giro": [True, False, False, True]
    })
    nodos_df = st.data_editor(nodos_default, num_rows="dynamic", key="nodos_ej1_real", use_container_width=True)

    # Barras: 1(1-2: columna 0.30x0.50), 2(2-3: viga 0.30x0.45), 3(3-4: col inclinada 0.30x0.50)
    # E = 15000*sqrt(210) = 2,173,706.5 Tn/m2
    st.subheader("🔗 Conectividad y Propiedades de Elementos")
    barras_default = pd.DataFrame({
        "Barra": [1, 2, 3],
        "Nodo_Ini": [1, 2, 3],
        "Nodo_Fin": [2, 3, 4],
        "Base (m)": [0.30, 0.30, 0.30],
        "Altura (m)": [0.50, 0.45, 0.50],
        "E (Tn/m2)": [2173706.5, 2173706.5, 2173706.5]
    })
    barras_df = st.data_editor(barras_default, num_rows="dynamic", key="barras_ej1_real", use_container_width=True)

    # Cargas: Barra 1 (columna izq trapezoidal w_prom=1.5), Barra 2 (viga w=2.0), Barra 3 (col incl=0)
    st.subheader("⚡ Cargas Distribuidas Equivalentes en los Elementos (w en Tn/m)")
    cargas_default = pd.DataFrame({
        "Barra": [1, 2, 3],
        "w (Tn/m)": [1.5, 2.0, 0.0]
    })
    cargas_df = st.data_editor(cargas_default, num_rows="dynamic", key="cargas_ej1_real", use_container_width=True)

    st.markdown("---")

    if st.button("🚀 INICIAR CÁLCULO MATRICIAL - EJERCICIO 01", use_container_width=True):
        try:
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
            
            elementos_info = []
            fuerzas_internas = []
            matrices_locales = {}
            matrices_globales = {}
            
            for _, barra in barras_clean.iterrows():
                b_id = int(barra["Barra"])
                n1_id = int(barra["Nodo_Ini"])
                n2_id = int(barra["Nodo_Fin"])
                
                n1 = nodos_clean[nodos_clean["Nodo"] == n1_id].iloc[0]
                n2 = nodos_clean[nodos_clean["Nodo"] == n2_id].iloc[0]
                
                dx = n2["X (m)"] - n1["X (m)"]
                dy = n2["Y (m)"] - n1["Y (m)"]
                L = np.sqrt(dx**2 + dy**2)
                
                cos_phi = dx / L
                sin_phi = dy / L
                
                b = barra["Base (m)"]
                h = barra["Altura (m)"]
                E = barra["E (Tn/m2)"]
                A = b * h
                I = (b * h**3) / 12.0
                
                ae_l = (A * E) / L
                ei = E * I
                
                k11 = ae_l
                k22 = 12.0 * ei / L**3
                k23 = 6.0 * ei / L**2
                k33 = 4.0 * ei / L
                k36 = 2.0 * ei / L
                
                K_L = np.zeros((6, 6))
                K_L[0,0] = k11; K_L[0,3] = -k11; K_L[3,0] = -k11; K_L[3,3] = k11
                K_L[1,1] = k22; K_L[1,2] = k23; K_L[1,4] = -k22; K_L[1,5] = k23
                K_L[2,1] = k23; K_L[2,2] = k33; K_L[2,4] = -k23; K_L[2,5] = k36
                K_L[4,1] = -k22; K_L[4,2] = -k23; K_L[4,4] = k22; K_L[4,5] = -k23
                K_L[5,1] = k23; K_L[5,2] = k36; K_L[5,4] = -k23; K_L[5,5] = k33
                
                matrices_locales[b_id] = K_L.copy()
                
                c = cos_phi
                s = sin_phi
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
                        
                w_val = cargas_df[cargas_df["Barra"] == b_id]["w (Tn/m)"].values[0]
                Fe_local = np.array([
                    0.0,
                    (w_val * L) / 2.0,
                    (w_val * L**2) / 12.0,
                    0.0,
                    (w_val * L) / 2.0,
                    -(w_val * L**2) / 12.0
                ])
                
                Fe_global = Tg.T @ Fe_local
                for i in range(6):
                    F_equivalente_global[gdl_elem[i]] += Fe_global[i]
                    
                elementos_info.append({
                    "Barra": b_id, "N1": n1_id, "N2": n2_id, "L": L, "w": w_val, "gdl": gdl_elem
                })

            K_LL = K_global[np.ix_(gdl_libres, gdl_libres)]
            F_LL = -F_equivalente_global[gdl_libres]
            
            U_libres = np.linalg.pinv(K_LL) @ F_LL
            U_global = np.zeros(n_gdl)
            U_global[gdl_libres] = U_libres
            
            R_global = K_global @ U_global + F_equivalente_global

            for el in elementos_info:
                b_id = el["Barra"]
                n1 = nodos_clean[nodos_clean["Nodo"] == el["N1"]].iloc[0]
                n2 = nodos_clean[nodos_clean["Nodo"] == el["N2"]].iloc[0]
                dx = n2["X (m)"] - n1["X (m)"]
                dy = n2["Y (m)"] - n1["Y (m)"]
                L = np.sqrt(dx**2 + dy**2)
                c, s = dx/L, dy/L
                
                b_row = barras_clean[barras_clean["Barra"] == b_id].iloc[0]
                A = b_row["Base (m)"] * b_row["Altura (m)"]
                I = (b_row["Base (m)"] * b_row["Altura (m)"]**3) / 12.0
                E = b_row["E (Tn/m2)"]
                ae_l, ei = (A * E) / L, E * I
                
                k11 = ae_l
                k22 = 12.0 * ei / L**3
                k23 = 6.0 * ei / L**2
                k33 = 4.0 * ei / L
                k36 = 2.0 * ei / L
                
                K_L = np.zeros((6, 6))
                K_L[0,0] = k11; K_L[0,3] = -k11; K_L[3,0] = -k11; K_L[3,3] = k11
                K_L[1,1] = k22; K_L[1,2] = k23; K_L[1,4] = -k22; K_L[1,5] = k23
                K_L[2,1] = k23; K_L[2,2] = k33; K_L[2,4] = -k23; K_L[2,5] = k36
                K_L[4,1] = -k22; K_L[4,2] = -k23; K_L[4,4] = k22; K_L[4,5] = -k23
                K_L[5,1] = k23; K_L[5,2] = k36; K_L[5,4] = -k23; K_L[5,5] = k33
                
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
                Fe_local = np.array([0.0, (el["w"] * L)/2.0, (el["w"] * L**2)/12.0, 0.0, (el["w"] * L)/2.0, -(el["w"] * L**2)/12.0])
                f_local = K_L @ u_local_elem + Fe_local
                
                fuerzas_internas.append({
                    "Barra": b_id,
                    "Axial Ini (Tn)": round(f_local[0], 3),
                    "Cortante Ini (Tn)": round(f_local[1], 3),
                    "Momento Ini (Tn.m)": round(f_local[2], 3),
                    "Axial Fin (Tn)": round(f_local[3], 3),
                    "Cortante Fin (Tn)": round(f_local[4], 3),
                    "Momento Fin (Tn.m)": round(f_local[5], 3)
                })

            st.balloons()
            st.success("¡Cálculo matricial procesado con éxito!")

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
                st.write("**Nodos y Coordenadas:**")
                st.dataframe(nodos_clean, hide_index=True, use_container_width=True)
                st.write("**Elementos y Secciones:**")
                st.dataframe(barras_clean, hide_index=True, use_container_width=True)
                
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
                    st.write(f"**Barra {b_id} (Sistema Local 6x6):**")
                    st.dataframe(pd.DataFrame(np.round(k_mat, 2)), use_container_width=True)

            with tab4:
                st.subheader("🌐 Matrices de Rigidez Global (Ke) por Elemento")
                for b_id, kg_mat in matrices_globales.items():
                    st.write(f"**Barra {b_id} (Sistema Global 6x6):**")
                    st.dataframe(pd.DataFrame(np.round(kg_mat, 2)), use_container_width=True)

            with tab5:
                st.subheader("📊 Matriz de Rigidez Global de la Estructura (Ensamblada)")
                st.dataframe(pd.DataFrame(np.round(K_global, 2)), use_container_width=True)

            with tab6:
                st.subheader("📉 Desplazamientos Nodales y Reacciones en los Apoyos")
                col_a, col_b = st.columns(2)
                with col_a:
                    st.write("**Desplazamientos:**")
                    desp_df = pd.DataFrame({
                        "Nodo": nodos_clean["Nodo"].astype(int),
                        "Dx (m)": [f"{U_global[3*i]:.6f}" for i in range(n_nodos)],
                        "Dy (m)": [f"{U_global[3*i+1]:.6f}" for i in range(n_nodos)],
                        "Giro (rad)": [f"{U_global[3*i+2]:.6f}" for i in range(n_nodos)]
                    })
                    st.dataframe(desp_df, hide_index=True, use_container_width=True)
                with col_b:
                    st.write("**Reacciones:**")
                    reac_df = pd.DataFrame({
                        "Nodo": nodos_clean["Nodo"].astype(int),
                        "Rx (Tn)": np.round(R_global[0::3], 3),
                        "Ry (Tn)": np.round(R_global[1::3], 3),
                        "Mz (Tn.m)": np.round(R_global[2::3], 3)
                    })
                    reac_df = reac_df[nodos_clean["Restringido_X"].values | nodos_clean["Restringido_Y"].values | nodos_clean["Restringido_Giro"].values]
                    st.dataframe(reac_df, hide_index=True, use_container_width=True)

            with tab7:
                st.subheader("⚖️ Equilibrio Estático y Fuerzas Internas (Axial, Cortante y Momento)")
                st.dataframe(pd.DataFrame(fuerzas_internas), hide_index=True, use_container_width=True)

            with tab8:
                st.subheader("🎨 Galería de Diagramas y Resultados Oficiales")
                st.info("💡 Aún no se han cargado imágenes para los gráficos de este Ejercicio 01. Cuando las tengas, puedes subirlas a GitHub.")

        except Exception as e:
            st.error(f"❌ Error en el cálculo estructural: {e}")

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
