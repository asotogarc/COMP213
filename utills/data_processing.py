# Importamos las librerias necesarias
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
import nltk

# Descargamos stopwords en español
nltk.download('stopwords')
stop_words = set(stopwords.words('spanish'))

# Comparamos la similitud entre una oferta y una candidatura
def calculate_similarity(offer, candidate):
    tfidf = TfidfVectorizer(stop_words=list(stop_words))
    
    # Eliminamos las stop words de los textos
    offer_text = ' '.join([word for word in f"{offer['Formación']} {offer['Conocimientos']} {offer['Experiencia']} {offer['Funciones']}".split() if word.lower() not in stop_words])
    candidate_text = ' '.join([word for word in f"{candidate['Formación']} {candidate['Conocimientos']} {candidate['Experiencia']}".split() if word.lower() not in stop_words])
    
    X = tfidf.fit_transform([offer_text, candidate_text])
    cosine_sim = cosine_similarity(X[0:1], X[1:2])[0][0]
    feature_names = tfidf.get_feature_names_out()
    offer_scores = X[0].toarray()[0]
    candidate_scores = X[1].toarray()[0]
    
    terms_scores = {feature: (offer_scores[i], candidate_scores[i]) for i, feature in enumerate(feature_names)}
    
    sorted_terms = sorted(terms_scores.items(), key=lambda x: sum(x[1]), reverse=True)
    
    top_terms = sorted_terms[:10]  
    return cosine_sim * 100, top_terms
