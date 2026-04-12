"# flowers" 
## Интернет магазин цветов.
### Используемые технологии
- Pyton 3.13
- Django 6.0
- Postgresql

- Redis
- Celery (добавляется)

- Yookassa

## 1. Клонировать репозиторий SSH 
`git clone git@github.com:Lavandazz/flowers.git`
## 2. Создать env файлы
Образец файла для проекта [.env_example](.env_example)
Образец файла для оплат [.env_pay_example](.env_pay_example)

## 3. Установка Docker, Docker-compose из официального репозитория Docker
`sudo apt-get update`

`sudo apt-get install -y ca-certificates curl gnupg`

`sudo install -m 0755 -d /etc/apt/keyrings`

GPG-ключ Docker
`curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg`

`sudo chmod a+r /etc/apt/keyrings/docker.gpg`

Добавление официального репозитория Docker в список источников APT
`echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null`

`sudo apt-get update`

Docker compose
`sudo apt-get install -y docker-compose-plugin`

Дать права докеру:
`sudo usermod -aG docker $USER`

Перезапуск Docker:
`sudo systemctl restart docker`

Запуск контейнеров: `docker compose build` `docker compose up`

## 4. На сервере создать файл для nginx
Создание файла:
`sudo nano /etc/nginx/sites-available/floristka_conf`

    server {
        listen 80;
        server_name floristka-msk.ru www.floristka-msk.ru;

        # Прокси в Docker-контейнер
        location / {
            proxy_pass http://127.0.0.1:8002; 
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }   

### Активация NGINX:
`sudo ln -s /etc/nginx/sites-available/floristka_conf /etc/nginx/sites-enabled/`

Проверка синтаксиса: 
`sudo nginx -t`

Перезапуск:
`sudo systemctl reload nginx`

### Права доступа к nginx
`sudo chown -R www-data:www-data /var/www/flowershop/`
`sudo chmod -R 755 /var/www/flowershop/`

## 5. Certbot

#### Удалить старую версию certbot, если была
`sudo apt-get remove certbot`
#### Установить certbot через snap
`sudo snap install --classic certbot`
#### Создание ссылки на команду
`sudo ln -s /snap/bin/certbot /usr/bin/certbot`
#### Получение сертификата certbot с автоматическим изменением nginx конфигурации
`sudo certbot --nginx -d floristka-msk.ru -d www.floristka-msk.ru`
#### Проверка, что HTTPS работает
`curl -I https://floristka-msk.ru`

#### Проверка автоматического обновления сертификата 
`sudo certbot renew --dry-run`

