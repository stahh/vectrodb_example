from flask import Flask, request, jsonify, render_template
from langchain_community.vectorstores import Neo4jVector
from langchain_community.embeddings import TensorflowHubEmbeddings

# local import
from conf import NEO4J_URL, NEO4J_PASS, NEO4J_USER
from helpers import init_logger, init_db

app = Flask(__name__)
logger = init_logger(__file__)
init_db(logger)



@app.route('/')
def index():
    """
    Render index template
    :return: str
    """
    return render_template('index.html')


@app.route('/search', methods=["POST"])
def search():
    """
    Get request string, search in Vector index and return results with scores
    :return: flask.wrappers.Response
    """
    to_search = request.json.get('text')
    try:
        hybrid_db = Neo4jVector(
            TensorflowHubEmbeddings(),
            url=NEO4J_URL,
            username=NEO4J_USER,
            password=NEO4J_PASS,
            search_type="hybrid",
        )
        results = hybrid_db.similarity_search_with_score(to_search, k=5)
        results = [{'score': x[1], 'document':
            x[0].to_json().get('kwargs', {}).get('page_content')}
                   for x in results]
        return jsonify({"result": results})
    except Exception as e:
        logger.error(e)
        return jsonify({"error": repr(e)})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555, debug=True)
