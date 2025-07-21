import unittest
from parser import extract_functions_and_calls, validate_graph


class TestExtractFunctionsAndCalls(unittest.TestCase):
    def test_basic_functions(self):
        code = '''
def main():
    helper()
    foo()

def helper():
    print("helping")

def foo():
    bar()

def bar():
    pass
'''
        result = extract_functions_and_calls(code)
        self.assertCountEqual(result['functions'], ['main', 'helper', 'foo', 'bar'])
        self.assertIn({'caller': 'main', 'callee': 'helper'}, result['calls'])
        self.assertIn({'caller': 'main', 'callee': 'foo'}, result['calls'])
        self.assertIn({'caller': 'foo', 'callee': 'bar'}, result['calls'])
        self.assertIn('main', result['code'])
        self.assertIn('helper', result['code'])
        self.assertIn('foo', result['code'])
        self.assertIn('bar', result['code'])

    def test_empty_code(self):
        result = extract_functions_and_calls("")
        self.assertEqual(result['functions'], [])
        self.assertEqual(result['calls'], [])
        self.assertEqual(result['code'], {})

    def test_syntax_error(self):
        code = 'def foo('  # invalid syntax
        result = extract_functions_and_calls(code)
        self.assertEqual(result['functions'], [])
        self.assertEqual(result['calls'], [])
        self.assertEqual(result['code'], {})

    def test_nested_functions(self):
        code = '''
def outer():
    def inner():
        pass
    inner()
outer()
'''
        result = extract_functions_and_calls(code)
        # Both 'outer' and 'inner' should be detected as functions
        self.assertIn('outer', result['functions'])
        self.assertIn('inner', result['functions'])
        # 'outer' calls 'inner'
        self.assertIn({'caller': 'outer', 'callee': 'inner'}, result['calls'])

    def test_no_functions(self):
        code = 'print("hello world")\nx = 5'
        result = extract_functions_and_calls(code)
        self.assertEqual(result['functions'], [])
        self.assertEqual(result['calls'], [])
        self.assertEqual(result['code'], {})

    def test_duplicate_function_names(self):
        code = '''
def foo():
    pass

def foo():
    print("redefined")
    '''
        result = extract_functions_and_calls(code)
        # Only one 'foo' in the set, but code should be the last definition
        self.assertEqual(result['functions'].count('foo'), 1)
        self.assertIn('foo', result['code'])
        self.assertIn('print("redefined")', result['code']['foo'])

    def test_call_to_undefined_function(self):
        code = '''
def main():
    not_defined()
'''
        result = extract_functions_and_calls(code)
        self.assertIn('main', result['functions'])
        self.assertIn({'caller': 'main', 'callee': 'not_defined'}, result['calls'])

    def test_valid_graph(self):
        graph = {
            "nodes": [{"id": "main"}, {"id": "helper"}],
            "edges": [{"source": "main", "target": "helper"}],
            "code": {"main": "def main():\n    helper()"}
        }
        self.assertTrue(validate_graph(graph))

if __name__ == '__main__':
    unittest.main() 