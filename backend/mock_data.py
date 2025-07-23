# backend/mock_data.py

def generate_mock_graph():
    return {
        "nodes": [
            {
                "id": "main",
                "data": {
                    "label": "main",
                    "code": "def main():\n    helper()\n    foo()"
                },
                "position": {"x": 0, "y": 100}
            },
            {
                "id": "helper",
                "data": {
                    "label": "helper",
                    "code": "def helper():\n    print('helping')"
                },
                "position": {"x": 200, "y": 100}
            },
            {
                "id": "foo",
                "data": {
                    "label": "foo",
                    "code": "def foo():\n    bar()"
                },
                "position": {"x": 0, "y": 250}
            },
            {
                "id": "bar",
                "data": {
                    "label": "bar",
                    "code": "def bar():\n    pass"
                },
                "position": {"x": 200, "y": 250}
            }
        ],
        "edges": [
            {"id": "e1", "source": "main", "target": "helper"},
            {"id": "e2", "source": "main", "target": "foo"},
            {"id": "e3", "source": "foo", "target": "bar"}
        ]
    }
