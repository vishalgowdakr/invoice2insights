from fpdf import FPDF
from datetime import datetime

# Sample Purchase Data (replace with your actual data loaded from JSON)
purchase_data = [
    {
        "model": "pharmacy.purchase",
        "pk": 6,
        "fields": {
            "purchase_date": "2025-02-12T15:00:00Z",
            "supplier": 2,
            "total_cost": "2850.00",
            "payment_mode": "Card",
            "created_by": 1
        }
    },
    {
        "model": "pharmacy.purchase",
        "pk": 7,
        "fields": {
            "purchase_date": "2025-02-18T11:30:00Z",
            "supplier": 3,
            "total_cost": "1980.00",
            "payment_mode": "UPI",
            "created_by": 2
        }
    },
    {
        "model": "pharmacy.purchase",
        "pk": 8,
        "fields": {
            "purchase_date": "2025-02-22T17:45:00Z",
            "supplier": 1,
            "total_cost": "6200.00",
            "payment_mode": "NetBanking",
            "created_by": 1
        }
    },
    {
        "model": "pharmacy.purchase",
        "pk": 9,
        "fields": {
            "purchase_date": "2025-02-28T09:00:00Z",
            "supplier": 4,
            "total_cost": "3500.00",
            "payment_mode": "Cash",
            "created_by": 2
        }
    },
    {
        "model": "pharmacy.purchase",
        "pk": 10,
        "fields": {
            "purchase_date": "2025-03-05T14:20:00Z",
            "supplier": 5,
            "total_cost": "2100.00",
            "payment_mode": "Card",
            "created_by": 1
        }
    },
    {
        "model": "pharmacy.purchase",
        "pk": 11,
        "fields": {
            "purchase_date": "2025-03-10T10:15:00Z",
            "supplier": 1,
            "total_cost": "4950.00",
            "payment_mode": "UPI",
            "created_by": 2
        }
    },
    {
        "model": "pharmacy.purchase",
        "pk": 12,
        "fields": {
            "purchase_date": "2025-03-15T16:30:00Z",
            "supplier": 2,
            "total_cost": "3100.00",
            "payment_mode": "NetBanking",
            "created_by": 1
        }
    },
    {
        "model": "pharmacy.purchase",
        "pk": 13,
        "fields": {
            "purchase_date": "2025-03-20T12:00:00Z",
            "supplier": 3,
            "total_cost": "2550.00",
            "payment_mode": "Cash",
            "created_by": 2
        }
    },
    {
        "model": "pharmacy.purchase",
        "pk": 14,
        "fields": {
            "purchase_date": "2025-03-25T18:00:00Z",
            "supplier": 4,
            "total_cost": "5800.00",
            "payment_mode": "Card",
            "created_by": 1
        }
    },
    {
        "model": "pharmacy.purchase",
        "pk": 15,
        "fields": {
            "purchase_date": "2025-03-30T14:45:00Z",
            "supplier": 5,
            "total_cost": "1750.00",
            "payment_mode": "UPI",
            "created_by": 2
        }
    }
]

purchase_detail_data = [
    {
        "model": "pharmacy.purchasedetail",
        "pk": 11,
        "fields": {
            "purchase": 6,
            "product": 11,
            "quantity": 300,
            "cost_price": "15.00",
            "subtotal": "4500.00"
        }
    },
    {
        "model": "pharmacy.purchasedetail",
        "pk": 12,
        "fields": {
            "purchase": 6,
            "product": 12,
            "quantity": 100,
            "cost_price": "20.00",
            "subtotal": "2000.00"
        }
    },
    {
        "model": "pharmacy.purchasedetail",
        "pk": 13,
        "fields": {
            "purchase": 7,
            "product": 5,
            "quantity": 200,
            "cost_price": "6.50",
            "subtotal": "1300.00"
        }
    },
    {
        "model": "pharmacy.purchasedetail",
        "pk": 14,
        "fields": {
            "purchase": 7,
            "product": 6,
            "quantity": 80,
            "cost_price": "9.00",
            "subtotal": "720.00"
        }
    },
    {
        "model": "pharmacy.purchasedetail",
        "pk": 15,
        "fields": {
            "purchase": 8,
            "product": 1,
            "quantity": 600,
            "cost_price": "5.00",
            "subtotal": "3000.00"
        }
    },
    {
        "model": "pharmacy.purchasedetail",
        "pk": 16,
        "fields": {
            "purchase": 8,
            "product": 2,
            "quantity": 200,
            "cost_price": "12.00",
            "subtotal": "2400.00"
        }
    },
    {
        "model": "pharmacy.purchasedetail",
        "pk": 17,
        "fields": {
            "purchase": 9,
            "product": 7,
            "quantity": 400,
            "cost_price": "7.00",
            "subtotal": "2800.00"
        }
    },
    {
        "model": "pharmacy.purchasedetail",
        "pk": 18,
        "fields": {
            "purchase": 9,
            "product": 8,
            "quantity": 100,
            "cost_price": "7.50",
            "subtotal": "750.00"
        }
    },
    {
        "model": "pharmacy.purchasedetail",
        "pk": 19,
        "fields": {
            "purchase": 10,
            "product": 9,
            "quantity": 200,
            "cost_price": "8.50",
            "subtotal": "1700.00"
        }
    },
    {
        "model": "pharmacy.purchasedetail",
        "pk": 20,
        "fields": {
            "purchase": 10,
            "product": 10,
            "quantity": 50,
            "cost_price": "30.00",
            "subtotal": "1500.00"
        }
    },
    {
        "model": "pharmacy.purchasedetail",
        "pk": 21,
        "fields": {
            "purchase": 11,
            "product": 3,
            "quantity": 500,
            "cost_price": "8.00",
            "subtotal": "4000.00"
        }
    },
    {
        "model": "pharmacy.purchasedetail",
        "pk": 22,
        "fields": {
            "purchase": 11,
            "product": 4,
            "quantity": 50,
            "cost_price": "25.00",
            "subtotal": "1250.00"
        }
    },
    {
        "model": "pharmacy.purchasedetail",
        "pk": 23,
        "fields": {
            "purchase": 12,
            "product": 13,
            "quantity": 20,
            "cost_price": "800.00",
            "subtotal": "16000.00"
        }
    },
    {
        "model": "pharmacy.purchasedetail",
        "pk": 24,
        "fields": {
            "purchase": 12,
            "product": 14,
            "quantity": 10,
            "cost_price": "1200.00",
            "subtotal": "12000.00"
        }
    },
    {
        "model": "pharmacy.purchasedetail",
        "pk": 25,
        "fields": {
            "purchase": 13,
            "product": 15,
            "quantity": 100,
            "cost_price": "45.00",
            "subtotal": "4500.00"
        }
    },
    {
        "model": "pharmacy.purchasedetail",
        "pk": 26,
        "fields": {
            "purchase": 13,
            "product": 16,
            "quantity": 50,
            "cost_price": "60.00",
            "subtotal": "3000.00"
        }
    },
    {
        "model": "pharmacy.purchasedetail",
        "pk": 27,
        "fields": {
            "purchase": 14,
            "product": 17,
            "quantity": 200,
            "cost_price": "300.00",
            "subtotal": "60000.00"
        }
    },
    {
        "model": "pharmacy.purchasedetail",
        "pk": 28,
        "fields": {
            "purchase": 14,
            "product": 18,
            "quantity": 50,
            "cost_price": "500.00",
            "subtotal": "25000.00"
        }
    },
    {
        "model": "pharmacy.purchasedetail",
        "pk": 29,
        "fields": {
            "purchase": 15,
            "product": 19,
            "quantity": 100,
            "cost_price": "40.00",
            "subtotal": "4000.00"
        }
    },
    {
        "model": "pharmacy.purchasedetail",
        "pk": 30,
        "fields": {
            "purchase": 15,
            "product": 20,
            "quantity": 30,
            "cost_price": "35.00",
            "subtotal": "1050.00"
        }
    }
]

supplier_data = [
    {
        "model": "pharmacy.supplier",
        "pk": 1,
        "fields": {
            "name": "MedPlus Distributors",
            "contact_person": "Rajesh Sharma",
            "phone": "9000112233",
            "email": "rajesh.sharma@medplus.com",
            "address": "Yeshwanthpur Industrial Area, Bengaluru",
            "created_at": "2023-01-10T11:30:00Z"
        }
    },
    {
        "model": "pharmacy.supplier",
        "pk": 2,
        "fields": {
            "name": "Apollo Pharma Supplies",
            "contact_person": "Priya Verma",
            "phone": "8000223344",
            "email": "priya.verma@apollopharma.com",
            "address": "Peenya Industrial Area, Bengaluru",
            "created_at": "2023-02-20T15:45:00Z"
        }
    },
    {
        "model": "pharmacy.supplier",
        "pk": 3,
        "fields": {
            "name": "Generic Medicine Agency",
            "contact_person": "Amit Patel",
            "phone": "7000334455",
            "email": "amit.patel@genericmeds.com",
            "address": "Bommasandra Industrial Area, Bengaluru",
            "created_at": "2023-04-05T09:00:00Z"
        }
    },
    {
        "model": "pharmacy.supplier",
        "pk": 4,
        "fields": {
            "name": "Wellness Healthcare Ltd",
            "contact_person": "Deepika Rao",
            "phone": "6000445566",
            "email": "deepika.rao@wellnesshc.com",
            "address": "Electronic City, Bengaluru",
            "created_at": "2023-05-15T13:20:00Z"
        }
    },
    {
        "model": "pharmacy.supplier",
        "pk": 5,
        "fields": {
            "name": "AyurHome Remedies",
            "contact_person": "Kumar Swamy",
            "phone": "9500556677",
            "email": "kumar.swamy@ayurhome.com",
            "address": "Jayanagar, Bengaluru",
            "created_at": "2023-07-01T16:55:00Z"
        }
    }
]

product_data = [
    {
        "model": "pharmacy.product",
        "pk": 1,
        "fields": {
            "name": "Paracetamol 500mg",
            "category": "Pain Relief",
            "manufacturer": "Cipla",
            "batch_number": "CP500-202412",
            "expiry_date": "2026-12-31",
            "cost_price": "5.00",
            "selling_price": "7.50",
            "stock_quantity": 500,
            "reorder_level": 50
        }
    },
    {
        "model": "pharmacy.product",
        "pk": 2,
        "fields": {
            "name": "Amoxicillin 250mg",
            "category": "Antibiotics",
            "manufacturer": "Sun Pharma",
            "batch_number": "AMX250-202411",
            "expiry_date": "2025-11-30",
            "cost_price": "12.00",
            "selling_price": "18.00",
            "stock_quantity": 250,
            "reorder_level": 30
        }
    },
    {
        "model": "pharmacy.product",
        "pk": 3,
        "fields": {
            "name": "Cetirizine 10mg",
            "category": "Antihistamines",
            "manufacturer": "Dr. Reddy's",
            "batch_number": "CTR10-202501",
            "expiry_date": "2027-01-15",
            "cost_price": "8.00",
            "selling_price": "12.00",
            "stock_quantity": 300,
            "reorder_level": 40
        }
    },
    {
        "model": "pharmacy.product",
        "pk": 4,
        "fields": {
            "name": "Vitamin D3 60000 IU",
            "category": "Vitamins & Supplements",
            "manufacturer": "Abbott",
            "batch_number": "VITD3-60K-202410",
            "expiry_date": "2026-10-31",
            "cost_price": "25.00",
            "selling_price": "35.00",
            "stock_quantity": 200,
            "reorder_level": 25
        }
    },
    {
        "model": "pharmacy.product",
        "pk": 5,
        "fields": {
            "name": "Ibuprofen 400mg",
            "category": "Pain Relief",
            "manufacturer": "Mankind Pharma",
            "batch_number": "IBU400-202502",
            "expiry_date": "2027-02-28",
            "cost_price": "6.50",
            "selling_price": "9.50",
            "stock_quantity": 450,
            "reorder_level": 60
        }
    },
    {
        "model": "pharmacy.product",
        "pk": 6,
        "fields": {
            "name": "Ranitidine 150mg",
            "category": "Gastrointestinal",
            "manufacturer": "Zydus Cadila",
            "batch_number": "RNT150-202409",
            "expiry_date": "2025-09-30",
            "cost_price": "9.00",
            "selling_price": "13.50",
            "stock_quantity": 180,
            "reorder_level": 20
        }
    },
    {
        "model": "pharmacy.product",
        "pk": 7,
        "fields": {
            "name": "Aspirin 75mg",
            "category": "Cardiovascular",
            "manufacturer": "Bayer",
            "batch_number": "ASP75-202412",
            "expiry_date": "2026-12-15",
            "cost_price": "7.00",
            "selling_price": "10.50",
            "stock_quantity": 320,
            "reorder_level": 45
        }
    },
    {
        "model": "pharmacy.product",
        "pk": 8,
        "fields": {
            "name": "Loratadine 10mg",
            "category": "Antihistamines",
            "manufacturer": "Glenmark",
            "batch_number": "LRT10-202501",
            "expiry_date": "2027-01-31",
            "cost_price": "7.50",
            "selling_price": "11.00",
            "stock_quantity": 280,
            "reorder_level": 35
        }
    },
    {
        "model": "pharmacy.product",
        "pk": 9,
        "fields": {
            "name": "Omeprazole 20mg",
            "category": "Gastrointestinal",
            "manufacturer": "Torrent Pharma",
            "batch_number": "OMP20-202411",
            "expiry_date": "2026-11-30",
            "cost_price": "8.50",
            "selling_price": "12.50",
            "stock_quantity": 220,
            "reorder_level": 30
        }
    },
    {
        "model": "pharmacy.product",
        "pk": 10,
        "fields": {
            "name": "Multivitamin Tablets",
            "category": "Vitamins & Supplements",
            "manufacturer": "Pfizer",
            "batch_number": "MTV-202502",
            "expiry_date": "2027-02-15",
            "cost_price": "30.00",
            "selling_price": "45.00",
            "stock_quantity": 150,
            "reorder_level": 20
        }
    },
    {
        "model": "pharmacy.product",
        "pk": 11,
        "fields": {
            "name": "Hand Sanitizer 50ml",
            "category": "Personal Care",
            "manufacturer": "Himalaya",
            "batch_number": "HS50-202412",
            "expiry_date": "2026-12-31",
            "cost_price": "15.00",
            "selling_price": "22.50",
            "stock_quantity": 600,
            "reorder_level": 100
        }
    },
    {
        "model": "pharmacy.product",
        "pk": 12,
        "fields": {
            "name": "Face Mask (Pack of 5)",
            "category": "Personal Care",
            "manufacturer": "Dettol",
            "batch_number": "FM5-202501",
            "expiry_date": "2027-01-31",
            "cost_price": "20.00",
            "selling_price": "30.00",
            "stock_quantity": 400,
            "reorder_level": 80
        }
    },
    {
        "model": "pharmacy.product",
        "pk": 13,
        "fields": {
            "name": "Glucose Meter",
            "category": "Health Devices",
            "manufacturer": "Accu-Chek",
            "batch_number": "GLUCO-202411",
            "expiry_date": None,
            "cost_price": "800.00",
            "selling_price": "1200.00",
            "stock_quantity": 50,
            "reorder_level": 10
        }
    },
    {
        "model": "pharmacy.product",
        "pk": 14,
        "fields": {
            "name": "Blood Pressure Monitor",
            "category": "Health Devices",
            "manufacturer": "Omron",
            "batch_number": "BPM-202412",
            "expiry_date": None,
            "cost_price": "1200.00",
            "selling_price": "1800.00",
            "stock_quantity": 30,
            "reorder_level": 5
        }
    },
    {
        "model": "pharmacy.product",
        "pk": 15,
        "fields": {
            "name": "Ayurvedic Cough Syrup",
            "category": "Ayurvedic Remedies",
            "manufacturer": "Dabur",
            "batch_number": "AYURCOUGH-202410",
            "expiry_date": "2026-10-31",
            "cost_price": "45.00",
            "selling_price": "65.00",
            "stock_quantity": 120,
            "reorder_level": 15
        }
    },
    {
        "model": "pharmacy.product",
        "pk": 16,
        "fields": {
            "name": "Homeopathic Arnica Cream",
            "category": "Homeopathic Remedies",
            "manufacturer": "Schwabe",
            "batch_number": "ARNICA-202501",
            "expiry_date": "2027-01-31",
            "cost_price": "60.00",
            "selling_price": "90.00",
            "stock_quantity": 90,
            "reorder_level": 10
        }
    },
    {
        "model": "pharmacy.product",
        "pk": 17,
        "fields": {
            "name": "Baby Diapers (Small)",
            "category": "Baby Care",
            "manufacturer": "Pampers",
            "batch_number": "DIAPER-S-202412",
            "expiry_date": "2026-12-31",
            "cost_price": "300.00",
            "selling_price": "450.00",
            "stock_quantity": 180,
            "reorder_level": 30
        }
    },
    {
        "model": "pharmacy.product",
        "pk": 18,
        "fields": {
            "name": "Baby Formula (Stage 1)",
            "category": "Baby Care",
            "manufacturer": "Nestle",
            "batch_number": "FORMULA-1-202501",
            "expiry_date": "2026-01-31",
            "cost_price": "500.00",
            "selling_price": "750.00",
            "stock_quantity": 100,
            "reorder_level": 20
        }
    },
    {
        "model": "pharmacy.product",
        "pk": 19,
        "fields": {
            "name": "Senior Citizen Multivitamin",
            "category": "Vitamins & Supplements",
            "manufacturer": "Geriatric Labs",
            "batch_number": "SENIORVIT-202411",
            "expiry_date": "2026-11-30",
            "cost_price": "40.00",
            "selling_price": "60.00",
            "stock_quantity": 80,
            "reorder_level": 15
        }
    },
    {
        "model": "pharmacy.product",
        "pk": 20,
        "fields": {
            "name": "Calcium Supplements",
            "category": "Vitamins & Supplements",
            "manufacturer": "HealthKart",
            "batch_number": "CALCIUM-202502",
            "expiry_date": "2027-02-28",
            "cost_price": "35.00",
            "selling_price": "52.50",
            "stock_quantity": 150,
            "reorder_level": 25
        }
    }
]


def get_supplier_name(supplier_id):
    for supplier in supplier_data:
        if supplier['pk'] == supplier_id:
            return supplier['fields']['name']
    return "Supplier Not Found"

def get_supplier_contact_details(supplier_id):
    for supplier in supplier_data:
        if supplier['pk'] == supplier_id:
            fields = supplier['fields']
            return f"{fields['contact_person']}\n{fields['address']}\nPhone: {fields['phone']}\nEmail: {fields['email']}"
    return "Contact Details Not Found"

def get_product_name(product_id):
    for product in product_data:
        if product['pk'] == product_id:
            return product['fields']['name']
    return "Product Not Found"


def generate_purchase_invoice(purchase, purchase_details):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)

    # Pharmacy Header
    pdf.cell(0, 10, "MediCure Pharmacy", 0, 1, "C")
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, "Purchase Invoice", 0, 1, "C")

    # Invoice Details
    pdf.ln(10)
    pdf.cell(30, 8, "Invoice No:", 0)
    pdf.cell(50, 8, f"INV-PUR-{purchase['pk']}-{datetime.now().strftime('%Y%m%d')}", 0)
    pdf.cell(30, 8, "Date:", 0)
    pdf.cell(0, 8, purchase['fields']['purchase_date'].split('T')[0], 0, 1)

    pdf.cell(30, 8, "Supplier:", 0)
    supplier_name = get_supplier_name(purchase['fields']['supplier'])
    pdf.cell(0, 8, supplier_name, 0, 1)

    pdf.cell(30, 8, "Payment Mode:", 0)
    pdf.cell(0, 8, purchase['fields']['payment_mode'], 0, 1)

    pdf.ln(10)

    # Supplier Contact Details Box
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Supplier Contact Information", 0, 1)
    pdf.set_font("Arial", "", 10)
    supplier_contact = get_supplier_contact_details(purchase['fields']['supplier'])
    pdf.multi_cell(0, 5, supplier_contact, border=1) # Added border for box effect
    pdf.ln(5)


    # Product Details Table Header
    pdf.set_font("Arial", "B", 12)
    pdf.cell(90, 8, "Product Name", 1)
    pdf.cell(30, 8, "Quantity", 1)
    pdf.cell(30, 8, "Cost Price", 1)
    pdf.cell(40, 8, "Subtotal", 1, 1)

    pdf.set_font("Arial", "", 10)
    for detail in purchase_details:
        product_name = get_product_name(detail['fields']['product'])
        pdf.cell(90, 8, product_name, 1)
        pdf.cell(30, 8, str(detail['fields']['quantity']), 1)
        pdf.cell(30, 8, str(detail['fields']['cost_price']), 1)
        pdf.cell(40, 8, str(detail['fields']['subtotal']), 1, 1)

    # Total
    pdf.set_font("Arial", "B", 12)
    pdf.cell(150, 8, "Total Cost", 1, 0, 'R')
    pdf.cell(40, 8, str(purchase['fields']['total_cost']), 1, 1)

    pdf.output(f"purchase_invoice_{purchase['pk']}.pdf", "F")
    print(f"Invoice purchase_invoice_{purchase['pk']}.pdf generated")


# --- Main Invoice Generation ---
if __name__ == '__main__':
    # Load your JSON data (replace with your file loading if needed)
    purchases = purchase_data
    purchase_details = purchase_detail_data


    # Group purchase details by purchase ID
    purchase_details_by_purchase = {}
    for detail in purchase_details:
        purchase_id = detail['fields']['purchase']
        if purchase_id not in purchase_details_by_purchase:
            purchase_details_by_purchase[purchase_id] = []
        purchase_details_by_purchase[purchase_id].append(detail)


    for purchase in purchases:
        purchase_id = purchase['pk']
        details_for_purchase = purchase_details_by_purchase.get(purchase_id, [])
        generate_purchase_invoice(purchase, details_for_purchase)

    print("All purchase invoices generated!")
