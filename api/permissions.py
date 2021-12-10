from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.contrib.auth.models import User

class IsSuperUser(BasePermission):
	def has_permission(self, request, view):
		return bool(
				request.method in SAFE_METHODS and
				request.user and
				request.user.is_superuser
			)

class IsUser(BasePermission):

	def has_object_permission(self, request, view, User):
		return bool(
				request.user.is_authenticated and
				request.user.is_superuser or
				request.user.is_authenticated and
				request.user.id == User.id
			)

class UserPosition(BasePermission):
	def has_object_permission(self, request, view, obj):
		print(request.user.id)
		print("---------------")
		print(obj.paper_trading.user.id)
		return bool(
				request.user.is_authenticated and
				request.user.is_superuser or
				request.user.is_authenticated and
				request.user.id == obj.paper_trading.user.id
			)


class IsStaffOrReadOnly(BasePermission):
	def has_permission(self, request, view):
		return bool(
				request.method in SAFE_METHODS or
				request.user and
				request.user.is_staff
			)
