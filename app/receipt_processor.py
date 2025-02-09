import math
from datetime import datetime
from app.models import Receipt

class ReceiptProcessor:
    """
    Description: This class is responsible for processing receipts and calculating points based on certain rules.
    """
    def calculate_points(self, receipt: Receipt) -> int:
        """
        Description: Calculates the points for a given receipt based on certain rules.
        Parameters:
            - receipt: The receipt object for which to calculate points.
        """
        points = 0
        
        # Rule 1: One point for every alphanumeric character in the retailer name
        retailer_name_points = sum(c.isalnum() for c in receipt.retailer)
        points += retailer_name_points
        
        # Rule 2: 50 points if the total is a round dollar amount
        total = float(receipt.total)
        if total.is_integer():
            points += 50
            
        # Rule 3: 25 points if the total is a multiple of 0.25
        if total % 0.25 == 0:
            points += 25
            
        # Rule 4: 5 points for every two items
        items_count = len(receipt.items)
        pair_points = (items_count // 2) * 5
        points += pair_points
        
        # Rule 5: Points for items with descriptions of length multiple of 3
        for item in receipt.items:
            description = item.shortDescription.strip()
            if len(description) % 3 == 0:
                item_points = math.ceil(float(item.price) * 0.2)
                points += item_points
                
        # Rule 7: 6 points if the day in the purchase date is odd
        purchaseDate = datetime.strptime(receipt.purchaseDate, '%Y-%m-%d')
        if purchaseDate.day % 2 == 1:
            points += 6
            
        # Rule 8: 10 points if purchase time is between 2:00pm and 4:00pm
        purchaseTime = datetime.strptime(receipt.purchaseTime, '%H:%M')
        if datetime.strptime('14:00', '%H:%M').time() <= purchaseTime.time() <= datetime.strptime('16:00', '%H:%M').time():
            points += 10

        return points