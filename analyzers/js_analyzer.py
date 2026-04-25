from pyjsparser import parse

def analyze_js(code):
    try:
        tree = parse(code)

        defined = set()
        used = set()

        def traverse(node):
            if isinstance(node, dict):
                node_type = node.get("type")

                # Function definitions
                if node_type == "FunctionDeclaration":
                    name = node.get("id", {}).get("name")
                    if name: defined.add(name)

                # Variable declarations
                if node_type == "VariableDeclarator":
                    name = node.get("id", {}).get("name")
                    if name: defined.add(name)

                # Function calls
                if node_type == "CallExpression":
                    name = node.get("callee", {}).get("name")
                    if name: used.add(name)

                for key in node:
                    traverse(node[key])

            elif isinstance(node, list):
                for item in node:
                    traverse(item)

        traverse(tree)

        return list(defined - used)

    except Exception:
        return ["Invalid JavaScript code"]
