from flask import Flask, request, jsonify
from binance.client import Client
import os

app = Flask(__name__)

# Claves desde entorno seguro (Render > Environment)
API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")

# Crear cliente Binance y apuntar a la red de pruebas
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

        # Validar datos recibidos
        if not data or 'action' not in data or 'symbol' not in data:
            print("❌ Datos inválidos:", data)
            return jsonify({'error': 'Datos inválidos'}), 400

        symbol = data['symbol']
        action = data['action'].lower()
        quantity = data.get('quantity', 0.001)

        print(f"🚀 Ejecutando orden: {action.upper()} {symbol} - cantidad: {quantity}")

        # Ejecutar orden según acción
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
            print("❌ Acción no soportada:", action)
            return jsonify({'error': 'Acción no soportada'}), 400

        print("✅ Orden ejecutada:", order)
        return jsonify({'message': '✅ Orden ejecutada', 'order': order})

    except Exception as e:
        print("❌ Error crítico:", str(e))
        return jsonify({'error': str(e)}), 500

# Ejecutar app si se corre localmente (opcional)
if __name__ == '__main__':
    app.run(debug=False, port=10000)
