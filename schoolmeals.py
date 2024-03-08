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

    return sentiments

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

def MostFreq(df, col_name, top_N=10, isWord=False):
    all_text = ','.join(df[col_name].astype(str))

    if isWord:
        print('\n Print word frequency:\n')
        mostFreq = WordFreq(all_text)
    else:
        print('\n Print sentence frequency:\n')
        phrases = [phrase.strip() for phrase in all_text.split(',')]
        mostFreq = FreqDist(phrases)

    word_counts = Counter(mostFreq)
    most_common_words = word_counts.most_common(top_N)

    for word, frequency in most_common_words:
        print(f'{word}: {frequency}\n')

    most_common_words_df = pd.DataFrame(most_common_words, columns=['Phrase', 'Frequency'])

    most_common_words_df = most_common_words_df.sort_values(by='Frequency', ascending=False)

    return most_common_words_df

def AppendSheet(xls_name, sheet_name, df):
    with pd.ExcelWriter(xls_name, engine='openpyxl', mode='a') as writer:
        df.to_excel(writer, sheet_name=sheet_name, index=False)

def AppendFreqSheet(xls_name, col_name, sheet_name, df):
    freq = MostFreq(df, col_name)

    AppendSheet(xls_name, sheet_name, freq)

def AppendSentimentSheet(xls_name, sheet_name, df, positive_sentiment_threshold=0.4):
    sentiment_df = pd.DataFrame(columns=['Positive Responses', 'Negative or Neutral Responses'])

    for index, row in df.iloc[1:].iterrows():
        compound = row['Q36_4_TEXT_SENTIMENT']['compound']
        phrase = row['Q36_4_TEXT']

        if compound >= positive_sentiment_threshold:
            sentiment_df.loc[len(sentiment_df)] = [phrase, None]
        else:
            sentiment_df.loc[len(sentiment_df)] = [None, phrase]

    sentiment_df = sentiment_df.dropna(subset=['Positive Responses', 'Negative or Neutral Responses'], how='all')

    with pd.ExcelWriter(xls_name, engine='openpyxl', mode='a') as writer:
        sentiment_df.to_excel(writer, sheet_name=sheet_name, index=False)

def main():
    school_xsl = 'SurveyData/School_2_2021.xlsx'
    df = pd.read_excel(school_xsl)

    nltk.download('vader_lexicon')

    sentimentAnalysis(df, 'Q36_4_TEXT')

    df.to_excel(school_xsl, sheet_name='Sheet1', index=False)

    AppendSentimentSheet(school_xsl, sheet_name='Q36_SENTIMENTS', df=df, positive_sentiment_threshold=0.4)

    AppendFreqSheet(xls_name=school_xsl, col_name='Q28', sheet_name='Freq_Q28', df=df)

    AppendFreqSheet(school_xsl, 'Q30', 'Freq_Q30', df)

    AppendFreqSheet(school_xsl, 'Q29_1', 'School_Meal_Rating_Q29', df)

    AppendFreqSheet(school_xsl, 'Q36', 'Meat_Free_Days_Q36', df)

main()
