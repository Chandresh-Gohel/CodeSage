import re

def extract_functions_from_diff(diff_text):
    """
    Extract added or modified Python functions from the given diff text.

    Returns:
        List[dict] of {
            'function_code': str,
            'change_type': str ("added" | "modified")
        }
    """
    functions = []
    current_function_lines = []
    inside_function = False
    change_type = None

    diff_lines = diff_text.splitlines()

    for i, line in enumerate(diff_lines):
        # Skip deleted lines
        if line.startswith('-'):
            continue

        # Check for added or context lines
        if line.startswith('+') or line.startswith(' '):
            code_line = line[1:] if line.startswith('+') else line  # Remove '+' for added lines

            # Check if a function starts here
            if re.match(r'^\s*def\s+\w+\s*\(', code_line) or re.match(r'^\s*@', code_line):
                # If already inside a function, save the previous one
                if current_function_lines:
                    functions.append({
                        'function_code': '\n'.join(current_function_lines),
                        'change_type': change_type
                    })
                    current_function_lines = []

                inside_function = True
                change_type = "added" if line.startswith('+') else "modified"
                current_function_lines.append(code_line)

            elif inside_function:
                # Inside a function block — collect indented lines
                if code_line.strip() == "":
                    # Allow blank lines inside functions
                    current_function_lines.append(code_line)
                elif re.match(r'^\s+', code_line):
                    current_function_lines.append(code_line)
                else:
                    # Out of function block
                    if current_function_lines:
                        functions.append({
                            'function_code': '\n'.join(current_function_lines),
                            'change_type': change_type
                        })
                    inside_function = False
                    current_function_lines = []

    # Catch last function if still collecting
    if current_function_lines:
        functions.append({
            'function_code': '\n'.join(current_function_lines),
            'change_type': change_type
        })

    return functions


def extract_changed_files(diff_text):
    # Regex to match file changes (added or modified)
    file_pattern = r"([+-]?\s*diff --git a/.*? b/.*?)\n"
    files = []
    for match in re.finditer(file_pattern, diff_text):
        file_path = match.group(1).split(' ')[2].strip()
        files.append(file_path)
    return files
