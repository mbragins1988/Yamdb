from rest_framework import permissions


class IsAdminorModeratorAuthorOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.method in ("PATCH", "DELETE") and (
            request.user
            and (
                (
                    request.user.role in ("admin", "moderator")
                    or request.user.is_staff
                )
                or obj.author == request.user
            )
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_admin()
        )


class IsAdminOrSuperuserOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_admin()

# class IsAdminorModeratorAuthorOnly(permissions.BasePermission):

#     def has_permission(self, request, view):
#         return (
#             request.method in permissions.SAFE_METHODS
#             or request.user.is_authenticated
#         )

#     def has_object_permission(self, request, view, obj):
#         return (
#             request.method in permissions.SAFE_METHODS
#             or request.user.is_authenticated
#             and request.user.is_admin
#             or obj.author.username == request.user.username
#             and request.user.is_moderator
#         )


# class IsAdminOrReadOnly(permissions.BasePermission):
#     def has_permission(self, request, view):
#         return (
#             request.method in permissions.SAFE_METHODS
#             or request.user.is_authenticated
#             and request.user.is_admin()
#         )


# class IsAdminOrSuperuserOnly(permissions.BasePermission):
#     def has_permission(self, request, view):
#         return request.user.is_admin()
