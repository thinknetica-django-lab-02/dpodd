from django.urls import path

from . import views

app_name = 'main'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('goods/', views.GoodsItemsList.as_view(), name='goods-list'),
    path('goods/<int:pk>/', views.GoodsDetailView.as_view(), name='goods-detail'),
    path('goods/<int:pk>/edit', views.EditItemOfGoodsView.as_view(), name='goods-edit'),
    path('goods/add', views.AddItemOfGoodsView.as_view(), name='goods-add'),
]
