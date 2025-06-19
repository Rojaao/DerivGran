
import streamlit as st
import asyncio, threading, websockets, json, random

# --- Lógica do robô ---
async def ws_receiver(ws, queue):
    try:
        while True:
            msg = await ws.recv()
            await queue.put(json.loads(msg))
    except:
        pass

async def bot_loop(token, stake, threshold, take_profit, stop_loss, multiplicador, estrategia):
    ws = await websockets.connect("wss://ws.derivws.com/websockets/v3?app_id=1089")
    await ws.send(json.dumps({"authorize": token}))
    auth = json.loads(await ws.recv())
    if auth.get("error"):
        st.session_state.logs.append("❌ Token inválido")
        st.session_state.bot_running = False
        return
    st.session_state.logs.append("✅ Autenticado Deriv")
    await ws.send(json.dumps({"ticks": "R_100", "subscribe": 1}))
    queue = asyncio.Queue()
    asyncio.create_task(ws_receiver(ws, queue))

    digits, total_profit, current_stake, loss_streak = [], 0.0, stake, 0
    waiting_buy = False
    contract_id = None
    contract_active = False

    while st.session_state.bot_running:
        if total_profit >= take_profit:
            st.session_state.logs.append(f"🏁 Meta atingida: +${total_profit:.2f}")
            break
        if total_profit <= -abs(stop_loss):
            st.session_state.logs.append(f"🛑 Stop loss: -${abs(total_profit):.2f}")
            break

        try:
            msg = await asyncio.wait_for(queue.get(), timeout=1.0)
        except asyncio.TimeoutError:
            continue

        if "tick" in msg and not contract_active and not waiting_buy:
            digit = int(str(msg["tick"]["quote"])[-1])
            digits.append(digit)
            if len(digits) > 8:
                digits.pop(0)
            st.session_state.logs.append(f"📥 Tick {digit} | Buffer: {digits}")

            if len(digits) == 8:
                c4 = sum(d < 4 for d in digits)
                alllt4 = all(d < 4 for d in digits)
                st.session_state.logs.append(f"📊 Análise: c4={c4}, all<4={alllt4}")

                if (estrategia == "Padrão" and c4 >= threshold) or                    (estrategia == "0matador" and alllt4):
                    st.session_state.logs.append(f"📈 Enviando Over3 com R${current_stake:.2f}")
                    await ws.send(json.dumps({
                        "buy":1, "price":current_stake,
                        "parameters":{
                            "amount":current_stake,"basis":"stake",
                            "contract_type":"DIGITOVER","barrier":"3",
                            "currency":"USD","duration":1,"duration_unit":"t","symbol":"R_100"
                        }
                    }))
                    waiting_buy = True

        if waiting_buy and "buy" in msg:
            contract_id = msg["buy"]["contract_id"]
            contract_active = True
            waiting_buy = False
            st.session_state.logs.append(f"✅ Ordem enviada #{contract_id}")
            digits.clear()

        if contract_active and "contract" in msg:
            c = msg["contract"]
            if c.get("contract_id") == contract_id:
                profit = c.get("profit",0)
                status = c.get("status")
                total_profit += profit
                if status == "won":
                    st.session_state.logs.append(f"🏆 WIN +${profit:.2f} | Total: {total_profit:.2f}")
                    current_stake = stake
                    loss_streak = 0
                else:
                    st.session_state.logs.append(f"💥 LOSS {profit:.2f} | Total: {total_profit:.2f}")
                    loss_streak += 1
                    if loss_streak >= 2:
                        current_stake *= multiplicador
                        st.session_state.logs.append(f"🔁 Multiplicador {current_stake:.2f}")
                contract_active = False

    await ws.close()

def run_bot():
    asyncio.run(bot_loop(
        st.session_state.token, st.session_state.stake,
        st.session_state.threshold,
        st.session_state.take_profit,
        st.session_state.stop_loss,
        st.session_state.mult, st.session_state.estrat
    ))

def start_bot():
    if not st.session_state.bot_running:
        st.session_state.logs.clear()
        st.session_state.bot_running = True
        threading.Thread(target=run_bot, daemon=True).start()

def stop_bot():
    st.session_state.bot_running = False

# --- Interface Streamlit ---
st.title("BassBOT com Estratégia 0matador")

st.text_input("Token Deriv", type="password", key="token")
st.number_input("Stake", value=1.0, key="stake", min_value=0.1, step=0.1)
st.selectbox("Estratégia", options=["Padrão","0matador"], key="estrat")
st.number_input("Threshold (mín dígitos <4)", value=3, key="threshold", min_value=1, max_value=8)
st.number_input("Take Profit", value=50.0, key="take_profit", min_value=0.1)
st.number_input("Stop Loss", value=20.0, key="stop_loss", min_value=0.1)
st.number_input("Multiplicador (após 2 perdas)", value=1.68, key="mult", min_value=1.0)

col1, col2 = st.columns(2)
if col1.button("▶️ Iniciar Robô"): start_bot()
if col2.button("⛔ Parar Robô"): stop_bot()

st.subheader("Logs em tempo real:")
if "logs" not in st.session_state:
    st.session_state.logs = []
for l in st.session_state.logs[-100:]:
    st.write(l)
