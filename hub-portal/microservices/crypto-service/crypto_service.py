"""
Crypto Service - Микросервис криптовалют
Порт: 5003
Категория: finance

Функции:
- Котировки криптовалют
- История цен
- Калькулятор конвертации
"""

from flask import Flask, jsonify, request
from datetime import datetime, timedelta
import requests
import random

app = Flask(__name__)

SERVICE_ID = 'crypto-service'
SERVICE_PORT = 5003
REGISTRY_URL = 'http://127.0.0.1:5000'

# Mock данные криптовалют
CRYPTO_DATA = {
    'BTC': {'name': 'Bitcoin', 'price': 43250.50, 'change_24h': 2.5, 'icon': '₿'},
    'ETH': {'name': 'Ethereum', 'price': 2280.30, 'change_24h': -1.2, 'icon': 'Ξ'},
    'BNB': {'name': 'Binance Coin', 'price': 315.75, 'change_24h': 0.8, 'icon': 'BNB'},
    'SOL': {'name': 'Solana', 'price': 98.20, 'change_24h': 5.3, 'icon': 'SOL'},
    'XRP': {'name': 'Ripple', 'price': 0.62, 'change_24h': -0.5, 'icon': 'XRP'},
}

def register_in_registry():
    try:
        requests.post(f'{REGISTRY_URL}/api/services/register', json={
            'id': SERVICE_ID,
            'name': 'Криптовалюты',
            'description': 'Котировки криптовалют',
            'port': SERVICE_PORT,
            'icon': 'currency_bitcoin',
            'color': '#FF9800',
            'category': 'finance',
            'version': '1.0.0',
            'ui_schema': {
                'type': 'list',
                'title': 'Криптовалюты',
                'endpoint': '/api/crypto/prices',
                'refresh': True,
                'item_template': {
                    'title': '{{symbol}} - {{name}}',
                    'subtitle': '${{price}}',
                    'badge': '{{change_24h}}%'
                }
            }
        })
        print("✅ Registered in Service Registry")
    except Exception as e:
        print(f"❌ Error: {e}")

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'service': SERVICE_ID})

@app.route('/api/crypto/prices', methods=['GET'])
def get_prices():
    """Текущие котировки"""
    prices = []
    for symbol, data in CRYPTO_DATA.items():
        # Добавляем небольшую случайную вариацию
        current_price = data['price'] * (1 + random.uniform(-0.01, 0.01))

        prices.append({
            'symbol': symbol,
            'name': data['name'],
            'price': round(current_price, 2),
            'change_24h': round(data['change_24h'], 2),
            'icon': data['icon'],
            'timestamp': datetime.now().isoformat()
        })

    return jsonify({
        'success': True,
        'prices': prices,
        'total': len(prices)
    })

@app.route('/api/crypto/convert', methods=['GET'])
def convert():
    """
    Калькулятор конвертации

    Query params:
    - from: BTC
    - to: USD
    - amount: 1.5
    """
    from_currency = request.args.get('from', 'BTC')
    to_currency = request.args.get('to', 'USD')
    amount = request.args.get('amount', 1.0, type=float)

    if from_currency not in CRYPTO_DATA and from_currency != 'USD':
        return jsonify({'success': False, 'error': 'Invalid currency'}), 400

    if from_currency == 'USD':
        # USD -> Crypto
        if to_currency not in CRYPTO_DATA:
            return jsonify({'success': False, 'error': 'Invalid target currency'}), 400
        result = amount / CRYPTO_DATA[to_currency]['price']
    else:
        # Crypto -> USD
        result = amount * CRYPTO_DATA[from_currency]['price']

    return jsonify({
        'success': True,
        'from': from_currency,
        'to': to_currency,
        'amount': amount,
        'result': round(result, 8),
        'rate': CRYPTO_DATA.get(from_currency, {}).get('price', 1.0)
    })

@app.route('/api/crypto/history/<symbol>', methods=['GET'])
def get_history(symbol):
    """История цен за последние 30 дней"""
    if symbol not in CRYPTO_DATA:
        return jsonify({'success': False, 'error': 'Symbol not found'}), 404

    base_price = CRYPTO_DATA[symbol]['price']
    history = []

    for i in range(30):
        date = datetime.now() - timedelta(days=29-i)
        # Симулируем изменение цены
        price = base_price * (1 + random.uniform(-0.1, 0.1))

        history.append({
            'date': date.strftime('%Y-%m-%d'),
            'price': round(price, 2),
            'volume': random.randint(1000000, 10000000)
        })

    return jsonify({
        'success': True,
        'symbol': symbol,
        'history': history
    })

if __name__ == '__main__':
    print(f"🚀 Starting {SERVICE_ID} on port {SERVICE_PORT}")
    register_in_registry()
    app.run(host='0.0.0.0', port=SERVICE_PORT, debug=False)
