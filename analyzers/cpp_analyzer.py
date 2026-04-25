import re

def analyze_cpp(code):
    try:
        # Find function definitions (excluding main)
        functions = re.findall(
            r'\b(?:int|void|float|double|char)\s+(\w+)\s*\([^)]*\)\s*\{',
            code
        )

        defined = set(f for f in functions if f != "main")
        used = set()

        # Find function calls ONLY inside main or other functions
        call_matches = re.findall(r'(\w+)\s*\(', code)

        for call in call_matches:
            if call in defined:
                used.add(call)

        # Remove self-calls (definition line issue)
        for func in defined:
            pattern = rf'\b(?:int|void|float|double|char)\s+{func}\s*\('
            if re.search(pattern, code):
                if func in used:
                    used.remove(func)

        return list(defined - used)

    except Exception:
        return ["Invalid C/C++ code"]