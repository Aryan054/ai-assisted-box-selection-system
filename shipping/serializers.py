from decimal import Decimal

from rest_framework import serializers

from .models import Product, Box, Order, OrderItem


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "length",
            "width",
            "height",
            "weight",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )

    def validate(self, attrs):
        dimensions = (
            attrs.get("length"),
            attrs.get("width"),
            attrs.get("height"),
        )

        if any(value <= 0 for value in dimensions):
            raise serializers.ValidationError(
                "All dimensions must be greater than zero."
            )

        if attrs.get("weight") <= 0:
            raise serializers.ValidationError("Weight must be greater than zero.")

        return attrs


class BoxSerializer(serializers.ModelSerializer):
    volume = serializers.ReadOnlyField()

    class Meta:
        model = Box
        fields = (
            "id",
            "name",
            "length",
            "width",
            "height",
            "max_weight",
            "volume",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "volume",
            "created_at",
            "updated_at",
        )

    def validate(self, attrs):
        dimensions = (
            attrs.get("length"),
            attrs.get("width"),
            attrs.get("height"),
        )

        if any(value <= 0 for value in dimensions):
            raise serializers.ValidationError(
                "All box dimensions must be greater than zero."
            )

        if attrs.get("max_weight") <= 0:
            raise serializers.ValidationError(
                "Maximum weight must be greater than zero."
            )

        return attrs


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(
        source="product.name",
        read_only=True,
    )

    class Meta:
        model = OrderItem
        fields = (
            "id",
            "product",
            "product_name",
            "quantity",
        )


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    selected_box = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Order
        fields = (
            "id",
            "status",
            "selected_box",
            "total_weight",
            "items",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "selected_box",
            "total_weight",
            "created_at",
            "updated_at",
        )

    def create(self, validated_data):
        items_data = validated_data.pop("items")

        order = Order.objects.create(**validated_data)

        total_weight = Decimal("0.00")

        for item in items_data:
            product = item["product"]
            quantity = item["quantity"]

            OrderItem.objects.create(order=order, product=product, quantity=quantity)

            total_weight += product.weight * quantity

        order.total_weight = total_weight
        order.save()

        return order

    def update(self, instance, validated_data):
        items_data = validated_data.pop("items", None)

        instance.status = validated_data.get("status", instance.status)
        instance.selected_box = validated_data.get(
            "selected_box", instance.selected_box
        )
        instance.save()

        if items_data is not None:
            instance.items.all().delete()

            total_weight = 0

            for item in items_data:
                product = item["product"]
                quantity = item["quantity"]

                OrderItem.objects.create(
                    order=instance, product=product, quantity=quantity
                )

                total_weight += product.weight * quantity

            instance.total_weight = total_weight
            instance.save()

        return instance


class RecommendationRequestSerializer(serializers.Serializer):
    order_id = serializers.IntegerField(min_value=1)


class RecommendationResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField()

    order_id = serializers.IntegerField()

    selected_box = serializers.CharField(
        allow_null=True,
    )

    total_weight = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    box_dimensions = serializers.DictField(
        child=serializers.DecimalField(
            max_digits=10,
            decimal_places=2,
        ),
        allow_null=True,
    )

    message = serializers.CharField()
