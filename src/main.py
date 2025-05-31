import sys
import os
import shutil
import pathlib
from processing import *

def copy_files(source, destination):

    if os.path.exists(destination):
        shutil.rmtree(destination)
        
    os.mkdir(destination)

    source_files = os.listdir(source)

    for source_file in source_files:
        if os.path.isfile(f"{source}{source_file}"):
            shutil.copy(f"{source}{source_file}", f"{destination}{source_file}")
        else:
            os.mkdir(f"{destination}{source_file}")
            copy_files(source + source_file + "/", destination + source_file + "/")

def generate_page(from_path, template_path, dest_path, base_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown = open(from_path).read()
    template = open(template_path).read()
    body = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    html = template.replace("{{ Title }}", title).replace("{{ Content }}", body)
    html = html.replace("href=\"/", f"href=\"{base_path}")
    html = html.replace("src=\"/", f"src=\"{base_path}")
    

    path = pathlib.Path(dest_path)
    if not os.path.exists(path.parent):
        os.makedirs(path.parent)

    open(dest_path, "w").write(html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, base_path):
    for file in os.listdir(dir_path_content):
        if (os.path.isfile(f"{dir_path_content}{file}")):
            filename, file_extension = os.path.splitext(file)
            if (file_extension == ".md"):
                generate_page(f"{dir_path_content}{file}", template_path, f"{dest_dir_path}{filename}.html", base_path)
        else:
            generate_pages_recursive(f"{dir_path_content}{file}/", template_path, f"{dest_dir_path}{file}/", base_path)

      

def main():
    base_path = "/"
    if len(sys.argv) > 1:
        base_path = sys.argv[1]

    base_filepath = os.getcwd()
    copy_files(f"{base_filepath}/static/", f"{base_filepath}/docs/")
    generate_pages_recursive(f"{base_filepath}/content/", f"{base_filepath}/template.html", f"{base_filepath}/docs/", base_path)

main()
