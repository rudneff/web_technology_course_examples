from django.urls import path

from catalog import views

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    # path('login/', views.login, name='login')
]