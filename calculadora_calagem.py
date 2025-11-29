import streamlit as st
import os

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Ferramentas Agronômicas",
    page_icon="🚜",
    layout="centered"
)

# --- ESTILO CSS FORÇADO (AGORA VAI!) ---
st.markdown("""
<style>
    /* 1. Forçar Fundo Cinza */
    .stApp {
        background-color: #f0f2f6 !important;
    }
    
    /* 2. Forçar Cartões Brancos (Com !important para não falhar) */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #ffffff !important;
        border-radius: 15px !important;
        padding: 20px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1) !important;
        border: 1px solid #e0e0e0 !important;
    }

    /* 3. Forçar cor do texto para Escuro (Caso o celular esteja em modo noturno) */
    p, .stMarkdown, h1, h2, h3, .stMetricLabel {
        color: #1E1E1E !important;
    }

    /* 4. Botões Verdes */
    .stButton>button {
        background-color: #2e7d32 !important;
        color: white !important;
        border-radius: 8px !important;
        border: none !important;
        font-weight: bold !important;
    }
</style>
""", unsafe_allow_html=True)

# --- BARRA LATERAL ---
with st.sidebar:
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
# FERRAMENTA 1: CALAGEM
# ==================================================
if opcao == "🪨 Calagem & Adubação":
    # Este container com border=True VAI VIRAR UM CARD BRANCO
    with st.container(border=True):
        st.title("🪨 Calculadora de Calagem")
        st.markdown("Método de **Saturação por Bases**.")
        st.divider()

        st.header("1. Dados da Análise de Solo")
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Bases e Acidez")
            k = st.number_input("Potássio (K)", min_value=0.0, format="%.2f")
            ca = st.number_input("Cálcio (Ca)", min_value=0.0, format="%.2f")
            mg = st.number_input("Magnésio (Mg)", min_value=0.0, format="%.2f")
            hal = st.number_input("H+Al (Acidez)", min_value=0.0, format="%.2f")

        with col2:
            st.subheader("Outros")
            p = st.number_input("Fósforo (P)", min_value=0.0, format="%.2f")
            v_alvo = st.number_input("V% Desejada", value=70.0, step=1.0)
            prnt = st.number_input("PRNT (%)", value=80.0, step=1.0)

        st.write("") 
        if st.button("Calcular Necessidades", type="primary"):
            sb = k + ca + mg
            ctc = sb + hal
            v_atual = (sb / ctc) * 100 if ctc > 0 else 0
            nc = ((v_alvo - v_atual) * ctc) / prnt
            if nc < 0: nc = 0

            st.markdown("---")
            st.subheader("📊 Resultados")
            
            # Outro card branco para o resultado
            with st.container(border=True):
                c1, c2, c3 = st.columns(3)
                c1.metric("Soma de Bases", f"{sb:.2f}")
                c2.metric("CTC", f"{ctc:.2f}")
                c3.metric("V% Atual", f"{v_atual:.1f}%")

            st.write("")
            if nc > 0:
                st.success(f"Necessidade: **{nc:.2f} ton/ha**")
                st.info(f"Calcário PRNT {prnt}%")
            else:
                st.success("✅ Solo corrigido!")

# ==================================================
# FERRAMENTA 2: PULVERIZADOR
# ==================================================
elif opcao == "🚜 Calibração de Pulverizador":
    with st.container(border=True):
        st.title("🚜 Pulverizador")
        st.markdown("Apoio para regulagem.")
        st.divider()

        col_config, col_vel = st.columns(2)
        with col_config:
            st.subheader("⚙️ Equipamento")
            vazao = st.number_input("Vazão (L/min)", value=0.80, format="%.3f")
            espacamento = st.number_input("Espaçamento (cm)", value=50.0)
            tanque = st.number_input("Tanque (L)", value=600)

        with col_vel:
            st.subheader("⏱️ Velocidade")
            metodo = st.radio("Método:", ("Painel", "Cronômetro"))
            vel_final = 0.0

            if metodo == "Painel":
                vel_final = st.slider("Km/h", 2.0, 25.0, 5.0)
            else:
                dist = st.number_input("Distância (m)", value=50.0)
                tempo = st.number_input("Tempo (s)", value=30.0)
                if tempo > 0:
                    vel_final = (dist / tempo) * 3.6
                    st.success(f"Velocidade: **{vel_final:.1f} km/h**")

        st.write("")
        if vel_final > 0 and espacamento > 0:
            vol = (vazao * 60000) / (vel_final * espacamento)
            autonomia = tanque / vol if vol > 0 else 0

            st.markdown("---")
            with st.container(border=True):
                c1, c2 = st.columns(2)
                c1.metric("Volume", f"{vol:.1f} L/ha")
                c2.metric("Autonomia", f"{autonomia:.1f} ha")
                
                if vol < 100: st.warning("⚠️ Baixo")
                elif vol <= 250: st.success("✅ Ideal")
                else: st.error("🚫 Alto")
        else:
            st.info("Insira os dados para calcular.")
