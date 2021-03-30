from django.urls import path, include

from .views import IndexView, GoodsItemsList, GoodsDetailView


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('goods/', GoodsItemsList.as_view(), name='goods-list'),
    path('goods/<int:pk>/', GoodsDetailView.as_view(), name='goods-detail')
]
