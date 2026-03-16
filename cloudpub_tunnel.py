"""
python cloudpub_tunnel.py
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from cloudpub_python_sdk import Connection, Protocol, Auth

PROJECT_ROOT = Path(__file__).resolve().parent
env_path = PROJECT_ROOT / '.env_cloud'

# Загрузка переменных окружения
load_dotenv(dotenv_path=env_path)


# Создание соединения с учетными данными
conn = Connection(
    email=os.getenv('EMAIL'),
    password=os.getenv('PASSWORD')
)

# Публикация локального веб-сервиса
endpoint = conn.publish(
    Protocol.HTTP,
    "localhost:8000",
    name="Мой Django сайт",
    auth=Auth.NONE
)

print(f"Сервис опубликован по адресу: {endpoint.url}")

# Поддержание сервиса в работе
try:
    input("Нажмите Enter для остановки...")
finally:
    # Очистка
    conn.unpublish(endpoint.guid)
