import sys
import os
import shutil
from bs4 import BeautifulSoup, Comment, Doctype


def extract_and_replace_text(soup, text_var_prefix='text_', starting_count=1):
    """
    Extract text from the soup (excluding comments & doctypes) and replace it
    with Jinja variables. Return a list of (var_name, original_text).
    """
    text_variables = []
    var_count = starting_count

    for text_node in soup.find_all(string=True):
        # Skip comments and doctypes
        if isinstance(text_node, (Comment, Doctype)):
            text_node.extract()
            continue

        stripped_text = text_node.strip()
        # If there's meaningful text, replace it with a Jinja variable
        if stripped_text:
            var_name = f"{text_var_prefix}{var_count}"
            var_count += 1

            # Optionally escape quotes or handle them as needed:
            text_for_jinja = stripped_text.replace('"', '\\"')

            # Save the variable
            text_variables.append((var_name, text_for_jinja))

            # Replace original text in the soup
            new_text = f"{{{{ {var_name} }}}}"
            text_node.replace_with(new_text)

    return text_variables


def extract_and_replace_attribute(soup, tag_name, attribute, var_prefix='var_', starting_count=1):
    """
    Find all tags in `soup` of type `tag_name` that have `attribute`,
    replace the attribute value with Jinja variables, and return a dictionary
    mapping var_name -> original_value.
    """
    var_dict = {}
    var_count = starting_count

    for tag in soup.find_all(tag_name, **{attribute: True}):
        original_value = tag.get(attribute, '').strip()
        if original_value:
            var_name = f"{var_prefix}{var_count}"
            var_count += 1

            var_dict[var_name] = original_value
            # Replace the attribute with a Jinja placeholder
            tag[attribute] = f"{{{{ {var_name} }}}}"

    return var_dict


def html_to_jinja(input_html_path: str,
                  output_jinja_path: str,
                  output_vars_path: str):
    """
    Convert HTML to a Jinja template, extracting text, link (href), and img (src)
    into variables. All variables are placed in a single Python file with
    separate sections for text, links, and images.
    """
    # Read the HTML file
    with open(input_html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Parse with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # 1) Extract & replace text
    text_variables = extract_and_replace_text(soup, text_var_prefix='txt_', starting_count=1)

    link_variables = extract_and_replace_attribute(soup, 'a', 'href', var_prefix='link_', starting_count=1)
    image_variables = extract_and_replace_attribute(soup, 'img', 'src', var_prefix='img_', starting_count=1)
    links_variables = extract_and_replace_attribute(soup, 'link', 'href', var_prefix='link_', starting_count=1)
    script_variables = extract_and_replace_attribute(soup, 'script', 'src', var_prefix='script_', starting_count=1)

    # Generate the Jinja template from the modified soup
    jinja_template_content = soup.prettify()

    # Write the Jinja template to file
    with open(output_jinja_path, 'w', encoding='utf-8') as f:
        f.write(jinja_template_content)

    # Usage in your file-writing logic:
    with open(output_vars_path, 'w', encoding='utf-8') as f:
        f.write("# Automatically generated variables for the Jinja template\n\n")

        # Assuming text_variables is already an iterable of tuples
        write_section(f, "text_variables", text_variables)
        
        # For dictionaries, pass .items() to get an iterable of pairs
        write_section(f, "link_variables", link_variables.items())
        write_section(f, "image_variables", image_variables.items())
        write_section(f, "links_variables", links_variables.items())
        write_section(f, "script_variables", script_variables.items())

    print("Files generated:")
    print(f"  Template: {output_jinja_path}")
    print(f"  Variables (text/links/images): {output_vars_path}")

def write_section(f, section_name, items):
    """
    Writes a section of variables to the file using an iterable of (key, value) pairs.
    
    Args:
        f: File object to write to.
        section_name: Name of the variable section (e.g., 'text_variables').
        items: Iterable yielding (key, value) pairs.
    """
    f.write(f"{section_name} = {{\n")
    for key, value in items:
        f.write(f"    '{key}': {repr(value)},\n")
    f.write("}\n\n")


if __name__ == "__main__":
    """
    Usage:
        python script.py input.html output_folder
    """
    if len(sys.argv) < 3:
        print("Usage: python script.py <input_html> <output_folder>")
        sys.exit(1)

    input_html_path = sys.argv[1]
    output_folder = sys.argv[2]

    # Recreate the output folder
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)
    os.makedirs(output_folder, exist_ok=True)

    # Define output paths
    output_jinja_path = os.path.join(output_folder, "template.jinja")
    output_vars_path = os.path.join(output_folder, "variables.py")

    html_to_jinja(
        input_html_path,
        output_jinja_path,
        output_vars_path
    )
