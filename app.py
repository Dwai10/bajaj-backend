from flask import Flask, request, jsonify
from collections import OrderedDict
import re

app = Flask(__name__)

# Utility function to validate and process the data
def process_request_data(data):
    if not isinstance(data, list):
        raise ValueError("The 'data' field must be an array.")
    
    numbers = []
    alphabets = []
    for item in data:
        if isinstance(item, str):
            if item.isdigit():
                numbers.append(item)
            elif re.match("^[a-zA-Z]$", item):
                alphabets.append(item)
            else:
                raise ValueError(f"Invalid character in array: {item}")
        else:
            raise ValueError(f"Invalid item type in array: {item} (Only strings allowed)")
    
    # Find the highest lowercase alphabet
    lowercase_alphabets = [char for char in alphabets if char.islower()]
    highest_lowercase_alphabet = max(lowercase_alphabets) if lowercase_alphabets else ""

    return numbers, alphabets, highest_lowercase_alphabet

@app.route('/bfhl', methods=['GET'])
def get_operation_code():
    return jsonify({"operation_code": 1}), 200

@app.route('/bfhl', methods=['POST'])
def process_data():
    try:
        json_data = request.get_json()
        if 'data' not in json_data:
            raise ValueError("Missing 'data' field in the request JSON.")
        
        data = json_data['data']

        numbers, alphabets, highest_lowercase_alphabet = process_request_data(data)

        response = OrderedDict([
            ("is_success", True),
            ("user_id", "john_doe_17091999"),
            ("email", "john.doe@college.edu"),
            ("roll_number", "1234ABCD"),
            ("numbers", numbers),
            ("alphabets", alphabets),
            ("highest_lowercase_alphabet", [highest_lowercase_alphabet] if highest_lowercase_alphabet else [])
        ])
        
        return jsonify(response), 200
    except ValueError as ve:
        return jsonify({"is_success": False, "error": str(ve)}), 400
    except Exception as e:
        return jsonify({"is_success": False, "error": "An unexpected error occurred."}), 500

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=80)
