import json
import string

# Load reviews from JSON files
def load_reviews(file_path):
    with open(file_path, "r") as file:
        reviews = json.load(file)
    return reviews

# Preprocess function
def preprocess(text, stop_words):
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    tokens = text.split()
    tokens = [word for word in tokens if word not in stop_words]
    return " ".join(tokens)