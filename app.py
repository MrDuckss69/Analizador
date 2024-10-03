from flask import Flask, render_template, request
from lexer_parser.lexer import prueba as run_lexer
from lexer_parser.parser import parse_syntax

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    text = ""
    tokens = []
    syntax_result = {}
    
    if request.method == "POST":
        text = request.form["text"]
        
        # Ejecutar el análisis léxico
        tokens = run_lexer(text)
        
        # Ejecutar el análisis sintáctico
        syntax_result = parse_syntax(text)
    
    return render_template(
        "index.html", 
        text=text, 
        tokens=tokens, 
        syntax_result=syntax_result
    )

if __name__ == "__main__":
    app.run(debug=True)
