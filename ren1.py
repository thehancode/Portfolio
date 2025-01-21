
import os
import sys
from jinja2 import Environment, FileSystemLoader, Template

def render_template(folder_name):
    # Paths and filenames
    template_file = os.path.join(folder_name, 'template.jinja')
    variable_files = [
        os.path.join(folder_name, 'text.jinja'),
        os.path.join(folder_name, 'links.jinja'),
        os.path.join(folder_name, 'imgs.jinja')
    ]
    output_file = os.path.join(folder_name, f'{folder_name}.html')

    # Check if the folder exists
    if not os.path.isdir(folder_name):
        raise FileNotFoundError(f"The folder '{folder_name}' does not exist.")

    # Check if the variable files exist
    for file_path in variable_files:
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"The variable file '{file_path}' does not exist.")

    # Load and combine variable data
    variables = {}
    for var_file in variable_files:
        with open(var_file, 'r') as f:
            local_vars = {}
            exec(f.read(), {}, local_vars)
            # Extract dictionaries defined in the file and update the main variables
            for val in local_vars.values():
                if isinstance(val, dict):
                    variables.update(val)

    # Read the Jinja template
    with open(template_file, 'r') as f:
        template_content = f.read()

    # Render the template with the combined variables
    template = Template(template_content)
    rendered_content = template.render(**variables)

    # Write the output
    os.makedirs(folder_name, exist_ok=True)
    with open(output_file, 'w') as f:
        f.write(rendered_content)

    print(f"HTML file rendered successfully to {os.path.abspath(output_file)}")

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
