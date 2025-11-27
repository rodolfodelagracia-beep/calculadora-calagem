import streamlit as st

# Configuração da Página
st.set_page_config(page_title="Ferramentas Agronômicas", page_icon="🚜")

# --- MENU LATERAL ---
st.sidebar.title("Navegação")
opcao = st.sidebar.radio(
    "Escolha a Ferramenta:",
    ("🪨 Calagem & Adubação", "🚜 Calibração de Pulverizador")
)

st.sidebar.info("Desenvolvido para auxílio no campo.")

# ==================================================
# FERRAMENTA 1: CALAGEM & ADUBAÇÃO
# ==================================================
if opcao == "🪨 Calagem & Adubação":
    st.title("🪨 Calculadora de Calagem")
    st.markdown("Método de **Saturação por Bases**.")

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
        v_alvo = st.number_input("Saturação por Bases Desejada (V% Alvo)", value=70.0, step=1.0)
        prnt = st.number_input("PRNT do Calcário (%)", value=80.0, step=1.0)

    # Botão de Calcular
    if st.button("Calcular Necessidades", type="primary"):
        # Cálculos Intermediários
        sb = k + ca + mg  # Soma de Bases
        ctc = sb + hal    # CTC
        
        if ctc > 0:
            v_atual = (sb / ctc) * 100
        else:
            v_atual = 0

        # Cálculo da Necessidade de Calagem (NC)
        # Fórmula: NC = (V2 - V1) * CTC / PRNT
        nc = ((v_alvo - v_atual) * ctc) / prnt

        # Se der negativo, não precisa calagem
        if nc < 0:
            nc = 0

        st.divider()
        
        # Exibição dos Resultados
        st.subheader("📊 Resultados da Análise")
        c1, c2, c3 = st.columns(3)
        c1.metric("Soma de Bases (SB)", f"{sb:.2f} cmol/dm³")
        c2.metric("CTC (T)", f"{ctc:.2f} cmol/dm³")
        c3.metric("Saturação Atual (V%)", f"{v_atual:.1f} %", delta=f"{v_atual - v_alvo:.1f}% do Alvo")

        st.subheader("🚜 Recomendação de Calagem")
        if nc > 0:
            st.success(f"Necessidade de Calagem (NC): **{nc:.2f} toneladas por hectare**")
            st.info(f"Aplicar calcário com PRNT de {prnt}%. Se usar outro PRNT, recalcular.")
        else:
            st.success("✅ O solo já está corrigido! Não é necessário aplicar calcário.")

# ==================================================
# FERRAMENTA 2: PULVERIZADOR
# ==================================================
elif opcao == "🚜 Calibração de Pulverizador":
    st.title("🚜 Calibração de Pulverizador")
    st.markdown("Ferramenta de apoio para regulagem de taxa de aplicação.")

    col_config, col_vel = st.columns(2)

    with col_config:
        st.subheader("⚙️ Equipamento")
        vazao = st.number_input("Vazão da Ponta (L/min)", value=0.80, step=0.05, format="%.3f", help="Vazão de um único bico")
        espacamento = st.number_input("Espaçamento entre Bicos (cm)", value=50.0, step=5.0)
        tanque = st.number_input("Capacidade do Tanque (Litros)", value=600, step=100)

    with col_vel:
        st.subheader("⏱️ Velocidade")
        metodo_vel = st.radio("Como definir a velocidade?", ("Selecionar no Painel", "Cronometrar no Campo"))

        velocidade_final = 0.0

        if metodo_vel == "Selecionar no Painel":
            velocidade_final = st.slider("Velocidade (km/h)", 2.0, 25.0, 5.0, 0.1)
        else:
            distancia = st.number_input("Distância Percorrida (m)", value=50.0)
            tempo = st.number_input("Tempo Gasto (segundos)", value=30.0)
            if tempo > 0:
                velocidade_ms = distancia / tempo
                velocidade_final = velocidade_ms * 3.6
                st.success(f"Velocidade Calculada: **{velocidade_final:.1f} km/h**")
            else:
                st.error("O tempo deve ser maior que zero.")

    st.divider()

    # Cálculos Finais
    if velocidade_final > 0 and espacamento > 0:
        # Fórmula: L/ha = (L/min * 60000) / (km/h * cm)
        volume_calda = (vazao * 60000) / (velocidade_final * espacamento)
        
        # Autonomia
        if volume_calda > 0:
            autonomia = tanque / volume_calda
        else:
            autonomia = 0

        st.subheader("💧 Resultados")
        
        col_res1, col_res2 = st.columns(2)
        
        with col_res1:
            st.metric("Volume de Calda", f"{volume_calda:.1f} L/ha")
            
            # Lógica de Cores
            if volume_calda < 100:
                st.warning("⚠️ Baixo Volume (Atenção à cobertura)")
            elif volume_calda <= 250:
                st.success("✅ Volume Ideal")
            else:
                st.error("🚫 Alto Volume (Risco de escorrimento)")
        
        with col_res2:
            st.metric("Autonomia do Tanque", f"{autonomia:.1f} ha", help=f"Área coberta com {tanque} Litros")
            st.caption(f"Com um tanque de {tanque}L")

    else:
        st.warning("Insira os valores de velocidade e espaçamento para calcular.")
