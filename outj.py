
import sys
from bs4 import BeautifulSoup, Comment, Doctype

def html_to_jinja(input_html_path: str, output_jinja_path: str, output_vars_path: str):
    # Read the HTML file
    with open(input_html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Parse with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # This list will hold tuples of (var_name, original_text).
    variables = []
    var_count = 1

    # Find all text nodes in the soup
    for text_node in soup.find_all(string=True):
        # Skip or remove comments and doctypes
        if isinstance(text_node, (Comment, Doctype)):
            text_node.extract()  # Removes the node from the tree
            continue

        # Strip leading/trailing whitespace to check if it’s meaningful text
        stripped_text = text_node.strip()
        if stripped_text:
            var_name = f"var_{var_count}"
            var_count += 1

            # Escape any internal quotes
            text_for_jinja = stripped_text.replace('"', '\\"')

            # Add to variables list
            variables.append((var_name, text_for_jinja))

            # Replace the original text node with {{ var_name }} for Jinja
            new_text = f"{{{{ {var_name} }}}}"
            text_node.replace_with(new_text)

    # 1) Generate the Jinja template from the modified soup
    jinja_template_content = soup.prettify()

    # 2) Write the Jinja template to file
    with open(output_jinja_path, 'w', encoding='utf-8') as f:
        f.write(jinja_template_content)

    # 3) Write the variables to a separate Python file
    with open(output_vars_path, 'w', encoding='utf-8') as f:
        f.write("# Automatically generated variables for the Jinja template\n")
        f.write("variables = {\n")
        for var_name, original_text in variables:
            f.write(f"    '{var_name}': {repr(original_text)},\n")
        f.write("}\n")

if __name__ == "__main__":
    # Example usage:
    # python script.py input.html output_template.jinja variables.py

    if len(sys.argv) < 4:
        print("Usage: python script.py <input_html_path> <output_jinja_path> <output_vars_path>")
        sys.exit(1)

    input_html_path = sys.argv[1]
    output_jinja_path = sys.argv[2]
    output_vars_path = sys.argv[3]

    html_to_jinja(input_html_path, output_jinja_path, output_vars_path)
    print(f"Finished generating: {output_jinja_path} and {output_vars_path}")
