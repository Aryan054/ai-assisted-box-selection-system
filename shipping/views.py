from django.db import transaction
from django.shortcuts import get_object_or_404

from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Product, Box, Order
from .serializers import (
    ProductSerializer,
    BoxSerializer,
    OrderSerializer,
    RecommendationRequestSerializer,
    RecommendationResponseSerializer,
)
from .services.box_selector import BoxRecommendationService


class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class BoxListCreateAPIView(generics.ListCreateAPIView):
    queryset = Box.objects.all()
    serializer_class = BoxSerializer


class BoxDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Box.objects.all()
    serializer_class = BoxSerializer


class OrderListCreateAPIView(generics.ListCreateAPIView):
    queryset = Order.objects.prefetch_related("items", "items__product").select_related(
        "selected_box"
    )

    serializer_class = OrderSerializer


class OrderDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.prefetch_related("items", "items__product").select_related(
        "selected_box"
    )

    serializer_class = OrderSerializer


class RecommendBoxAPIView(APIView):
    """
    Recommend the best shipping box for an order.
    """

    @transaction.atomic
    def post(self, request):
        """
        POST /api/recommend-box/
        """

        # Validate request payload
        request_serializer = RecommendationRequestSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)

        order_id = request_serializer.validated_data["order_id"]

        # Fetch order
        order = get_object_or_404(Order, pk=order_id)

        try:
            service = BoxRecommendationService(order)

            selected_box = service.recommend_box()

            if selected_box is None:

                response = {
                    "success": False,
                    "order_id": order.id,
                    "selected_box": None,
                    "total_weight": order.total_weight,
                    "box_dimensions": None,
                    "message": "No suitable box found.",
                }

                serializer = RecommendationResponseSerializer(response)

                return Response(
                    serializer.data,
                    status=status.HTTP_404_NOT_FOUND,
                )

            # Update order
            order.selected_box = selected_box
            order.status = Order.Status.BOX_SELECTED
            order.save(
                update_fields=[
                    "selected_box",
                    "status",
                ]
            )

            response = {
                "success": True,
                "order_id": order.id,
                "selected_box": selected_box.name,
                "total_weight": order.total_weight,
                "box_dimensions": {
                    "length": selected_box.length,
                    "width": selected_box.width,
                    "height": selected_box.height,
                },
                "message": "Recommended box selected successfully.",
            }

            serializer = RecommendationResponseSerializer(response)

            return Response(
                serializer.data,
                status=status.HTTP_200_OK,
            )

        except ValueError as exc:

            return Response(
                {
                    "success": False,
                    "message": str(exc),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Exception:

            return Response(
                {
                    "success": False,
                    "message": "Internal server error.",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
