from flask import Flask, jsonify, request
from urllib.parse import unquote

from langchain import OpenAI
from langchain.document_loaders import SeleniumURLLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document


import os
os.environ["OPENAI_API_KEY"] = ''

app=Flask(__name__)

#1. Extract Data From the Website, where a user can submit a URL and the app will extract the text from the website.
def extract_data_website(url):
    loader=SeleniumURLLoader([url])
    data=loader.load()
    text=""
    for page in data:
        text +=page.page_content + " "
        return text
    
#2. Generate a Summary of the Text, by first chunking the text into smaller pieces and then generating a summary for each chunk and finally pass all the summaries to the summarizer to generate a final summary.
def split_text_chunks_and_summary_generator(text):
    text_splitter=CharacterTextSplitter(separator='\n',chunk_size=2000,chunk_overlap=20)
    text_chunks=text_splitter.split_text(text)
    print(len(text_chunks))
    llm = OpenAI(model_name='gpt-4')
    docs = [Document(page_content=t) for t in text_chunks]
    chain=load_summarize_chain(llm=llm, chain_type='map_reduce', verbose=True)
    summary = chain.run(docs)
    return summary


@app.route('/', methods=['GET'])
def home():
    return "Summaries any text you want!"

@app.route('/summary_generate', methods=['GET'])
def summary_generator():
    encode_url=unquote(unquote(request.args.get('url')))
    if not encode_url:
        return jsonify({'error':'URL is required'}), 400
    text=extract_data_website(encode_url)
    summary=split_text_chunks_and_summary_generator(text)
    response= {
        'submitted_url': encode_url,
        'summary': summary
    }
    return jsonify(response)
if __name__ == '__main__':
    app.run(debug=True)
