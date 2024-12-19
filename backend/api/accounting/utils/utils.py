from langchain_google_genai import ChatGoogleGenerativeAI
from typing import List
from pydantic import BaseModel, Field
from datetime import datetime
from langchain.schema.messages import HumanMessage, AIMessage
import base64
from PIL import Image


class PurchaseDetail(BaseModel):
    product_name: str = Field(..., description="Name of the purchased product")
    quantity: int = Field(..., description="Quantity of the product purchased")
    cost_price: float = Field(..., description="Cost price of the product")
    subtotal: float = Field(..., description="Subtotal cost for this product")


class Purchase(BaseModel):
    purchase_date: datetime = Field(..., description="Date and time of the purchase")
    supplier_name: str = Field(..., description="Name of the supplier")
    total_cost: float = Field(..., description="Total cost of the purchase")
    payment_mode: str = Field(..., description="Mode of payment used", max_length=15)
    purchase_details: List[PurchaseDetail] = Field(
        ..., description="List of detailed purchase information"
    )


class StructuredDataExtractor:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def _encode_image(self):
        with Image.open(self.file_path) as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def extract(self):
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
        )

        try:
            # Prepare the image
            image_part = self._encode_image()

            messages = [
                AIMessage(content="""
                You are an intelligent assistant trained to analyze invoice images.
                Extract the information and provide output in this exact JSON format:
                {
                    "purchase_date": "YYYY-MM-DD HH:MM:SS",
                    "supplier_name": "string",
                    "total_cost": number,
                    "payment_mode": "string (max 15 chars)",
                    "purchase_details": [
                        {
                            "product_name": "string",
                            "quantity": integer,
                            "cost_price": number,
                            "subtotal": number
                        }
                    ]
                }
                Important rules:
                - purchase_date must be in ISO format (YYYY-MM-DD HH:MM:SS)
                - payment_mode must not exceed 15 characters
                - subtotal for each item should be quantity * cost_price
                - total_cost should equal the sum of all subtotals

                Only return valid JSON. Do not include any explanatory text.
                """),
                HumanMessage(
                    content=[
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_part}"
                            },
                        },
                    ]
                )
            ]

            # Get JSON response
            json_response = llm.invoke(messages)

            # Parse into Pydantic model
            structured_data = Purchase.model_validate_json(json_response.content)

            # Validate business rules
            self._validate_business_rules(structured_data)

            return structured_data

        except Exception as e:
            print(f"Error processing image: {str(e)}")
            return None

    def _validate_business_rules(self, data: Purchase):
        """Validate business rules for the extracted data"""
        for detail in data.purchase_details:
            expected_subtotal = detail.quantity * detail.cost_price
            if abs(detail.subtotal - expected_subtotal) > 0.01:
                raise ValueError(
                    f"Subtotal mismatch for {detail.product_name}: "
                    f"Expected {expected_subtotal}, got {detail.subtotal}"
                )

        expected_total = sum(detail.subtotal for detail in data.purchase_details)
        if abs(data.total_cost - expected_total) > 0.01:
            raise ValueError(
                f"Total cost mismatch: Expected {expected_total}, got {data.total_cost}"
            )
