import ast
from typing import Optional


class ParseResult:
    def __init__(self, success: bool, tree: Optional[ast.AST] = None, error: Optional[str] = None):
        self.success = success
        self.tree = tree
        self.error = error


def parse_python_code(code: str) -> ParseResult:
    """
    Attempts to parse Python source code into an AST.
    Returns a ParseResult indicating success/failure — never raises.
    """
    try:
        tree = ast.parse(code)
        return ParseResult(success=True, tree=tree)
    except SyntaxError as e:
        return ParseResult(success=False, error=f"SyntaxError: {e.msg} at line {e.lineno}")
    except Exception as e:
        return ParseResult(success=False, error=f"ParseError: {str(e)}")


def get_node_counts(tree: ast.AST) -> dict:
    """
    Quick sanity-check utility: counts occurrences of each AST node type.
    Useful for debugging and for early feature ideas in Step 12.
    """
    counts = {}
    for node in ast.walk(tree):
        node_type = type(node).__name__
        counts[node_type] = counts.get(node_type, 0) + 1
    return counts