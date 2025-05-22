from flask import Flask, render_template, request, redirect
import json, os

app = Flask(__name__)
DATA_FILE = "data/quotes.json"

def load_quotes():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, encoding='utf-8') as f:
        return json.load(f)

def save_quotes(quotes):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(quotes, f, ensure_ascii=False, indent=2)

@app.route("/")
def index():
    quotes = load_quotes()
    query = request.args.get("q", "").lower()
    selected_lang = request.args.get("lang", "").lower()

    if selected_lang:
        quotes = [q for q in quotes if q.get("language", "").lower() == selected_lang]

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
        sample_quotes=sample_quotes
    )

@app.route("/add", methods=["POST"])
def add_quote():
    quotes = load_quotes()
    new_quote = {
        "text": request.form.get("text", ""),
        "author": request.form.get("author", ""),
        "tags": [tag.strip() for tag in request.form.get("tags", "").split(",") if tag.strip()],
        "note": request.form.get("note", ""),
        "favorite": "favorite" in request.form,
        "language": request.form.get("language", "unknown"),
        "result": request.form.get("result", "")
    }
    quotes.append(new_quote)
    save_quotes(quotes)
    return redirect("/")

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
