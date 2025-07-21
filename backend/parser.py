import ast
import logging
from typing import Dict, List, Set, Tuple

logger = logging.getLogger(__name__)

def extract_functions_and_calls(code_str: str) -> Dict[str, List]:
    """
    Parse Python code and extract function definitions, calls, and source code.
    
    Args:
        code_str (str): Python source code as string
        
    Returns:
        Dict containing:
            - functions: List of function names defined in the code
            - calls: List of function call relationships
            - code: Dictionary mapping function names to their source code
    """
    
    try:
        # Parse the code string into an AST (Abstract Syntax Tree)
        tree = ast.parse(code_str)
        
        # Initialize containers
        functions: Set[str] = set()
        calls: List[Dict[str, str]] = []
        code_snippets: Dict[str, str] = {}
        
        # Traverse the AST to find function definitions and calls
        for node in ast.walk(tree):
            # Find function definitions
            if isinstance(node, ast.FunctionDef):
                function_name = node.name
                functions.add(function_name)
                logger.info(f"Found function definition: {function_name}")
                
                # Extract the source code for this function
                function_source = ast.get_source_segment(code_str, node)
                if function_source:
                    code_snippets[function_name] = function_source
                    logger.debug(f"Extracted source for {function_name}: {len(function_source)} chars")
                
                # Look for function calls within this function
                function_calls = _extract_calls_from_function(node)
                for callee in function_calls:
                    calls.append({
                        "caller": function_name,
                        "callee": callee
                    })
        
        logger.info(f"Extracted {len(functions)} functions and {len(calls)} calls")
        
        return {
            "functions": list(functions),
            "calls": calls,
            "code": code_snippets
        }
        
    except SyntaxError as e:
        logger.error(f"Syntax error in code: {e}")
        return {"functions": [], "calls": [], "code": {}}
    except Exception as e:
        logger.error(f"Error parsing code: {e}")
        return {"functions": [], "calls": [], "code": {}}

def _extract_calls_from_function(function_node: ast.FunctionDef) -> Set[str]:
    """
    Extract function calls from within a function definition.
    
    Args:
        function_node (ast.FunctionDef): AST node representing a function
        
    Returns:
        Set of function names that are called within this function
    """
    calls: Set[str] = set()
    
    # Recursively search for function calls in the function body
    for node in ast.walk(function_node):
        if isinstance(node, ast.Call):
            # Check if it's a function call (not a method call)
            if isinstance(node.func, ast.Name):
                callee_name = node.func.id
                calls.add(callee_name)
                logger.debug(f"Found function call: {callee_name}")
    
    return calls

def validate_graph(graph: dict) -> bool:
    try:
        nodes = {node["id"] for node in graph["nodes"]}
        for edge in graph["edges"]:
            assert edge["source"] in nodes
            assert edge["target"] in nodes
        return True
    except Exception as e:
        logger.error(f"Graph validation failed: {e}")
        return False

# Test function
def test_parser():
    """Test the parser with sample code."""
    test_code = """
def main():
    helper()
    foo()
    
def helper():
    print("helping")
    
def foo():
    bar()
    
def bar():
    pass
"""
    
    result = extract_functions_and_calls(test_code)
    print("Test Result:")
    print(f"Functions: {result['functions']}")
    print(f"Calls: {result['calls']}")
    print("Code snippets:")
    for func_name, code in result['code'].items():
        print(f"  {func_name}: {repr(code)}")
    
    # Expected output:
    # {
    #     "functions": ["main", "helper", "foo", "bar"],
    #     "calls": [
    #         {"caller": "main", "callee": "helper"},
    #         {"caller": "main", "callee": "foo"},
    #         {"caller": "foo", "callee": "bar"}
    #     ],
    #     "code": {
    #         "main": "def main():\n    helper()\n    foo()",
    #         "helper": "def helper():\n    print(\"helping\")",
    #         "foo": "def foo():\n    bar()",
    #         "bar": "def bar():\n    pass"
    #     }
    # }

if __name__ == "__main__":
    test_parser()
