import nltk
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
from pickle import load as load_pickle
from json import loads as load_json
from random import choice as random_choice
from numpy import array as np_array
from keras.models import load_model
from os import path

# Deployment
nltk.download('punkt')
nltk.download('wordnet')
# Deployment

# Main Paths
cwd = path.dirname(path.abspath(__file__)) + "/Final Model"

# load files
model = load_model(cwd + "/chatbot_model.h5")
classes = load_pickle(open(cwd + "/classes.pkl", "rb"))
words = load_pickle(open(cwd + "/words.pkl", 'rb'))
dataset = load_json(open(cwd + "/DataSet.json", encoding='utf-8').read())


def prepare_sentence(current_sentence, current_words):
    lemmatizer = WordNetLemmatizer()

    # tokenize the pattern
    sentence_words = word_tokenize(current_sentence)
    # stem each word - create short form for word
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]

    # bag of words - matrix of N words, vocabulary matrix
    bag = [0] * len(current_words)
    for sentence_word in sentence_words:
        for i, word in enumerate(current_words):
            if word == sentence_word:
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1

    return np_array(bag)


def predict_class(current_sentence):
    # filter out predictions below a threshold
    
    sentence = prepare_sentence(current_sentence, words)

    res = model.predict(np_array([sentence]))[0]

    ERROR_THRESHOLD = 0.2
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
        print({"intent": classes[r[0]], "probability": str(r[1])})

    return return_list


def get_response(ints):

    result = "الأمر غير واضح بالنسبة لي هل تستطيع ان تعطيني معلومات اكثر"
    if len(ints) != 0:
        tag = ints[0]['intent']
        list_of_intents = dataset['intents']
        for i in list_of_intents:
            if (i['tag'] == tag):
                result = random_choice(i['responses'])
                break
    return result



def chatbot_response(msg ):
   return get_response(predict_class(msg))
