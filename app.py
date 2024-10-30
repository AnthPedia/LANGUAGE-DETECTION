from flask import Flask, request, jsonify
from sklearn import feature_extraction, pipeline
from sklearn.linear_model import LogisticRegression
from flask_cors import CORS
import pandas as pd
import string

app = Flask(__name__)
CORS(app)

df = pd.read_csv('./Dataset/Language Detection.csv')
punctuation_list = string.punctuation
def remove_punctuation(text):
    for pun in punctuation_list:
        text = text.replace(pun, "")
    return text.lower()

df['Text'] = df['Text'].apply(remove_punctuation)

text = df['Text']
language = df['Language']
tfidf = feature_extraction.text.TfidfVectorizer(ngram_range=(2, 3), analyzer='char')
model_pipe = pipeline.Pipeline([('tfidf', tfidf), ('clf', LogisticRegression(max_iter=1000))])
model_pipe.fit(text, language)

@app.route('/predict', methods=['POST'])
def predict_language():
    
    data = request.json
    text = data.get('text')
    
    if not text:
        return jsonify({'error': 'No text provided'}), 400

    prediction = model_pipe.predict([text])[0]
    
    return jsonify({'language': prediction})

if __name__ == '__main__':
    app.run(debug=True)
