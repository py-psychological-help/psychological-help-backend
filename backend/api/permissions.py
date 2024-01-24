from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsOwnerOrReadOnly(BasePermission):
    """
    Доступ разрешен только для суперпользователей, администраторов, авторов.
    объектов или пользователей с ролью модератора. Остальные пользователи
    могут только просматривать объекты, но не редактировать или удалять их.
    """

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or request.user == obj.author
        )


class ApprovedByModerator(BasePermission):
    """Не дает анонимам и User без approved_by_moderator получать список."""

    def has_permission(self, request, view):
        if view.action == 'list':
            user = request.user
            if (user.is_authenticated and user.approved_by_moderator):
                return True
            return False
        return True


class IsModeratorOrAdmin(BasePermission):
    """Позволяет только Модераторам и Орга-м получать список психологов."""

    def has_permission(self, request, view):
        user = request.user
        if (user.is_authenticated and (user.is_superuser
                                       or user.role == 'moderator'
                                       or user.is_staff)):
            return True
        return False
