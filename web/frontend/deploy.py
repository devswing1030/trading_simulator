import os
import shutil
import subprocess

# Define paths
REACT_APP_PATH = "."  # Change this to your React project path
DJANGO_APP_PATH = "../backend"  # Change this to your Django project path
DJANGO_STATIC_PATH = os.path.join(DJANGO_APP_PATH, 'nasdaq/static/nasdaq')  # Assuming 'myapp' is your Django app
DJANGO_TEMPLATES_PATH = os.path.join(DJANGO_APP_PATH, 'nasdaq/templates/nasdaq')  # Assuming 'myapp' is your Django app


# Build the React app
def build_react_app():
    print("Building React app...")
    subprocess.run(["npm", "run", "build"], cwd=REACT_APP_PATH, check=True)


# Move React build files to Django
def move_react_build():
    build_dir = os.path.join(REACT_APP_PATH, 'build')

    if not os.path.exists(build_dir):
        raise FileNotFoundError(f"React build directory not found at {build_dir}")

    print(f"Moving React build files from {build_dir} to Django app...")

    # Create necessary directories in Django project if not exist
    if not os.path.exists(DJANGO_STATIC_PATH):
        os.makedirs(DJANGO_STATIC_PATH)

    if not os.path.exists(DJANGO_TEMPLATES_PATH):
        os.makedirs(DJANGO_TEMPLATES_PATH)

    # Move build folder content into Django's static directory
    shutil.copytree(os.path.join(build_dir, 'static'), DJANGO_STATIC_PATH, dirs_exist_ok=True)

    # Move the index.html to Django's templates directory
    shutil.copy(os.path.join(build_dir, 'index.html'), DJANGO_TEMPLATES_PATH)

    print(f"React build files moved to {DJANGO_STATIC_PATH} and index.html to {DJANGO_TEMPLATES_PATH}")


# Update the index.html to use Django static tag
def update_index_html():
    index_html_path = os.path.join(DJANGO_TEMPLATES_PATH, 'index.html')

    print(f"Updating {index_html_path} to use Django's static tag...")

    with open(index_html_path, 'r') as file:
        content = file.read()

    # Add {% load static %} at the top of the file
    if not content.startswith("{% load static %}"):
        content = "{% load static %}\n" + content

    # Replace the paths to JS and CSS files to use Django's {% static %} tag
    content = content.replace("/static/css", "{% static 'nasdaq/css")
    content = content.replace("/static/js", "{% static 'nasdaq/js")

    # Ensure the closing quotation mark for the static tag
    content = content.replace('.css', ".css' %}")
    content = content.replace('.js', ".js' %}")

    with open(index_html_path, 'w') as file:
        file.write(content)

    print(f"Updated {index_html_path} to use static tag")


# Run collectstatic for Django
def collect_static():
    print("Running collectstatic for Django...")
    subprocess.run(["python", "manage.py", "collectstatic", "--noinput"], cwd=DJANGO_APP_PATH, check=True)


# Main function to automate the process
def automate_react_django_integration():
    try:
        #build_react_app()
        move_react_build()
        update_index_html()
        #collect_static()
        print("React app successfully integrated into Django!")
    except Exception as e:
        print(f"An error occurred: {e}")


# Run the automation
if __name__ == "__main__":
    automate_react_django_integration()