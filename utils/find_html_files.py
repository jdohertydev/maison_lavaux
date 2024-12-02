import os

def find_html_files(start_dir):
    html_files = []
    for root, _, files in os.walk(start_dir):
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
    return html_files

if __name__ == "__main__":
    # Change '.' to your project root directory if needed
    project_root = '.'
    html_files = find_html_files(project_root)

    for html_file in html_files:
        print(html_file)
