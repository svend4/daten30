"""
Weather Service - Микросервис погоды
Порт: 5002
Категория: information

Функции:
- Текущая погода
- Прогноз на 7 дней
- Почасовой прогноз
"""

from flask import Flask, jsonify, request
from datetime import datetime, timedelta
import requests
import random

app = Flask(__name__)

# Конфигурация
SERVICE_ID = 'weather-service'
SERVICE_PORT = 5002
REGISTRY_URL = 'http://127.0.0.1:5000'

# ============= MOCK DATA =============
# В production можно использовать OpenWeatherMap API

CITIES = {
    'Москва': {'temp': -5, 'feels_like': -8, 'humidity': 75, 'wind_speed': 4.5},
    'Санкт-Петербург': {'temp': -3, 'feels_like': -6, 'humidity': 80, 'wind_speed': 5.2},
    'Казань': {'temp': -7, 'feels_like': -10, 'humidity': 70, 'wind_speed': 3.8},
    'Новосибирск': {'temp': -15, 'feels_like': -20, 'humidity': 65, 'wind_speed': 6.0},
    'Екатеринбург': {'temp': -10, 'feels_like': -14, 'humidity': 68, 'wind_speed': 4.2},
}

WEATHER_CONDITIONS = [
    {'id': 'clear', 'description': 'Ясно', 'icon': '☀️'},
    {'id': 'clouds', 'description': 'Облачно', 'icon': '☁️'},
    {'id': 'rain', 'description': 'Дождь', 'icon': '🌧️'},
    {'id': 'snow', 'description': 'Снег', 'icon': '❄️'},
    {'id': 'fog', 'description': 'Туман', 'icon': '🌫️'},
]

def get_weather_condition(temp):
    """Определить погодные условия на основе температуры"""
    if temp < -10:
        return WEATHER_CONDITIONS[3]  # Снег
    elif temp < 0:
        return random.choice([WEATHER_CONDITIONS[1], WEATHER_CONDITIONS[3]])  # Облачно или Снег
    elif temp < 10:
        return random.choice([WEATHER_CONDITIONS[1], WEATHER_CONDITIONS[2]])  # Облачно или Дождь
    else:
        return random.choice([WEATHER_CONDITIONS[0], WEATHER_CONDITIONS[1]])  # Ясно или Облачно

# ============= SERVICE REGISTRATION =============

def register_in_registry():
    """Зарегистрировать себя в Service Registry"""
    try:
        response = requests.post(f'{REGISTRY_URL}/api/services/register', json={
            'id': SERVICE_ID,
            'name': 'Погода',
            'description': 'Прогноз погоды',
            'port': SERVICE_PORT,
            'icon': 'wb_sunny',
            'color': '#2196F3',
            'category': 'information',
            'version': '1.0.0',
            'ui_schema': {
                'type': 'card',
                'title': 'Погода',
                'endpoint': '/api/weather/current',
                'refresh': True,
                'template': {
                    'title': '{{city}}',
                    'subtitle': '{{temp}}°C - {{description}}',
                    'content': [
                        {'label': 'Ощущается как', 'value': '{{feels_like}}°C'},
                        {'label': 'Влажность', 'value': '{{humidity}}%'},
                        {'label': 'Ветер', 'value': '{{wind_speed}} м/с'}
                    ]
                }
            }
        })

        if response.status_code in [200, 201]:
            print(f"✅ Registered in Service Registry")
        else:
            print(f"⚠️ Failed to register: {response.text}")

    except Exception as e:
        print(f"❌ Error registering in registry: {e}")

# ============= ENDPOINTS =============

@app.route('/health', methods=['GET'])
def health():
    return jsonify({
        'status': 'healthy',
        'service': SERVICE_ID,
        'version': '1.0.0',
        'port': SERVICE_PORT,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/weather/current', methods=['GET'])
def get_current_weather():
    """
    Получить текущую погоду

    Query params:
    - city: название города (default: Москва)
    """
    city = request.args.get('city', 'Москва')

    if city not in CITIES:
        return jsonify({
            'success': False,
            'error': f'City {city} not found',
            'available_cities': list(CITIES.keys())
        }), 404

    weather_data = CITIES[city]
    condition = get_weather_condition(weather_data['temp'])

    return jsonify({
        'success': True,
        'city': city,
        'temp': weather_data['temp'],
        'feels_like': weather_data['feels_like'],
        'humidity': weather_data['humidity'],
        'wind_speed': weather_data['wind_speed'],
        'description': condition['description'],
        'icon': condition['icon'],
        'condition_id': condition['id'],
        'timestamp': datetime.now().isoformat(),
        'last_updated': datetime.now().strftime('%H:%M')
    })

@app.route('/api/weather/forecast', methods=['GET'])
def get_forecast():
    """
    Прогноз на 7 дней

    Query params:
    - city: название города
    """
    city = request.args.get('city', 'Москва')

    if city not in CITIES:
        return jsonify({
            'success': False,
            'error': f'City {city} not found'
        }), 404

    base_temp = CITIES[city]['temp']
    forecast = []

    for i in range(7):
        date = datetime.now() + timedelta(days=i)
        # Варьировать температуру ±3°C
        temp = base_temp + random.randint(-3, 3)
        condition = get_weather_condition(temp)

        forecast.append({
            'date': date.strftime('%Y-%m-%d'),
            'day_of_week': date.strftime('%A'),
            'temp_min': temp - 2,
            'temp_max': temp + 3,
            'temp_avg': temp,
            'description': condition['description'],
            'icon': condition['icon'],
            'humidity': random.randint(60, 85),
            'wind_speed': round(random.uniform(2.0, 8.0), 1)
        })

    return jsonify({
        'success': True,
        'city': city,
        'forecast': forecast,
        'total_days': len(forecast)
    })

@app.route('/api/weather/hourly', methods=['GET'])
def get_hourly():
    """
    Почасовой прогноз на сегодня

    Query params:
    - city: название города
    """
    city = request.args.get('city', 'Москва')

    if city not in CITIES:
        return jsonify({
            'success': False,
            'error': f'City {city} not found'
        }), 404

    base_temp = CITIES[city]['temp']
    hourly = []

    current_hour = datetime.now().hour

    for i in range(24):
        hour = (current_hour + i) % 24
        # Температура меняется в течение дня
        if 6 <= hour <= 12:
            temp_delta = (hour - 6) * 0.5  # Утром теплеет
        elif 12 < hour <= 18:
            temp_delta = 3  # Днём тепло
        elif 18 < hour <= 22:
            temp_delta = 3 - (hour - 18) * 0.5  # Вечером холодает
        else:
            temp_delta = 0  # Ночью холодно

        temp = base_temp + temp_delta
        condition = get_weather_condition(temp)

        hourly.append({
            'hour': f'{hour:02d}:00',
            'temp': round(temp, 1),
            'description': condition['description'],
            'icon': condition['icon'],
            'humidity': random.randint(60, 85),
            'wind_speed': round(random.uniform(2.0, 6.0), 1)
        })

    return jsonify({
        'success': True,
        'city': city,
        'hourly': hourly,
        'total_hours': len(hourly)
    })

@app.route('/api/weather/cities', methods=['GET'])
def get_cities():
    """Список доступных городов"""
    return jsonify({
        'success': True,
        'cities': list(CITIES.keys()),
        'total': len(CITIES)
    })

@app.route('/api/weather/compare', methods=['GET'])
def compare_cities():
    """Сравнение погоды в разных городах"""
    comparison = []

    for city, data in CITIES.items():
        condition = get_weather_condition(data['temp'])
        comparison.append({
            'city': city,
            'temp': data['temp'],
            'feels_like': data['feels_like'],
            'description': condition['description'],
            'icon': condition['icon']
        })

    # Сортировать по температуре
    comparison.sort(key=lambda x: x['temp'], reverse=True)

    return jsonify({
        'success': True,
        'comparison': comparison,
        'warmest': comparison[0]['city'],
        'coldest': comparison[-1]['city']
    })

# ============= MAIN =============

if __name__ == '__main__':
    print("=" * 50)
    print(f"🚀 Starting {SERVICE_ID}")
    print("=" * 50)
    print(f"🌐 Server running on http://127.0.0.1:{SERVICE_PORT}")
    print(f"📍 Available cities: {', '.join(CITIES.keys())}")
    print("=" * 50)

    # Регистрация в Service Registry
    register_in_registry()

    app.run(host='0.0.0.0', port=SERVICE_PORT, debug=False)
