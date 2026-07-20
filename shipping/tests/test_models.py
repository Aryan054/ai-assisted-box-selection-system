from decimal import Decimal

from django.test import TestCase

from shipping.models import Product, Box, Order, OrderItem


class ProductModelTest(TestCase):

    def test_create_product(self):
        product = Product.objects.create(
            name="Laptop",
            length=Decimal("30"),
            width=Decimal("20"),
            height=Decimal("5"),
            weight=Decimal("2.50"),
        )

        self.assertEqual(product.name, "Laptop")
        self.assertEqual(product.weight, Decimal("2.50"))

    def test_string_representation(self):
        product = Product.objects.create(
            name="Keyboard",
            length=40,
            width=15,
            height=5,
            weight=1,
        )

        self.assertEqual(str(product), "Keyboard")


class BoxModelTest(TestCase):

    def test_volume_property(self):
        box = Box.objects.create(
            name="Small Box",
            length=Decimal("10"),
            width=Decimal("5"),
            height=Decimal("4"),
            max_weight=Decimal("20"),
        )

        self.assertEqual(box.volume, Decimal("200"))

    def test_string_representation(self):
        box = Box.objects.create(
            name="Large Box",
            length=40,
            width=30,
            height=20,
            max_weight=30,
        )

        self.assertEqual(str(box), "Large Box")


class OrderModelTest(TestCase):

    def setUp(self):

        self.product = Product.objects.create(
            name="Mouse",
            length=10,
            width=5,
            height=3,
            weight=1,
        )

    def test_add_order_item(self):

        order = Order.objects.create()

        OrderItem.objects.create(
            order=order,
            product=self.product,
            quantity=2,
        )

        self.assertEqual(order.items.count(), 1)

    def test_order_has_products(self):

        order = Order.objects.create()

        OrderItem.objects.create(
            order=order,
            product=self.product,
            quantity=5,
        )

        self.assertTrue(order.items.exists())
