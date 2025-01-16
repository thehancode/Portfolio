import os
from jinja2 import Template

# Paths to the files
template_file = 'out.jinja'
variables_file = 'out.vars'
output_file = 'rendered.html'

# Load the variables from the .vars file
variables = {}
with open(variables_file, 'r') as vars_file:
    exec(vars_file.read())  # This will populate the `variables` dictionary

# Read the Jinja template
with open(template_file, 'r') as template_file:
    template_content = template_file.read()

# Render the template
template = Template(template_content)
rendered_content = template.render(**variables)

# Write the output to an HTML file
with open(output_file, 'w') as output_file:
    output_file.write(rendered_content)

print(f"HTML file rendered successfully to {os.path.abspath(output_file.name)}")

