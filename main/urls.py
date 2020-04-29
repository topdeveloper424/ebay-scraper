from django.urls import path,include
from . import views
    
app_name = 'main'

urlpatterns = [
    path('', views.home,name='home'),
    path('/search', views.search,name='search'),
    path('/save-search', views.save_search,name='save_search'),
]