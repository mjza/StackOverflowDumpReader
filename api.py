from database import open_connection, close_connection, create_tables, insert_post_data
from utils import html_to_markdown
import re

def process_xml_line(conn, line):
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
    count = 0
    try:
        with open(path, 'r', encoding='utf-8') as file:
            
            for line in file:
                process_xml_line(conn, line)
                count += 1
    except Exception as e:
        print(f"{red}An error occurred: {e}{reset}")        
    print(f"{green}number of processed lines: {count}{reset}")        
    close_connection(conn)        