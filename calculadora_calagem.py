import streamlit as st
import os
st.error("🚨 ESTOU NA VERSÃO NOVA COM FUNDO CINZA! 🚨")
# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Ferramentas Agronômicas",
    page_icon="🚜",
    layout="centered"
)

# --- ESTILO CSS (A MÁGICA DO VISUAL) ---
st.markdown("""
<style>
    /* Fundo da aplicação */
    .stApp {
        background-color: #f0f2f6;
    }
    
    /* Estilo dos Cards (Containers) */
    .css-1r6slb0, .css-12oz5g7 {
        background-color: white;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
    }

    /* Botões */
    .stButton>button {
        background-color: #2e7d32; /* Verde Agronômico */
        color: white;
        border-radius: 8px;
        border: none;
        height: 3em;
        width: 100%;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #1b5e20; /* Verde mais escuro ao passar o mouse */
        color: white;
    }

    /* Títulos */
    h1, h2, h3 {
        color: #1b5e20;
    }
</style>
""", unsafe_allow_html=True)

# --- BARRA LATERAL (LOGO E MENU) ---
with st.sidebar:
    # Tenta mostrar o logo
    if os.path.exists("logo.png"):
        st.image("logo.png", width=150)
    elif os.path.exists("logo.jpg"):
        st.image("logo.jpg", width=150)
    else:
        st.markdown("# 🚜")

    st.title("Menu")
    opcao = st.radio(
        "Escolha a Ferramenta:",
        ("🪨 Calagem & Adubação", "🚜 Calibração de Pulverizador")
    )
    
    st.markdown("---")
    st.caption("Desenvolvido por:")
    st.markdown("**Eng. Agr. Rodolfo Degaspari Delagracia**")
    st.caption("© 2025")

# ==================================================
# FERRAMENTA 1: CALAGEM & ADUBAÇÃO
# ==================================================
if opcao == "🪨 Calagem & Adubação":
    # Container Principal (Card)
    with st.container():
        st.title("🪨 Calculadora de Calagem")
        st.markdown("Método de **Saturação por Bases**.")
        st.markdown("---")

        st.header("1. Dados da Análise de Solo")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Bases e Acidez")
            k = st.number_input("Potássio (K) [cmol/dm³]", min_value=0.0, format="%.2f")
            ca = st.number_input("Cálcio (Ca) [cmol/dm³]", min_value=0.0, format="%.2f")
            mg = st.number_input("Magnésio (Mg) [cmol/dm³]", min_value=0.0, format="%.2f")
            hal = st.number_input("H+Al (Acidez Potencial) [cmol/dm³]", min_value=0.0, format="%.2f")

        with col2:
            st.subheader("Outros Parâmetros")
            p = st.number_input("Fósforo (P) [mg/dm³]", min_value=0.0, format="%.2f")
            v_alvo = st.number_input("Saturação Desejada (V%)", value=70.0, step=1.0)
            prnt = st.number_input("PRNT do Calcário (%)", value=80.0, step=1.0)

        st.write("") # Espaço
        if st.button("Calcular Necessidades"):
            sb = k + ca + mg
            ctc = sb + hal
            
            v_atual = (sb / ctc) * 100 if ctc > 0 else 0
            nc = ((v_alvo - v_atual) * ctc) / prnt
            if nc < 0: nc = 0

            st.markdown("---")
            st.subheader("📊 Resultados")
            
            # Resultados em Cards Menores
            c1, c2, c3 = st.columns(3)
            c1.metric("Soma de Bases (SB)", f"{sb:.2f}")
            c2.metric("CTC (T)", f"{ctc:.2f}")
            c3.metric("V% Atual", f"{v_atual:.1f}%", delta=f"{v_atual - v_alvo:.1f}%")

            st.markdown("### Recomendação")
            if nc > 0:
                st.success(f"Necessidade de Calagem: **{nc:.2f} ton/ha**")
                st.info(f"Calcário PRNT {prnt}%.")
            else:
                st.success("✅ Solo já corrigido!")

# ==================================================
# FERRAMENTA 2: PULVERIZADOR
# ==================================================
elif opcao == "🚜 Calibração de Pulverizador":
    with st.container():
        st.title("🚜 Calibração de Pulverizador")
        st.markdown("Apoio para regulagem de taxa de aplicação.")
        st.markdown("---")

        col_config, col_vel = st.columns(2)

        with col_config:
            st.subheader("⚙️ Equipamento")
            vazao = st.number_input("Vazão da Ponta (L/min)", value=0.80, step=0.05, format="%.3f")
            espacamento = st.number_input("Espaçamento (cm)", value=50.0, step=5.0)
            tanque = st.number_input("Capacidade Tanque (L)", value=600, step=100)

        with col_vel:
            st.subheader("⏱️ Velocidade")
            metodo_vel = st.radio("Método:", ("Painel do Trator", "Cronometrar no Campo"))
            velocidade_final = 0.0

            if metodo_vel == "Painel do Trator":
                velocidade_final = st.slider("Km/h", 2.0, 25.0, 5.0, 0.1)
            else:
                distancia = st.number_input("Distância (m)", value=50.0)
                tempo = st.number_input("Tempo (s)", value=30.0)
                if tempo > 0:
                    velocidade_ms = distancia / tempo
                    velocidade_final = velocidade_ms * 3.6
                    st.success(f"Velocidade: **{velocidade_final:.1f} km/h**")

        st.write("")
        if velocidade_final > 0 and espacamento > 0:
            volume_calda = (vazao * 60000) / (velocidade_final * espacamento)
            autonomia = tanque / volume_calda if volume_calda > 0 else 0

            st.markdown("---")
            st.subheader("💧 Resultados")
            col_res1, col_res2 = st.columns(2)
            
            with col_res1:
                st.metric("Volume de Calda", f"{volume_calda:.1f} L/ha")
                if volume_calda < 100: st.warning("⚠️ Baixo Volume")
                elif volume_calda <= 250: st.success("✅ Volume Ideal")
                else: st.error("🚫 Alto Volume")
            
            with col_res2:
                st.metric("Autonomia", f"{autonomia:.1f} ha")
                st.caption(f"Tanque de {tanque}L")
        else:
            st.info("Ajuste os parâmetros para calcular.")

