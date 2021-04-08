from django.urls import path

from .views import IndexView, GoodsItemsList, GoodsDetailView, AddItemOfGoodsView


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('goods/', GoodsItemsList.as_view(), name='goods-list'),
    path('goods/<int:pk>/', GoodsDetailView.as_view(), name='goods-detail'),
    path('goods/add/', AddItemOfGoodsView.as_view(), name='goods-add'),
]
