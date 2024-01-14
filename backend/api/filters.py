import django_filters
from django_filters.rest_framework import BooleanFilter

from chats.models import Chat


class ChatFilter(django_filters.FilterSet):
    """Фильтр для запросов к объектам модели Chat по active, new."""

    active = BooleanFilter(field_name='active')
    new = BooleanFilter(field_name='new', method='filter_is_new')
    is_mine = BooleanFilter(field_name='is_mine', method='filter_is_mine')

    class Meta:
        model = Chat
        fields = ('active', 'new', 'is_mine')

    def filter_is_new(self, queryset, name, value):
        return queryset.filter(psychologist__isnull=value)

    def filter_is_mine(self, queryset, name, value):
        user = self.request.user
        if value:
            return queryset.filter(psychologist=user)
        return queryset
