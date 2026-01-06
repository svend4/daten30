"""
News Service - Микросервис новостей
Порт: 5004
Категория: information
"""

from flask import Flask, jsonify, request
from datetime import datetime, timedelta
import requests
import random

app = Flask(__name__)

SERVICE_ID = 'news-service'
SERVICE_PORT = 5004
REGISTRY_URL = 'http://127.0.0.1:5000'

# Mock новости
NEWS_CATEGORIES = ['Технологии', 'Бизнес', 'Наука', 'Спорт']

SAMPLE_NEWS = [
    {'title': 'Новый релиз Flutter 3.25', 'category': 'Технологии', 'content': 'Google выпустил новую версию Flutter с улучшенной производительностью'},
    {'title': 'Биткоин достиг новых высот', 'category': 'Бизнес', 'content': 'Криптовалюта побила рекорд'},
    {'title': 'Открыта новая планета', 'category': 'Наука', 'content': 'Астрономы обнаружили экзопланету'},
    {'title': 'Чемпионат мира по футболу', 'category': 'Спорт', 'content': 'Россия вышла в плей-офф'},
]

def register_in_registry():
    try:
        requests.post(f'{REGISTRY_URL}/api/services/register', json={
            'id': SERVICE_ID,
            'name': 'Новости',
            'description': 'Лента новостей',
            'port': SERVICE_PORT,
            'icon': 'article',
            'color': '#F44336',
            'category': 'information',
            'ui_schema': {
                'type': 'list',
                'title': 'Новости',
                'endpoint': '/api/news',
                'item_template': {
                    'title': '{{title}}',
                    'subtitle': '{{category}} • {{time_ago}}',
                    'description': '{{content}}'
                }
            }
        })
        print("✅ Registered")
    except: pass

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'service': SERVICE_ID})

@app.route('/api/news', methods=['GET'])
def get_news():
    category = request.args.get('category')

    news = []
    for i, item in enumerate(SAMPLE_NEWS * 3):  # Повторить для большего объёма
        if category and item['category'] != category:
            continue

        news.append({
            'id': i + 1,
            'title': item['title'],
            'content': item['content'],
            'category': item['category'],
            'published_at': (datetime.now() - timedelta(hours=random.randint(1, 48))).isoformat(),
            'time_ago': f'{random.randint(1, 48)} часов назад',
            'views': random.randint(100, 10000)
        })

    return jsonify({
        'success': True,
        'news': news[:20],  # Первые 20
        'total': len(news)
    })

@app.route('/api/news/categories', methods=['GET'])
def get_categories():
    return jsonify({'success': True, 'categories': NEWS_CATEGORIES})

if __name__ == '__main__':
    print(f"🚀 Starting {SERVICE_ID}")
    register_in_registry()
    app.run(host='0.0.0.0', port=SERVICE_PORT, debug=False)
