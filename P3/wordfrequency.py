import nltk
from nltk.tokenize import sent_tokenize, RegexpTokenizer
from collections import Counter

# Download the required NLTK data
nltk.download('punkt')

# Define a function to perform frequency analysis on a block of text
def analyze_text(text):
    # Tokenize sentences
    sentences = sent_tokenize(text)

    # Tokenize words (excluding punctuation)
    tokenizer = RegexpTokenizer(r'\w+')
    
    # Initialize counters for word and phrase frequencies
    word_freq = Counter()
    phrase_freq_2 = Counter()
    phrase_freq_3 = Counter()
    phrase_freq_4 = Counter()

    # Process each sentence
    total_words = 0
    total_2_word_phrases = 0
    total_3_word_phrases = 0
    total_4_word_phrases = 0
    for sentence in sentences:
        # Tokenize words in the sentence (excluding punctuation)
        words = tokenizer.tokenize(sentence.lower())
        total_words += len(words)

        # Update word frequency
        word_freq.update(words)

        # Update 2-word phrase frequency
        phrases_2 = list(zip(words, words[1:]))
        phrase_freq_2.update(phrases_2)
        total_2_word_phrases += len(phrases_2)

        # Update 3-word phrase frequency
        phrases_3 = list(zip(words, words[1:], words[2:]))
        phrase_freq_3.update(phrases_3)
        total_3_word_phrases += len(phrases_3)

        # Update 4-word phrase frequency
        phrases_4 = list(zip(words, words[1:], words[2:], words[3:]))
        phrase_freq_4.update(phrases_4)
        total_4_word_phrases += len(phrases_4)

    # Sort the items by percentage in descending order
    word_freq_sorted = sorted(word_freq.items(), key=lambda x: (x[1] / total_words), reverse=True)
    phrase_freq_2_sorted = sorted(phrase_freq_2.items(), key=lambda x: (x[1] / total_2_word_phrases), reverse=True)
    phrase_freq_3_sorted = sorted(phrase_freq_3.items(), key=lambda x: (x[1] / total_3_word_phrases), reverse=True)
    phrase_freq_4_sorted = sorted(phrase_freq_4.items(), key=lambda x: (x[1] / total_4_word_phrases), reverse=True)

    # Output results to a text file
    with open('frequency_analysis_results.txt', 'w') as file:
        file.write("Frequency Analysis Results:\n\n")

        # Word frequencies
        file.write("Word Frequencies:\n")
        for word, freq in word_freq_sorted:
            percentage = (freq / total_words) * 100
            file.write(f"{word}: {percentage:.2f}% (of total words)\n")

        # 2-word phrase frequencies
        file.write("\n2-Word Phrase Frequencies:\n")
        for phrase, freq in phrase_freq_2_sorted:
            percentage = (freq / total_2_word_phrases) * 100
            file.write(f"{' '.join(phrase)}: {percentage:.2f}% (of two word phrases)\n")

        # 3-word phrase frequencies
        file.write("\n3-Word Phrase Frequencies:\n")
        for phrase, freq in phrase_freq_3_sorted:
            percentage = (freq / total_3_word_phrases) * 100
            file.write(f"{' '.join(phrase)}: {percentage:.2f}% (of three word phrases)\n")

        # 4-word phrase frequencies
        file.write("\n4-Word Phrase Frequencies:\n")
        for phrase, freq in phrase_freq_4_sorted:
            percentage = (freq / total_4_word_phrases) * 100
            file.write(f"{' '.join(phrase)}: {percentage:.2f}% (of four word phrases)\n")

# Test the function with input as a plain text block
input_text = """
The new menu is definitely less popular, my child says bring back sausage and mash - apparently the new sausages in the hot dogs are not so nice. He would like the old plates back that are reusable (less waste) and keeps the food separate rather than everything piled into a tub - he hates the vegetables being all mixed in with the other food.
Burgers/meatballs/hotdog contain more meat than veg.
Go back to how they used to be.
change gammon roast for a different meat ?pork or beef.
it's mainly vegetables that I don't eat.
Carrotts not cooked enough and they are hard.  Make the fruit separate and don't mix it up, it goes soggy.
The fruit when it is cut up and put together goes soggy, this is not nice, are you able to keep the fruit separate? The macaroni cheese has been changed and it isn't as good anymore, it doesn't taste nice, the cheese is different. The brocoli is over cooked and soggy.
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
Stop serving in disposable packaging with plastic cutlery. Please start reusing the original plates and cutlery. This seems so wasteful and not necessary as the children are back eating in the school hall now.
More meat content.
More organic produce.
Up until last term I have always had School Meals every day but I don't like them anymore.
more plant based meals. get the children eating a variety of veg.
No, there is a good, varied choice.
They are not big enough and I don’t have a big appetite.
More vegan meals.
My daughter has not liked the change in menu,  says the food doesn’t taste like it used to do, and she often doesn’t eat it. She misses the pasta pots they used to do and make your own pizza. I feel the choice has been reduced greatly since returning this term.
Buy locally from a butcher not a, whole sale.
Do something to reduce the amount of food wasted as lots of children don’t eat all of their school lunch.
The menu would be better if it was clearer what it actually involved rather than being creative with the names. Vegan burger - what is that? Bolgnaise boats - what is that?. My daughter has always appreciated having a ham or cheese pack lunch on offer as back up if she doesn't fancy any joy meals. That is no longer an option most days and has caused problems since the menu changed.
Butter in sandwiches and wholemeal bread.
Stop serving random vegetables with every meal and especially with meals that wouldn’t generally have them, eg serving courgette as a side to Macaroni cheese, ultimately these vegetable options don’t get eaten so they end up getting thrown away and filling up landfill.
Organic, less food miles, less red meat, less/reusable/recyclable packaging.
Often errors. Once this week even when fruit ordered, ticket with meal showed correct child name and correct order (fruit for pudding) but chocolate cake given. Not happy. (Mum).
Food children like so they do not waste it.
Using local produce ( reducing food miles) Consider packaging & reusable plates, cups and cutlery  etc Meat free days with a tasty variety of options  Try and taste once a month/week. Option to try new healthy/ environmental foods without having to have a plateful of the unknown.  Help us try more things and reduce waste.
Local.
more local produce.
Too many vegetables and mixing of foods.
"""

# Perform frequency analysis
analyze_text(input_text)
