# psychological-help-backend

Настроен workflow для автоматического деплоя на сервер из ветки main. 


Вручную задеплоить можно следующими командами из папки "psyhelp"
```bash
docker compose -f docker-compose.production.yml down
docker compose -f docker-compose.production.yml pull
docker compose -f docker-compose.production.yml up -d
```

Полезные команды:

Залить новые файлы фронта
В папку "psyhelp" загрузить папку "build". Выполнить команду из папки "psyhelp":

```bash
sudo docker compose -f docker-compose.production.yml cp build/. gateway:staticfiles
```

Сделать бэкап БД
```bash
sudo docker compose -f docker-compose.production.yml exec pg_dump -U username dbname > db.dump
sudo docker compose -f docker-compose.production.yml cp db:db.dump db.dump
```


Восстановить БД
```bash
pg_dump -U username dbname > db.dump
sudo docker compose -f docker-compose.production.yml cp db.dump db:.
sudo docker compose -f docker-compose.production.yml exec pg_restore -U psyhelp_user -f db.dump
```

Для запуска проекта локально требуется сервер Redis и PostgreSQL:
```bash
sudo docker compose up
sudo docker compose exec backend python manage.py migrate 
```