## Стек инструментов

🖥 Backend
- Language: Python 3.11+.
- Framework: FastAPI.
- Database: PostgreSQL (драйвер asyncpg).
- ORM: SQLAlchemy 2.0 + Alembic (миграции).
- Async Task Queue: Celery + Redis (Брокер и Result Backend).
- Object Storage: S3 (MinIO для локальной разработки). Если что еще подкорректируем

🧠 AI (Groq Cloud)
- Provider: Groq API.
- STT (Speech-to-Text): Model whisper-large-v3.
- LLM (Analysis): Model llama-3.3-70b-versatile.

📱 Mobile
- Framework: React Native (через Expo Managed Workflow).
- Audio: expo-av (запись в .m4a AAC, Mono, 16kHz, ~32-48kbps).
- Network: TanStack Query (React Query) — для очередей синхронизации и кэширования.
- Storage: AsyncStorage — для хранения очереди файлов офлайн.

## Архитектура папок (пока без react)
```
android_app/
├── alembic/                # Миграции БД
├── docker-compose.yml      # DB, Redis, MinIO, Celery
├── requirements.txt
├── .env                    # GROQ_API_KEY, DB_URL, S3_KEYS
│
└── src/
    ├── app/
    │   ├── main.py         # Точка входа FastAPI
    │   └── config.py       # Pydantic Settings (все конфиги тут)
    │
    ├── api/
    │   ├── v1/
    │   │   └── ai_endpoints.py # endpoints для ИИ 
    │   └── dependencies.py # dependency injections проекта
    │
    ├── visits/             
    │   ├── schemas.py      # Pydantic (VisitCreate, VisitResponse, ReportJSON)
    │   ├── models.py       # SQLAlchemy (class Visit)
    │   ├── service.py      # CRUD логика, бизнес-правила
    │   └── dependencies.py # Получение сессии БД
    │
    ├── data/
    │   └── google-sheets-credentials # Ключи для выгрузки анализа в Google Sheets
    │
    ├── worker/             # Фоновые задачи
    │   ├── celery.py       # Настройка Celery app
    │   └── tasks.py        # process_audio_task(visit_id)
    │
    └── infrastructure/     # Внешние интеграции (Грязный слой)
        ├── s3.py           # Генерация ссылок, загрузка/скачивание
        ├── groq.py         # Клиент к Groq API (transcribe, analyze)
        └── google_sheets.py # Логика записи в таблицу
```
