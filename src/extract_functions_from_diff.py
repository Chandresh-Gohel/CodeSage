import re

def extract_functions_from_diff(diff_text):
    functions = []
    current_function_lines = []
    inside_function = False
    change_type = None

    func_def_pattern = re.compile(r'^\s*(def\s+\w+\s*\(|@)')
    indent_pattern = re.compile(r'^\s+')

    diff_lines = diff_text.splitlines()

    for line in diff_lines:
        if line.startswith('-'):
            continue

        if line.startswith('+') or line.startswith(' '):
            code_line = line[1:] if line.startswith('+') else line

            if func_def_pattern.match(code_line):
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
                if code_line.strip() == "":
                    current_function_lines.append(code_line)
                elif indent_pattern.match(code_line):
                    current_function_lines.append(code_line)
                else:
                    functions.append({
                        'function_code': '\n'.join(current_function_lines),
                        'change_type': change_type
                    })
                    inside_function = False
                    current_function_lines = []

    if current_function_lines:
        functions.append({
            'function_code': '\n'.join(current_function_lines),
            'change_type': change_type
        })

    return functions
