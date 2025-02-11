import random
from django.contrib.auth.hashers import make_password
from faker import Faker
from django.utils import timezone

fake = Faker()


def clear_accounting_data():
    """Clear existing data only from models within the 'accounting' app."""
    from django.apps import apps

    accounting_app_name = 'accounting'

    # Get all models from installed apps
    models = apps.get_models()

    for model in models:
        if model._meta.app_label == accounting_app_name:
            model.objects.all().delete()
            print(f"Data cleared from model: {model._meta.model_name} in '{accounting_app_name}' app") # Optional: Print cleared models

    print(f"Existing data cleared from all models in the '{accounting_app_name}' app.")


def generate_users(num=10):
    """Generate mock users"""
    from .models import User

    users = []

    for _ in range(num):
        user = User.objects.create(
            username=fake.user_name(),
            password=make_password('password123'),  # Never use in production!
        )
        users.append(user)

    print(f"{num} users created.")
    return users


def generate_products(num=50):
    """Generate mock products with category-based pricing"""
    from .models import Product

    categories = ['Electronics', 'Clothing', 'Food', 'Beverages', 'Stationery']
    manufacturers = ['ABC Corp', 'XYZ Ltd', 'Global Traders', 'Local Brands']
    products = []

    for _ in range(num):
        category = random.choice(categories)
        manufacturer = random.choice(manufacturers)
        cost_price = 0
        selling_price = 0

        if category == 'Electronics':
            cost_price = round(random.uniform(200, 1500), 2)
            selling_price = round(cost_price * random.uniform(1.3, 2.5), 2) # Higher markup
        elif category == 'Clothing':
            cost_price = round(random.uniform(30, 200), 2)
            selling_price = round(cost_price * random.uniform(1.5, 3.0), 2) # Higher markup
        elif category == 'Food':
            cost_price = round(random.uniform(5, 50), 2)
            selling_price = round(cost_price * random.uniform(1.2, 2.0), 2)
        elif category == 'Beverages':
            cost_price = round(random.uniform(2, 30), 2)
            selling_price = round(cost_price * random.uniform(1.2, 2.2), 2)
        elif category == 'Stationery':
            cost_price = round(random.uniform(1, 20), 2)
            selling_price = round(cost_price * random.uniform(1.3, 2.5), 2)

        product = Product.objects.create(
            name=fake.word().capitalize() + " " + category, # More descriptive name
            category=category,
            manufacturer=manufacturer,
            batch_number=fake.bothify(text='BATCH-#####'),
            expiry_date=fake.date_between(start_date='+1y', end_date='+3y'),
            cost_price=cost_price,
            selling_price=selling_price,
            stock_quantity=random.randint(10, 500),
            reorder_level=random.randint(5, 20)
        )
        products.append(product)

    print(f"{num} products created with category-based pricing.")
    return products


def generate_customers(num=30):
    """Generate mock customers"""
    from .models import Customer
    customers = []

    print(f'91 {fake.msisdn()[3:]}')
    for _ in range(num):
        customer = Customer.objects.create(
            name=fake.name(),
            phone=f'+91 {fake.msisdn()[3:]}',
            email=fake.email(),
            address=fake.address()
        )
        customers.append(customer)

    print(f"{num} customers created.")
    return customers


def generate_suppliers(num=15):
    """Generate mock suppliers"""
    from .models import Supplier
    suppliers = []

    for _ in range(num):
        supplier = Supplier.objects.create(
            name=fake.company(),
            contact_person=fake.name(),
            phone=f'+91 {fake.msisdn()[3:]}',
            email=fake.company_email(),
            address=fake.address()
        )
        suppliers.append(supplier)

    print(f"{num} suppliers created.")
    return suppliers


def generate_sales(users, customers, products, num=100):
    """Generate mock sales"""
    from .models import Sale, SaleDetail
    sales = []

    payment_modes = ['Cash', 'Card', 'UPI', 'NetBanking']

    for _ in range(num):
        # Create Sale
        customer = random.choice(customers) if random.random() > 0.2 else None
        total_amount = 0
        discount = round(random.uniform(0, 50), 2)

        sale = Sale.objects.create(
            customer=customer,
            total_amount=0,  # Will be updated
            discount=discount,
            net_amount=0,  # Will be updated
            payment_mode=random.choice(payment_modes),
            created_by=random.choice(users)
        )

        # Create Sale Details
        num_products = random.randint(1, 5)
        for _ in range(num_products):
            product = random.choice(products)
            quantity = random.randint(1, 10)
            price = product.selling_price
            subtotal = round(quantity * price, 2)
            total_amount += subtotal

            SaleDetail.objects.create(
                sale=sale,
                product=product,
                quantity=quantity,
                price=price,
                subtotal=subtotal
            )

            # Reduce product stock
            product.stock_quantity -= quantity
            product.save()

        # Update sale totals
        sale.total_amount = total_amount
        sale.net_amount = total_amount - discount
        sale.save()

        sales.append(sale)

    print(f"{num} sales created.")
    return sales


def generate_purchases(users, suppliers, products, num=50):
    """Generate mock purchases"""
    from .models import Purchase, PurchaseDetail
    purchases = []

    payment_modes = ['Cash', 'Card', 'UPI', 'NetBanking']

    for _ in range(num):
        supplier = random.choice(suppliers)
        total_cost = 0

        purchase = Purchase.objects.create(
            supplier=supplier,
            total_cost=0,  # Will be updated
            payment_mode=random.choice(payment_modes),
            created_by=random.choice(users)
        )

        # Create Purchase Details
        num_products = random.randint(1, 5)
        for _ in range(num_products):
            product = random.choice(products)
            quantity = random.randint(10, 100)
            cost_price = product.cost_price
            subtotal = round(quantity * cost_price, 2)
            total_cost += subtotal

            PurchaseDetail.objects.create(
                purchase=purchase,
                product=product,
                quantity=quantity,
                cost_price=cost_price,
                subtotal=subtotal
            )

            # Increase product stock
            product.stock_quantity += quantity
            product.save()

        # Update purchase totals
        purchase.total_cost = total_cost
        purchase.save()

        purchases.append(purchase)

    print(f"{num} purchases created.")
    return purchases


def generate_expenses(users, num=30):
    """Generate mock expenses"""
    from .models import Expense
    expenses = []

    expense_categories = [
        'Rent', 'Utilities', 'Salaries', 'Marketing',
        'Maintenance', 'Office Supplies', 'Travel'
    ]

    for _ in range(num):
        expense = Expense.objects.create(
            category=random.choice(expense_categories),
            amount=round(random.uniform(50, 5000), 2),
            notes=fake.sentence(),
            created_by=random.choice(users)
        )
        expenses.append(expense)

    print(f"{num} expenses created.")
    return expenses


def generate_financial_transactions(users, num=50):
    """Generate mock financial transactions"""
    from .models import FinancialTransaction
    transactions = []

    for _ in range(num):
        transaction = FinancialTransaction.objects.create(
            type=random.choice(['Income', 'Expense']),
            amount=round(random.uniform(100, 10000), 2),
            description=fake.sentence(),
            created_by=random.choice(users)
        )
        transactions.append(transaction)

    print(f"{num} financial transactions created.")
    return transactions


def generate_mock_data():
    """Generate complete mock dataset"""
    # Clear existing data first
    clear_existing_data()

    # Generate base entities first
    users = generate_users()
    products = generate_products()
    customers = generate_customers()
    suppliers = generate_suppliers()

    # Generate dependent entities
    generate_sales(users, customers, products)
    generate_purchases(users, suppliers, products)
    generate_expenses(users)
    generate_financial_transactions(users)

    print("Mock data generation complete!")


def alter_sales_date():
    """Alter sales date"""
    from .models import Sale
    sales = Sale.objects.all()
    for sale in sales:
        naive_datetime = fake.date_time_between(start_date='-1y', end_date='now')
        # Make the naive datetime timezone-aware
        sale.sale_date = timezone.make_aware(naive_datetime)
        sale.save()

from django.utils import timezone
from faker import Faker

fake = Faker()

def alter_expenses_date():
    """Alter expenses date"""
    from .models import Expense
    expenses = Expense.objects.all()
    for expense in expenses:
        naive_datetime = fake.date_time_between(
            start_date='-1y', end_date='now')
        expense.expense_date = timezone.make_aware(naive_datetime)
        expense.save()


def alter_purchase_date():
    """Alter purchase date"""
    from .models import Purchase
    purchases = Purchase.objects.all()
    for purchase in purchases:
        naive_datetime = fake.date_time_between(
            start_date='-1y', end_date='now'
    )
        purchase.purchase_date = timezone.make_aware(naive_datetime)
        purchase.save()


# Usage instructions
print("""
Mock Data Generator Ready!

To generate mock data, run in Django shell:
>>> from your_app.mock_data import generate_mock_data
>>> generate_mock_data()
""")
