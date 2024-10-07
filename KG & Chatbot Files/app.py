from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from build_graph import KnowledgeGraph
from happytransformer import HappyTextToText, TTSettings
happy_tt = HappyTextToText("T5", "grammar_model")
args = TTSettings(num_beams=5, min_length=1)
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# Loading knowledge graph
kg = KnowledgeGraph('data/disease_cleaned.json')

@app.route('/')
def index():
    return render_template('chat.html')


@app.route('/grammar', methods=['GET','POST'])
def grammar_enhancer():
    user_input = request.json['input']
    print('User-input ==== :', user_input)
    result = happy_tt.generate_text("grammar: " +user_input, args=args)
    print('enhanced input ==== :', result.text)
    return jsonify({'result':result.text})


@app.route('/api', methods=['POST'])
def process_query():
    user_input = request.json['input']

    result = kg.bfs_search(user_input, 'description') 

    return jsonify({'output': result}) 

if __name__ == '__main__':
    app.run(debug=True)
