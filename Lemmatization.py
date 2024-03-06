from nltk.stem import WordNetLemmatizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
import pandas as pd
import nltk

nltk.download('wordnet')
nltk.download('omw-1.4')

def lemmatize_sentences(column):
    lemmatizer = WordNetLemmatizer()
    lemmatized_sentences = []

    for sentence in column:
        if pd.notna(sentence):  # Check if the sentence is not NaN
            words = sentence.split()
            lemmatized_words = [lemmatizer.lemmatize(word) for word in words]
            lemmatized_sentence = ' '.join(lemmatized_words)
            lemmatized_sentences.append(lemmatized_sentence)

    return lemmatized_sentences

def generate_summary(responses):
    full_text = '.'.join(responses)
    parser = PlaintextParser.from_string(full_text, Tokenizer("english"))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, sentences_count=3)  # Adjust sentences_count as needed
    return ' '.join(str(sentence) for sentence in summary)