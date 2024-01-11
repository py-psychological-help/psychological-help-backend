# psychological-help-backend

Временно не работает доступ по SSH к серверу со стороны GitHub, поэтому для деплоя необходимо

1. Запушить изменения в ветку main
2. Закинуть в папку psyhelp (при необходимости) docker-compose.production.yml
3. Выполнить в папке psyhelp:

```bash
docker compose -f docker-compose.production.yml down
docker compose -f docker-compose.production.yml up
```
