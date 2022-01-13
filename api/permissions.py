from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.contrib.auth import get_user_model
User = get_user_model()

class IsSuperUser(BasePermission):
	def has_permission(self, request, view):
		return bool(
				request.method in SAFE_METHODS and
				request.user and
				request.user.is_superuser
			)

class Is_Authenticated(BasePermission):
	def has_permission(self, request, view):
		return bool(
				request.user.is_authenticated
			)

class IsUser(BasePermission):

	def has_object_permission(self, request, view, User):
		return bool(
				request.user.is_authenticated and
				request.user.is_superuser or
				request.user.is_authenticated and
				request.user.id == User.id
			)

class UserWatchList(BasePermission):
	def has_object_permission(self, request, view, obj):
		return bool(
				request.user.is_authenticated and
				request.user.is_superuser or
				request.user.is_authenticated and
				request.user.id == obj.user.id
			)
class UserPosition(BasePermission):
	def has_object_permission(self, request, view, obj):
		return bool(
				request.user.is_authenticated and
				request.user.is_superuser or
				request.user.is_authenticated and
				request.user.id == obj.paper_trading.user.id
			)

class UserPositionOption(BasePermission):
	def has_object_permission(self, request, view, obj):
		return bool(
				request.user.is_authenticated and
				request.user.is_superuser or
				request.user.is_authenticated and
				request.user.id == obj.in_position.paper_trading.user.id
			)

class UserPapertrading(BasePermission):
	def has_object_permission(self, request, view, obj):
		return bool(
				request.user.is_authenticated and
				request.user.is_superuser or
				request.user.is_authenticated and
				request.user.id == obj.user.id
			)


# class is_authenticated(BasePermission):
# 	def has_permission(self, request, view):
# 		print("*************************************")
# 		return bool(
# 				request.method in SAFE_METHODS
# 			)

class IsStaffOrReadOnly(BasePermission):
	def has_permission(self, request, view):
		return bool(
				request.method in SAFE_METHODS or
				request.user and
				request.user.is_staff
			)


class IsSuperUserOrReadOnly(BasePermission):
	def has_permission(self, request, view):
		if request.method == "POST":
			return bool(
				request.user.is_authenticated and
				request.user.is_superuser
				)
		else:
			return True

