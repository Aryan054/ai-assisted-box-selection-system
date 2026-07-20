from rest_framework import status
from rest_framework.test import APITestCase

from shipping.models import (
    Product,
    Box,
    Order,
    OrderItem,
)


class RecommendationAPITest(APITestCase):

    def setUp(self):

        self.product = Product.objects.create(
            name="Laptop",
            length=30,
            width=20,
            height=5,
            weight=2,
        )

        Box.objects.create(
            name="Medium",
            length=40,
            width=30,
            height=20,
            max_weight=10,
        )

        self.order = Order.objects.create()

        OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=1,
        )

    def test_recommend_box_api(self):

        response = self.client.post(
            "/api/recommend-box/",
            {"order_id": self.order.id},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertTrue(response.data["success"])

    def test_invalid_order(self):

        response = self.client.post(
            "/api/recommend-box/",
            {"order_id": 999},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_missing_order_id(self):

        response = self.client.post(
            "/api/recommend-box/",
            {},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
