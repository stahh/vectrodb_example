import os

DIR_NAME = 'articles'
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
NEO4J_PASS = os.getenv("NEO4J_PASSWORD")
NEO4J_USER = 'neo4j'
NEO4J_URL = 'bolt://neo4j:7687'
CHECK_FILE = './init'

for name, value in [('OPENAI_KEY', OPENAI_KEY),
                    ('NEO4J_PASS', NEO4J_PASS), ]:
    if not value:
        raise RuntimeError(
            f'Missing ENV variable(s). {name} = {value}')
