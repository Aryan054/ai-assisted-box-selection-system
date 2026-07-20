from django.urls import path
from .views import (
    ProductListCreateAPIView,
    ProductDetailAPIView,
    BoxListCreateAPIView,
    BoxDetailAPIView,
    OrderListCreateAPIView,
    OrderDetailAPIView,
    RecommendBoxAPIView,
)

urlpatterns = [
    path("products/", ProductListCreateAPIView.as_view(), name="product-list"),
    path("products/<int:pk>/", ProductDetailAPIView.as_view(), name="product-detail"),
    path("boxes/", BoxListCreateAPIView.as_view(), name="box-list"),
    path("boxes/<int:pk>/", BoxDetailAPIView.as_view(), name="box-detail"),
    path("orders/", OrderListCreateAPIView.as_view(), name="order-list"),
    path("orders/<int:pk>/", OrderDetailAPIView.as_view(), name="order-detail"),
    path("recommend-box/", RecommendBoxAPIView.as_view(), name="recommend-box"),
]
