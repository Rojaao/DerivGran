
# 🤖 Deriv Over 3 Bot (com Streamlit)

Este robô analisa os últimos 8 dígitos da volatilidade R_100 na Deriv e faz entrada com base na estratégia "Over 3" usando Python + WebSocket + Streamlit.

## 🔧 Requisitos

- Conta na Deriv.com
- Token de API com permissão de negociação (https://app.deriv.com/account/api-token)
- Conta no [Streamlit Cloud](https://streamlit.io/cloud)
- Repositório GitHub com este projeto

## ▶️ Como rodar no Streamlit Cloud

1. Clone ou envie os arquivos para seu GitHub (público)
2. Vá para https://streamlit.io/cloud
3. Clique em **Deploy an app**
4. Escolha seu repositório e defina o arquivo principal como `app.py`

## 📌 Observações

- A entrada é com 1 tick no OVER 3 (R_100)
- Após 2 perdas consecutivas, o robô pausa por tempo aleatório (6-487s)
- Tudo exibido em tempo real na tela

⚠️ **Use em conta virtual primeiro!**
