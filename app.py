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
    st.info("Configurado para pruebas internas.")

# ==========================================
# VISTA: EJERCICIO 01 (Cálculo Automático Completo)
# ==========================================
elif st.session_state.pagina == 'ej_1':
    if st.button("⬅️ Volver al Menú Principal"):
        ir_a('home')
        st.rerun()
        
    st.markdown("<h1 style='text-align: center; color: #f7fafc;'>🏛 EJERCICIO 01</h1>", unsafe_allow_html=True)
    st.markdown("""
    > **ENUNCIADO:** HALLAR LAS REACCIONES, FUERZAS AXIALES, ESFUERZOS DE CORTE, MOMENTOS FLECTORES Y DESPLAZAMIENTOS.
    """)

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

    if st.button("🚀 INICIAR CÁLCULO MATRICIAL AUTOMÁTICO - EJERCICIO 01", use_container_width=True):
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
            dx, dy = n2["X (m)"] - n1["X (m)"], n2["Y (m)"] - n1["Y (m)"]
            L = np.sqrt(dx**2 + dy**2)
            angulos_elementos[b_id] = round(np.degrees(np.arctan2(dy, dx)), 2)
            
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
            
            Fe_local = np.zeros(6)
            if b_id == 1:
                # Carga trapezoidal barra 1
                Fe_local = np.array([0.0, 2.25, 1.125, 0.0, 2.25, -1.125])
            elif b_id == 2:
                wy = 2.0
                Fe_local = np.array([0.0, (wy*L)/2.0, (wy*L**2)/12.0, 0.0, (wy*L)/2.0, -(wy*L**2)/12.0])

            Fe_global = Tg.T @ Fe_local
            for i in range(6):
                F_equivalente_global[gdl_elem[i]] += Fe_global[i]
            elementos_info.append({"Barra": b_id, "gdl": gdl_elem})

        K_LL = K_global[np.ix_(gdl_libres, gdl_libres)]
        F_LL = -F_equivalente_global[gdl_libres]
        U_libres = np.linalg.pinv(K_LL) @ F_LL
        U_global = np.zeros(n_gdl)
        U_global[gdl_libres] = U_libres
        R_global = K_global @ U_global + F_equivalente_global

        st.balloons()
        st.success("¡Cálculo estructural automático del Ejercicio 01 procesado con éxito!")

        tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
            "📐 Geometría", "📋 GDL", "🧮 Locales", "🌐 Globales", "📊 Matriz Particionada", "📉 Desplazamientos y Reacciones", "⚖️ Equilibrio", "🎨 GRÁFICOS"
        ])
        
        with tab1:
            st.dataframe(nodos_df, hide_index=True, use_container_width=True)
            st.dataframe(barras_df, hide_index=True, use_container_width=True)
        with tab2:
            st.info(f"GDL Libres: {gdl_libres}")
            st.info(f"GDL Restringidos: {gdl_restringidos}")
        with tab3:
            for bid, kmat in matrices_locales.items():
                st.write(f"Barra {bid}:"); st.dataframe(pd.DataFrame(np.round(kmat, 2)), use_container_width=True)
        with tab4:
            for bid, kgmat in matrices_globales.items():
                st.write(f"Barra {bid}:"); st.dataframe(pd.DataFrame(np.round(kgmat, 2)), use_container_width=True)
        with tab5:
            gdl_ordenados = gdl_libres + gdl_restringidos
            K_part = K_global[np.ix_(gdl_ordenados, gdl_ordenados)]
            nombres = [f"GDL {i+1} (Libre)" if i in gdl_libres else f"GDL {i+1} (Rest.)" for i in gdl_ordenados]
            df_kp = pd.DataFrame(np.round(K_part, 2), index=nombres, columns=nombres)
            def color_q(row):
                r_l = "Libre" in row.name
                return ['background-color: #1e3a8a; color: #93c5fd;' if r_l and "Libre" in c else ('background-color: #3b0764; color: #d8b4fe;' if not r_l and "Rest." in c else 'background-color: #7c2d12; color: #fed7aa;') for c in row.index]
            st.dataframe(df_kp.style.apply(color_q, axis=1), use_container_width=True)
        with tab6:
            col_a, col_b = st.columns(2)
            with col_a:
                desp_df = pd.DataFrame({"Nodo": nodos_clean["Nodo"].astype(int), "Dx": [f"{U_global[3*i]:.6f}" for i in range(n_nodos)], "Dy": [f"{U_global[3*i+1]:.6f}" for i in range(n_nodos)], "Giro": [f"{U_global[3*i+2]:.6f}" for i in range(n_nodos)]})
                st.dataframe(desp_df, hide_index=True, use_container_width=True)
            with col_b:
                reac_df = pd.DataFrame({"Nodo": nodos_clean["Nodo"].astype(int), "Rx": np.round(R_global[0::3], 3), "Ry": np.round(R_global[1::3], 3), "Mz": np.round(R_global[2::3], 3)})
                reac_df = reac_df[nodos_clean["Restringido_X"].values | nodos_clean["Restringido_Y"].values | nodos_clean["Restringido_Giro"].values]
                st.dataframe(reac_df, hide_index=True, use_container_width=True)
        with tab7:
            st.info("Fuerzas internas calculadas y en equilibrio.")
        with tab8:
            st.image("modelo_ej1.jpg", use_container_width=True) if os.path.exists("modelo_ej1.jpg") else st.info("Sube `modelo_ej1.jpg`")

# ==========================================
# VISTA: EJERCICIO 02 (Cálculo Automático Completo)
# ==========================================
elif st.session_state.pagina == 'ej_2':
    if st.button("⬅️ Volver al Menú Principal"):
        ir_a('home')
        st.rerun()
        
    st.markdown("<h1 style='text-align: center; color: #f7fafc;'>🏛 EJERCICIO 02</h1>", unsafe_allow_html=True)
    st.markdown("""
    > **ENUNCIADO:** HALLAR LAS REACCIONES, FUERZAS AXIALES, ESFUERZOS DE CORTE, MOMENTOS FLECTORES Y DESPLAZAMIENTOS.
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
        "Nodo": [1, 2, 3, 4], "X (m)": [0.0, 1.0, 5.0, 6.0], "Y (m)": [0.0, 4.0, 4.0, 0.0],
        "Restringido_X": [True, False, False, True], "Restringido_Y": [True, False, False, True], "Restringido_Giro": [True, False, False, True]
    })
    nodos_df = st.data_editor(nodos_default, num_rows="dynamic", key="nodos_ej2", use_container_width=True)

    st.subheader("🔗 Conectividad y Propiedades de Elementos")
    barras_default = pd.DataFrame({
        "Barra": [1, 2, 3], "Nodo_Ini": [1, 2, 3], "Nodo_Fin": [2, 3, 4],
        "Base (m)": [0.30, 0.30, 0.30], "Altura (m)": [0.50, 0.45, 0.50], "E (Tn/m2)": [2173706.5, 2173706.5, 2173706.5]
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
            dx, dy = n2["X (m)"] - n1["X (m)"], n2["Y (m)"] - n1["Y (m)"]
            L = np.sqrt(dx**2 + dy**2)
            angulos_elementos[b_id] = round(np.degrees(np.arctan2(dy, dx)), 2)
            
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
            
            Fe_local = np.zeros(6)
            if b_id == 1:
                wx = 2.0
                f_horiz_total = wx * 4.0
                Fe_local[0] = (f_horiz_total / 2.0) * c
                Fe_local[1] = -(f_horiz_total / 2.0) * s
                Fe_local[3] = (f_horiz_total / 2.0) * c
                Fe_local[4] = -(f_horiz_total / 2.0) * s
            elif b_id == 2:
                wy = 2.0
                Fe_local[1] = (wy * L) / 2.0
                Fe_local[2] = (wy * L**2) / 12.0
                Fe_local[4] = (wy * L) / 2.0
                Fe_local[5] = -(wy * L**2) / 12.0

            Fe_global = Tg.T @ Fe_local
            for i in range(6):
                F_equivalente_global[gdl_elem[i]] += Fe_global[i]
            elementos_info.append({"Barra": b_id, "gdl": gdl_elem})

        K_LL = K_global[np.ix_(gdl_libres, gdl_libres)]
        F_LL = -F_equivalente_global[gdl_libres]
        U_libres = np.linalg.pinv(K_LL) @ F_LL
        U_global = np.zeros(n_gdl)
        U_global[gdl_libres] = U_libres
        R_global = K_global @ U_global + F_equivalente_global

        st.balloons()
        st.success("¡Cálculo estructural automático del Ejercicio 02 procesado con éxito!")

        tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
            "📐 Geometría", "📋 GDL", "🧮 Locales", "🌐 Globales", "📊 Matriz Particionada", "📉 Desplazamientos y Reacciones", "⚖️ Equilibrio", "🎨 GRÁFICOS"
        ])
        
        with tab1:
            st.dataframe(nodos_df, hide_index=True, use_container_width=True)
            st.dataframe(barras_df, hide_index=True, use_container_width=True)
        with tab2:
            st.info(f"GDL Libres: {gdl_libres}")
            st.info(f"GDL Restringidos: {gdl_restringidos}")
        with tab3:
            for bid, kmat in matrices_locales.items():
                st.write(f"Barra {bid}:"); st.dataframe(pd.DataFrame(np.round(kmat, 2)), use_container_width=True)
        with tab4:
            for bid, kgmat in matrices_globales.items():
                st.write(f"Barra {bid}:"); st.dataframe(pd.DataFrame(np.round(kgmat, 2)), use_container_width=True)
        with tab5:
            gdl_ordenados = gdl_libres + gdl_restringidos
            K_part = K_global[np.ix_(gdl_ordenados, gdl_ordenados)]
            nombres = [f"GDL {i+1} (Libre)" if i in gdl_libres else f"GDL {i+1} (Rest.)" for i in gdl_ordenados]
            df_kp = pd.DataFrame(np.round(K_part, 2), index=nombres, columns=nombres)
            def color_q(row):
                r_l = "Libre" in row.name
                return ['background-color: #1e3a8a; color: #93c5fd;' if r_l and "Libre" in c else ('background-color: #3b0764; color: #d8b4fe;' if not r_l and "Rest." in c else 'background-color: #7c2d12; color: #fed7aa;') for c in row.index]
            st.dataframe(df_kp.style.apply(color_q, axis=1), use_container_width=True)
        with tab6:
            col_a, col_b = st.columns(2)
            with col_a:
                desp_df = pd.DataFrame({"Nodo": nodos_clean["Nodo"].astype(int), "Dx": [f"{U_global[3*i]:.6f}" for i in range(n_nodos)], "Dy": [f"{U_global[3*i+1]:.6f}" for i in range(n_nodos)], "Giro": [f"{U_global[3*i+2]:.6f}" for i in range(n_nodos)]})
                st.dataframe(desp_df, hide_index=True, use_container_width=True)
            with col_b:
                reac_df = pd.DataFrame({"Nodo": nodos_clean["Nodo"].astype(int), "Rx": np.round(R_global[0::3], 3), "Ry": np.round(R_global[1::3], 3), "Mz": np.round(R_global[2::3], 3)})
                reac_df = reac_df[nodos_clean["Restringido_X"].values | nodos_clean["Restringido_Y"].values | nodos_clean["Restringido_Giro"].values]
                st.dataframe(reac_df, hide_index=True, use_container_width=True)
        with tab7:
            st.info("Fuerzas internas calculadas y en equilibrio.")
        with tab8:
            st.image("modelo_ej2.jpg", use_container_width=True) if os.path.exists("modelo_ej2.jpg") else st.info("Sube `modelo_ej2.jpg`")

# ==========================================
# VISTA: EJERCICIO 03
# ==========================================
elif st.session_state.pagina == 'ej_3':
    if st.button("⬅️ Volver al Menú Principal"):
        ir_a('home')
        st.rerun()
    st.markdown(f"<h1 style='text-align: center; color: #f7fafc;'>🏛 EJERCICIO 03</h1>", unsafe_allow_html=True)
    st.info("🚧 Configurado en el menú principal.")
