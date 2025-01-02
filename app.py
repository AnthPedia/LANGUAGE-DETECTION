from flask import Flask, request, jsonify
from sklearn import feature_extraction, pipeline
from sklearn.svm import SVC
from sklearn.feature_extraction.text import TfidfVectorizer
from flask_cors import CORS
from nltk.tokenize import word_tokenize
import pandas as pd
import string

app = Flask(__name__)
CORS(app)

df = pd.read_csv('./Dataset/Language Detection.csv')
punctuation_list = string.punctuation

def preprocess_text(text, lang="english"):
    
    words = word_tokenize(text)
    
    words = [word for word in words if word not in string.punctuation]

    words = [word for word in words if word.isalpha()]
    
    preprocessed_text = ' '.join(words)
    return preprocessed_text

df['Text'] = df['Text'].apply(preprocess_text)

text = df['Text']
language = df['Language']
tfidf = TfidfVectorizer(ngram_range=(2, 3), analyzer='char')
model_pipe = pipeline.Pipeline([('tfidf', tfidf), ('clf', SVC())])
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
