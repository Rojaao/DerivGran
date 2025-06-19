# BassBOT - Deriv.com Automático

Este robô conecta-se à sua conta Deriv e executa operações automáticas com base em análise de dígitos dos últimos ticks.

## Estratégias Disponíveis

- **Padrão**: entra no OVER 3 se 3 ou mais dos últimos 8 dígitos forem menores que 4.
- **0matador**: entra no OVER 3 se todos os últimos 8 dígitos forem menores que 4.

## Como usar

1. Clone o repositório ou extraia o zip.
2. Instale as dependências:

```
pip install -r requirements.txt
```

3. Execute o app:

```
streamlit run app.py
```

4. Cole seu token da Deriv e inicie o robô.

> Desenvolvido com amor para automação de operações digitais.