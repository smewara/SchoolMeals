from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import sent_tokenize

def sentiment_analysis_by_sentence(text, output_file):
    # Initialize the VADER sentiment analyzer
    sid = SentimentIntensityAnalyzer()

    sentences = sent_tokenize(text)
    positive_count = 0
    negative_count = 0
    neutral_count = 0

    with open(output_file, 'w') as file:
        for sentence in sentences:
            # Analyze sentiment using VADER
            scores = sid.polarity_scores(sentence)

            # Determine sentiment label based on compound score
            if scores['compound'] > 0.05:
                sentiment_label = "Positive"
                positive_count += 1
            elif scores['compound'] < -0.05:
                sentiment_label = "Negative"
                negative_count += 1
            else:
                sentiment_label = "Neutral"
                neutral_count += 1

            file.write(f"Sentence: {sentence}\n")
            file.write(f"VADER Sentiment: {sentiment_label}\n\n")

    total_sentences = len(sentences)
    positive_percentage = (positive_count / total_sentences) * 100
    negative_percentage = (negative_count / total_sentences) * 100
    neutral_percentage = (neutral_count / total_sentences) * 100

    with open(output_file, 'a') as file:
        file.write(f"\nAnalysis Summary:\n")
        file.write(f"Positive Sentiment: {positive_percentage:.2f}%\n")
        file.write(f"Negative Sentiment: {negative_percentage:.2f}%\n")
        file.write(f"Neutral Sentiment: {neutral_percentage:.2f}%\n")

# Test the function and save results to a file
text = """
Can I have a swing please.
add more opsions like tomato soup carbanara and salad.
carbonara,tomato soup,salald.
Tastier meals, and cooked properly food is sometimes cold or vegetables and roast potatoes hard . different choices .
Bigger meals served with more standard things. Cooking potatoes so they aren't hard. Making sandwiches more kid sized.
More pasta dishes tuna pasta bake etc.
they can have more vegetarian options.
they can put more on the plate.
It can be improved more if it had a lot more healty options.
Not really I like all the school meals.
No I like them all.
More packed lunch options.
no plastic cutlery.
no plastic cutley.
Don't always overcook the meat.
More options for different fruit rather than just apples. Lots of the food is really hard like the burgers. Sometimes the food has a taste but often it just takes like nothing.
source food from local areas.
Add a bit more different meals other than roast and spaghetti.
They could get their ingredients from places that sell natural food.
More of a longer time to eat.
The Puddings are delicious but the actual dinners are horrible. I usually get an extra snack that my mum gives me because she knows i dont get full enough.
make the containers bigger to have more food in them, may be a tiny bit more.
Have more vegetables, like even simple vegetables on the side, make the containers a bit bigger to contain more food.
not have the food mixed and tins not made from plastic so you can out food in different bits, and also plastic is not good for the environment, it s good for us but if we keep garbaging it it will take over the world, today I had to pick up two bits off the floor from the playground and put it in the bin.
may be only two days a week you eat meat because I sometimes I get really slow when I eat meat because it feels it s not right, I don't know why t makes me feel that.
we could have more veggies, some of my friends really like vegetables same as me, broccoli carrots peas and sweetcorn, cabbage, I haven't tried beetroot or kale ( when prompted what about).
May be have more pasta.
may be more lasagne ( Prompted).
have some carrot sticks to go with the jacket potatoes, because they normally only have beans or tuna but it would be good to add some vegetables. Make healthy cakes, like carrot cakes for example. I also don't like green beans in the macaroni cheese.
add a bit more butter to the mash.
may be not too much junk food like pizza I do like pizza but it's not good for me.
I remember in one of my old schools instead of giving us cake or something they would give us fruit salad.
I think they can make some more meals like some more because it's normally the same, like more puddings like ice cream.
less vegetables and more fruit.
I like pizza, burgers, spaghetti.
no carrots but love yorkshire, cabbage and gravy.
more apples, the yoghurt.
Favourite vegetables carrots, bbq corn, cucumber.
roast potatoes and broccoli and ice cream.
more healthy things , vegetables sweetcorn.
may be add new food any kind of new food and chicken nuggets, and I like fries.
Like the spaghetti bolognaise.
more vegetarian food because a lot of people are vegetarian actually I am vegetarian because my big sister is vegetarian and I want to be vegetarian because vegetarians eats lots and lots of vegetables broccolis tomatoes and sweetcorn and peas.
more cheese!.
roast chicken, more fruit when we have dessert, I like carrots I don't really like the other ones.
get something else like fish fingers fish and beans and apples oranges, bananas.
More cheese packed lunches!.
if it was a bit quieter at lunch time, more fruit and vegetables, more chicken broccoli and chips.
Drink more choices.
Pesto.
Bigger meals.
use less foil for the lunch containers.
they should make more fruit and veg options for vegatarians and vegans.
More standard meals. Meals for children with sensory issues.
Use sustainable local companies use biodegradable packaging.
less meat.
they can use less tin foil.
no plastic.
eat healthy.
Less meat.
it can by more healthy.
A little more healthier.
eat healthy.
Don't wrap cling film round the cakes.
wooden cutlery that doesn't brake every time you stab something.
No plastic cutlery.
we could wash plates and cutlery up so all germs will be removed and it will save plastic.also they should obvs stop using awful bendy plastic kutlery.
To give more options for desert.
use less plastic utensils.
more health foods and less meat foods.
Going by the what I've eaten and seen the, school meals are not great. Due to Covid 19 restrictions we had to: eat in our classroom ( making the salad bar not available), having to eat out of foil like,  non reusable containers. I used to have 1 school meal a week but coming back to school after Christmas I have not had a single school meal as all of the food gets mashed to the bottom in no  order. I have seen peoples plastic forks breaking, odd combinations of food, and the school not allowing certain foods like chocolate and crisps but serving cake and other unhealthy stuff.
Do not use plastic for the cutlery as it is always thrown away after you eat, I suggest that you use cardboard or paper cutlery instead.  If the cutlery is plastic, please make it more unbreakable, last time I accidently broke my fork so then I didn't know what to do.
They could offer more healthy meals.
They could offer more choices to people.
Maybe they can let the sdutents have a choice because one of my school meals they put macaroni cheese with rice. They gave my friends meatbalss and nan bread. Like  d -_-  b.
I just like packed lunch more, because you get chocolate and I love chocolate.
yes, want to know because I don't know. 
more salad, like lettuce, tomatoes, cucumber onions.
because I want to know where the food comes from don't know why. have some more options of fruit, pears, bananas, we normally just have an apple.
Add a bit more vegetables.
plant some of your own, there is one thing with the pizza I don't really like it, the taste is a bit weird, it might be the topping I just find it a bit weird.
more vegetables because that's helping the environment because animals don't get killed.
need more food to keep the animals alive, if you had no food then we would die that's why we have to have food.
a bit more meat because the food doesn't have enough in it.
may be have more vegetables, because they make you grow, use less chocolaty puddings.
may be stuff like you can harvest from the ground so you don't have to use the oven so much, because ovens use gas and it makes bad air for the environment.
make it healthier, add some vegetables, like cucumbers.
I think it would be good to not kill meat, should respect the planet, and it food in the bin rather than chucking it everywhere.
they should put new ingredients like mashed potatoes not jacket potatoes.
more recyclable things, like recyclable paper bags, may be not so much meat everyday because its not very good for animals.
more vegetarian food because they don't that that much, more fruit and vegetables, always want meat though.
if I know where my food comes from it might make me like it more.
If they put no ketchup in mind, I don't really like fruit that much or vegetables, because they don't taste that good mainly because of the way they are cooked, I don't eat them at home much.
more wraps with ham.
I like more sweet flavours, and strawberry in ice cream and real strawberries but we don't get real strawberries.
more fish fingers.
make food for the animals, more fruit and vegetables carrots and apples lettuce.
use wooden forks.
it's hard to think, may be like vegetables or fruit, sugar stuff are not good for the environment.
have real cutlery not plastic ones (prompted).
Having reusable plates and cutlery.
Use reusable containers.
"""

output_file = "sentiment_analysis_results_va.txt"
sentiment_analysis_by_sentence(text, output_file)
