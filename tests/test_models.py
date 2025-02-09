import unittest
from app.models import Receipt, Item, ValidationError

class TestItemValidation(unittest.TestCase):
    """
    Description: Test cases for Item validation
    """
    def test_valid_item(self):
        """Description: Test valid item passes validation"""
        item = Item(shortDescription="Mountain Dew 12PK", price="6.49")
        self.assertTrue(item.validate())

    def test_empty_description(self):
        """Description: Test description cannot be empty"""
        item = Item(shortDescription="", price="6.49")
        with self.assertRaises(ValidationError) as context:
            item.validate()
        self.assertEqual(str(context.exception), "Short description cannot be empty")

    def test_invalid_price(self):
        """Description: Test price must be a valid number"""
        item = Item(shortDescription="Test Item", price="invalid")
        with self.assertRaises(ValidationError) as context:
            item.validate()
        self.assertEqual(str(context.exception), "Invalid price format")

    def test_negative_price(self):
        """Description: Test price cannot be negative"""
        item = Item(shortDescription="Test Item", price="-1.00")
        with self.assertRaises(ValidationError) as context:
            item.validate()
        self.assertEqual(str(context.exception), "Price cannot be negative")

class TestReceiptValidation(unittest.TestCase):
    """
    Description: Test cases for Receipt validation
    """
    def setUp(self):
        self.valid_item = Item(
            shortDescription="Mountain Dew 12PK",
            price="6.49"
        )
        self.valid_receipt = Receipt(
            retailer="Target",
            purchaseDate="2022-01-01",
            purchaseTime="13:01",
            total="6.49",
            items=[self.valid_item]
        )

    def test_valid_receipt(self):
        """Description: Test valid receipt passes validation"""
        self.assertTrue(self.valid_receipt.validate())

    def test_invalid_date_format(self):
        """Description: Test date format must be YYYY-MM-DD"""
        receipt = Receipt(
            retailer="Target",
            purchaseDate="01-01-2022",  # invalid format
            purchaseTime="13:01",
            total="6.49",
            items=[self.valid_item]
        )
        with self.assertRaises(ValidationError) as context:
            receipt.validate()
        self.assertTrue("Invalid purchase date format" in str(context.exception))

    def test_invalid_time_format(self):
        """Description: Test time format must be HH:MM"""
        receipt = Receipt(
            retailer="Target",
            purchaseDate="2022-01-01",
            purchaseTime="1:01 PM",  # invalid format
            total="6.49",
            items=[self.valid_item]
        )
        with self.assertRaises(ValidationError) as context:
            receipt.validate()
        self.assertTrue("Invalid purchase time format" in str(context.exception))

class TestReceiptFromDict(unittest.TestCase):
    """
    Description: Test cases for creating Receipt from dictionary
    """
    def setUp(self):
        self.valid_receipt_data = {
            "retailer": "Target",
            "purchaseDate": "2022-01-01",
            "purchaseTime": "13:01",
            "items": [
                {
                    "shortDescription": "Mountain Dew 12PK",
                    "price": "6.49"
                }
            ],
            "total": "6.49"
        }

    def test_valid_dict(self):
        """Description: Test valid dictionary creates receipt"""
        receipt = Receipt.from_dict(self.valid_receipt_data)
        self.assertIsInstance(receipt, Receipt)
        self.assertEqual(receipt.retailer, "Target")

    def test_missing_fields(self):
        """Description: Test missing required fields raises error"""
        invalid_data = {
            "retailer": "Target",
            "purchaseDate": "2022-01-01"
        }
        with self.assertRaises(ValidationError) as context:
            Receipt.from_dict(invalid_data)
        self.assertTrue("Missing required fields" in str(context.exception))

    def test_invalid_items_format(self):
        """Description: Test items must be a list"""
        self.valid_receipt_data["items"] = "not a list"
        with self.assertRaises(ValidationError) as context:
            Receipt.from_dict(self.valid_receipt_data)
        self.assertEqual(str(context.exception), "Items must be a list")

if __name__ == '__main__':
    unittest.main()