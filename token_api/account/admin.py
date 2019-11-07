#django/rest_framework imports
from django.contrib import admin

# # app level imports
from .users.models import User
# from .users.models import UserDetails

# # Register User models.
admin.site.register(User)