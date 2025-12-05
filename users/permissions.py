from rest_framework import permissions

class IsModerator(permissions.BasePermission):
    message = 'You do not have permissions'

    def has_permission(self, request, view):
        return request.user.groups.filter(name='moderator').exists()