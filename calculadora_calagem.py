import streamlit as st

def main():
    # Configuração da Página
    st.set_page_config(
        page_title="Calculadora Agronômica",
        page_icon="🌱",
        layout="centered"
    )

    # Título e Descrição
    st.title("🌱 Calculadora de Calagem e Adubação")
    st.markdown("""
    Esta ferramenta auxilia no cálculo da necessidade de calagem (NC) pelo método de **Saturação por Bases** 
    e fornece sugestões simplificadas de adubação baseadas nos teores de Fósforo e Potássio.
    """)
    st.markdown("---")

    # --- 1. Dados de Entrada (Sidebar ou Principal) ---
    st.header("1. Dados da Análise de Solo")
    
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Bases e Acidez")
        k = st.number_input("Potássio (K) [cmol/dm³]", min_value=0.0, format="%.2f", help="Teor de Potássio no solo")
        ca = st.number_input("Cálcio (Ca) [cmol/dm³]", min_value=0.0, format="%.2f", help="Teor de Cálcio no solo")
        mg = st.number_input("Magnésio (Mg) [cmol/dm³]", min_value=0.0, format="%.2f", help="Teor de Magnésio no solo")
        hal = st.number_input("H + Al (Acidez Potencial) [cmol/dm³]", min_value=0.0, format="%.2f", help="Acidez Potencial")

    with col2:
        st.subheader("Outros Parâmetros")
        p = st.number_input("Fósforo (P) [mg/dm³]", min_value=0.0, format="%.2f", help="Teor de Fósforo (Mehlich ou Resina)")
        v_alvo = st.number_input("Saturação por Bases Desejada (V% Alvo)", min_value=0.0, max_value=100.0, value=70.0, help="Ex: 70% para Milho, 60% para Soja")
        prnt = st.number_input("PRNT do Calcário (%)", min_value=0.0, max_value=100.0, value=80.0, help="Poder Relativo de Neutralização Total")

    # Botão para Calcular
    if st.button("Calcular Necessidades", type="primary"):
        
        # --- 2. Cálculos (Backend) ---
        
        # Soma de Bases (SB)
        sb = ca + mg + k
        
        # Capacidade de Troca de Cátions (CTC)
        ctc = sb + hal
        
        # Saturação por Bases Atual (V%)
        if ctc > 0:
            v_atual = (sb / ctc) * 100
        else:
            v_atual = 0.0

        # Necessidade de Calagem (NC)
        # Fórmula: NC (t/ha) = ( (V_alvo - V_atual) * CTC ) / (10 * PRNT)
        if v_atual < v_alvo:
            nc = ((v_alvo - v_atual) * ctc) / prnt
        else:
            nc = 0.0
        
        # Garantir que não seja negativo (caso V_atual > V_alvo)
        nc = max(0.0, nc)

        # --- 3. Lógica de Adubação (Simplificada) ---
        
        sugestao_p = ""
        sugestao_k = ""
        
        # Lógica para Fósforo (P)
        # NOTA: Esta é uma lógica simplificada. Em um cenário real, deve-se consultar a tabela oficial do estado (ex: Boletim 100 SP, Manual RS/SC, 5ª Aproximação MG).
        if p < 10:
            sugestao_p = "⚠️ **Baixo teor de Fósforo (< 10 mg/dm³):** Sugere-se aplicar uma dose ALTA de adubo fosfatado (P₂O₅) no plantio ou sulco."
        elif p < 20:
             sugestao_p = "ℹ️ **Teor Médio de Fósforo:** Sugere-se dose de manutenção de P₂O₅."
        else:
            sugestao_p = "✅ **Bom teor de Fósforo:** Aplicar apenas reposição da extração da cultura."

        # Lógica para Potássio (K)
        if k < 0.15:
            sugestao_k = "⚠️ **Baixo teor de Potássio (< 0.15 cmol/dm³):** Sugere-se aplicar uma dose ALTA de adubo potássico (K₂O), parcelando se necessário para evitar salinização."
        elif k < 0.30:
             sugestao_k = "ℹ️ **Teor Médio de Potássio:** Sugere-se dose de manutenção de K₂O."
        else:
            sugestao_k = "✅ **Bom teor de Potássio:** Aplicar apenas reposição."

        # --- 4. Saída (Output) ---
        
        st.markdown("---")
        st.header("📊 Resultados da Análise")

        # Métricas Principais
        col_res1, col_res2, col_res3 = st.columns(3)
        col_res1.metric("Soma de Bases (SB)", f"{sb:.2f} cmol/dm³")
        col_res2.metric("CTC (T)", f"{ctc:.2f} cmol/dm³")
        col_res3.metric("Saturação Atual (V%)", f"{v_atual:.1f} %", delta=f"{v_atual - v_alvo:.1f} % do Alvo")

        st.markdown("### 🚜 Recomendação de Calagem")
        if nc > 0:
            st.success(f"**Necessidade de Calagem (NC):** {nc:.2f} toneladas por hectare")
            st.info(f"Aplicar calcário com PRNT de {prnt}%. Se usar outro PRNT, recalcular.")
        else:
            st.success("**Não há necessidade de calagem.** O solo já atingiu ou superou a saturação desejada.")

        st.markdown("### 🌱 Sugestão de Adubação (P & K)")
        st.write(sugestao_p)
        st.write(sugestao_k)
        
        st.warning("""
        **Atenção:** As sugestões de adubação acima são genéricas e baseadas apenas em níveis críticos simplificados. 
        Para uma recomendação precisa, **consulte a Tabela Oficial de Recomendação de Adubação e Calagem do seu Estado** 
        (ex: Boletim 100 para SP, Manual de Adubação e Calagem RS/SC, etc.) e considere a cultura específica e a produtividade esperada.
        """)

if __name__ == "__main__":
    main()
