
from colored import fg, attr
from html import unescape
import markdownify
import html2text
import re

def remove_nul_characters(text):
    """Remove NUL (0x00) characters from a string."""
    return text.replace('\x00', '')

def remove_surrogates(text):
    # Remove surrogate characters from a string
    return ''.join(char for char in text if not 0xD800 <= ord(char) <= 0xDFFF)

def tags_to_comma_separated(tag_string):
    # Decode HTML entities to get the actual characters ("<", ">")
    decoded_tag_string = tag_string.replace("&lt;", "<").replace("&gt;", ">")

    # Split the string into individual tags, remove the angle brackets, then join with commas
    tags = decoded_tag_string.strip("<>").split("><")
    comma_separated_tags = ", ".join(tags)
    
    return comma_separated_tags

def html_to_markdown1(html):
    return remove_surrogates(remove_nul_characters(markdownify.markdownify(unescape(html), heading_style="ATX")))

def html_to_markdown2(encoded_html):
    # Decode HTML entities
    html = unescape(encoded_html)

    # Initialize html2text
    text_maker = html2text.HTML2Text()
    text_maker.ignore_links = False
    text_maker.ignore_images = True
    text_maker.ignore_emphasis = False
    text_maker.ignore_tables = False
    text_maker.mark_code = True
    text_maker.body_width = 0
    text_maker.skip_internal_links = True

    error = False
    try:
        # Convert HTML to Markdown
        markdown = text_maker.handle(html)
        # Clean up code blocks if necessary (this step may not be needed with html2text, but included for completeness)
        markdown = re.sub(r'^\[code\]\s*$', '```', markdown, flags=re.MULTILINE)
        markdown = re.sub(r'^\[/code\]\s*$', '```', markdown, flags=re.MULTILINE)
    except Exception as e:
        print(f"An error occurred during HTML to Markdown conversion: {e}")    
        markdown = html
        error = True

    return remove_surrogates(remove_nul_characters(markdown)), error

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
            
def skip_to_line(file, line_number):
    """Skip to the specified line number in the file and return the number of bytes passed."""
    from colored import fg, attr
    magenta = fg('magenta')
    reset = attr('reset')
    if line_number > 1:
        print(f"{magenta}Skeeping to the start line ...{reset}")
    bytes_passed = 0
    for _ in range(line_number - 1):
        line = next(file)
        bytes_passed += len(line.encode('utf-8'))  # Assuming UTF-8 encoding for byte length calculation
    return bytes_passed  

def print_progress(current_bytes, total_bytes, last_printed_percent=None):
    """Prints progress based on bytes processed, updating at each 1% increment of progress."""
    from colored import fg, attr
    magenta = fg('magenta')
    reset = attr('reset')
    percentage = int(100 * (current_bytes / total_bytes))  # Convert to int for whole number percentages
    if last_printed_percent is None or percentage > last_printed_percent:
        bar_length = 50  # Modify this to change the progress bar length
        progress_mark = int(bar_length * (current_bytes / total_bytes))
        bar = '[' + '#' * progress_mark + '-' * (bar_length - progress_mark) + ']'
        print(f"{magenta}\rProgress: {percentage}% {bar}{reset}", end='', flush=True)
        return percentage  # Return the current percentage for tracking
    return last_printed_percent          