from flask import Flask, render_template, request
from lexer_parser.lexer import prueba as run_lexer
from lexer_parser.parser import parse_syntax, count_tokens

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
        
        # Ejecutar el análisis léxico
        tokens = run_lexer(text)
        
        # Contar los tipos de tokens
        token_counts = count_tokens(tokens)
        
        # Ejecutar el análisis sintáctico
        syntax_result = parse_syntax(text)
    
    return render_template(
        "index.html", 
        text=text, 
        tokens=tokens, 
        syntax_result=syntax_result,
        token_counts=token_counts
    )

if __name__ == "__main__":
    app.run(debug=True)