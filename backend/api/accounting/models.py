from django.contrib.auth.models import User
from django.db import models


class Invoice(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='invoices')
    invoice_date = models.DateTimeField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50)

    def __str__(self):
        return f"Invoice {self.id} - {self.status}"


class IncomingInvoice(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='incoming_invoices')
    supplier_name = models.CharField(max_length=255)
    invoice_date = models.DateTimeField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50)
    category = models.CharField(max_length=100)

    def __str__(self):
        return f"Incoming Invoice {self.id} - {self.supplier_name}"


class Transaction(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='transactions')
    transaction_date = models.DateTimeField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=50, choices=[
                            ('Credit', 'Credit'), ('Debit', 'Debit')])

    def __str__(self):
        return f"Transaction {self.id} - {self.type}"


class Product(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField()

    def __str__(self):
        return self.name


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(
        Invoice, on_delete=models.CASCADE, related_name='invoice_items')
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='invoice_items')
    quantity = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Invoice Item {self.id} for Invoice {self.invoice.id}"
