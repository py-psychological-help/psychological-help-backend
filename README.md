# psychological-help-backend

Руководство по подключению gmail api

1. создаем проект google https://console.cloud.google.com/projectcreate
2. в меню menu > IAM & Admin > Создать проект
3. после создания в этом окне в поиске вбиваем gmail api
4. в самом низу в категории marketplace выбираем Gmail Api
5. загрузится окно и нажимаем enable
6. слева в поле нажимаем credentials
7. наверху выбираем + create credentials в всплывающем окне OAuth client ID
8. нажимаем configure consent screen
9. выбираем extenal и кнопку create
10. заполняем все данные жмем сохранить, в другом окне создать
11. выполняем 6 и 7 пункт
12. выбираем desktop app и сохраняем
13. в всплывающем окне нажимаем dowanload json
14. слева нажимаем OAuth consent screen и делаем проект публичным publishing status

Json файл переименовываем в credentials.json и закидываем в папку backend
запускаем локально через runserver, в консоле переходим по ссылке и все подтверждаем
после нас перекидывает на локалхост, копируем весь url, вставляем в терминал и нажимаем enter
наш json файл обновляется и больше никаих манипуляций делать не нужно
после собираем докер


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
