import streamlit as st
import os

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Ferramentas Agronômicas",
    page_icon="🚜",
    layout="centered"
)

# --- ESTILO CSS ---
st.markdown("""
<style>
    /* Fundo Cinza */
    .stApp {
        background-color: #f0f2f6 !important;
    }
    
    /* Estilo dos Cartões Brancos */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #ffffff !important;
        border-radius: 15px !important;
        padding: 20px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1) !important;
        border: 1px solid #e0e0e0 !important;
    }

    /* Cores de Texto e Botões */
    h1, h2, h3, h4, h5 { color: #2e7d32 !important; }
    .stButton>button {
        background-color: #2e7d32 !important;
        color: white !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        border: none !important;
    }
    
    /* Aumentar a fonte das Abas */
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size: 1.2rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# --- CABEÇALHO (LOGO E TÍTULO) ---
col_logo, col_titulo = st.columns([1, 4])

with col_logo:
    # Mostra o logo no topo da página (não mais na lateral)
    if os.path.exists("logo.png"):
        st.image("logo.png", width=100)
    elif os.path.exists("logo.jpg"):
        st.image("logo.jpg", width=100)
    else:
        st.markdown("# 🚜")

with col_titulo:
    st.title("Ferramentas Agrícolas")
    st.caption("Eng. Agr. Rodolfo Degaspari Delagracia")

st.write("") # Espaço

# --- NAVEGAÇÃO POR ABAS (TABS) ---
tab1, tab2 = st.tabs(["🪨 Calagem", "🚜 Pulverizador"])

# ==================================================
# ABA 1: CALAGEM
# ==================================================
with tab1:
    with st.container(border=True):
        st.header("Calculadora de Calagem")
        st.markdown("Método: **Saturação por Bases**")
        st.divider()

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Bases")
            k = st.number_input("Potássio (K)", min_value=0.0, format="%.2f", key="k")
            ca = st.number_input("Cálcio (Ca)", min_value=0.0, format="%.2f", key="ca")
            mg = st.number_input("Magnésio (Mg)", min_value=0.0, format="%.2f", key="mg")
            hal = st.number_input("H+Al (Acidez)", min_value=0.0, format="%.2f", key="hal")

        with col2:
            st.subheader("Outros")
            p = st.number_input("Fósforo (P)", min_value=0.0, format="%.2f", key="p")
            v_alvo = st.number_input("V% Desejada", value=70.0, step=1.0, key="valvo")
            prnt = st.number_input("PRNT (%)", value=80.0, step=1.0, key="prnt")

        st.write("")
        if st.button("Calcular Calagem", type="primary", key="btn_calagem"):
            sb = k + ca + mg
            ctc = sb + hal
            v_atual = (sb / ctc) * 100 if ctc > 0 else 0
            nc = ((v_alvo - v_atual) * ctc) / prnt
            if nc < 0: nc = 0

            st.markdown("---")
            with st.container(border=True):
                st.subheader("📊 Resultados")
                c1, c2, c3 = st.columns(3)
                c1.metric("Soma Bases", f"{sb:.2f}")
                c2.metric("CTC", f"{ctc:.2f}")
                c3.metric("V% Atual", f"{v_atual:.1f}%")
                
                st.divider()
                if nc > 0:
                    st.success(f"Necessidade: **{nc:.2f} ton/ha**")
                else:
                    st.success("✅ Solo corrigido!")

# ==================================================
# ABA 2: PULVERIZADOR
# ==================================================
with tab2:
    with st.container(border=True):
        st.header("Calibração de Pulverizador")
        st.divider()

        col_config, col_vel = st.columns(2)
        with col_config:
            st.subheader("⚙️ Equipamento")
            vazao = st.number_input("Vazão (L/min)", value=0.80, format="%.3f", key="vazao")
            espacamento = st.number_input("Espaçamento (cm)", value=50.0, key="esp")
            tanque = st.number_input("Tanque (L)", value=600, key="tanque")

        with col_vel:
            st.subheader("⏱️ Velocidade")
            metodo = st.radio("Método:", ("Painel", "Cronômetro"), key="metodo")
            vel_final = 0.0

            if metodo == "Painel":
                vel_final = st.slider("Km/h", 2.0, 25.0, 5.0, key="slider_vel")
            else:
                dist = st.number_input("Distância (m)", value=50.0, key="dist")
                tempo = st.number_input("Tempo (s)", value=30.0, key="tempo")
                if tempo > 0:
                    vel_final = (dist / tempo) * 3.6
                    st.success(f"Velocidade: **{vel_final:.1f} km/h**")

        st.write("")
        if vel_final > 0 and espacamento > 0:
            vol = (vazao * 60000) / (vel_final * espacamento)
            autonomia = tanque / vol if vol > 0 else 0

            st.markdown("---")
            with st.container(border=True):
                st.subheader("💧 Resultados")
                c1, c2 = st.columns(2)
                c1.metric("Volume", f"{vol:.1f} L/ha")
                c2.metric("Autonomia", f"{autonomia:.1f} ha")
                
                if vol < 100: st.warning("⚠️ Baixo")
                elif vol <= 250: st.success("✅ Ideal")
                else: st.error("🚫 Alto")
