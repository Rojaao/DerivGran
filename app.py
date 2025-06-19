
import streamlit as st
from deriv_bot import DerivBot

st.set_page_config(page_title="DerivGran Bot", layout="centered")
st.title("🤖 DerivGran — Robô Deriv Automatizado")

# Interface do usuário
token = st.text_input("🔑 Token da API Deriv", type="password")
strategy = st.selectbox("🎯 Estratégia", ["6em7Digit", "0Matador"])
stake = st.number_input("💰 Stake inicial (USD)", value=0.35)
factor = st.number_input("🧮 Fator de Martingale", value=1.65)
martingale = st.checkbox("🎲 Ativar Martingale", value=True)
profit_limit = st.number_input("🏁 Limite de lucro (USD)", value=10.0)
loss_limit = st.number_input("🛑 Limite de perda (USD)", value=10.0)

# Inicializar estado
if 'bot' not in st.session_state:
    st.session_state.bot = None
if 'log' not in st.session_state:
    st.session_state.log = []

# Botões
col1, col2 = st.columns(2)
if col1.button("▶️ Iniciar Robô"):
    if not token:
        st.error("⚠️ Por favor, insira seu token da Deriv.")
    else:
        st.session_state.bot = DerivBot(
            token=token,
            strategy=strategy,
            stake=stake,
            martingale=martingale,
            factor=factor,
            profit_limit=profit_limit,
            loss_limit=loss_limit,
            interface_mode=True
        )
        st.session_state.bot.start()
        st.success("✅ Robô iniciado!")

if col2.button("⏹ Parar Robô"):
    if st.session_state.bot:
        st.session_state.bot.stop()
        st.warning("⛔ Robô parado.")

# Histórico
st.markdown("### 📊 Histórico das operações")
if st.session_state.bot and st.session_state.bot.history:
    for item in st.session_state.bot.history[-15:][::-1]:
        st.write(item)
else:
    st.info("O robô ainda não executou nenhuma operação.")
