
def explain_dead_code(code, dead_code):
    if not dead_code:
        return "No dead code detected. Your code is clean and optimized."

    explanation = "The following parts of the code are unused:\n\n"

    for item in dead_code:
        explanation += f"• '{item}' is defined but never used.\n"

    explanation += "\nRemoving unused code improves readability, reduces complexity, and makes maintenance easier."

    return explanation