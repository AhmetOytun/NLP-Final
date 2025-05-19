import random
from nltk.corpus import stopwords
import random
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score
from utils.helper import load_reviews, preprocess

# Load reviews from JSON files
positive_reviews = load_reviews("./playwright_scraper/positive_reviews.json")
negative_reviews = load_reviews("./playwright_scraper/negative_reviews.json")

# Combine and shuffle data
reviews = positive_reviews + negative_reviews

# Create labels
labels = ["Positive"] * len(positive_reviews) + ["Negative"] * len(negative_reviews)

# Shuffle data
combined = list(zip(reviews, labels))
random.shuffle(combined)

# Unzip the combined list
reviews, labels = zip(*combined)

# Preprocessing
stop_words = set(stopwords.words("english"))

# Preprocess function
reviews = [preprocess(review, stop_words) for review in reviews]

# Vectorization
vectorizer = TfidfVectorizer(max_features=5000)
X = vectorizer.fit_transform(reviews)
y = labels

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model training
clf = LogisticRegression()
clf.fit(X_train, y_train)

# Evaluation
y_pred = clf.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

# Example inference
def predict_sentiment(review: str):
    processed = preprocess(review, stop_words)
    vectorized = vectorizer.transform([processed])
    return clf.predict(vectorized)[0]

# Example usage
print("\nExample prediction:")
print(predict_sentiment("This movie was great! Loved it!"))
print(predict_sentiment("Movie was stupid, boring and i hated it."))
print(predict_sentiment("Movie was shit, insanely bad."))
print(predict_sentiment("It was great and beautiful"))
print(predict_sentiment("Magnificent experience"))
print(predict_sentiment("Terrible movie, I will never watch it again"))
print(predict_sentiment("Absolutely loved the acting and the story"))
print(predict_sentiment("Not worth the time, very disappointing"))
print(predict_sentiment("A masterpiece, truly unforgettable!"))
print(predict_sentiment("Worst film I've seen in years."))
