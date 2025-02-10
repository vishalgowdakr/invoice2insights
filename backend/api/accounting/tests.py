import unittest
from datetime import date
from accounting.utils.utils import StructuredDataExtractor, Purchase # Assuming your script is named as such
import io
import sys

class TestStructuredDataExtractorHappyPath(unittest.TestCase):

    def setUp(self):
        # Assuming "valid_invoice_image.png" exists in the "invoices" directory
        # and represents a valid invoice for happy path testing.
        self.extractor = StructuredDataExtractor("invoices/Screenshot_from_2024-12-20_01-22-09_Nkvqq1h.png")

    def test_output_capture_example(self): # Renamed to avoid confusion with captureOutput
        with self.assertLogs() as captured: # Note: assertLogs is for logging module, not general output
            print("This is standard output example")
            sys.stderr.write("This is standard error example\n") # Another way to write to stderr

        # Access captured output
        output = captured.output # List of strings, each line of output
        print("Captured Output (example):", output) # Print to *your* test's output, not the captured output

        # Assertions based on captured output (example)
        self.assertIn("standard output example", "".join(captured.output)) # Join lines for easier searching
        self.assertIn("standard error example", "".join(captured.output))

    def test_extract_valid_invoice_happy_path_capture_output(self): # More descriptive name
        with io.StringIO() as captured_output: # Use StringIO to capture print output
            original_stdout = sys.stdout
            sys.stdout = captured_output
            try:
                purchase = self.extractor.extract()
                print(purchase) # This print will be captured
            finally:
                sys.stdout = original_stdout # Restore stdout

        captured_purchase_output = captured_output.getvalue()
        print("Captured Purchase Output:\n", captured_purchase_output) # Print the captured output for inspection

        self.assertIsInstance(purchase, Purchase)  # Check if it's a Purchase object

        # Assert specific extracted values for the happy path scenario
        self.assertEqual(purchase.invoice_date, date(2024, 12, 20)) # Example date, adjust as needed
        self.assertEqual(purchase.supplier_name, "Butler-Logan") # Example supplier, adjust as needed
        self.assertEqual(purchase.total_amount, 1144.60) # Example amount, adjust as needed
        self.assertEqual(purchase.payment_term, "online") # Example payment term, adjust as needed
        self.assertEqual(purchase.invoice_number, "#1") # Example invoice number, adjust as needed
        self.assertEqual(purchase.due_date, date(2024, 12, 24)) # Example due date, adjust as needed

        self.assertEqual(len(purchase.purchase_details), 2)  # Example item count, adjust as needed

        # Check the first item - adjust product names, quantities, prices as needed for happy path
        self.assertEqual(purchase.purchase_details[0].product_name, "necessary")
        self.assertEqual(purchase.purchase_details[0].quantity, 3)
        self.assertEqual(purchase.purchase_details[0].cost_price, 100.00)
        self.assertEqual(purchase.purchase_details[0].subtotal, 300.00)

        # Check the second item - adjust product names, quantities, prices as needed for happy path
        self.assertEqual(purchase.purchase_details[1].product_name, "attorney")
        self.assertEqual(purchase.purchase_details[1].quantity, 5)
        self.assertEqual(purchase.purchase_details[1].cost_price, 134.00)
        self.assertEqual(purchase.purchase_details[1].subtotal, 670.00)


if __name__ == '__main__':
    unittest.main()
