from django.urls import path

from apps.main import views
from apps.main.periodic_tasks import start_scheduler


app_name = 'main'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('goods/', views.GoodsItemsList.as_view(), name='goods-list'),
    path('goods/add/', views.AddItemOfGoodsView.as_view(), name='goods-add'),
    path('goods/<slug:slug>/', views.GoodsDetailView.as_view(), name='goods-detail'),
    path('goods/<slug:slug>/edit', views.EditItemOfGoodsView.as_view(), name='goods-edit'),

]

# start scheduler here to avoid duplication of threads in development server (as opposed to doing this in `ready()`
# method in apps.py)
start_scheduler()
