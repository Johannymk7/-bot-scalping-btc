from flask import Flask, request, jsonify
from binance.client import Client
import os

app = Flask(__name__)

# Reemplaza con tus claves reales de API de Binance (usa variables de entorno en producción)
API_KEY = os.getenv("BINANCE_API_KEY", "TU_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET", "TU_API_SECRET")
client = Client(API_KEY, API_SECRET)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()

    if not data or 'action' not in data or 'symbol' not in data:
        return jsonify({'error': 'Datos inválidos'}), 400

    symbol = data['symbol']
    action = data['action'].lower()

    try:
        if action == 'buy':
            order = client.create_order(
                symbol=symbol,
                side=Client.SIDE_BUY,
                type=Client.ORDER_TYPE_MARKET,
                quantity=data.get('quantity', 0.001)
            )
        elif action == 'sell':
            order = client.create_order(
                symbol=symbol,
                side=Client.SIDE_SELL,
                type=Client.ORDER_TYPE_MARKET,
                quantity=data.get('quantity', 0.001)
            )
        else:
            return jsonify({'error': 'Acción no soportada'}), 400

        return jsonify({'message': 'Orden ejecutada', 'order': order})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
