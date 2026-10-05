with tab4:
            st.write("**🎨 Diagramas Técnicos sobre la Geometría Real del Pórtico (Orientación Oficial UNS)**")
            
            fig, axes = plt.subplots(1, 3, figsize=(16, 5))
            fig.patch.set_facecolor('#0f172a')
            titles = ["Momento Flector (Tn.m)", "Esfuerzo Cortante (Tn)", "Fuerza Axial (Tn)"]
            
            for idx, ax in enumerate(axes):
                ax.set_facecolor('#1e293b')
                # Estructura base del pórtico (Columna izq y Viga sup)
                ax.plot([0, 0], [0, 4], color='#94a3b8', lw=4, zorder=3)
                ax.plot([0, 4], [4, 4], color='#94a3b8', lw=4, zorder=3)
                ax.set_title(titles[idx], color='white', fontweight='bold', fontsize=12)
                ax.set_xlim(-2.5, 5.5)
                ax.set_ylim(-1.0, 5.5)
                ax.axis('off')

            # --- 1. MOMENTO FLECTOR (Corregido: 3.0 arriba en el nudo, 0 abajo) ---
            # Columna: Ancho arriba (3.0), cero abajo
            axes[0].fill_betweenx([0, 4], [0, 0], [0, -1.2], color='#f43f5e', alpha=0.35)
            axes[0].plot([0, -1.2], [4, 4], color='#f43f5e', lw=2) # Base superior
            axes[0].plot([0, -1.2], [0, 4], color='#f43f5e', lw=2)
            axes[0].text(-1.5, 3.5, "3.0 Tn.m", color='#fca5a5', fontsize=9, fontweight='bold')
            
            # Viga: Negativo arriba en extremos (3.0 y 4.537), positivo abajo al centro (2.26)
            axes[0].fill_between([0, 4], [4, 4], [5.2, 5.8], color='#f43f5e', alpha=0.35) # Arriba extremos
            axes[0].plot([0, 4], [5.2, 5.8], color='#f43f5e', lw=2)
            axes[0].fill_between([0, 2, 4], [4, 4, 4], [2.8, 3.2, 2.8], color='#f43f5e', alpha=0.35) # Abajo centro
            axes[0].plot([0, 2, 4], [2.8, 3.2, 2.8], color='#f43f5e', lw=2)
            axes[0].text(3.6, 6.0, "4.537", color='#fca5a5', fontsize=9, fontweight='bold')
            axes[0].text(1.8, 3.4, "2.26 (+)", color='#fca5a5', fontsize=9, fontweight='bold')

            # --- 2. ESFUERZO CORTANTE (Corregido: 1.25 abajo, 5.62 arriba en columna) ---
            axes[1].fill_betweenx([0, 4], [0, 0], [0.5, 1.8], color='#38bdf8', alpha=0.35)
            axes[1].plot([0.5, 1.8], [0, 4], color='#38bdf8', lw=2)
            axes[1].text(0.7, 0.5, "1.25", color='#7dd3fc', fontsize=9, fontweight='bold')
            axes[1].text(1.3, 3.5, "5.62", color='#7dd3fc', fontsize=9, fontweight='bold')

            # Viga: Cortante constante/lineal de 5.62 a 6.38
            axes[1].fill_between([0, 4], [4, 4], [4.8, 5.4], color='#38bdf8', alpha=0.35)
            axes[1].plot([0, 4], [4.8, 5.4], color='#38bdf8', lw=2)
            axes[1].text(3.5, 5.6, "6.38 Tn", color='#7dd3fc', fontsize=9, fontweight='bold')

            # --- 3. FUERZA AXIAL (Corregido: Rectangulares exactos) ---
            # Columna: 5.62 Tn constante
            axes[2].fill_betweenx([0, 4], [0, 0], [1.2, 1.2], color='#10b981', alpha=0.35)
            axes[2].plot([1.2, 1.2], [0, 4], color='#10b981', lw=2)
            axes[2].text(1.4, 2.0, "5.62 Tn", color='#6ee7b7', fontsize=9, fontweight='bold')

            # Viga: 2.75 Tn constante
            axes[2].fill_between([0, 4], [4, 4], [4.8, 4.8], color='#10b981', alpha=0.35)
            axes[2].plot([0, 4], [4.8, 4.8], color='#10b981', lw=2)
            axes[2].text(1.8, 5.1, "2.75 Tn", color='#6ee7b7', fontsize=9, fontweight='bold')

            st.pyplot(fig)
            st.info("💡 Ahora los diagramas reflejan de manera precisa los lados, signos y formas correctas de los apuntes de clase.")
