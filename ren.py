import os
import sys
import importlib.util
from jinja2 import Template

def render_template(folder_name):
    # Paths and filenames
    template_file = os.path.join(folder_name, 'template.jinja')
    variables_file = os.path.join(folder_name, 'variables.py')
    output_file = os.path.join(folder_name, f'{folder_name}.html')

    # Check if the folder exists
    if not os.path.isdir(folder_name):
        raise FileNotFoundError(f"The folder '{folder_name}' does not exist.")

    # Check if the template file existors
    if not os.path.isfile(template_file):
        raise FileNotFoundError(f"The template file '{template_file}' does not exist.")

    # Check if variables.py exists
    if not os.path.isfile(variables_file):
        raise FileNotFoundError(f"The file 'variables.py' does not exist in '{folder_name}'.")

    # Dynamically import the variables module from variables.py
    spec = importlib.util.spec_from_file_location("variables", variables_file)
    if spec is None:
        raise ImportError(f"Could not load module spec from {variables_file}")
    variables_module = importlib.util.module_from_spec(spec)
    if spec.loader is None:
        raise ImportError(f"Spec loader is None for {variables_file}")
    spec.loader.exec_module(variables_module)

    # Combine all variables into one dictionary
    combined_variables = {}

    # List of dictionary attribute names in variables.py that we want to merge
    dict_names = [
        "text_variables",
        "link_variables",
        "image_variables",
        "links_variables",
        "script_variables"
    ]

    for dict_name in dict_names:
        if hasattr(variables_module, dict_name):
            var_dict = getattr(variables_module, dict_name)
            if isinstance(var_dict, dict):
                if dict_name in {"image_variables", "links_variables", "script_variables"}:
                    prefix_values(var_dict, "../")
                combined_variables.update(var_dict)

    # Read the Jinja template
    with open(template_file, 'r', encoding='utf-8') as f:
        template_content = f.read()

    # Render the template with the combined variables
    template = Template(template_content)
    rendered_content = template.render(**combined_variables)

    # Write the output
    os.makedirs(folder_name, exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(rendered_content)

    print(f"HTML file rendered successfully to {os.path.abspath(output_file)}")

def prefix_values(var_dict, prefix):
    """Add a prefix to each string value in the dictionary."""
    for key, value in var_dict.items():
        if isinstance(value, str):
            var_dict[key] = prefix + value
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python script.py <folder_name>")
        sys.exit(1)

    folder_name = sys.argv[1]
    try:
        render_template(folder_name)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
