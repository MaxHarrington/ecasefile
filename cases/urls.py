from django.urls import path
from . import views

from .models import Case

urlpatterns = [
	path('', views.index, name='index'),
	path('search/<str:search_term>/<int:page_number>', views.search, name='search'),
	path('mycases/<int:page_number>', views.my_cases, name='my_cases'),
	path('case/<int:case_id>/', views.case, name='case'),
	path('case/<int:case_id>/edit/', views.edit, name='edit'),
	path('case/create', views.create_case, name='create'),
	path('case/upload', views.upload_case, name='upload'),
	path('case/process_case/<int:file_id>', views.process_case, name='process_case'),
	path('casefile/create', views.create_casefile, name='create_casefile'),
	path('casefile/<int:casefile_id>', views.casefile, name='casefile'),
	path('casefile/<int:casefile_id>/add_cases', views.add_cases, name='add_cases'),
]