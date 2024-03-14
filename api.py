from database import open_connection, close_connection, create_tables, insert_post_data, insert_vote_data, insert_user_data, insert_tag_data, insert_postlink_data, insert_comment_data
from utils import html_to_markdown, tags_to_comma_separated
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
        
        if table == "Votes": 
            insert_vote_data(conn, attributes)
        elif table == "Users":
            if 'AboutMe' in attributes:
                attributes['AboutMe'] = html_to_markdown(attributes['AboutMe'])
            insert_user_data(conn, attributes)
        elif table == "Tags":
            insert_tag_data(conn, attributes)
        elif table == "PostLinks":
            insert_postlink_data(conn, attributes)
        elif table == 'Posts':
            if 'Body' in attributes:
                attributes['Body'] = html_to_markdown(attributes['Body'])
            if 'Tags' in attributes:   
                attributes['Tags'] = tags_to_comma_separated(attributes['Tags'])
            insert_post_data(conn, attributes)
        elif table == "Comments":   
            if 'Text' in attributes:
                attributes['Text'] = html_to_markdown(attributes['Text']) 
            insert_comment_data(conn, attributes)
        else:
            raise ValueError(f"Unknown type: {table}. Data insertion skipped.")
            
def skip_to_line(file, line_number):
    """Skip to the specified line number in the file."""
    for _ in range(line_number - 1):
        next(file)
        
def process_xml_file(path, table, line_number):
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
        with open(path, 'r', encoding='utf-8', errors='replace') as file:   
            skip_to_line(file, line_number)         
            for line in file:
                process_xml_line(conn, line, table)
                count += 1
                processed_bytes += len(line.encode('utf-8'))  # Update processed bytes
                last_percent_printed = print_progress(processed_bytes, total_bytes, last_percent_printed)
    except Exception as e:
        print(f"{red}\nAn error occurred: {e}{reset}")
    else:
        print(f"\n{green}Processing completed.{reset}")
        print(f"{green}Number of processed lines: {count}{reset}")  
    finally:      
        close_connection(conn)        