from flask import Flask, render_template, request, redirect, url_for
import os
import sqlite3

app = Flask(__name__)
DATABASE = 'data/quotes.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def load_quotes_from_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM quotes")
    rows = cursor.fetchall()
    conn.close()

    quotes = []
    for row in rows:
        quotes.append({
            "id": row["id"],
            "text": row["text"],
            "author": row["author"],
            "tags": row["tags"].split(",") if row["tags"] else [],
            "note": row["note"],
            "favorite": bool(row["favorite"]),
            "language": row["language"],
            "result": row["result"]
        })
    return quotes


@app.route("/", methods=["GET"])
def index():
    def safe_lower(val):
        return val.lower() if isinstance(val, str) else ""

    quotes = load_quotes_from_db()
    
    query = request.args.get("q", "").lower()
    selected_lang = request.args.get("lang", "").lower()

    if selected_lang:
        quotes = [q for q in quotes if q.get("language", "").lower() == selected_lang]
    print(f"フィルター後の引用数: {len(quotes)}")

    if query:
        quotes = [
            q for q in quotes if
            query in safe_lower(q.get("text")) or
            query in safe_lower(q.get("author")) or
            query in safe_lower(q.get("note")) or
            any(query in tag.lower() for tag in q.get("tags", []))
        ]
    print(f"検索後の引用数: {len(quotes)}")

    sample_quotes = {
        "python": "print('Hello, world!')",
        "html": "<!DOCTYPE html>\n<html>\n  <head>...</head>\n</html>",
        "css": "body {\n  background: #fff;\n}",
        "javascript": "console.log('Hello!');",
        "php": "<?php echo 'Hello'; ?>",
        "java": "public class Main { public static void main(String[] args) {} }",
        "jsp": "<%@ page language=\"java\" %>\n<html>...</html>",
        "servlet": "public class HelloServlet extends HttpServlet { ... }",
        "sql": "SELECT * FROM users;"
    }

    return render_template(
        "index.html",
        quotes=quotes,
        current_lang=selected_lang if selected_lang else None,
        languages=list(sample_quotes.keys()),
        sample_quotes=sample_quotes,
        search_query=query
    )

@app.route("/add", methods=["POST"])
def add_quote():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO quotes (text, author, tags, note, favorite, language, result)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        request.form.get("text", ""),
        request.form.get("author", ""),
        ",".join([tag.strip() for tag in request.form.get("tags", "").split(",") if tag.strip()]),
        request.form.get("note", ""),
        int("favorite" in request.form),
        request.form.get("language", "unknown"),
        request.form.get("result", "")
    ))
    conn.commit()
    conn.close()
    return redirect("/")

@app.route('/edit/<int:quote_id>', methods=['GET', 'POST'])
def edit_quote(quote_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        cursor.execute("""
            UPDATE quotes SET
                text = ?, author = ?, tags = ?, note = ?, favorite = ?, language = ?, result = ?
            WHERE id = ?
        """, (
            request.form.get('text', ''),
            request.form.get('author', ''),
            ",".join([tag.strip() for tag in request.form.get('tags', '').split(',') if tag.strip()]),
            request.form.get('note', ''),
            int('favorite' in request.form),
            request.form.get('language', 'unknown'),
            request.form.get('result', ''),
            quote_id
        ))
        conn.commit()
        conn.close()
        return redirect("/")

    cursor.execute("SELECT * FROM quotes WHERE id = ?", (quote_id,))
    row = cursor.fetchone()
    conn.close()

    if row is None:
        return "引用が見つかりません", 404

    quote = {
        "id": row["id"],
        "text": row["text"],
        "author": row["author"],
        "tags": row["tags"].split(",") if row["tags"] else [],
        "note": row["note"],
        "favorite": bool(row["favorite"]),
        "language": row["language"],
        "result": row["result"]
    }
    return render_template('edit.html', quote=quote, quote_id=quote_id)

@app.route('/delete/<int:quote_id>', methods=['POST'])
def delete_quote(quote_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM quotes WHERE id = ?", (quote_id,))
    conn.commit()
    conn.close()
    return redirect("/")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
