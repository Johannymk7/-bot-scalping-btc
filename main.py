from flask import Flask, request, jsonify
from binance.client import Client
import os

app = Flask(__name__)

# Leer claves API desde variables de entorno (Render > Environment)
API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")

# Configurar cliente Binance con la red de prueba (Testnet)
client = Client(API_KEY, API_SECRET)
client.API_URL = 'https://testnet.binance.vision'

@app.route('/')
def home():
    return "✅ Bot activo en Render", 200

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json()
        print("📩 Alerta recibida:", data)

        if not data or 'action' not in data or 'symbol' not in data:
            print("❌ Datos incompletos o malformateados:", data)
            return jsonify({'error': 'Datos inválidos'}), 400

        symbol = data['symbol']
        action = data['action'].lower()
        quantity = data.get('quantity', 0.001)

        print(f"🚀 Ejecutando orden: {action.upper()} {symbol} - cantidad: {quantity}")

        if action == 'buy':
            order = client.create_order(
                symbol=symbol,
                side=Client.SIDE_BUY,
                type=Client.ORDER_TYPE_MARKET,
                quantity=quantity
            )
        elif action == 'sell':
            order = client.create_order(
                symbol=symbol,
                side=Client.SIDE_SELL,
                type=Client.ORDER_TYPE_MARKET,
                quantity=quantity
            )
        else:
            print("❌ Acción no reconocida:", action)
            return jsonify({'error': 'Acción no válida'}), 400

        print("✅ Orden ejecutada con éxito:", order)
        return jsonify({'message': '✅ Orden ejecutada', 'order': order})

    except Exception as e:
        print("❌ Error durante la ejecución:", str(e))
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
