from python_parser import parse_python_code, get_node_counts

sample_code = """
def add(a, b):
    return a + b

class Calculator:
    def multiply(self, x, y):
        result = x * y
        return result
"""

result = parse_python_code(sample_code)

if result.success:
    print("Parse succeeded!")
    print(get_node_counts(result.tree))
else:
    print("Parse failed:", result.error)

print("\n--- Testing broken code ---")
broken_result = parse_python_code("def add(a, b:\n    return a + b")
print("Success:", broken_result.success)
print("Error:", broken_result.error)