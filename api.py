from database import open_connection, close_connection, create_tables, insert_post_data
from utils import html_to_markdown, count_lines
import re
import os

def print_progress(current_bytes, total_bytes, last_printed_percent=None):
    """Prints progress based on bytes processed, updating at each 1% increment of progress."""
    percentage = int(100 * (current_bytes / total_bytes))  # Convert to int for whole number percentages
    if last_printed_percent is None or percentage > last_printed_percent:
        bar_length = 50  # Modify this to change the progress bar length
        progress_mark = int(bar_length * (current_bytes / total_bytes))
        bar = '[' + '#' * progress_mark + '-' * (bar_length - progress_mark) + ']'
        print(f"\rProgress: {percentage}% {bar}", end='', flush=True)
        return percentage  # Return the current percentage for tracking
    return last_printed_percent
    
def process_xml_line(conn, line, table):
    # Regular expression to match the <row> elements and capture their attributes
    row_regex = re.compile(r'<row ([^>]+)>')
    match = row_regex.search(line)
    if match:
        attributes_str = match.group(1)
        # Convert the attributes string to a dictionary
        attributes = dict(re.findall(r'(\S+)="([^"]*)"', attributes_str))
        # Convert &amp;, &lt;, &gt;, etc. in 'Body' to their character equivalents
        if 'Body' in attributes:
            attributes['Body'] = html_to_markdown(attributes.get('Body'))
        # Here you would call insert_post with the attributes dictionary
        # For demonstration, just print the attributes
        insert_post_data(conn, attributes)  # Replace this with your database insert function call

def process_xml_file(path, table):
    from colored import fg, attr
    red = fg('red')
    green = fg('green')
    reset = attr('reset')
    conn = open_connection()
    create_tables(conn)
    
    # Get the total size of the file in bytes
    total_bytes = os.path.getsize(path)
    count = 0
    processed_bytes = 0
    last_percent_printed = None
    
    try:
        with open(path, 'r', encoding='utf-8') as file:            
            for line in file:
                process_xml_line(conn, line, table)
                count += 1
                processed_bytes += len(line.encode('utf-8'))  # Update processed bytes
                last_percent_printed = print_progress(processed_bytes, total_bytes, last_percent_printed)
    except Exception as e:
        print(f"{red}An error occurred: {e}{reset}")
    else:
        print(f"\n{green}Processing completed.{reset}")
        print(f"{green}Number of processed lines: {count}{reset}")  
    finally:      
        close_connection(conn)        