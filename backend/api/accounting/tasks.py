import time
import logging

from celery import shared_task
from django.db.transaction import atomic

from .models import Invoice, Product, Purchase as PurchaseModel, PurchaseDetail, Supplier
from .utils.utils import StructuredDataExtractor, Purchase

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


# Create a handler for console output
handler = logging.StreamHandler()  # Logs to sys.stdout/stderr
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s') # Customize format
handler.setFormatter(formatter)
logger.addHandler(handler)


@shared_task()
def run_data_extraction_task(upload_id):
    invoices = Invoice.objects.filter(upload_id=upload_id)
    for invoice in invoices:
        extract_and_save_invoice_data( invoice)
        time.sleep(3)


@atomic
def extract_and_save_invoice_data(invoice):
    extractor = StructuredDataExtractor(invoice.invoice_file.path)
    data: Purchase = extractor.extract()
    logger.warning(data)
    logger.warning(data.supplier_name)
    supplier = Supplier.objects.get(name=data.supplier_name)
    purchase= PurchaseModel.objects.create(
        purchase_date=data.purchase_date,
        supplier=supplier,
        total_cost=data.total_cost,
        payment_mode=data.payment_mode,
        created_by=invoice.upload.user
    )
    for purhcase_detail in data.purchase_details:
        product = Product.objects.get(name=purhcase_detail.product_name)
        PurchaseDetail.objects.create(
            purchase=purchase,
            product=product,
            quantity=purhcase_detail.quantity,
            cost_price=purhcase_detail.cost_price,
            subtotal=purhcase_detail.subtotal
        )

    invoice.analyzed = True
    invoice.save()
