import sqlite3

def save_to_database(data, db_name="corpus.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS posts (id TEXT PRIMARY KEY, content TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS comments (id TEXT PRIMARY KEY, post_id TEXT, content TEXT)''')


    for i, item in enumerate(data):
        post_id = f"post_{i}"
        cursor.execute("INSERT OR REPLACE INTO post (id, content) VALUES (?, ?)", (post_id, ' '.join(item['post'])))
        
        for j, comment in enumerate(item['comments']):
            comment_id = f"comment_{j}"
            cursor.execute('INSERT OR REPLACE INTO comments (id, post_id, content) VALUES (?, ?, ?)', (comment_id, post_id, ' '.join(comment)))

    conn.commit()
    conn.close()

save_to_database(preprocessed_data)
