from dataclasses import dataclass
from datetime import datetime
import decimal

class ValidationError(Exception):
    # Custom exception class for validation errors. Passes the error message to the base Exception class
    pass

@dataclass
class Item:
    shortDescription: str
    price: str

    def validate(self) -> bool:
        """
        Validates the item data
        Returns True if valid, raises ValidationError if invalid
        """
        if not self.shortDescription:
            raise ValidationError("Short description cannot be empty")
        
        try:
            # convert price to Decimal to validate it
            price = decimal.Decimal(self.price)
            if price < 0:
                raise ValidationError("Price cannot be negative")
        except (ValueError, TypeError, decimal.InvalidOperation):
            raise ValidationError("Invalid price format")
        
        return True

@dataclass
class Receipt:
    retailer: str
    purchaseDate: str
    purchaseTime: str
    total: str
    items: list[Item]

    def validate(self) -> bool:
        """
        Validates the receipt data
        Returns True if valid, raises ValidationError if invalid
        """
        # Validate retailer
        if not self.retailer or not self.retailer.strip():
            raise ValidationError("Retailer name cannot be empty")

        # Validate purchase date
        try:
            datetime.strptime(self.purchaseDate, "%Y-%m-%d")
        except ValueError:
            raise ValidationError("Invalid purchase date format. Expected YYYY-MM-DD")

        # Validate purchase time
        try:
            datetime.strptime(self.purchaseTime, "%H:%M")
        except ValueError:
            raise ValidationError("Invalid purchase time format. Expected HH:MM")

        # Validate total
        try:
            total = decimal.Decimal(self.total)
            if total < 0:
                raise ValidationError("Total cannot be negative")
        except (ValueError, TypeError):
            raise ValidationError("Invalid total format")

        # Validate items
        if not self.items:
            raise ValidationError("Receipt must have at least one item")

        # Validate each item
        for item in self.items:
            item.validate()
        
        return True

    @classmethod
    def from_dict(cls, data: dict) -> 'Receipt':
        """
        Creates a Receipt instance from a dictionary we get from the JSON input
        Validates the dictionary structure but not the data itself. Data validation is done in the validate method
        """
        if not isinstance(data, dict):
            raise ValidationError("Input must be a dictionary")

        # Check for required fields
        required_fields = {'retailer', 'purchaseDate', 'purchaseTime', 'total', 'items'}
        missing_fields = required_fields - set(data.keys())
        if missing_fields:
            raise ValidationError(f"Missing required fields: {missing_fields}")

        if not isinstance(data['items'], list):
            raise ValidationError("Items must be a list")

        items = [Item(shortDescription=item.get("shortDescription", ""), 
                     price=item.get("price", "")) 
                for item in data['items']]

        return cls(
            retailer=data['retailer'],
            purchaseDate=data['purchaseDate'],
            purchaseTime=data['purchaseTime'],
            total=data['total'],
            items=items
        )