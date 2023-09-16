# Web Content Summarizer API

## Overview

The Web Content Summarizer API is a Flask-based application that allows users to summarize articles, blog posts, or any web content by passing in the URL. This API leverages the power of GPT-4 and the langchain library to extract and summarize content.

## Features

- Extracts content from a given URL
- Splits the content into manageable chunks
- Summarizes each chunk using GPT-4
- Returns a final summarized version of the entire content

## Architecture diagram

## Prerequisites

- Python 3.x
- Flask
- langchain
- Selenium

## Installation

First, clone the repository to your local machine:

```bash
git clone https://github.com/yourusername/Web-Content-Summarizer-API.git
```

Navigate to the project directory:

```bash
cd content-Summarizer-API
```

Install the required packages:

```bash
pip install -r requirements.txt
```

## Usage

Set your OpenAI API key as an environment variable:

```bash
export OPENAI_API_KEY=your_openai_api_key_here
```

Run the Flask application:

```bash
python app.py
```

To summarize a web page, make a GET request to the `/summary_generate` endpoint with the `url` parameter:

```bash
http://127.0.0.1:5000/summary_generate?url=http%3A%2F%2Fexample.com
```

## API Rate Limiting

The API is rate-limited to 5 requests per minute per IP address.

## Contributing

Feel free to fork the repository and submit pull requests.
