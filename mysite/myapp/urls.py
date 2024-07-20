from django.urls import path
from .views import index, recommendations

urlpatterns = [
    path('', index, name='index'),
    path('recommendations/<int:user_id>/', recommendations, name='recommendations'),
]
