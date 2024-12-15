from models import (
    Product, Customer, Supplier,
    Sale, SaleDetail, Purchase, PurchaseDetail,
    Expense, FinancialTransaction
)
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
import os
import django
import random
from faker import Faker

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings')
django.setup()


fake = Faker()


def generate_users(num=10):
    """Generate mock users"""
    roles = ['Owner', 'Staff']
    for _ in range(num):
        User.objects.create(
            username=fake.user_name(),
            # Never use this in production!
            password=make_password('password123'),
            role=random.choice(roles)
        )


def generate_products(num=50):
    """Generate mock products"""
    categories = ['Electronics', 'Clothing', 'Food', 'Beverages', 'Stationery']
    manufacturers = ['ABC Corp', 'XYZ Ltd', 'Global Traders', 'Local Brands']

    for _ in range(num):
        cost_price = round(random.uniform(10, 500), 2)
        selling_price = round(cost_price * random.uniform(1.2, 2.0), 2)

        Product.objects.create(
            name=fake.word(),
            category=random.choice(categories),
            manufacturer=random.choice(manufacturers),
            batch_number=fake.bothify(text='BATCH-#####'),
            expiry_date=fake.date_between(start_date='+1y', end_date='+3y'),
            cost_price=cost_price,
            selling_price=selling_price,
            stock_quantity=random.randint(10, 500),
            reorder_level=random.randint(5, 20)
        )


def generate_customers(num=30):
    """Generate mock customers"""
    for _ in range(num):
        Customer.objects.create(
            name=fake.name(),
            phone=fake.phone_number(),
            email=fake.email(),
            address=fake.address()
        )


def generate_suppliers(num=15):
    """Generate mock suppliers"""
    for _ in range(num):
        Supplier.objects.create(
            name=fake.company(),
            contact_person=fake.name(),
            phone=fake.phone_number(),
            email=fake.company_email(),
            address=fake.address()
        )


def generate_sales(num=100):
    """Generate mock sales"""
    users = list(User.objects.all())
    customers = list(Customer.objects.all())
    products = list(Product.objects.all())
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


def generate_purchases(num=50):
    """Generate mock purchases"""
    users = list(User.objects.all())
    suppliers = list(Supplier.objects.all())
    products = list(Product.objects.all())
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


def generate_expenses(num=30):
    """Generate mock expenses"""
    users = list(User.objects.all())
    expense_categories = [
        'Rent', 'Utilities', 'Salaries', 'Marketing',
        'Maintenance', 'Office Supplies', 'Travel'
    ]

    for _ in range(num):
        Expense.objects.create(
            category=random.choice(expense_categories),
            amount=round(random.uniform(50, 5000), 2),
            notes=fake.sentence(),
            created_by=random.choice(users)
        )


def generate_financial_transactions(num=50):
    """Generate mock financial transactions"""
    users = list(User.objects.all())

    for _ in range(num):
        FinancialTransaction.objects.create(
            type=random.choice(['Income', 'Expense']),
            amount=round(random.uniform(100, 10000), 2),
            description=fake.sentence(),
            created_by=random.choice(users)
        )


def generate_mock_data():
    """Generate complete mock dataset"""
    generate_users()
    generate_products()
    generate_customers()
    generate_suppliers()
    generate_sales()
    generate_purchases()
    generate_expenses()
    generate_financial_transactions()


if __name__ == '__main__':
    generate_mock_data()
    print("Mock data generation complete!")
