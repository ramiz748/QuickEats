from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase

from .models import Cart, CartItem, Category, FoodItem


class CartQueryOptimizationTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="query_test_user",
            password="testpass123"
        )

        self.category = Category.objects.create(
            name="Test Category"
        )

        self.cart = Cart.objects.create(user=self.user)

        for number in range(5):
            food_item = FoodItem.objects.create(
                category=self.category,
                name=f"Food {number}",
                price=Decimal("10.00")
            )

            CartItem.objects.create(
                cart=self.cart,
                food_item=food_item,
                quantity=2
            )

    def test_get_total_uses_one_query(self):
        with self.assertNumQueries(1):
            total = self.cart.get_total()

        self.assertEqual(total, Decimal("100.00"))