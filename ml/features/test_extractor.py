import sys
sys.path.append("..")
from parsing.python_parser import parse_python_code
from extractor import extract_all_features
import json

sample_code = """
def calculate_total(items):
    total = 0
    for item in items:
        if item > 0:
            total += item
    return total

class ShoppingCart:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)
"""

result = parse_python_code(sample_code)
if result.success:
    features = extract_all_features(sample_code, result.tree)
    print(json.dumps(features, indent=2))
else:
    print("Parse failed:", result.error)