from datetime import datetime
from rest_framework.views import exception_handler
from drf_api_logger.models import APILogsModel
import json


def custom_exception_handler(exc, context):
    """Отлавливаем ошибку на сервере и сохраняем в логи"""
    response = exception_handler(exc, context)

    if response is None:
        request = context['request']
        body_str = request.body.decode('utf-8')
        api_log = APILogsModel(
            headers=json.dumps(
                dict(request.headers), sort_keys=True, indent=4
            ),
            body=json.dumps(
                json.loads(body_str),
                sort_keys=True,
                indent=4,
                ensure_ascii=False
            ),
            api=request.build_absolute_uri(),
            method=request.method,
            client_ip_address=request.META.get('REMOTE_ADDR'),
            response='Что то пошло не так',
            status_code=500,
            added_on=datetime.now(),
            execution_time=0
        )
        api_log.save()

    if response is not None:
        response.data['status_code'] = response.status_code

    return response
