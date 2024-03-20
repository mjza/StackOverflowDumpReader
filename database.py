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
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS posts (
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
        ContentLicense TEXT,
        Error BOOLEAN
    )
    ''')  
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS comments (
        Id INTEGER PRIMARY KEY,
        PostId INTEGER,
        Score INTEGER,
        Text TEXT,
        CreationDate TEXT,
        UserId INTEGER,
        ContentLicense TEXT,
        Error BOOLEAN
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS postlinks (
        Id INTEGER PRIMARY KEY,
        CreationDate TEXT,
        PostId INTEGER,
        RelatedPostId INTEGER,
        LinkTypeId INTEGER
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tags (
        Id INTEGER PRIMARY KEY,
        TagName TEXT,
        Count INTEGER,
        ExcerptPostId INTEGER,
        WikiPostId INTEGER
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        Id INTEGER PRIMARY KEY,
        Reputation INTEGER,
        CreationDate TEXT,
        DisplayName TEXT,
        LastAccessDate TEXT,
        AboutMe TEXT,
        Views INTEGER,
        UpVotes INTEGER,
        DownVotes INTEGER,
        Error BOOLEAN
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS votes (
        Id INTEGER PRIMARY KEY,
        PostId INTEGER,
        VoteTypeId INTEGER,
        CreationDate TEXT
    )
    ''')
    
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
        data.get('ContentLicense', None), data.get('Error', None)
    )
    
    # Insert into database with ON CONFLICT clause
    sql = f'''INSERT INTO posts (Id, PostTypeId, AcceptedAnswerId, CreationDate, Score, ViewCount, Body, OwnerUserId, LastEditorUserId, LastEditorDisplayName, LastEditDate, LastActivityDate, Title, Tags, AnswerCount, CommentCount, FavoriteCount, CommunityOwnedDate, ContentLicense, Error)
              VALUES ({PLACE_HOLDER}, {PLACE_HOLDER}, {PLACE_HOLDER}, {PLACE_HOLDER}, {PLACE_HOLDER}, {PLACE_HOLDER}, {PLACE_HOLDER}, {PLACE_HOLDER}, {PLACE_HOLDER}, {PLACE_HOLDER}, {PLACE_HOLDER}, {PLACE_HOLDER}, {PLACE_HOLDER}, {PLACE_HOLDER}, {PLACE_HOLDER}, {PLACE_HOLDER}, {PLACE_HOLDER}, {PLACE_HOLDER}, {PLACE_HOLDER}, {PLACE_HOLDER})
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
                ContentLicense = EXCLUDED.ContentLicense,
                Error = EXCLUDED.Error
           '''
    cursor.execute(sql, post_data)
    conn.commit()

def insert_comment_data(conn, data):
    cursor = conn.cursor()
    # Prepare data tuple
    comment_data = (
        data.get('Id', 0), data.get('PostId', 0), data.get('Score', 0),
        data.get('Text', None), data.get('CreationDate', None),
        data.get('UserId', 0), data.get('ContentLicense', None), 
        data.get('Error', None)
    )

    # Insert into database with ON CONFLICT clause
    sql = f'''
    INSERT INTO comments (Id, PostId, Score, Text, CreationDate, UserId, ContentLicense, Error)
    VALUES ({PLACE_HOLDER}, {PLACE_HOLDER}, {PLACE_HOLDER}, {PLACE_HOLDER}, {PLACE_HOLDER}, {PLACE_HOLDER}, {PLACE_HOLDER}, {PLACE_HOLDER})
    ON CONFLICT(Id) DO UPDATE SET
        PostId = EXCLUDED.PostId,
        Score = EXCLUDED.Score,
        Text = EXCLUDED.Text,
        CreationDate = EXCLUDED.CreationDate,
        UserId = EXCLUDED.UserId,
        ContentLicense = EXCLUDED.ContentLicense,
        Error = EXCLUDED.Error
    '''
    cursor.execute(sql, comment_data)
    conn.commit()

def insert_postlink_data(conn, data):
    cursor = conn.cursor()
    # Prepare data tuple
    postlink_data = (
        data.get('Id', 0), data.get('CreationDate', None),
        data.get('PostId', 0), data.get('RelatedPostId', 0),
        data.get('LinkTypeId', 0)
    )

    # Insert into database with ON CONFLICT clause
    sql = f'''
    INSERT INTO postlinks (Id, CreationDate, PostId, RelatedPostId, LinkTypeId)
    VALUES ({PLACE_HOLDER}, {PLACE_HOLDER}, {PLACE_HOLDER}, {PLACE_HOLDER}, {PLACE_HOLDER})
    ON CONFLICT(Id) DO UPDATE SET
        CreationDate = EXCLUDED.CreationDate,
        PostId = EXCLUDED.PostId,
        RelatedPostId = EXCLUDED.RelatedPostId,
        LinkTypeId = EXCLUDED.LinkTypeId
    '''
    cursor.execute(sql, postlink_data)
    conn.commit()

def insert_tag_data(conn, data):
    cursor = conn.cursor()
    # Prepare data tuple
    tag_data = (
        data.get('Id', 0), data.get('TagName', None),
        data.get('Count', 0), data.get('ExcerptPostId', 0),
        data.get('WikiPostId', 0)
    )

    # Insert into database with ON CONFLICT clause
    sql = f'''
    INSERT INTO tags (Id, TagName, Count, ExcerptPostId, WikiPostId)
    VALUES ({PLACE_HOLDER}, {PLACE_HOLDER}, {PLACE_HOLDER}, {PLACE_HOLDER}, {PLACE_HOLDER})
    ON CONFLICT(Id) DO UPDATE SET
        TagName = EXCLUDED.TagName,
        Count = EXCLUDED.Count,
        ExcerptPostId = EXCLUDED.ExcerptPostId,
        WikiPostId = EXCLUDED.WikiPostId
    '''
    cursor.execute(sql, tag_data)
    conn.commit()

def insert_user_data(conn, data):
    cursor = conn.cursor()
    # Prepare data tuple, converting special HTML entities and newline characters in 'AboutMe'
    user_data = (
        data.get('Id', 0), data.get('Reputation', 0), 
        data.get('CreationDate', None), data.get('DisplayName', None), 
        data.get('LastAccessDate', None), 
        data.get('AboutMe', None), 
        data.get('Views', 0), data.get('UpVotes', 0), 
        data.get('DownVotes', 0), data.get('Error', None)
    )

    # Insert into database with ON CONFLICT clause
    sql = f'''
    INSERT INTO users (Id, Reputation, CreationDate, DisplayName, LastAccessDate, AboutMe, Views, UpVotes, DownVotes, Error)
    VALUES ({PLACE_HOLDER}, {PLACE_HOLDER}, {PLACE_HOLDER}, {PLACE_HOLDER}, {PLACE_HOLDER}, {PLACE_HOLDER}, {PLACE_HOLDER}, {PLACE_HOLDER}, {PLACE_HOLDER}, {PLACE_HOLDER})
    ON CONFLICT(Id) DO UPDATE SET
        Reputation = EXCLUDED.Reputation,
        CreationDate = EXCLUDED.CreationDate,
        DisplayName = EXCLUDED.DisplayName,
        LastAccessDate = EXCLUDED.LastAccessDate,
        AboutMe = EXCLUDED.AboutMe,
        Views = EXCLUDED.Views,
        UpVotes = EXCLUDED.UpVotes,
        DownVotes = EXCLUDED.DownVotes,
        Error = EXCLUDED.Error
    '''
    cursor.execute(sql, user_data)
    conn.commit()

def insert_vote_data(conn, data):
    cursor = conn.cursor()
    # Prepare data tuple
    vote_data = (
        data.get('Id', None), data.get('PostId', 0), 
        data.get('VoteTypeId', 0), data.get('CreationDate', None)
    )

    # Insert into database with ON CONFLICT clause
    sql = f'''
    INSERT INTO votes (Id, PostId, VoteTypeId, CreationDate)
    VALUES ({PLACE_HOLDER}, {PLACE_HOLDER}, {PLACE_HOLDER}, {PLACE_HOLDER})
    ON CONFLICT(Id) DO UPDATE SET
        PostId = EXCLUDED.PostId,
        VoteTypeId = EXCLUDED.VoteTypeId,
        CreationDate = EXCLUDED.CreationDate
    '''
    cursor.execute(sql, vote_data)
    conn.commit()
