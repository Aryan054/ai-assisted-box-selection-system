from django.contrib import admin
from .models import Product, Box, Order, OrderItem


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "length",
        "width",
        "height",
        "weight",
        "created_at",
    )

    search_fields = ("name",)

    ordering = ("name",)
    list_per_page = 10


@admin.register(Box)
class BoxAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "length",
        "width",
        "height",
        "max_weight",
    )

    search_fields = ("name",)

    ordering = (
        "length",
        "width",
        "height",
    )
    list_per_page = 10


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "status",
        "selected_box",
        "total_weight",
        "created_at",
    )

    search_fields = ("id",)

    list_filter = (
        "status",
        "selected_box",
        "created_at",
    )

    ordering = ("-created_at",)
    list_per_page = 20


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "order",
        "product",
        "quantity",
    )

    search_fields = (
        "product__name",
        "order__id",
    )

    list_filter = ("product",)

    ordering = ("order",)
    list_per_page = 20
