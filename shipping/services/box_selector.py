from decimal import Decimal

from django.db.models import Prefetch

from shipping.models import Box, Order


class BoxRecommendationService:
    """
    Service responsible for selecting the most suitable
    shipping box for an order.
    """

    def __init__(self, order):
        self.order = order

    def recommend_box(self):
        """
        Main entry point.

        Executes the complete recommendation process and
        returns the selected box or None.
        """

        self._validate_order()

        items = self._get_order_items()

        total_weight = self._calculate_total_weight(items)

        required_dimensions = self._calculate_required_dimensions(items)

        candidate_boxes = self._find_candidate_boxes(
            required_dimensions,
            total_weight,
        )

        if not candidate_boxes:
            return None

        selected_box = self._select_best_box(candidate_boxes)

        return selected_box

    def _validate_order(self):
        """
        Ensures the order contains at least one item.
        """

        if not self.order.items.exists():
            raise ValueError("Order does not contain any products.")

    def _get_order_items(self):
        """
        Returns all order items together with their products
        using select_related to avoid additional queries.
        """

        return self.order.items.select_related("product").all()

    def _calculate_total_weight(self, items):
        """
        Calculates:

        product.weight × quantity

        for every order item.
        """

        total = Decimal("0")

        for item in items:
            total += item.product.weight * item.quantity

        return total

    def _calculate_required_dimensions(self, items):
        """
        Simple stacking strategy.

        Length = maximum product length

        Width = maximum product width

        Height = sum(product height × quantity)
        """

        max_length = Decimal("0")
        max_width = Decimal("0")
        total_height = Decimal("0")

        for item in items:

            product = item.product

            max_length = max(max_length, product.length)

            max_width = max(max_width, product.width)

            total_height += product.height * item.quantity

        return {
            "length": max_length,
            "width": max_width,
            "height": total_height,
        }

    def _find_candidate_boxes(
        self,
        required_dimensions,
        total_weight,
    ):
        """
        Returns every box satisfying:

        - dimensions
        - weight
        """

        boxes = Box.objects.all()

        candidates = []

        for box in boxes:

            if (
                box.length >= required_dimensions["length"]
                and box.width >= required_dimensions["width"]
                and box.height >= required_dimensions["height"]
                and box.max_weight >= total_weight
            ):
                candidates.append(box)

        return candidates

    def _select_best_box(self, boxes):
        """
        Select the smallest valid box.

        Primary:
            Lowest volume

        Secondary:
            Lowest maximum weight

        Final:
            Alphabetical name
        """

        return min(
            boxes,
            key=lambda box: (
                box.volume,
                box.max_weight,
                box.name,
            ),
        )
