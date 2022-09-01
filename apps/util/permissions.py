from rest_framework.permissions import BasePermission, IsAuthenticated

ALL_SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')


# MEMBER_SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')

class IsOwnerOnlyManageAndOtherGet(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method in ALL_SAFE_METHODS or
            request.user and
            request.user.is_authenticated
        )


class IsBookMemberUse(IsAuthenticated):
    def has_permission(request, view):
        return bool(
            request.method in ALL_SAFE_METHODS or
            request.user and
            request.user.is_authenticated
        )


class BookOwnerCheck(IsAuthenticated):
    def has_permission(instance, user):
        return bool(
            instance.bookmember_set.get(user_id=user.id).owner
        )


class BookMemberCheck(IsAuthenticated):
    def has_permission(instance, user):
        return bool(
            instance.bookmember_set.filter(user_id=user.id)
        )
