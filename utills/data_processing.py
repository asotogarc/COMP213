# Importamos las librerias necesarias
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
import nltk

# Descargamos stopwords en español
nltk.download('stopwords')
stop_words = set(stopwords.words('spanish'))

# Función para limpiar el texto
def clean_text(text):
    # Convert text to lowercase and split into words
    words = text.lower().split()
    # Remove stopwords
    cleaned_words = [word for word in words if word not in stop_words]
    # Join the cleaned words back into a string
    return ' '.join(cleaned_words)
    
# Comparamos la similitud entre una oferta y una candidatura
def calculate_similarity(offer, candidate):
    # Clean and combine offer text fields
    offer_text = clean_text(f"{offer['Formación']} {offer['Conocimientos']} {offer['Experiencia']} {offer['Funciones']}")
    
    # Clean and combine candidate text fields
    candidate_text = clean_text(f"{candidate['Formación']} {candidate['Conocimientos']} {candidate['Experiencia']}")
    
    # Create TF-IDF vectorizer without specifying stopwords (we've already removed them)
    tfidf = TfidfVectorizer()
    
    # Transform the texts
    X = tfidf.fit_transform([offer_text, candidate_text])
    
    # Calculate cosine similarity
    cosine_sim = cosine_similarity(X[0:1], X[1:2])[0][0]
    
    # Get feature names and scores
    feature_names = tfidf.get_feature_names_out()
    offer_scores = X[0].toarray()[0]
    candidate_scores = X[1].toarray()[0]
    
    # Create a dictionary of terms and their scores
    terms_scores = {feature: (offer_scores[i], candidate_scores[i]) for i, feature in enumerate(feature_names)}
    
    # Sort terms by combined score
    sorted_terms = sorted(terms_scores.items(), key=lambda x: sum(x[1]), reverse=True)
    
    # Get top 10 terms
    top_terms = sorted_terms[:10]
    
    return cosine_sim * 100, top_terms
