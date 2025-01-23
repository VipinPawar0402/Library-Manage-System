from django.urls import path
from . import views
from .views import ItemRetrieveUpdateDestroy, LoginView


urlpatterns = [
    path('items/', views.ItemListCreate.as_view(), name='item-list-create'),
    path('items/<int:pk>/', ItemRetrieveUpdateDestroy.as_view(), name='item-retrieve-update-destroy'),
    path('login/', LoginView.as_view(), name='login'),
]