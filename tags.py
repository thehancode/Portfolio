import sys
from bs4 import BeautifulSoup, Comment, Doctype

def html_to_jinja(input_html_path: str,
                  output_jinja_path: str,
                  output_text_vars_path: str,
                  output_link_vars_path: str,
                  output_img_vars_path: str):
    # Read the HTML file
    with open(input_html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Parse with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # These lists/dictionaries will hold extracted information
    text_variables = []
    links_dict = {}
    images_dict = {}

    # Counters for variable naming
    var_count = 1
    link_count = 1
    img_count = 1

    # ------------------------------------------------------------------------
    # 1) Extract and replace all textual content (excluding comments & doctypes)
    # ------------------------------------------------------------------------
    for text_node in soup.find_all(string=True):
        # Skip or remove comments and doctypes
        if isinstance(text_node, (Comment, Doctype)):
            text_node.extract()
            continue

        # Strip leading/trailing whitespace to check if it's meaningful text
        stripped_text = text_node.strip()
        if stripped_text:
            var_name = f"var_{var_count}"
            var_count += 1

            # We can choose to escape any internal quotes, if needed:
            text_for_jinja = stripped_text.replace('"', '\\"')

            # Add to text_variables list
            text_variables.append((var_name, text_for_jinja))

            # Replace the original text node with {{ var_name }} for Jinja
            new_text = f"{{{{ {var_name} }}}}"
            text_node.replace_with(new_text)

    # ------------------------------------------------------------------------
    # 2) Extract and replace all `href` attributes from <a> tags
    # ------------------------------------------------------------------------
    for a_tag in soup.find_all('a', href=True):
        original_href = a_tag['href'].strip()
        if original_href:
            link_var_name = f"link_{link_count}"
            link_count += 1

            # Save the original href in the dictionary
            links_dict[link_var_name] = original_href

            # Replace the href attribute with a Jinja placeholder
            a_tag['href'] = f"{{{{ {link_var_name} }}}}"

    # ------------------------------------------------------------------------
    # 3) Extract and replace all `src` attributes from <img> tags
    # ------------------------------------------------------------------------
    for img_tag in soup.find_all('img', src=True):
        original_src = img_tag['src'].strip()
        if original_src:
            img_var_name = f"img_{img_count}"
            img_count += 1

            # Save the original src in the dictionary
            images_dict[img_var_name] = original_src

            # Replace the src attribute with a Jinja placeholder
            img_tag['src'] = f"{{{{ {img_var_name} }}}}"

    # ------------------------------------------------------------------------
    # Generate the Jinja template from the modified soup
    # ------------------------------------------------------------------------
    jinja_template_content = soup.prettify()

    # Write the Jinja template to file
    with open(output_jinja_path, 'w', encoding='utf-8') as f:
        f.write(jinja_template_content)

    # ------------------------------------------------------------------------
    # Write the text variables to a separate Python file
    # ------------------------------------------------------------------------
    with open(output_text_vars_path, 'w', encoding='utf-8') as f:
        f.write("# Automatically generated text variables for the Jinja template\n")
        f.write("text_variables = {\n")
        for var_name, original_text in text_variables:
            f.write(f"    '{var_name}': {repr(original_text)},\n")
        f.write("}\n")

    # ------------------------------------------------------------------------
    # Write the link variables to a separate Python file
    # ------------------------------------------------------------------------
    with open(output_link_vars_path, 'w', encoding='utf-8') as f:
        f.write("# Automatically generated link variables for the Jinja template\n")
        f.write("link_variables = {\n")
        for link_var_name, href_value in links_dict.items():
            f.write(f"    '{link_var_name}': {repr(href_value)},\n")
        f.write("}\n")

    # ------------------------------------------------------------------------
    # Write the image variables to a separate Python file
    # ------------------------------------------------------------------------
    with open(output_img_vars_path, 'w', encoding='utf-8') as f:
        f.write("# Automatically generated image variables for the Jinja template\n")
        f.write("image_variables = {\n")
        for img_var_name, src_value in images_dict.items():
            f.write(f"    '{img_var_name}': {repr(src_value)},\n")
        f.write("}\n")

    print("Files generated:")
    print(f"  Template: {output_jinja_path}")
    print(f"  Text vars: {output_text_vars_path}")
    print(f"  Link vars: {output_link_vars_path}")
    print(f"  Image vars: {output_img_vars_path}")


if __name__ == "__main__":
    """
    Example usage:
    python script.py input.html output_template.jinja text_vars.py link_vars.py image_vars.py
    """
    if len(sys.argv) < 6:
        print("Usage: python script.py <input_html> <output_jinja> <output_text_vars> <output_link_vars> <output_img_vars>")
        sys.exit(1)

    input_html_path = sys.argv[1]
    output_jinja_path = sys.argv[2]
    output_text_vars_path = sys.argv[3]
    output_link_vars_path = sys.argv[4]
    output_img_vars_path = sys.argv[5]

    html_to_jinja(
        input_html_path,
        output_jinja_path,
        output_text_vars_path,
        output_link_vars_path,
        output_img_vars_path
    )
