from flask import Flask, request, jsonify
import hashlib
import json
from app.receipt_processor import ReceiptProcessor
from app.models import Receipt

app = Flask(__name__)
# In-memory storage for receipts. We are using a simple dictionary for this example since we are storing just the receipt_id and its associated points
# but if the complexity of the application increases, we can use a database to store and retrieve the data.
receipts = {}  

@app.route('/receipts/process', methods=['POST'])
def process_receipt():
    """
    Description: This function is responsible for processing a receipt and storing the points.
    """
    try:
        receipt_data = request.get_json()
        if not receipt_data:
            return jsonify({"error": "Invalid receipt data"}), 400

        # Parse the receipt data
        try:
            receipt = Receipt.from_dict(receipt_data)
        except (KeyError, TypeError) as e:
            return jsonify({"error": "404 NOT FOUND\n invalid JSON"}), 404
            
        # Generate a SHA256 hash of the receipt JSON as Receipt ID https://www.geeksforgeeks.org/sha-in-python/ (can also use UUID for this. But SHA256 is more secure)
        receipt_json = json.dumps(receipt_data, sort_keys=True).encode()
        receipt_id = hashlib.sha256(receipt_json).hexdigest()
        
        # Process the receipt and store points
        processor = ReceiptProcessor()
        points = processor.calculate_points(receipt)
        receipts[receipt_id] = points

        return jsonify({"id": receipt_id}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/receipts/<id>/points', methods=['GET'])
def get_points(id):
    """
    Description: This function is responsible for returning the points for a given receipt ID.
    Parameters: id - The ID of the receipt for which to retrieve the points.
    """
    # Validate path structure
    path_parts = request.path.split('/')
    if len(path_parts) != 4 or path_parts[1] != 'receipts' or path_parts[3] != 'points':
        return jsonify({"error": "404 NOT FOUND"}), 404
        
    points = receipts.get(id)
    if points is None:
        return jsonify({"error": "404 NOT FOUND"}), 404
    return jsonify({"points": points}), 200

if __name__ == '__main__':
    print("Listening on port 8080...")
    app.run(host='0.0.0.0', port=8080)

