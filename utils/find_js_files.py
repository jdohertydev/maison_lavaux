import os


def find_js_files(start_dir):
    js_files = []
    for root, _, files in os.walk(start_dir):
        for file in files:
            if file.endswith(".js"):
                js_files.append(os.path.join(root, file))
    return js_files


if __name__ == "__main__":
    # Change '.' to your project root directory if needed
    project_root = "."
    js_files = find_js_files(project_root)

    for js_file in js_files:
        print(js_file)
