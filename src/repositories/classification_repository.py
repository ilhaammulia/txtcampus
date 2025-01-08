import joblib
import re
import string
import os

from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

class ClassificationRepository:
    # Load the saved model and vectorizer
    model = joblib.load('src/notebook/naive_bayes_model.pkl')
    vectorizer = joblib.load('src/notebook/vectorizer.pkl')

    factory = StemmerFactory()
    stemmer = factory.create_stemmer()

    def clean_text(self, text):
        text = re.sub(r'[^\x00-\x7F]+', ' ', text)
        text = text.translate(str.maketrans('', '', string.punctuation))
        text = re.sub(r'\d+', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def preprocess_text(self, text):
        text = self.clean_text(text)  # Clean text
        text = text.lower()  # Lowercase
        text = self.stemmer.stem(text)  # Stemming
        return text

    def predict(self, text):
        text = self.preprocess_text(text)

        vectorized_text = self.vectorizer.transform([text])
        vectorized_text_dense = vectorized_text.toarray()
        prediction = self.model.predict(vectorized_text_dense)
        probabilities = self.model.predict_proba(vectorized_text_dense)

        data = {
            class_label: round(prob, 4)
            for class_label, prob in zip(self.model.classes_, probabilities[0])
        }

        return prediction[0], data[prediction[0]]
