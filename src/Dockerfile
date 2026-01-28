from python:3.13-slim

env PYTHONDONTWRITEBYTECODE=1
env PYTHONUNBUFFERED=1

workdir /user/project

copy requirements.txt .

run pip install --no-cache-dir -r requirements.txt

copy . .

expose 8000

cmd ["uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
