
from livereload import Server, shell
import os

# Directory where your files reside
project_dir = os.path.abspath('.')  # Adjust if needed

# Initialize the server
server = Server()

# List files to watch for changes
watch_files = [
    'temp.jinja',
    'txt.jinja',
    'links.jinja',
    'img.jinja'
]

# For each file, set up a watcher that runs your rendering script when changes occur
for f in watch_files:
    server.watch(f, shell('python3.10 ren1.py', cwd=project_dir))

# Also watch the generated HTML to trigger browser reload
server.watch('renderedd.html')

# Serve files from the project directory (or specify the directory containing rendered.html)
server.serve(root=project_dir, open_url_delay=1 , default_filename='./renderedd.html')
