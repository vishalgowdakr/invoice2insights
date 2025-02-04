from langchain_google_genai import ChatGoogleGenerativeAI
from typing import List
from pydantic import BaseModel, Field
from datetime import datetime
from langchain.schema.messages import HumanMessage, AIMessage
import base64
from PIL import Image
import io
import re


class PurchaseDetail(BaseModel):
    product_name: str = Field(..., description="Name of the purchased product")
    quantity: int = Field(..., description="Quantity of the product purchased")
    cost_price: float = Field(..., description="Cost price of the product")
    subtotal: float = Field(..., description="Subtotal cost for this product")


class Purchase(BaseModel):
    purchase_date: datetime = Field(...,
                                    description="Date and time of the purchase")
    supplier_name: str = Field(..., description="Name of the supplier")
    total_cost: float = Field(..., description="Total cost of the purchase")
    payment_mode: str = Field(...,
                              description="Mode of payment used", max_length=15)
    purchase_details: List[PurchaseDetail] = Field(
        ..., description="List of detailed purchase information"
    )


class StructuredDataExtractor:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def _get_base64_image(self, image_path):
        # Open the image using PIL
        with Image.open(image_path) as img:
            # Create a bytes buffer
            buffer = io.BytesIO()
            # Save the image to the buffer in PNG format
            img.save(buffer, format='PNG')
            # Get the bytes value and encode to base64
            buffer.seek(0)
            image_bytes = buffer.getvalue()
            return base64.b64encode(image_bytes).decode('utf-8')

    def _clean_json_response(self, response: str) -> str:
        """Clean the JSON response by removing markdown code blocks and finding the JSON content"""
        # Remove markdown code blocks if present
        json_content = re.search(
            r'```(?:json)?\s*(.*?)```', response, re.DOTALL)
        if json_content:
            return json_content.group(1).strip()
        return response.strip()

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
            image_part = self._get_base64_image(self.file_path)

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

                Return the JSON without any markdown formatting or explanation.
                """),
                HumanMessage(
                    content=[
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{image_part}"
                            }
                        },
                    ]
                )
            ]

            # Get response and clean it
            response = llm.invoke(messages)
            cleaned_json = self._clean_json_response(response.content)
            print(cleaned_json)

            # Parse into Pydantic model
            structured_data = Purchase.model_validate_json(cleaned_json)
            print(structured_data)

            return structured_data

        except Exception as e:
            print(f"Error processing image: {str(e)}")
            return None
