from flask import Flask, request, jsonify
from flask_cors import CORS
from qa_engine import get_answer_from_query, load_and_index_documents

app = Flask(__name__)
CORS(app)

print("Indexing documents...")
load_and_index_documents()

@app.route("/ask", methods=["POST"])
def ask_question():
    data = request.json
    query = data.get("question", "")
    if not query:
        return jsonify({"error": "No question provided"}), 400
    answer = get_answer_from_query(query)
    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(debug=True)
