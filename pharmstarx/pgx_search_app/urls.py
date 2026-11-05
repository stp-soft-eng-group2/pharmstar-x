from django.urls import path
from . import views

urlpatterns = [
    path('pgx_search_app/', views.pgx_search_app, name='pgx_search_app'),
]