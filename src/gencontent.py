import os
from pathlib import Path
from markdown_blocks import markdown_to_html_node


def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            line = line[2:].strip()
            return line
    raise Exception("No title found!")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path} ...")
    
    with open(from_path, mode="r", encoding="utf-8") as file:
        markdown_content = file.read()

    with open(template_path, mode="r", encoding="utf-8") as file:
        template_content = file.read()

    html_content = markdown_to_html_node(markdown_content).to_html()
    html_title = extract_title(markdown_content)
    
    final_html = template_content.replace("{{ Title }}", html_title).replace("{{ Content }}", html_content)

    directory = os.path.dirname(dest_path)
    os.makedirs(directory, exist_ok=True)

    with open(dest_path, mode="w", encoding="utf-8") as file:
        file.write(final_html)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    all_paths = os.listdir(dir_path_content)
    for path in all_paths:
        full_dir_path = os.path.join(dir_path_content, path)
        full_dest_path = os.path.join(dest_dir_path, path)

        if os.path.isfile(full_dir_path):
            full_dest_path = Path(full_dest_path).with_suffix(".html")
            generate_page(full_dir_path, template_path, full_dest_path)
        else:
            generate_pages_recursive(full_dir_path, template_path, full_dest_path)

