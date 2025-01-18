
import os
from jinja2 import Template

# Path to the template file
template_file = 'temp.jinja'

# List of variable files to load
variable_files = ['txt.jinja', 'links.jinja', 'img.jinja']

# Output file path
output_file = 'renderedd.html'

# Load and merge variables from all files
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

# Write the output to an HTML file
with open(output_file, 'w') as f:
    f.write(rendered_content)

print(f"HTML file rendered successfully to {os.path.abspath(output_file)}")
