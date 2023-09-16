from flask import Flask, jsonify, request
from urllib.parse import unquote
from flask_limiter import Limiter
from langchain import OpenAI
from langchain.document_loaders import SeleniumURLLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document
import logging
import os

# Setup Logging
logging.basicConfig(level=logging.INFO)

# Initialize app
app = Flask(__name__)

#A way to get the IP address of the incoming request for rate limiting
def get_remote_address():
    return request.remote_addr

limiter = Limiter(app, key_func=get_remote_address)

# Load OpenAI API Key from environment variables
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')

# Initialize OpenAI
llm = OpenAI(model_name='gpt-4', api_key=OPENAI_API_KEY)

#1. Extract Data From the Website, where a user can submit a URL and the app will extract the text from the website.
def extract_data_website(url):
    """Extracts data from a given URL."""
    loader = SeleniumURLLoader([url])
    data = loader.load()
    text = ""
    for page in data:
        text += page.page_content + " "
    return text

#2. Generate a Summary of the Text, by first chunking the text into smaller pieces and then generating a summary for each chunk and finally pass all the summaries to the summarizer to generate a final summary.
def split_text_chunks_and_summary_generator(text):
    """Splits the text into chunks and generates a summary."""
    text_splitter = CharacterTextSplitter(separator='\n', chunk_size=2000, chunk_overlap=20)
    text_chunks = text_splitter.split_text(text)
    logging.info(f"Number of text chunks: {len(text_chunks)}")
    docs = [Document(page_content=t) for t in text_chunks]
    chain = load_summarize_chain(llm=llm, chain_type='map_reduce', verbose=True)
    summary = chain.run(docs)
    return summary


@app.route('/', methods=['GET'])
def home():
    return "Summarizes any text you want!"


@limiter.limit("5 per minute")
@app.route('/summary_generate', methods=['GET'])
def summary_generator():
    try:
        encode_url = unquote(unquote(request.args.get('url')))
        if not encode_url:
            return jsonify({'error': 'URL is required'}), 400
        text = extract_data_website(encode_url)
        summary = split_text_chunks_and_summary_generator(text)
        response = {
            'submitted_url': encode_url,
            'summary': summary
        }
        return jsonify(response)
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return jsonify({'error': 'An error occurred while processing your request.'}), 500


if __name__ == '__main__':
    app.run(debug=True)
