import json
import sqlite3

DATA_FILE = "data/quotes.json"
DATABASE = "data/quotes.db"

def migrate_json_to_db():
    with open(DATA_FILE, encoding="utf-8") as f:
        quotes = json.load(f)

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    for q in quotes:
        cursor.execute("""
            INSERT INTO quotes (text, author, tags, note, favorite, language, result)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            q.get("text", ""),
            q.get("author", ""),
            ",".join(q.get("tags", [])),
            q.get("note", ""),
            int(q.get("favorite", False)),
            q.get("language", "unknown"),
            q.get("result", "")
        ))

    conn.commit()
    conn.close()
    print(f"{len(quotes)}件の引用をDBに移行しました。")

if __name__ == "__main__":
    migrate_json_to_db()
