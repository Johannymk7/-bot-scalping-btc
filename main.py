from flask import Flask, request, jsonify
from binance.client import Client
import os

app = Flask(__name__)

# Leer claves API desde variables de entorno (en Render > Environment)
API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")

# Validación básica por si están vacías
if not API_KEY or not API_SECRET:
    raise ValueError("❌ Las claves de API no están definidas. Verifica las variables de entorno.")

# Conexión a la Testnet de Binance
client = Client(API_KEY, API_SECRET)
client.API_URL = 'https://testnet.binance.vision/api'  # importante usar /api al final

@app.route('/')
def home():
    return "✅ Bot activo en Render", 200

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.get_json()

        if not data:
            return jsonify({'error': '⚠️ JSON vacío o mal formado'}), 400

        action = data.get('action')
        symbol = data.get('symbol')
        quantity = float(data.get('quantity', 0.001))

        if not action or not symbol:
            return jsonify({'error': '⚠️ Faltan campos necesarios'}), 400

        if action.lower() == 'buy':
            order = client.create_order(
                symbol=symbol,
                side=Client.SIDE_BUY,
                type=Client.ORDER_TYPE_MARKET,
                quantity=quantity
            )
        elif action.lower() == 'sell':
            order = client.create_order(
                symbol=symbol,
                side=Client.SIDE_SELL,
                type=Client.ORDER_TYPE_MARKET,
                quantity=quantity
            )
        else:
            return jsonify({'error': '⚠️ Acción no reconocida'}), 400

        return jsonify({'message': '✅ Orden ejecutada', 'order': order}), 200

    except Exception as e:
        print("❌ Error:", str(e))
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
