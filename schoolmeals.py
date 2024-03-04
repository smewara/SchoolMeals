import nltk
import pandas as pd
from nltk.sentiment import SentimentIntensityAnalyzer

school_xsl = 'SurveyData/School_1a_2021.xlsx'
df = pd.read_excel(school_xsl)

meat_free_good_idea_q = df['Q36_4_TEXT']

nltk.download('vader_lexicon')

sia = SentimentIntensityAnalyzer()

sentiments_meat_free_idea = []

for w in meat_free_good_idea_q.values:
    sentiments_meat_free_idea.append(sia.polarity_scores(str(w)))

print(sia.polarity_scores('That feels like we are imposing a choice on children. There are plenty of fish possibilities to replace meat and also quorn  etc'))


df.insert(df.columns.get_loc('Q36_4_TEXT') + 1, 'Q36_4_TEXT_SENTIMENT', sentiments_meat_free_idea)

print(df['Q36_4_TEXT_SENTIMENT'])

df.to_excel(school_xsl, sheet_name='Sheet2', index=False)