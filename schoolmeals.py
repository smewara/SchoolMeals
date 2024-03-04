import nltk
import pandas as pd
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from collections import Counter
from nltk import Text, FreqDist

nltk.download('stopwords')
nltk.download('punkt')

def sentimentAnalysis(df, col_name):
    sia = SentimentIntensityAnalyzer()
    sentiments = []
    sentiments_col_name = col_name + '_SENTIMENT'
    
    for w in df[col_name].values:
        sentiments.append(sia.polarity_scores(str(w)))
    
    try:
        df.insert(df.columns.get_loc(col_name) + 1, sentiments_col_name, sentiments)
    except ValueError as e:
        df[sentiments_col_name] = sentiments

    print(df[sentiments_col_name])

    return df

def WordFreq(all_text):
    # Load English stop words
    stop_words = set(stopwords.words('english'))

    # Tokenize the text into words
    words = word_tokenize(all_text)

    # Filter out stop words
    filtered_words = [word.lower() for word in words if word.isalpha() and word.lower() not in stop_words]

    return filtered_words

def SentenceFreq(all_text):
    return sent_tokenize(all_text)

def MostFreq(df, col_name, top_N=10, isWord=True):
    all_text = ' '.join(df[col_name].astype(str))

    if isWord:
        print('\n Print word frequency:\n')
        mostFreq = WordFreq(all_text)
    else:
        print('\n Print sentence frequency:\n')
        phrases = [phrase.strip() for phrase in all_text.split(',')]
        mostFreq = FreqDist(phrases)

    word_counts = Counter(mostFreq)
    most_common_words = word_counts.most_common(top_N)

    text_object = Text(mostFreq)

    concordance_lists = []

    for word, frequency in most_common_words:
        print(f'{word}: {frequency}\n')
        concordance_list = text_object.concordance_list(word, lines=5)
        #print(f'Concordance for {word}: {concordance_list}\n')
        concordance_lists.append(concordance_list)

    most_common_words_df = pd.DataFrame(most_common_words, columns=['Phrase', 'Frequency'])
    #most_common_words_df['ConcordanceList'] = concordance_lists

    # Sort the DataFrame by frequency in descending order
    most_common_words_df = most_common_words_df.sort_values(by='Frequency', ascending=False)

    return most_common_words_df

def AppendSheet(xls_name, sheet_name, df):
    with pd.ExcelWriter(xls_name, engine='openpyxl', mode='a') as writer:
        df.to_excel(writer, sheet_name=sheet_name, index=False)

def main():
    school_xsl = 'SurveyData/School_1a_2021.xlsx'
    df = pd.read_excel(school_xsl)

    nltk.download('vader_lexicon')

    sentimentAnalysis(df, 'Q36_4_TEXT')

    df.to_excel(school_xsl, sheet_name='Sheet1', index=False)

    word_freq = MostFreq(df, 'Q28', isWord=False)

    AppendSheet(school_xsl, 'Word_Freq_Q28', word_freq)

    sent_freq = MostFreq(df, 'Q30', isWord=False)

    AppendSheet(school_xsl, 'Sent_Freq_Q30', sent_freq)

main()
