with tab4:
            st.write("**🎨 Diagramas Técnicos Dinámicos (Corregido: Diagrama Axial Rectangular)**")
            
            fig, axes = plt.subplots(1, 3, figsize=(16, 5))
            fig.patch.set_facecolor('#0f172a')
            titles = ["Momento Flector (Tn.m)", "Esfuerzo Cortante (Tn)", "Fuerza Axial (Tn)"]
            
            for idx, ax in enumerate(axes):
                ax.set_facecolor('#1e293b')
                for el in elementos_info:
                    ax.plot([el["x1"], el["x2"]], [el["y1"], el["y2"]], color='#94a3b8', lw=4, zorder=3)
                ax.set_title(titles[idx], color='white', fontweight='bold', fontsize=12)
                ax.set_xlim(-2.0, 5.5)
                ax.set_ylim(-1.0, 5.5)
                ax.axis('off')

            f1 = fuerzas_internas[0]["f_local"]
            f2 = fuerzas_internas[1]["f_local"]

            # 1. Momento Flector
            axes[0].fill_betweenx([0, 4], [0, 0], [0, -f1[5]/3.0], color='#f43f5e', alpha=0.35)
            axes[0].plot([0, -f1[5]/3.0], [0, 4], color='#f43f5e', lw=2)
            axes[0].text(-1.5, 3.5, f"{abs(f1[5]):.2f}", color='#fca5a5', fontsize=9, fontweight='bold')

            axes[0].fill_between([0, 4], [4, 4], [4.5 + abs(f2[2])/10, 4.5 + abs(f2[5])/10], color='#f43f5e', alpha=0.35)
            axes[0].plot([0, 4], [4.5 + abs(f2[2])/10, 4.5 + abs(f2[5])/10], color='#f43f5e', lw=2)
            axes[0].text(3.5, 5.2, f"{abs(f2[5]):.3f} Tn.m", color='#fca5a5', fontsize=9, fontweight='bold')

            # 2. Cortante
            axes[1].fill_betweenx([0, 4], [0, 0], [0, f1[1]/3.0], color='#38bdf8', alpha=0.35)
            axes[1].plot([0, f1[1]/3.0], [0, 4], color='#38bdf8', lw=2)
            axes[1].text(0.5, 0.5, f"{f1[1]:.2f} Tn", color='#7dd3fc', fontsize=9, fontweight='bold')
            axes[1].text(0.5, 3.5, f"{f1[4]:.2f} Tn", color='#7dd3fc', fontsize=9, fontweight='bold')

            axes[1].fill_between([0, 4], [4, 4], [4 + f2[1]/4.0, 4 - abs(f2[4])/4.0], color='#38bdf8', alpha=0.35)
            axes[1].plot([0, 4], [4 + f2[1]/4.0, 4 - abs(f2[4])/4.0], color='#38bdf8', lw=2)
            axes[1].text(3.5, 3.2, f"{abs(f2[4]):.2f} Tn", color='#7dd3fc', fontsize=9, fontweight='bold')

            # 3. Fuerza Axial (CORREGIDO A RECTÁNGULO CONSTANTE)
            # Columna: Rectángulo uniforme de ancho -1.2 desde y=0 hasta y=4
            axes[2].fill_betweenx([0, 4], [0, 0], [-1.2, -1.2], color='#10b981', alpha=0.35)
            axes[2].plot([0, -1.2], [0, 4], color='#10b981', lw=2)
            axes[2].plot([-1.2, -1.2], [0, 4], color='#10b981', lw=2)
            axes[2].text(-1.8, 2.0, f"{abs(f1[0]):.2f} Tn (-)", color='#6ee7b7', fontsize=9, fontweight='bold')

            # Viga: Rectángulo uniforme de altura 4.8 desde x=0 hasta x=4
            axes[2].fill_between([0, 4], [4, 4], [4.8, 4.8], color='#10b981', alpha=0.35)
            axes[2].plot([0, 4], [4.8, 4.8], color='#10b981', lw=2)
            axes[2].text(1.8, 5.1, f"{abs(f2[0]):.2f} Tn (-)", color='#6ee7b7', fontsize=9, fontweight='bold')

            st.pyplot(fig)
            st.info("💡 Diagrama axial corregido a formato rectangular constante, manteniendo la precisión de los cálculos matriciales.")

    except Exception as e:
        st.error(f"❌ Error en el cálculo estructural: {e}")
