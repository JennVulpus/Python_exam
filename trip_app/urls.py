from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('dashboard', views.dashboard),
    path('add', views.add),
    path('create', views.create),
    path('edit/<int:trip_id>',views.edit),
    path('save/<int:trip_id>',views.save),
    path('details/<int:trip_id>',views.details),
    path('delete/<int:trip_id>',views.delete),
]
