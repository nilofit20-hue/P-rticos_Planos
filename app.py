import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="SYNCRET - Pórticos Planos", page_icon="🏛️", layout="wide")

st.markdown("""
<style>
    .block-container { padding-top: 1rem !important; }
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

st.markdown("<h1 style='text-align: center; color: #f7fafc;'>🏛 SYNCRET: Análisis Matricial de Pórticos Planos</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #93c5fd;'>Método de Rigideces • Análisis Estructural II • UNS</p>", unsafe_allow_html=True)
st.markdown("---")

# --- ENTRADA DE DATOS: NODOS ---
st.subheader("📍 Coordenadas Nodales y Restricciones")
nodos_default = pd.DataFrame({
    "Nodo": [1, 2, 3],
    "X (m)": [0.0, 0.0, 4.0],
    "Y (m)": [0.0, 4.0, 4.0],
    "Restringido_X": [True, False, True],
    "Restringido_Y": [True, False, True],
    "Restringido_Giro": [False, False, True]
})
nodos_df = st.data_editor(nodos_default, num_rows="dynamic", key="nodos_portico_v18", use_container_width=True)

# --- ENTRADA DE DATOS: BARRAS ---
st.subheader("🔗 Conectividad y Propiedades de Elementos")
barras_default = pd.DataFrame({
    "Barra": [1, 2],
    "Nodo_Ini": [1, 2],
    "Nodo_Fin": [2, 3],
    "Base (m)": [0.30, 0.30],
    "Altura (m)": [0.40, 0.35],
    "E (Tn/m2)": [1900000.0, 1900000.0]
})
barras_df = st.data_editor(barras_default, num_rows="dynamic", key="barras_portico_v18", use_container_width=True)

# --- CARGAS DISTRIBUIDAS ---
st.subheader("⚡ Cargas Distribuidas en los Elementos (w en Tn/m)")
cargas_default = pd.DataFrame({
    "Barra": [1, 2],
    "w (Tn/m)": [1.0, 3.0]
})
cargas_df = st.data_editor(cargas_default, num_rows="dynamic", key="cargas_portico_v18", use_container_width=True)

st.markdown("---")

if st.button("🚀 INICIAR CÁLCULO MATRICIAL DEL PÓRTICO", use_container_width=True):
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
                "Barra": b_id, "N1": n1_id, "N2": n2_id, "L": L, "w": w_val
            })

        # --- RESOLUCIÓN MATRICIAL ---
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
        st.success("¡Cálculo matricial y resultados procesados con éxito!")

        tab1, tab2, tab3, tab4 = st.tabs([
            "📉 Desplazamientos", "⚖️ Reacciones", "🔗 Fuerzas Internas", "🎨 GRÁFICOS"
        ])
        
        with tab1:
            st.write("**Desplazamientos Nodales**")
            desp_df = pd.DataFrame({
                "Nodo": nodos_clean["Nodo"].astype(int),
                "Dx (m)": [f"{U_global[3*i]:.6f}" for i in range(n_nodos)],
                "Dy (m)": [f"{U_global[3*i+1]:.6f}" for i in range(n_nodos)],
                "Giro (rad)": [f"{U_global[3*i+2]:.6f}" for i in range(n_nodos)]
            })
            st.dataframe(desp_df, hide_index=True, use_container_width=True)
            
        with tab2:
            st.write("**Reacciones en los Apoyos**")
            reac_df = pd.DataFrame({
                "Nodo": nodos_clean["Nodo"].astype(int),
                "Rx (Tn)": np.round(R_global[0::3], 3),
                "Ry (Tn)": np.round(R_global[1::3], 3),
                "Mz (Tn.m)": np.round(R_global[2::3], 3)
            })
            reac_df = reac_df[nodos_clean["Restringido_X"].values | nodos_clean["Restringido_Y"].values | nodos_clean["Restringido_Giro"].values]
            st.dataframe(reac_df, hide_index=True, use_container_width=True)

        with tab3:
            st.write("**Fuerzas en los Extremos de los Elementos**")
            st.dataframe(pd.DataFrame(fuerzas_internas), hide_index=True, use_container_width=True)

        with tab4:
            st.subheader("🎨 Galería de Diagramas y Resultados Gráficos")
            st.markdown("Sube las capturas de tus gráficos del problema (Modelo, Axial, Cortante, Momento, Deformación y Cuerpo Libre) para presentarlos ordenadamente:")
            
            uploaded_files = st.file_uploader(
                "Sube tus imágenes de gráficos aquí (puedes seleccionar varias a la vez)", 
                type=["png", "jpg", "jpeg"], 
                accept_multiple_files=True
            )
            
            if uploaded_files:
                st.markdown("---")
                # Mostrarlas en columnas de 2 para que se vea estético y ordenado
                cols = st.columns(2)
                for index, uploaded_file in enumerate(uploaded_files):
                    with cols[index % 2]:
                        st.image(uploaded_file, caption=uploaded_file.name, use_container_width=True)
            else:
                st.info("💡 Consejo: Selecciona o arrastra todas tus capturas juntas en el botón de arriba para organizarlas automáticamente en la galería.")

    except Exception as e:
        st.error(f"❌ Error en el cálculo estructural: {e}")
