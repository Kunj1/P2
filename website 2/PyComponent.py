import ast
import json

def parse_python_code(code):
    tree = ast.parse(code)
    return tree

def find_parents(tree):
    parents = {}
    functions = {}
    
    class_name = ""
    
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            parents[node.name] = class_name
            functions[node.name] = ast.unparse(node)
        elif isinstance(node, ast.ClassDef):
            class_name = node.name
            for subnode in node.body:
                if isinstance(subnode, ast.FunctionDef):
                    parents[subnode.name] = class_name
                    functions[subnode.name] = ast.unparse(subnode)
                    
    return parents, functions

def analyze_python_code(code):
    tree = parse_python_code(code)
    parents, functions = find_parents(tree)
    
    output_data = {}
    for name, parent in parents.items():
        output_data[name] = {
            "Type": 'Function' if parent else 'Class',
            "Parent": parent,
            "Contents": functions[name]
        }
    
    return json.dumps(output_data, indent=4)