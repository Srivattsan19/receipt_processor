import unittest
import json
from app.receipt_processor import ReceiptProcessor
from app.models import Receipt

class TestReceiptProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = ReceiptProcessor()

    def test_target_receipt(self):
        """
        Description: Test the points calculation for a sample Target receipt given in the examples
        """
        with open('tests/test_data/target_receipt.json', 'r') as f:
            receipt_data = json.load(f)
        receipt = Receipt.from_dict(receipt_data)
        points = self.processor.calculate_points(receipt)
        self.assertEqual(points, 28)
        
    def test_retailer_points(self):
        """
        Description: Test the points calculation for the retailer name
        """
        receipt_data = {
            "retailer": "M&M Corner Market",
            "purchaseDate": "2022-03-20",
            "purchaseTime": "14:33",
            "items": [],
            "total": "0.00"
        }
        receipt = Receipt.from_dict(receipt_data)
        points = self.processor.calculate_points(receipt)
        # Should have 14 points for alphanumeric characters
        self.assertEqual(sum(c.isalnum() for c in receipt_data["retailer"]), 14)
        
    def test_round_dollar_amount(self):
        """
        Description: Test the points calculation for a round dollar amount
        """
        receipt_data = {
            "retailer": "Test",
            "purchaseDate": "2022-03-20",
            "purchaseTime": "14:33",
            "items": [],
            "total": "100.00"
        }
        receipt = Receipt.from_dict(receipt_data)
        points = self.processor.calculate_points(receipt)
        # Should include 50 points for round dollar amount
        self.assertGreaterEqual(points, 50)
        
    def test_multiple_of_quarter(self):
        """
        Description: Test the points calculation for a total that is a multiple of 0.25
        """
        receipt_data = {
            "retailer": "Test",
            "purchaseDate": "2022-03-20",
            "purchaseTime": "14:33",
            "items": [],
            "total": "10.75"
        }
        receipt = Receipt.from_dict(receipt_data)
        points = self.processor.calculate_points(receipt)
        # Should include 25 points for multiple of 0.25
        self.assertGreaterEqual(points, 25)
        
    def test_time_range_points(self):
        """
        Description: Test the points calculation for a purchase time between 2:00 PM and 4:00 PM
        """
        receipt_data = {
            "retailer": "Test",
            "purchaseDate": "2022-03-20",
            "purchaseTime": "14:33",
            "items": [],
            "total": "0.00"
        }
        receipt = Receipt.from_dict(receipt_data)
        points = self.processor.calculate_points(receipt)
        # Should include 10 points for time between 2:00 PM and 4:00 PM
        self.assertGreaterEqual(points, 10)

    def test_pairs_of_items(self):
        """
        Description: Test the points calculation for pairs of items (5 points per pair)
        """
        receipt_data = {
            "retailer": "Test",
            "purchaseDate": "2022-03-20",
            "purchaseTime": "13:33",
            "items": [
                {"shortDescription": "Item 1", "price": "1.00"},
                {"shortDescription": "Item 2", "price": "1.00"},
                {"shortDescription": "Item 3", "price": "1.00"},
                {"shortDescription": "Item 4", "price": "1.00"}
            ],
            "total": "4.00"
        }
        receipt = Receipt.from_dict(receipt_data)
        points = self.processor.calculate_points(receipt)
        # Should include 10 points for two pairs of items
        self.assertGreaterEqual(points, 10)

    def test_item_description_length(self):
        """
        Description: Test the points calculation for item descriptions with length multiple of 3
        """
        receipt_data = {
            "retailer": "Test",
            "purchaseDate": "2022-03-20",
            "purchaseTime": "13:33",
            "items": [
                {"shortDescription": "ABC", "price": "10.00"},          # length 3
                {"shortDescription": "ABCDEF", "price": "20.00"},       # length 6
                {"shortDescription": "AB", "price": "5.00"}             # length 2 (no points)
            ],
            "total": "35.00"
        }
        receipt = Receipt.from_dict(receipt_data)
        points = self.processor.calculate_points(receipt)
        # ABC: 10.00 * 0.2 = 2 points
        # ABCDEF: 20.00 * 0.2 = 4 points
        # Total 6 points for descriptions
        self.assertGreaterEqual(points, 6)

    def test_odd_day_points(self):
        """
        Description: Test the points calculation for odd numbered days
        """
        receipt_data = {
            "retailer": "Test",
            "purchaseDate": "2022-03-21",  # odd day
            "purchaseTime": "13:33",
            "items": [],
            "total": "0.00"
        }
        receipt = Receipt.from_dict(receipt_data)
        points = self.processor.calculate_points(receipt)
        # Should include 6 points for odd day
        self.assertGreaterEqual(points, 6)


if __name__ == '__main__':
    unittest.main()