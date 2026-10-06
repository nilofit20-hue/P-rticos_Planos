with tab5:
            st.subheader("📊 Matriz Global del Sistema Particionada (K_LL, K_LR, K_RL, K_RR)")
            st.markdown("""
            <div style="display: flex; gap: 15px; margin-bottom: 15px; font-size: 14px; font-weight: bold;">
                <div style="background-color: #1d4ed8; padding: 8px 15px; border-radius: 8px; color: white;">🟦 K_LL (Libres - Libres)</div>
                <div style="background-color: #c2410c; padding: 8px 15px; border-radius: 8px; color: white;">🟧 K_LR / K_RL (Acoplamiento)</div>
                <div style="background-color: #581c87; padding: 8px 15px; border-radius: 8px; color: white;">🟪 K_RR (Restringidos - Restringidos)</div>
            </div>
            """, unsafe_allow_html=True)

            # Reordenar K_global agrupando primero los GDL Libres y luego los Restringidos
            gdl_ordenados = gdl_libres + gdl_restringidos
            K_particionada = K_global[np.ix_(gdl_ordenados, gdl_ordenados)]

            # Crear etiquetas ordenadas
            nombres_gdl_ordenados = [f"GDL {i+1} (Libre)" if i in gdl_libres else f"GDL {i+1} (Rest.)" for i in gdl_ordenados]
            df_K_part = pd.DataFrame(np.round(K_particionada, 2), index=nombres_gdl_ordenados, columns=nombres_gdl_ordenados)

            n_libres = len(gdl_libres)

            # Función para pintar exactamente en 4 cuadrantes limpios
            def color_cuadrantes(row):
                styles = []
                row_idx = row.name
                # Identificar si la fila actual pertenece a los libres o restringidos
                es_libre_fila = "Libre" in row_idx
                
                for col_name in row.index:
                    es_libre_col = "Libre" in col_name
                    
                    if es_libre_fila and es_libre_col:
                        styles.append('background-color: #1e3a8a; color: #93c5fd;') # Bloque K_LL (Azul)
                    elif not es_libre_fila and not es_libre_col:
                        styles.append('background-color: #3b0764; color: #d8b4fe;') # Bloque K_RR (Morado)
                    else:
                        styles.append('background-color: #7c2d12; color: #fed7aa;') # Bloques K_LR / K_RL (Naranja/Marrón)
                return styles

            st.dataframe(df_K_part.style.apply(color_cuadrantes, axis=1), use_container_width=True)
