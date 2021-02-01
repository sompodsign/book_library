from django.urls import path
from . import views

app_name = 'library'

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('library/', views.library, name='book_library'),
    path('delete_book/<int:id>', views.delete_book, name='delete_book'),
    path('change_status/<int:id>', views.change_status, name='change_book_status'),
]
