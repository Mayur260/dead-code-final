import ast

def find_dead_code(code):
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return ["Invalid Python code"]

    defined = set()
    used = set()

    class Analyzer(ast.NodeVisitor):
        def visit_FunctionDef(self, node):
            defined.add(node.name)
            self.generic_visit(node)

        def visit_ClassDef(self, node):
            defined.add(node.name)
            self.generic_visit(node)

        def visit_Call(self, node):
            # function calls
            if isinstance(node.func, ast.Name):
                used.add(node.func.id)

            # method calls like obj.method()
            elif isinstance(node.func, ast.Attribute):
                used.add(node.func.attr)

            self.generic_visit(node)

    Analyzer().visit(tree)

    # remove built-ins
    builtins = set(dir(__builtins__))

    unused = defined - used - builtins

    return list(unused)