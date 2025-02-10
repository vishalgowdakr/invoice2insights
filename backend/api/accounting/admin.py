from django.contrib import admin

# Register your models here.
from .models import Invoice, Supplier, Purchase, Sale, Product, PurchaseDetail, Customer, Expense, FinancialTransaction, Upload, SaleDetail

admin.site.register(Invoice)
admin.site.register(Supplier)
admin.site.register(Purchase)
admin.site.register(Sale)
admin.site.register(Product)
admin.site.register(PurchaseDetail)
admin.site.register(Customer)
admin.site.register(Expense)
admin.site.register(FinancialTransaction)
admin.site.register(Upload)
admin.site.register(SaleDetail)
