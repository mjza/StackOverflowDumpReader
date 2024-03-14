
from colored import fg, attr
from html import unescape
import markdownify

def remove_nul_characters(s):
    """Remove NUL (0x00) characters from a string."""
    return s.replace('\x00', '')

def html_to_markdown(html):
    return markdownify.markdownify(unescape(remove_nul_characters(html)), heading_style="ATX")

def list_xml_files(root_folder):
    """Recursively list all XML files in the given root folder and its subfolders."""
    import os
    xml_files = []
    for root, dirs, files in os.walk(root_folder):
        for file in files:
            if file.endswith('.xml'):
                xml_files.append(os.path.join(root, file))
    return xml_files

def read_first_node(file_path):
    """Reads the file line by line and prints the first XML node."""
    first_node_started = False
    node_lines = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            stripped_line = line.strip()
            if stripped_line.startswith('<?xml'):
                continue  # Skip XML declaration
            if '<' in stripped_line and not first_node_started:
                # Start of the first node
                first_node_started = True
                node_lines.append(line)
            elif first_node_started:
                # Continuation or end of the first node
                node_lines.append(line)
                if '>' in stripped_line and stripped_line.endswith('>'):
                    if '/' in stripped_line or \
                       (len(node_lines) > 1 and node_lines[-2].strip().endswith('/')):
                        # End of the first node found
                        break
    print(''.join(node_lines))  

def camel_to_snake(name):
    """
    Convert a string from CamelCase to snake_case.
    """
    import re
    str1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', str1).lower()

def read_integer(prompt_message):
    red = fg('red')
    reset = attr('reset')
    while True:
        user_input = input(prompt_message)
        try:
            return int(user_input)
        except ValueError:
            print(f"{red}Please enter a valid integer.{reset}")

def read_yes_no(prompt_message):
    """
    Prompts the user with the given message and expects a 'Y' or 'N' input.
    Returns True for 'Y' and False for 'N'.
    """
    green = fg('green')
    red = fg('red')
    reset = attr('reset')    
    while True:
        user_input = input(prompt_message + f"{green} (Y/N): {reset}").strip().upper()
        if user_input == 'Y':
            return True
        elif user_input == 'N':
            return False
        else:
            print(f"{red}Invalid input. Please enter 'Y' for Yes or 'N' for No.{reset}")