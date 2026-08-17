import ast
import re
from collections import Counter


def extract_lexical_features(code: str, tree: ast.AST) -> dict:
    lines = code.split("\n")
    total_lines = len(lines)
    comment_lines = sum(1 for line in lines if line.strip().startswith("#"))

    keyword_counts = Counter()
    for node in ast.walk(tree):
        keyword_counts[type(node).__name__] += 1

    return {
        "token_count": sum(keyword_counts.values()),
        "comment_ratio": round(comment_lines / total_lines, 4) if total_lines else 0.0,
        "if_count": keyword_counts.get("If", 0),
        "for_count": keyword_counts.get("For", 0),
        "while_count": keyword_counts.get("While", 0),
        "def_count": keyword_counts.get("FunctionDef", 0),
    }


def extract_stylometric_features(tree: ast.AST) -> dict:
    identifiers = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.arg)):
            identifiers.append(node.name if hasattr(node, "name") else node.arg)
        elif isinstance(node, ast.Name):
            identifiers.append(node.id)

    if not identifiers:
        return {"snake_case_ratio": 0.0, "camel_case_ratio": 0.0, "avg_identifier_length": 0.0}

    snake_case = sum(1 for i in identifiers if re.fullmatch(r"[a-z_][a-z0-9_]*", i) and "_" in i)
    camel_case = sum(1 for i in identifiers if re.fullmatch(r"[a-z][a-zA-Z0-9]*", i) and any(c.isupper() for c in i))

    return {
        "snake_case_ratio": round(snake_case / len(identifiers), 4),
        "camel_case_ratio": round(camel_case / len(identifiers), 4),
        "avg_identifier_length": round(sum(len(i) for i in identifiers) / len(identifiers), 2),
    }


def extract_structural_features(tree: ast.AST) -> dict:
    function_count = sum(1 for n in ast.walk(tree) if isinstance(n, ast.FunctionDef))
    class_count = sum(1 for n in ast.walk(tree) if isinstance(n, ast.ClassDef))
    loop_count = sum(1 for n in ast.walk(tree) if isinstance(n, (ast.For, ast.While)))
    conditional_count = sum(1 for n in ast.walk(tree) if isinstance(n, ast.If))

    return {
        "function_count": function_count,
        "class_count": class_count,
        "loop_count": loop_count,
        "conditional_count": conditional_count,
        "max_nesting_depth": _max_nesting_depth(tree),
    }


def _max_nesting_depth(tree: ast.AST) -> int:
    def depth(node, current=0):
        max_depth = current
        nestable = (ast.If, ast.For, ast.While, ast.FunctionDef, ast.ClassDef, ast.Try, ast.With)
        for child in ast.iter_child_nodes(node):
            child_depth = depth(child, current + 1) if isinstance(child, nestable) else depth(child, current)
            max_depth = max(max_depth, child_depth)
        return max_depth
    return depth(tree)


def extract_complexity_features(code: str, tree: ast.AST) -> dict:
    lines = [l for l in code.split("\n") if l.strip() and not l.strip().startswith("#")]
    loc = len(lines)

    function_count = sum(1 for n in ast.walk(tree) if isinstance(n, ast.FunctionDef))
    decision_points = sum(
        1 for n in ast.walk(tree)
        if isinstance(n, (ast.If, ast.For, ast.While, ast.BoolOp, ast.ExceptHandler))
    )
    cyclomatic_complexity = 1 + decision_points

    return {
        "loc": loc,
        "cyclomatic_complexity": cyclomatic_complexity,
        "avg_function_length": round(loc / function_count, 2) if function_count else float(loc),
    }


def extract_all_features(code: str, tree: ast.AST) -> dict:
    return {
        "lexical": extract_lexical_features(code, tree),
        "stylometric": extract_stylometric_features(tree),
        "structural": extract_structural_features(tree),
        "complexity": extract_complexity_features(code, tree),
    }