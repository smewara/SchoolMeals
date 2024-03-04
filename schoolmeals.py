import nltk
import pandas as pd
from nltk.sentiment import SentimentIntensityAnalyzer

def sentimentAnalysis(df, col_name):

    sia = SentimentIntensityAnalyzer()

    sentiments = []

    for w in df[col_name].values:
        sentiments.append(sia.polarity_scores(str(w)))
    
    df[col_name+'_SENTIMENT'] = sentiments

    print(df['Q36_4_TEXT_SENTIMENT'])

    return df

def main():
    school_xsl = 'SurveyData/School_1a_2021.xlsx'
    df = pd.read_excel(school_xsl)

    nltk.download('vader_lexicon')

    sentimentAnalysis(df, 'Q36_4_TEXT')

    df.to_excel(school_xsl, sheet_name='Sheet1', index=False)

main()
