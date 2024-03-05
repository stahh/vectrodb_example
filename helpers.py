import os
from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import Neo4jVector
from langchain_community.embeddings import TensorflowHubEmbeddings
import logging
from logging import handlers

from conf import CHECK_FILE, DIR_NAME, NEO4J_PASS, NEO4J_URL, NEO4J_USER


def init_db(logger):
    """
    Just for application test
    Load data to Neo4j if file "init" is missing.
    :return: None
    """
    if os.path.exists(CHECK_FILE):
        return
    logger.info('Start load data...')
    loader = DirectoryLoader(DIR_NAME)
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)

    try:
        Neo4jVector.from_documents(
            docs,
            TensorflowHubEmbeddings(),
            url=NEO4J_URL,
            username=NEO4J_USER,
            password=NEO4J_PASS,
            search_type="hybrid",
        )
        with open(CHECK_FILE, 'w'):
            ...
        logger.info('Data loaded')
    except Exception as e:
        logger.error(e)


def init_logger(module: str):
    """
    Create logger hadlers with formatting
    :param module: str: module name
    :return: Logger: logger object
    """
    root_path = os.path.dirname(os.path.realpath(module))
    name = '.'.join(os.path.basename(module).split('.')[:-1])
    log_dir = f'{root_path}/logs/'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(threadName)s %(filename)s:"
        "%(lineno)-4d - %(message)s")

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    file_handler_error = logging.handlers.RotatingFileHandler(
        f"{log_dir}{name}_error.log", maxBytes=100 * 1024 * 1024,
        backupCount=5, encoding='utf8')
    file_handler_error.setFormatter(formatter)
    file_handler_error.setLevel(logging.ERROR)
    logger.addHandler(file_handler_error)

    stdout_handler = logging.StreamHandler()
    stdout_handler.setFormatter(formatter)
    stdout_handler.setLevel(logging.INFO)
    logger.addHandler(stdout_handler)
    return logger
