from core.models import Category, FoodItem

categories = {
    'Burgers': ['Classic Beef Burger', 'Chicken Zinger Burger', 'Veggie Burger'],
    'Pizza': ['Margherita Pizza', 'Pepperoni Pizza', 'BBQ Chicken Pizza'],
    'Biryani': ['Chicken Biryani', 'Mutton Biryani', 'Veg Biryani'],
    'Drinks': ['Mango Lassi', 'Cold Coffee', 'Fresh Lime Soda'],
    'Desserts': ['Chocolate Brownie', 'Gulab Jamun', 'Ice Cream Sundae'],
}

descriptions = {
    'Classic Beef Burger': 'Juicy beef patty with lettuce, tomato and special sauce.',
    'Chicken Zinger Burger': 'Crispy fried chicken with spicy mayo.',
    'Veggie Burger': 'Fresh veggie patty with cheese and greens.',
    'Margherita Pizza': 'Classic tomato sauce, mozzarella and basil.',
    'Pepperoni Pizza': 'Loaded with pepperoni and cheese.',
    'BBQ Chicken Pizza': 'Smoky BBQ chicken with caramelized onions.',
    'Chicken Biryani': 'Aromatic basmati rice with tender chicken.',
    'Mutton Biryani': 'Slow-cooked mutton with fragrant spices.',
    'Veg Biryani': 'Mixed vegetables with fragrant basmati rice.',
    'Mango Lassi': 'Creamy mango yogurt drink.',
    'Cold Coffee': 'Chilled coffee blended with milk and ice cream.',
    'Fresh Lime Soda': 'Refreshing lime with soda and mint.',
    'Chocolate Brownie': 'Warm fudgy brownie with vanilla ice cream.',
    'Gulab Jamun': 'Soft milk-solid dumplings in sugar syrup.',
    'Ice Cream Sundae': 'Three scoops with chocolate sauce and nuts.',
}

prices = {
    'Classic Beef Burger': 199, 'Chicken Zinger Burger': 179, 'Veggie Burger': 149,
    'Margherita Pizza': 299, 'Pepperoni Pizza': 349, 'BBQ Chicken Pizza': 369,
    'Chicken Biryani': 249, 'Mutton Biryani': 349, 'Veg Biryani': 199,
    'Mango Lassi': 89, 'Cold Coffee': 99, 'Fresh Lime Soda': 69,
    'Chocolate Brownie': 149, 'Gulab Jamun': 99, 'Ice Cream Sundae': 129,
}

veg_items = {'Veggie Burger', 'Margherita Pizza', 'Veg Biryani',
             'Mango Lassi', 'Cold Coffee', 'Fresh Lime Soda',
             'Chocolate Brownie', 'Gulab Jamun', 'Ice Cream Sundae'}

for cat_name, items in categories.items():
    cat, _ = Category.objects.get_or_create(name=cat_name)
    for item_name in items:
        FoodItem.objects.get_or_create(
            name=item_name,
            defaults={
                'category': cat,
                'description': descriptions.get(item_name, ''),
                'price': prices.get(item_name, 99),
                'is_veg': item_name in veg_items,
                'is_available': True,
            }
        )

print("Sample data loaded successfully!")
print(f"Categories: {Category.objects.count()}")
print(f"Food Items: {FoodItem.objects.count()}")