from django.urls import path
from . import views

urlpatterns = [
	path('', views.login, name='login'),
	path('create_account/', views.create_account, name='create_account'),
	path('logout/', views.logout_user, name='logout'),
	]