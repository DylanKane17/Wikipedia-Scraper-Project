'''This module instantiates flask to run the web application'''

from flask import Flask, jsonify, request
from flask_cors import CORS
import scraper
import ai

app = Flask(__name__)
cors = CORS(app, origins='*')

@app.route("/")
def index():
    '''Handles requests to root url'''
    pass

@app.route('/generate-summaries', methods=['POST'])
def process_source_summaries():
    '''Scrapes wikipedia url; obtains citations; summarises them in accordance with robots.txt'''

    url = request.json['url']
    print(url)
    source_objects = scraper.scrape_wiki(url)
    summarised_source_objects = []

    for i, source in enumerate(source_objects):
        if i > 30: #upper limit
            break

        source_text = scraper.scrape_source(source['href'])
        print(source_text)

        if source_text and source_text != "Disallowed":
            source_summary = ai.summarise_source(source_text)
            source['summary'] = source_summary
            summarised_source_objects.append(source)
        else:
            source_summary = "Unable to provide summary."
    
    return jsonify(summarised_source_objects), 200

if __name__ == "__main__":
    app.run(debug=True, port=5000)
