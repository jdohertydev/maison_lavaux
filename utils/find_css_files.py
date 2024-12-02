import os

def find_css_files(start_dir):
    css_files = []
    for root, _, files in os.walk(start_dir):
        for file in files:
            if file.endswith('.css'):
                css_files.append(os.path.join(root, file))
    return css_files

if __name__ == "__main__":
    # Change '.' to your project root directory if needed
    project_root = '.'
    css_files = find_css_files(project_root)

    for css_file in css_files:
        print(css_file)
