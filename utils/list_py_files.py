import os

def find_py_files(start_dir):
    py_files = []
    for root, _, files in os.walk(start_dir):
        for file in files:
            if file.endswith('.py'):
                py_files.append(os.path.join(root, file))
    return py_files

if __name__ == "__main__":
    # Change '.' to your project root directory if needed
    project_root = '.'
    python_files = find_py_files(project_root)

    for py_file in python_files:
        print(py_file)
