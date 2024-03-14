import os
import sqlite3
import psycopg2

DBMS = os.getenv('DBMS')
if DBMS == 'SQLITE':
    PLACE_HOLDER = "?"
elif DBMS == 'POSTGRES':
    PLACE_HOLDER = "%s"
else:
    raise ValueError("Unsupported DBMS")

def open_connection():
    if DBMS == 'SQLITE':
        conn = sqlite3.connect(os.getenv('DB_PATH'))
    elif DBMS == 'POSTGRES':
        conn = psycopg2.connect(
            dbname=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            host=os.getenv('DB_HOST'),
            port=os.getenv('DB_PORT')
        )
    else:
        raise ValueError("Unsupported DBMS")

    return conn

def close_connection(conn):
    conn.commit()
    # Close the database connection
    conn.close()
    
def create_tables(conn):
    cursor = conn.cursor()
    # Create the tags table
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS posts (
        Id INTEGER PRIMARY KEY,
        PostTypeId INTEGER,
        AcceptedAnswerId INTEGER,
        CreationDate TEXT,
        Score INTEGER,
        ViewCount INTEGER,
        Body TEXT,
        OwnerUserId INTEGER,
        LastEditorUserId INTEGER,
        LastEditorDisplayName TEXT,
        LastEditDate TEXT,
        LastActivityDate TEXT,
        Title TEXT,
        Tags TEXT,
        AnswerCount INTEGER,
        CommentCount INTEGER,
        FavoriteCount INTEGER,
        CommunityOwnedDate TEXT,
        ContentLicense TEXT
    )''')  
    
    conn.commit() 
    
def insert_post_data(conn, data):
    cursor = conn.cursor()
    # Prepare data tuple
    post_data = (
        data.get('Id', None), data.get('PostTypeId', None), data.get('AcceptedAnswerId', None), 
        data.get('CreationDate', None), data.get('Score', None), data.get('ViewCount', None), 
        data.get('Body', None), data.get('OwnerUserId', None), data.get('LastEditorUserId', None), 
        data.get('LastEditorDisplayName', None), data.get('LastEditDate', None), 
        data.get('LastActivityDate', None), data.get('Title', None), 
        data.get('Tags', None), data.get('AnswerCount', None), data.get('CommentCount', None), 
        data.get('FavoriteCount', None), data.get('CommunityOwnedDate', None), 
        data.get('ContentLicense', None)
    )
    
    # Insert into database with ON CONFLICT clause
    sql = f'''INSERT INTO posts (Id, PostTypeId, AcceptedAnswerId, CreationDate, Score, ViewCount, Body, OwnerUserId, LastEditorUserId, LastEditorDisplayName, LastEditDate, LastActivityDate, Title, Tags, AnswerCount, CommentCount, FavoriteCount, CommunityOwnedDate, ContentLicense)
              VALUES ({PLACE_HOLDER}, {PLACE_HOLDER}, {PLACE_HOLDER}, {PLACE_HOLDER}, {PLACE_HOLDER}, {PLACE_HOLDER}, {PLACE_HOLDER}, {PLACE_HOLDER}, {PLACE_HOLDER}, {PLACE_HOLDER}, {PLACE_HOLDER}, {PLACE_HOLDER}, {PLACE_HOLDER}, {PLACE_HOLDER}, {PLACE_HOLDER}, {PLACE_HOLDER}, {PLACE_HOLDER}, {PLACE_HOLDER}, {PLACE_HOLDER})
              ON CONFLICT(Id) DO UPDATE SET
                PostTypeId = EXCLUDED.PostTypeId,
                AcceptedAnswerId = EXCLUDED.AcceptedAnswerId,
                CreationDate = EXCLUDED.CreationDate,
                Score = EXCLUDED.Score,
                ViewCount = EXCLUDED.ViewCount,
                Body = EXCLUDED.Body,
                OwnerUserId = EXCLUDED.OwnerUserId,
                LastEditorUserId = EXCLUDED.LastEditorUserId,
                LastEditorDisplayName = EXCLUDED.LastEditorDisplayName,
                LastEditDate = EXCLUDED.LastEditDate,
                LastActivityDate = EXCLUDED.LastActivityDate,
                Title = EXCLUDED.Title,
                Tags = EXCLUDED.Tags,
                AnswerCount = EXCLUDED.AnswerCount,
                CommentCount = EXCLUDED.CommentCount,
                FavoriteCount = EXCLUDED.FavoriteCount,
                CommunityOwnedDate = EXCLUDED.CommunityOwnedDate,
                ContentLicense = EXCLUDED.ContentLicense
           '''
    cursor.execute(sql, post_data)
    conn.commit()

