from textblob import TextBlob
from nltk import sent_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import stanfordnlp

stanfordnlp.download('en')

def sentiment_analysis_by_sentence(text, output_file):
    # Initialize sentiment analyzers
    tb = TextBlob()
    sid = SentimentIntensityAnalyzer()
    stanford_nlp = stanfordnlp.Pipeline(processors='tokenize,sentiment')

    sentences = sent_tokenize(text)
    positive_count_tb = 0
    negative_count_tb = 0
    neutral_count_tb = 0

    positive_count_vader = 0
    negative_count_vader = 0
    neutral_count_vader = 0

    positive_count_stanford = 0
    negative_count_stanford = 0
    neutral_count_stanford = 0

    with open(output_file, 'w') as file:
        for sentence in sentences:
            # TextBlob
            tb_sentiment = tb(sentence).sentiment.polarity
            if tb_sentiment > 0:
                sentiment_label = "Positive"
                positive_count_tb += 1
            elif tb_sentiment < 0:
                sentiment_label = "Negative"
                negative_count_tb += 1
            else:
                sentiment_label = "Neutral"
                neutral_count_tb += 1

            # VADER
            vader_scores = sid.polarity_scores(sentence)
            compound_score = vader_scores['compound']
            if compound_score > 0.05:
                sentiment_label_vader = "Positive"
                positive_count_vader += 1
            elif compound_score < -0.05:
                sentiment_label_vader = "Negative"
                negative_count_vader += 1
            else:
                sentiment_label_vader = "Neutral"
                neutral_count_vader += 1

            # StanfordNLP
            sentence_obj = stanford_nlp(sentence)
            sentiment_stanford = sentence_obj.sentences[0].sentiment
            if sentiment_stanford == "Positive":
                sentiment_label_stanford = "Positive"
                positive_count_stanford += 1
            elif sentiment_stanford == "Negative":
                sentiment_label_stanford = "Negative"
                negative_count_stanford += 1
            else:
                sentiment_label_stanford = "Neutral"
                neutral_count_stanford += 1

            file.write(f"Sentence: {sentence}\n")
            file.write(f"TextBlob: {sentiment_label}\n")
            file.write(f"VADER: {sentiment_label_vader}\n")
            file.write(f"StanfordNLP: {sentiment_label_stanford}\n\n")

    total_sentences = len(sentences)

    with open(output_file, 'a') as file:
        file.write(f"\nAnalysis Summary:\n")

        file.write("TextBlob:\n")
        file.write(f"Positive Sentiment: {(positive_count_tb / total_sentences) * 100:.2f}%\n")
        file.write(f"Negative Sentiment: {(negative_count_tb / total_sentences) * 100:.2f}%\n")
        file.write(f"Neutral Sentiment: {(neutral_count_tb / total_sentences) * 100:.2f}%\n")

        file.write("\nVADER:\n")
        file.write(f"Positive Sentiment: {(positive_count_vader / total_sentences) * 100:.2f}%\n")
        file.write(f"Negative Sentiment: {(negative_count_vader / total_sentences) * 100:.2f}%\n")
        file.write(f"Neutral Sentiment: {(neutral_count_vader / total_sentences) * 100:.2f}%\n")

        file.write("\nStanfordNLP:\n")
        file.write(f"Positive Sentiment: {(positive_count_stanford / total_sentences) * 100:.2f}%\n")
        file.write(f"Negative Sentiment: {(negative_count_stanford / total_sentences) * 100:.2f}%\n")
        file.write(f"Neutral Sentiment: {(neutral_count_stanford / total_sentences) * 100:.2f}%\n")

# Test the function and save results to a file
text = """
The new menu is definitely less popular, my child says bring back sausage and mash - apparently the new sausages in the hot dogs are not so nice. He would like the old plates back that are reusable (less waste) and keeps the food separate rather than everything piled into a tub - he hates the vegetables being all mixed in with the other food.
Burgers/meatballs/hotdog contain more meat than veg.
Go back to how they used to be.
change gammon roast for a different meat ?pork or beef.
it's mainly vegetables that I don't eat.
Carrotts not cooked enough and they are hard.  Make the fruit separate and don't mix it up, it goes soggy.
The fruit when it is cut up and put together goes soggy, this is not nice, are you able to keep the fruit separate? The macaroni cheese has been changed and it isn't as good anymore, it doesn't taste nice, the cheese is different. The brocoli is over cooked and soggy.
No.
Portion size needs improving choices are not as good now as when my sister was my age.
Portion size needs improving and the options some are quite random.
Bigger portions.
They have changed and are not as good.
Some of the meals before the new menu were enjoyed by the students not many do so now one example my sone loves fish finger and chips but cant eat the new version .I understand not may like it at all.
Although I appreciate the effort of meatless Mondays, soup is not a substantial meal! Especially in summer?.
Go back to old menu? Add in old favourites. Taste has changed according to my daughter. Also maybe have 4 week rolling me I, I feel it seems like a 2 week once at the moment x.
It would be nice to have more options of foods not using cooked tomato sauces and low dairy options but that's just us.
I am having less school dinners now because I don't like the new menu. I don't like burgers, hot dogs and pizza. I used to like the meals like curry, pasta pots and chicken and rice but these aren't there now. I don't like the new meat balls either.
Better variety and more home cooking type like cottage pie, lasagne.
Some if the pudding choices are not as healthy as they could be.=
Please be clear about what the food is that's on offer - some titles are confusing.
See previous comment.
When it says macaroni cheese and garlic bread we get served penne pasta with a cheese sauce and a slice of plain white bread, it’s never macaroni pasta. The roast chicken is always really dry and we don’t have the option of having meat on the bone, it’s always chicken breast. I’d like to see prawns on the menu.
Choice of fillings for potatoes instead of fixed.
Don’t like the new sausages and burgers they taste really bad.
Healthier desserts.
Often complains of plastic taste to specific options (ie. Barbeque sticky chicken), potatoes often very dry and hard. Wrong options/orders handed out regardless of preference at ordering.
Class appropriate sized meals. Better puddings than boring cake. Tastier cooking.
More choice. More fish.
Simple meals, fresh ingredients.
Foods not to be similar, more roasts, food they will eat. My daughter does not like cheese, today two of the items contained cheese with 1 ingrediant different.
Vegetables are always soft and soggy. Don’t over cook.  Pizzas are not nice  either. Portions are small, I am  always hungry when I come home.
Not comprise o quality.
Different desserts each day.
More accurate description on parentpay ordering: ie I don’t know what rainbow potatoes are.
To taste better and to be warmer, sometimes the food is cold.
No.
Stop serving in disposable packaging with plastic cutlery. Please start reusing the original plates and cutlery. This seems so wasteful and not necessary as the children are back eating in the school hall now.
More meat content.
No.
More organic produce.
Up until last term I have always had School Meals every day but I don't like them anymore.
more plant based meals. get the children eating a variety of veg.
No.
No, there is a good, varied choice.
They are not big enough and I don’t have a big appetite.
More vegan meals.
My daughter has not liked the change in menu,  says the food doesn’t taste like it used to do, and she often doesn’t eat it. She misses the pasta pots they used to do and make your own pizza. I feel the choice has been reduced greatly since returning this term.
No.
No.
Buy locally from a butcher not a, whole sale.
Do something to reduce the amount of food wasted as lots of children don’t eat all of their school lunch.
The menu would be better if it was clearer what it actually involved rather than being creative with the names. Vegan burger - what is that? Bolgnaise boats - what is that?. My daughter has always appreciated having a ham or cheese pack lunch on offer as back up if she doesn't fancy any joy meals. That is no longer an option most days and has caused problems since the menu changed.
Butter in sandwiches and wholemeal bread.
Stop serving random vegetables with every meal and especially with meals that wouldn’t generally have them, eg serving courgette as a side to Macaroni cheese, ultimately these vegetable options don’t get eaten so they end up getting thrown away and filling up landfill.
No.
Organic, less food miles, less red meat, less/reusable/recyclable packaging.
Often errors. Once this week even when fruit ordered, ticket with meal showed correct child name and correct order (fruit for pudding) but chocolate cake given. Not happy. (Mum).
Food children like so they do not waste it.
No.
Using local produce ( reducing food miles) Consider packaging & reusable plates, cups and cutlery  etc Meat free days with a tasty variety of options  Try and taste once a month/week. Option to try new healthy/ environmental foods without having to have a plateful of the unknown.  Help us try more things and reduce waste.
Local.
more local produce.
Don’t know.
Too many vegetables and mixing of foods.
"""

output_file = "sentiment_analysis_results.txt"
sentiment_analysis_by_sentence(text, output_file)
