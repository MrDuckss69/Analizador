from flask import Flask, render_template, request
from lexer import prueba as run_lexer
from parser import parse_syntax, count_tokens

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    text = ""
    tokens = []
    syntax_result = {}
    token_counts = {
        "total": 0,
        "reserved_words": 0,
        "identifiers": 0,
        "variables": 0,
        "numbers": 0,
        "symbols": 0
    }
    
    if request.method == "POST":
        text = request.form["text"]
        tokens = run_lexer(text)
        token_counts = count_tokens(tokens)
        syntax_result = parse_syntax(text)
    
    return render_template("index.html", text=text, tokens=tokens, token_counts=token_counts, syntax_result=syntax_result)

if __name__ == "__main__":
    app.run(debug=True)