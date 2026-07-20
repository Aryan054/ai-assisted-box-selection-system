from django.test import TestCase

from shipping.models import (
    Product,
    Box,
    Order,
    OrderItem,
)

from shipping.services.box_selector import BoxRecommendationService


class RecommendationServiceTest(TestCase):

    def setUp(self):

        self.product = Product.objects.create(
            name="Laptop",
            length=30,
            width=20,
            height=5,
            weight=2,
        )

        self.small = Box.objects.create(
            name="Small",
            length=20,
            width=20,
            height=10,
            max_weight=3,
        )

        self.medium = Box.objects.create(
            name="Medium",
            length=40,
            width=30,
            height=20,
            max_weight=10,
        )

    def test_recommend_box(self):

        order = Order.objects.create()

        OrderItem.objects.create(
            order=order,
            product=self.product,
            quantity=1,
        )

        service = BoxRecommendationService(order)

        box = service.recommend_box()

        self.assertEqual(box.name, "Medium")

    def test_no_box_available(self):

        huge = Product.objects.create(
            name="Machine",
            length=200,
            width=200,
            height=200,
            weight=200,
        )

        order = Order.objects.create()

        OrderItem.objects.create(
            order=order,
            product=huge,
            quantity=1,
        )

        service = BoxRecommendationService(order)

        self.assertIsNone(service.recommend_box())

    def test_empty_order(self):

        order = Order.objects.create()

        service = BoxRecommendationService(order)

        with self.assertRaises(ValueError):
            service.recommend_box()
