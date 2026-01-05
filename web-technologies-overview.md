# Обзор Веб-Технологий

## Что такое веб-технологии?

**Веб-технологии** — это набор инструментов, языков программирования, протоколов и стандартов, которые используются для создания, разработки и поддержки веб-сайтов и веб-приложений в интернете.

---

## Основные виды веб-технологий

### 1. **Frontend (Клиентская часть)**

Технологии, которые работают в браузере пользователя и отвечают за визуальное представление и взаимодействие.

#### Основные технологии:
- **HTML** (HyperText Markup Language) — структура страницы
- **CSS** (Cascading Style Sheets) — оформление и стили
- **JavaScript** — интерактивность и логика

#### Пример простой HTML/CSS/JS страницы:

```html
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Пример Frontend</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-align: center;
            padding: 50px;
        }
        button {
            padding: 10px 20px;
            font-size: 16px;
            cursor: pointer;
            background: white;
            color: #667eea;
            border: none;
            border-radius: 5px;
        }
    </style>
</head>
<body>
    <h1>Добро пожаловать!</h1>
    <p id="counter">Вы нажали: 0 раз</p>
    <button onclick="increment()">Нажми меня</button>

    <script>
        let count = 0;
        function increment() {
            count++;
            document.getElementById('counter').textContent = `Вы нажали: ${count} раз`;
        }
    </script>
</body>
</html>
```

#### Популярные Frontend фреймворки:
- **React** — библиотека от Facebook
- **Vue.js** — прогрессивный фреймворк
- **Angular** — полноценный фреймворк от Google
- **Svelte** — компилирующий фреймворк

#### Пример React компонента:

```jsx
import React, { useState } from 'react';

function Counter() {
    const [count, setCount] = useState(0);

    return (
        <div className="counter">
            <h2>Счетчик: {count}</h2>
            <button onClick={() => setCount(count + 1)}>
                Увеличить
            </button>
            <button onClick={() => setCount(0)}>
                Сбросить
            </button>
        </div>
    );
}

export default Counter;
```

---

### 2. **Backend (Серверная часть)**

Технологии, которые работают на сервере и обрабатывают запросы, работают с базами данных и бизнес-логикой.

#### Основные языки и фреймворки:

**Node.js (JavaScript)**
```javascript
// Express.js сервер
const express = require('express');
const app = express();

app.get('/api/users', (req, res) => {
    res.json([
        { id: 1, name: 'Иван' },
        { id: 2, name: 'Мария' }
    ]);
});

app.listen(3000, () => {
    console.log('Сервер запущен на порту 3000');
});
```

**Python (Django/Flask)**
```python
# Flask API
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/users')
def get_users():
    return jsonify([
        {'id': 1, 'name': 'Иван'},
        {'id': 2, 'name': 'Мария'}
    ])

if __name__ == '__main__':
    app.run(debug=True)
```

**PHP**
```php
<?php
// Простой API endpoint
header('Content-Type: application/json');

$users = [
    ['id' => 1, 'name' => 'Иван'],
    ['id' => 2, 'name' => 'Мария']
];

echo json_encode($users);
?>
```

**Java (Spring Boot)**
```java
@RestController
@RequestMapping("/api")
public class UserController {

    @GetMapping("/users")
    public List<User> getUsers() {
        return List.of(
            new User(1, "Иван"),
            new User(2, "Мария")
        );
    }
}
```

---

### 3. **Базы данных**

Системы хранения и управления данными.

#### SQL (Реляционные):
- **PostgreSQL**
- **MySQL**
- **SQLite**

```sql
-- Создание таблицы пользователей
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Вставка данных
INSERT INTO users (name, email) VALUES ('Иван', 'ivan@example.com');

-- Запрос данных
SELECT * FROM users WHERE name LIKE 'И%';
```

#### NoSQL (Нереляционные):
- **MongoDB**
- **Redis**
- **Cassandra**

```javascript
// MongoDB пример
db.users.insertOne({
    name: "Иван",
    email: "ivan@example.com",
    age: 28,
    tags: ["developer", "javascript"]
});

// Поиск
db.users.find({ age: { $gt: 25 } });
```

---

### 4. **API и протоколы**

#### REST API
```javascript
// GET запрос - получить пользователя
GET /api/users/1

// POST запрос - создать пользователя
POST /api/users
{
    "name": "Петр",
    "email": "petr@example.com"
}

// PUT запрос - обновить пользователя
PUT /api/users/1
{
    "name": "Петр Иванов"
}

// DELETE запрос - удалить пользователя
DELETE /api/users/1
```

#### GraphQL
```graphql
# Запрос
query {
    user(id: 1) {
        name
        email
        posts {
            title
            content
        }
    }
}

# Мутация
mutation {
    createUser(name: "Анна", email: "anna@example.com") {
        id
        name
    }
}
```

#### WebSocket (Реальное время)
```javascript
// Клиент
const socket = new WebSocket('ws://localhost:8080');

socket.onmessage = (event) => {
    console.log('Получено:', event.data);
};

socket.send('Привет, сервер!');
```

---

## Виды веб-приложений

### 1. **Статические сайты**

Простые HTML/CSS страницы без серверной логики.

**Пример структуры:**
```
/website
  ├── index.html
  ├── about.html
  ├── css/
  │   └── style.css
  └── js/
      └── script.js
```

**Технологии:** HTML, CSS, JavaScript
**Хостинг:** GitHub Pages, Netlify, Vercel

---

### 2. **Single Page Application (SPA)**

Одностраничное приложение, которое динамически обновляет содержимое без перезагрузки страницы.

**Пример (React Router):**
```jsx
import { BrowserRouter, Routes, Route } from 'react-router-dom';

function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/about" element={<About />} />
                <Route path="/users" element={<Users />} />
            </Routes>
        </BrowserRouter>
    );
}
```

**Технологии:** React, Vue, Angular
**Примеры:** Gmail, Facebook, Twitter

---

### 3. **Progressive Web Apps (PWA)**

Веб-приложения с возможностями нативных приложений.

**Пример Service Worker:**
```javascript
// service-worker.js
self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open('v1').then((cache) => {
            return cache.addAll([
                '/',
                '/index.html',
                '/styles.css',
                '/app.js'
            ]);
        })
    );
});

self.addEventListener('fetch', (event) => {
    event.respondWith(
        caches.match(event.request).then((response) => {
            return response || fetch(event.request);
        })
    );
});
```

**Manifest файл:**
```json
{
    "name": "Мое PWA приложение",
    "short_name": "PWA",
    "start_url": "/",
    "display": "standalone",
    "background_color": "#ffffff",
    "theme_color": "#667eea",
    "icons": [
        {
            "src": "/icon-192.png",
            "sizes": "192x192",
            "type": "image/png"
        }
    ]
}
```

**Возможности:** Офлайн режим, push-уведомления, установка на устройство

---

### 4. **Multi-Page Application (MPA)**

Традиционное веб-приложение с множеством HTML страниц.

**Пример (Express.js + EJS):**
```javascript
app.get('/', (req, res) => {
    res.render('home', { title: 'Главная' });
});

app.get('/products', (req, res) => {
    res.render('products', {
        products: database.getProducts()
    });
});
```

**Технологии:** Server-Side Rendering (SSR)
**Примеры:** Amazon, Wikipedia

---

### 5. **Real-time приложения**

Приложения с мгновенной синхронизацией данных.

**Пример (Socket.io):**
```javascript
// Сервер
io.on('connection', (socket) => {
    console.log('Пользователь подключился');

    socket.on('chat message', (msg) => {
        io.emit('chat message', msg);
    });
});

// Клиент
const socket = io();
socket.on('chat message', (msg) => {
    addMessageToChat(msg);
});
```

**Примеры:** Чаты, онлайн игры, коллаборативные редакторы

---

### 6. **API-first приложения**

Backend предоставляет API, frontend потребляет его.

**Пример архитектуры:**
```javascript
// Backend API (Node.js + Express)
app.get('/api/products', async (req, res) => {
    const products = await Product.find();
    res.json(products);
});

// Frontend (Fetch)
async function loadProducts() {
    const response = await fetch('/api/products');
    const products = await response.json();
    displayProducts(products);
}
```

---

## Современные подходы

### 1. **JAMstack**

**J**avaScript + **A**PIs + **M**arkup

**Пример (Next.js Static Generation):**
```javascript
export async function getStaticProps() {
    const res = await fetch('https://api.example.com/posts');
    const posts = await res.json();

    return {
        props: { posts }
    };
}

export default function Blog({ posts }) {
    return (
        <div>
            {posts.map(post => (
                <article key={post.id}>
                    <h2>{post.title}</h2>
                    <p>{post.content}</p>
                </article>
            ))}
        </div>
    );
}
```

---

### 2. **Serverless (Бессерверная архитектура)**

**Пример (AWS Lambda):**
```javascript
exports.handler = async (event) => {
    const { name } = JSON.parse(event.body);

    return {
        statusCode: 200,
        body: JSON.stringify({
            message: `Привет, ${name}!`
        })
    };
};
```

---

### 3. **Microservices (Микросервисы)**

```
┌─────────────┐
│   Gateway   │
└──────┬──────┘
       │
   ┌───┴────┬────────┬────────┐
   │        │        │        │
┌──▼──┐ ┌──▼──┐ ┌──▼──┐ ┌───▼────┐
│Users│ │Posts│ │Auth │ │Comments│
└─────┘ └─────┘ └─────┘ └────────┘
```

**Пример:**
```javascript
// User Service
app.get('/users/:id', (req, res) => {
    // Обработка пользователей
});

// Post Service
app.get('/posts/:id', (req, res) => {
    // Обработка постов
});

// API Gateway объединяет все сервисы
```

---

## Инструменты разработки

### 1. **Сборщики (Build Tools)**
- **Webpack** — модульный сборщик
- **Vite** — быстрый сборщик нового поколения
- **Parcel** — zero-config сборщик

### 2. **Системы контроля версий**
- **Git** — распределенная система контроля версий

```bash
git init
git add .
git commit -m "Начальный коммит"
git push origin main
```

### 3. **Package Managers**
- **npm** — Node Package Manager
- **yarn** — альтернатива npm
- **pnpm** — быстрый менеджер пакетов

```bash
npm install react
yarn add vue
pnpm install express
```

### 4. **Тестирование**
```javascript
// Jest тест
describe('Calculator', () => {
    test('складывает 2 + 2 равно 4', () => {
        expect(add(2, 2)).toBe(4);
    });
});
```

---

## Полный пример Full-Stack приложения

### Backend (Node.js + Express + MongoDB)

```javascript
// server.js
const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');

const app = express();
app.use(cors());
app.use(express.json());

// Модель
const Task = mongoose.model('Task', {
    title: String,
    completed: Boolean
});

// CRUD операции
app.get('/api/tasks', async (req, res) => {
    const tasks = await Task.find();
    res.json(tasks);
});

app.post('/api/tasks', async (req, res) => {
    const task = new Task(req.body);
    await task.save();
    res.json(task);
});

app.put('/api/tasks/:id', async (req, res) => {
    const task = await Task.findByIdAndUpdate(
        req.params.id,
        req.body,
        { new: true }
    );
    res.json(task);
});

app.delete('/api/tasks/:id', async (req, res) => {
    await Task.findByIdAndDelete(req.params.id);
    res.json({ message: 'Задача удалена' });
});

mongoose.connect('mongodb://localhost/taskapp')
    .then(() => app.listen(5000, () => console.log('Сервер запущен')));
```

### Frontend (React)

```jsx
// App.jsx
import React, { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
    const [tasks, setTasks] = useState([]);
    const [newTask, setNewTask] = useState('');

    useEffect(() => {
        loadTasks();
    }, []);

    const loadTasks = async () => {
        const { data } = await axios.get('http://localhost:5000/api/tasks');
        setTasks(data);
    };

    const addTask = async () => {
        await axios.post('http://localhost:5000/api/tasks', {
            title: newTask,
            completed: false
        });
        setNewTask('');
        loadTasks();
    };

    const toggleTask = async (id, completed) => {
        await axios.put(`http://localhost:5000/api/tasks/${id}`, {
            completed: !completed
        });
        loadTasks();
    };

    const deleteTask = async (id) => {
        await axios.delete(`http://localhost:5000/api/tasks/${id}`);
        loadTasks();
    };

    return (
        <div className="app">
            <h1>Список задач</h1>

            <div className="add-task">
                <input
                    value={newTask}
                    onChange={(e) => setNewTask(e.target.value)}
                    placeholder="Новая задача"
                />
                <button onClick={addTask}>Добавить</button>
            </div>

            <ul>
                {tasks.map(task => (
                    <li key={task._id}>
                        <input
                            type="checkbox"
                            checked={task.completed}
                            onChange={() => toggleTask(task._id, task.completed)}
                        />
                        <span style={{
                            textDecoration: task.completed ? 'line-through' : 'none'
                        }}>
                            {task.title}
                        </span>
                        <button onClick={() => deleteTask(task._id)}>
                            Удалить
                        </button>
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default App;
```

---

## Заключение

Веб-технологии постоянно развиваются. Ключевые направления:

1. **Performance** — оптимизация скорости загрузки
2. **Accessibility** — доступность для всех пользователей
3. **Security** — безопасность данных
4. **Mobile-first** — приоритет мобильных устройств
5. **AI Integration** — интеграция искусственного интеллекта

Выбор технологий зависит от требований проекта, масштаба и команды разработчиков.
