#django/rest_framework
from django.contrib import admin
from django.urls import path,include
from rest_framework.routers import SimpleRouter

#project level imports
from account.users import views as account_views

#initialize DefaultRouter
router = SimpleRouter()

#register account app url with router
router.register(r'accounts', account_views.UserViewSet, base_name='accounts')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include((router.urls, 'api'),namespace='v1')),
]
