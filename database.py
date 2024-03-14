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
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tags (
        name TEXT NOT NULL PRIMARY KEY,
        count INTEGER NOT NULL,
        has_synonyms BOOLEAN NOT NULL
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tag_synonyms (
        from_tag TEXT NOT NULL,
        to_tag TEXT NOT NULL,
        creation_date INTEGER,
        last_applied_date INTEGER,
        applied_count INTEGER,
        PRIMARY KEY (from_tag, to_tag)
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        account_id INTEGER PRIMARY KEY,
        reputation INTEGER,
        user_id INTEGER,
        user_type TEXT,
        accept_rate INTEGER,
        profile_image TEXT,
        display_name TEXT,
        link TEXT
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS questions (
        question_id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        tags TEXT,
        owner_id INTEGER,
        is_answered BOOLEAN,
        view_count INTEGER,
        bounty_amount INTEGER,
        bounty_closes_date INTEGER,
        answer_count INTEGER,
        score INTEGER,
        last_activity_date INTEGER,
        creation_date INTEGER,
        last_edit_date INTEGER,
        content_license TEXT,
        link TEXT NOT NULL,
        body TEXT NULL,
        error BOOLEAN
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS answers (
        answer_id INTEGER PRIMARY KEY,
        question_id INTEGER NOT NULL,
        owner_id INTEGER,
        is_accepted BOOLEAN,
        score INTEGER,
        last_activity_date INTEGER,
        last_edit_date INTEGER,
        creation_date INTEGER,
        content_license TEXT,
        body TEXT,
        error BOOLEAN
    )
    ''')
    
    conn.commit() 
    
def insert_post_data(conn, data):
    cursor = conn.cursor()
    # Prepare data tuple
    post_data = (
        data.get('Id'), data.get('PostTypeId'), data.get('AcceptedAnswerId'), 
        data.get('CreationDate'), data.get('Score'), data.get('ViewCount'), 
        data.get('Body'), data.get('OwnerUserId'), data.get('LastEditorUserId'), 
        data.get('LastEditorDisplayName'), data.get('LastEditDate'), 
        data.get('LastActivityDate'), data.get('Title'), 
        data.get('Tags'), data.get('AnswerCount'), data.get('CommentCount'), 
        data.get('FavoriteCount'), data.get('CommunityOwnedDate'), 
        data.get('ContentLicense')
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

def insert_tag_data(conn, name, count, has_synonyms):
    """
    Inserts tag data into the SQLite database.
    """
    cursor = conn.cursor()
    cursor.execute(f'''
    INSERT INTO tags (name, count, has_synonyms) 
    VALUES ({PLACE_HOLDER}, {PLACE_HOLDER}, {PLACE_HOLDER})
    ON CONFLICT(name) DO UPDATE SET 
        count = EXCLUDED.count, 
        has_synonyms = EXCLUDED.has_synonyms
    ''', 
    (name, count, has_synonyms))
    conn.commit()

def insert_tag_synonym_data(conn, from_tag, to_tag, creation_date, last_applied_date, applied_count):
    """
    Inserts a tag synonym into the SQLite database.
    """  
    cursor = conn.cursor()
    cursor.execute(f'''
    INSERT INTO tag_synonyms (from_tag, to_tag, creation_date, last_applied_date, applied_count)
    VALUES ({PLACE_HOLDER}, {PLACE_HOLDER}, {PLACE_HOLDER}, {PLACE_HOLDER}, {PLACE_HOLDER})
    ON CONFLICT(from_tag, to_tag) DO UPDATE SET 
        creation_date = EXCLUDED.creation_date, 
        last_applied_date = EXCLUDED.last_applied_date, 
        applied_count = EXCLUDED.applied_count
    ''', 
    (from_tag, to_tag, creation_date, last_applied_date, applied_count))
    conn.commit()

def insert_user_data(conn, account_id, reputation, user_id, user_type, accept_rate, profile_image, display_name, link):
    """
    Inserts user data into the SQLite database.
    """
    cursor = conn.cursor()
    cursor.execute(f'''
    INSERT INTO users (account_id, reputation, user_id, user_type, accept_rate, profile_image, display_name, link) 
    VALUES ({PLACE_HOLDER}, {PLACE_HOLDER}, {PLACE_HOLDER}, {PLACE_HOLDER}, {PLACE_HOLDER}, {PLACE_HOLDER}, {PLACE_HOLDER}, {PLACE_HOLDER})
    ON CONFLICT(account_id) DO UPDATE SET 
        reputation = EXCLUDED.reputation, 
        user_id = EXCLUDED.user_id, 
        user_type = EXCLUDED.user_type, 
        accept_rate = EXCLUDED.accept_rate, 
        profile_image = EXCLUDED.profile_image, 
        display_name = EXCLUDED.display_name, 
        link = EXCLUDED.link
    ''', 
    (account_id, reputation, user_id, user_type, accept_rate, profile_image, display_name, link))
    conn.commit()

def insert_question_data(conn, question_id, title, tags, owner_id, is_answered, view_count, bounty_amount, bounty_closes_date, answer_count, score, last_activity_date, creation_date, last_edit_date, content_license, link, body, error):
    """
    Inserts or updates question data into the SQLite database.
    """
    cursor = conn.cursor()
    cursor.execute(f'''
    INSERT INTO questions (question_id, title, tags, owner_id, is_answered, view_count, bounty_amount, bounty_closes_date, answer_count, score, last_activity_date, creation_date, last_edit_date, content_license, link, body, error) 
    VALUES ({PLACE_HOLDER}, {PLACE_HOLDER}, {PLACE_HOLDER}, {PLACE_HOLDER}, {PLACE_HOLDER}, {PLACE_HOLDER}, {PLACE_HOLDER}, {PLACE_HOLDER}, {PLACE_HOLDER}, {PLACE_HOLDER}, {PLACE_HOLDER}, {PLACE_HOLDER}, {PLACE_HOLDER}, {PLACE_HOLDER}, {PLACE_HOLDER}, {PLACE_HOLDER}, {PLACE_HOLDER})
    ON CONFLICT(question_id) DO UPDATE SET 
        title = EXCLUDED.title, 
        tags = EXCLUDED.tags, 
        owner_id = EXCLUDED.owner_id, 
        is_answered = EXCLUDED.is_answered, 
        view_count = EXCLUDED.view_count, 
        bounty_amount = EXCLUDED.bounty_amount, 
        bounty_closes_date = EXCLUDED.bounty_closes_date, 
        answer_count = EXCLUDED.answer_count, 
        score = EXCLUDED.score, 
        last_activity_date = EXCLUDED.last_activity_date, 
        creation_date = EXCLUDED.creation_date, 
        last_edit_date = EXCLUDED.last_edit_date, 
        content_license = EXCLUDED.content_license, 
        link = EXCLUDED.link,
        body = EXCLUDED.body,
        error = EXCLUDED.error
    ''', 
    (question_id, title, tags, owner_id, is_answered, view_count, bounty_amount, bounty_closes_date, answer_count, score, last_activity_date, creation_date, last_edit_date, content_license, link, body, error))
    conn.commit()

def insert_answer_data(conn, answer_id, question_id, owner_id, is_accepted, score, last_activity_date, last_edit_date, creation_date, content_license, body, error):
    """
    Inserts or updates answer data into the SQLite database.
    """
    cursor = conn.cursor()
    cursor.execute(f'''
    INSERT INTO answers (answer_id, question_id, owner_id, is_accepted, score, last_activity_date, last_edit_date, creation_date, content_license, body, error) 
    VALUES ({PLACE_HOLDER}, {PLACE_HOLDER}, {PLACE_HOLDER}, {PLACE_HOLDER}, {PLACE_HOLDER}, {PLACE_HOLDER}, {PLACE_HOLDER}, {PLACE_HOLDER}, {PLACE_HOLDER}, {PLACE_HOLDER}, {PLACE_HOLDER})
    ON CONFLICT(answer_id) DO UPDATE SET 
        question_id = EXCLUDED.question_id,
        owner_id = EXCLUDED.owner_id,
        is_accepted = EXCLUDED.is_accepted,
        score = EXCLUDED.score,
        last_activity_date = EXCLUDED.last_activity_date,
        last_edit_date = EXCLUDED.last_edit_date,
        creation_date = EXCLUDED.creation_date,
        content_license = EXCLUDED.content_license,
        body = EXCLUDED.body,
        error = EXCLUDED.error
    ''', 
    (answer_id, question_id, owner_id, is_accepted, score, last_activity_date, last_edit_date, creation_date, content_license, body, error))
    conn.commit()
    
def get_nonexistent_question_ids(conn, question_ids):
    """
    Returns the IDs from question_ids that are not found in the questions table.
    """

    comma_separated_ids = ', '.join(map(str, question_ids))
    
    cursor = conn.cursor()
    query = f"SELECT question_id FROM questions WHERE question_id IN ({comma_separated_ids})"
    cursor.execute(query)
    
    # Fetch all existing question_ids from the query result
    existing_question_ids = [row[0] for row in cursor.fetchall()]

    # Determine which of the provided question_ids are not found in the existing_question_ids
    nonexistent_question_ids = [question_id for question_id in question_ids if question_id not in existing_question_ids]
    
    return nonexistent_question_ids

def get_nonexistent_answer_ids(conn, answer_ids):
    """
    Returns the IDs from answer_ids that are not found in the answers table.
    """

    comma_separated_ids = ', '.join(map(str, answer_ids))
    
    cursor = conn.cursor()
    query = f"SELECT answer_id FROM answers WHERE answer_id IN ({comma_separated_ids})"
    cursor.execute(query)
    
    # Fetch all existing answer_ids from the query result
    existing_answer_ids = [row[0] for row in cursor.fetchall()]

    # Determine which of the provided answer_ids are not found in the existing_answer_ids
    nonexistent_answer_ids = [answer_id for answer_id in answer_ids if answer_id not in existing_answer_ids]
    
    return nonexistent_answer_ids