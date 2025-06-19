
class DerivBot:
    def __init__(self, token, strategy, stake, martingale, factor, profit_limit, loss_limit, interface_mode=True):
        self.token = token
        self.strategy = strategy
        self.stake = stake
        self.martingale = martingale
        self.factor = factor
        self.profit_limit = profit_limit
        self.loss_limit = loss_limit
        self.interface_mode = interface_mode
        self.history = []
        self.running = False

    def start(self):
        self.running = True
        self.history.append("🤖 Robô iniciado com a estratégia: " + self.strategy)

    def stop(self):
        self.running = False
        self.history.append("⛔ Robô parado")


# Bot com verificação de lucro/perda, histórico e execução contínua