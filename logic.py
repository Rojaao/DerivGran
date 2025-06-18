import asyncio
import websockets
import json
import random

async def start_bot(token, stake):
    uri = "wss://ws.derivws.com/websockets/v3?app_id=1089"
    async with websockets.connect(uri) as ws:
        await ws.send(json.dumps({"authorize": token}))
        auth_response = json.loads(await ws.recv())

        if auth_response.get("error"):
            yield "❌ Erro de Autorização", "Token inválido ou sem permissão de negociação."
            return

        yield "✅ Conectado com sucesso", "Autenticado na conta Deriv."

        await ws.send(json.dumps({
            "ticks": "R_100",
            "subscribe": 1
        }))

        digits = []
        loss_count = 0

        while True:
            try:
                msg = json.loads(await ws.recv())
            except websockets.exceptions.ConnectionClosed:
                yield "🔌 Conexão fechada", "Tentando reconectar..."
                break

            if "tick" in msg:
                quote = msg["tick"]["quote"]
                digit = int(str(quote)[-1])
                digits.append(digit)

                yield "📥 Tick recebido", f"Preço: {quote} | Último dígito: {digit}"

                if len(digits) > 8:
                    digits.pop(0)

                if len(digits) == 8:
                    count_under_4 = sum(1 for d in digits if d < 4)
                    yield "📊 Analisando", f"Dígitos: {digits} | < 4: {count_under_4}"

                    if count_under_4 >= 3:
                        yield "📈 Sinal Detectado", "Condição para OVER 3 atendida (3+ dígitos < 4). Enviando ordem..."

                        await ws.send(json.dumps({
                            "buy": 1,
                            "price": stake,
                            "parameters": {
                                "amount": stake,
                                "basis": "stake",
                                "contract_type": "DIGITOVER",
                                "barrier": "3",
                                "currency": "USD",
                                "duration": 1,
                                "duration_unit": "t",
                                "symbol": "R_100"
                            }
                        }))

                        buy_response = json.loads(await ws.recv())
                        if "buy" in buy_response:
                            contract_id = buy_response["buy"]["contract_id"]
                            yield "✅ Compra enviada", f"Contrato #{contract_id} iniciado."

                            while True:
                                result_msg = json.loads(await ws.recv())
                                if result_msg.get("contract") and result_msg["contract"].get("contract_id") == contract_id:
                                    status = result_msg["contract"]["status"]
                                    if status == "won":
                                        yield "🏆 WIN", f"Lucro! Contrato #{contract_id}"
                                        loss_count = 0
                                    elif status == "lost":
                                        yield "💥 LOSS", f"Perda. Contrato #{contract_id}"
                                        loss_count += 1
                                    break

                            digits.clear()  # Limpa os dígitos para reiniciar a coleta

                            if loss_count >= 2:
                                wait = random.randint(6, 487)
                                yield "🕒 Espera aleatória", f"Aguardando {wait} segundos após 2 perdas."
                                await asyncio.sleep(wait)
                                loss_count = 0
