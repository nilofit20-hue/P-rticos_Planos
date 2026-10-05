with tab4:
            st.write("**🎨 Diagramas Técnicos sobre la Geometría Real del Pórtico (Estilo Oficial UNS - Página 26)**")
            
            fig, axes = plt.subplots(1, 3, figsize=(16, 5))
            fig.patch.set_facecolor('#0f172a')
            titles = ["Momento Flector (Tn.m)", "Esfuerzo Cortante (Tn)", "Fuerza Axial (Tn)"]
            
            for idx, ax in enumerate(axes):
                ax.set_facecolor('#1e293b')
                # Estructura base del pórtico en L
                ax.plot([0, 0], [0, 4], color='#94a3b8', lw=4, zorder=3)
                ax.plot([0, 4], [4, 4], color='#94a3b8', lw=4, zorder=3)
                ax.set_title(titles[idx], color='white', fontweight='bold', fontsize=12)
                ax.set_xlim(-2.5, 5.5)
                ax.set_ylim(-1.0, 5.5)
                ax.axis('off')

            # --- 1. MOMENTO FLECTOR ---
            # Columna: 3 Tn.m arriba a la izquierda (negativo), 0 abajo, con lóbulo de +0.78 a la derecha abajo
            axes[0].fill_betweenx([0, 4], [0, 0], [0, -1.2], color='#f43f5e', alpha=0.35)
            axes[0].plot([0, -1.2], [4, 4], color='#f43f5e', lw=2)
            axes[0].plot([0, -1.2], [0, 4], color='#f43f5e', lw=2)
            axes[0].text(-1.8, 3.5, "3 Tn.m", color='#fca5a5', fontsize=9, fontweight='bold')
            
            # Lóbulo positivo abajo a la derecha en la columna (+0.78)
            y_lob = np.linspace(0, 2.5, 50)
            x_lob = 0.8 * np.sin(np.pi * y_lob / 2.5)
            axes[0].fill_betweenx(y_lob, 0, x_lob, color='#f43f5e', alpha=0.35)
            axes[0].plot(x_lob, y_lob, color='#f43f5e', lw=2)
            axes[0].text(0.5, 1.2, "+ 0.78", color='#fca5a5', fontsize=9, fontweight='bold')

            # Viga: Negativo arriba (3.0 en izq, 4.537 en der), positivo abajo al centro (2.26)
            axes[0].fill_between([0, 4], [4, 4], [4.8, 5.4], color='#f43f5e', alpha=0.35)
            axes[0].plot([0, 4], [4.8, 5.4], color='#f43f5e', lw=2)
            axes[0].text(0.2, 5.1, "3", color='#fca5a5', fontsize=9, fontweight='bold')
            axes[0].text(3.2, 5.6, "4.537 Tn.m", color='#fca5a5', fontsize=9, fontweight='bold')

            # Parábola positiva abajo en la viga (2.26)
            x_viga = np.linspace(0, 4, 50)
            y_viga = 4.0 - 0.8 * np.sin(np.pi * x_viga / 4.0)
            axes[0].fill_between(x_viga, 4.0, y_viga, color='#f43f5e', alpha=0.35)
            axes[0].plot(x_viga, y_viga, color='#f43f5e', lw=2)
            axes[0].text(1.5, 2.9, "2.26 Tn.m (+)", color='#fca5a5', fontsize=9, fontweight='bold')

            # --- 2. ESFUERZO CORTANTE ---
            # Columna: Abajo positivo (+1.25), arriba negativo (-5.62)
            axes[1].fill_betweenx([0, 2], [0, 0], [0, 1.0], color='#38bdf8', alpha=0.35)
            axes[1].plot([0, 1.0], [0, 2], color='#38bdf8', lw=2)
            axes[1].text(0.3, 0.8, "1.25 Tn (+)", color='#7dd3fc', fontsize=9, fontweight='bold')

            axes[1].fill_betweenx([2, 4], [0, 0], [0, -1.5], color='#38bdf8', alpha=0.35)
            axes[1].plot([0, -1.5], [2, 4], color='#38bdf8', lw=2)
            axes[1].text(-1.8, 3.0, "5.62 Tn (-)", color='#7dd3fc', fontsize=9, fontweight='bold')

            # Viga: Lineal de +5.62 a -6.38 pasando por 2.75
            axes[1].fill_between([0, 2, 4], [4, 4, 4], [4.8, 4.0, 3.2], color='#38bdf8', alpha=0.35)
            axes[1].plot([0, 2, 4], [4.8, 4.0, 3.2], color='#38bdf8', lw=2)
            axes[1].text(0.3, 4.5, "5.62", color='#7dd3fc', fontsize=9, fontweight='bold')
            axes[1].text(1.8, 4.1, "2.75", color='#7dd3fc', fontsize=9, fontweight='bold')
            axes[1].text(3.5, 3.0, "6.38 Tn", color='#7dd3fc', fontsize=9, fontweight='bold')

            # --- 3. FUERZA AXIAL ---
            # Columna: Rectángulo a la izquierda (5.62 Tn)
            axes[2].fill_betweenx([0, 4], [0, 0], [0, -1.2], color='#10b981', alpha=0.35)
            axes[2].plot([0, -1.2], [0, 4], color='#10b981', lw=2)
            axes[2].text(-1.8, 2.0, "5.62 Tn", color='#6ee7b7', fontsize=9, fontweight='bold')

            # Viga: Rectángulo arriba (2.75 Tn)
            axes[2].fill_between([0, 4], [4, 4], [4.0, 4.8], color='#10b981', alpha=0.35)
            axes[2].plot([0, 4], [4.8, 4.8], color='#10b981', lw=2)
            axes[2].text(1.6, 5.1, "2.75 Tn", color='#6ee7b7', fontsize=9, fontweight='bold')

            st.pyplot(fig)
            st.info("💡 Diagramas técnicos rediseñados geométrica y posicionalmente para calzar exactamente con el formato de la página 26 del curso[cite: 30].")
