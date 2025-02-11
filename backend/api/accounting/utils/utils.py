from langchain_google_genai import ChatGoogleGenerativeAI
from typing import List, Optional
from pydantic import BaseModel, Field, computed_field
from datetime import datetime
from langchain.schema.messages import HumanMessage
import base64
from PIL import Image
import io
import re


class PurchaseDetail(BaseModel):
    product_name: str = Field(..., description="Name of the purchased product")
    quantity: int = Field(..., description="Quantity of the product purchased")
    subtotal: float = Field(..., description="Subtotal cost for this product")

    @computed_field
    @property
    def cost_price(self) -> float:
        if self.quantity == 0:
            raise ValueError("Quantity cannot be zero.")
        return self.subtotal / self.quantity


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

    def _get_base64_image(self, image_path):
        with Image.open(image_path) as image:
            buffer = io.BytesIO()
            image.save(buffer, format='PNG')
            image_bytes = buffer.getvalue()
            return base64.b64encode(image_bytes).decode('utf-8')

    def _clean_json_response(self, response: str) -> str:
        json_content = re.search(r'```(?:json)?\s*(.*?)```', response, re.DOTALL)
        return json_content.group(1).strip() if json_content else response.strip()

    def extract(self) -> Optional[Purchase]:
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
        )

        try:
            image_part = self._get_base64_image(self.file_path)

            prompt = """
            Analyze this invoice image and extract the following structured information:
            - Purchase date in ISO format
            - Supplier name
            - Total cost
            - Payment mode (max 15 characters)
            - List of purchase details including:
              * Product name
              * Quantity
              * Subtotal (total cost for this product)

            Ensure all calculations are correct and the total cost matches the sum of subtotals.
            """

            structured_llm = llm.with_structured_output(Purchase)

            messages = [
                HumanMessage(
                    content=[
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/png;base64,{image_part}"},
                        },
                    ]
                )
            ]

            response = structured_llm.invoke(messages)
            return response

        except Exception as e:
            print(f"Error processing image: {str(e)}")
            return None
