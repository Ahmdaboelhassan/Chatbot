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


def predict_class(current_sentence, current_model, current_words, current_classes):
    # filter out predictions below a threshold
    sentence = prepare_sentence(current_sentence, current_words)

    res = current_model.predict(np_array([sentence]))[0]

    ERROR_THRESHOLD = 0.1
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": current_classes[r[0]], "probability": str(r[1])})
        print({"intent": current_classes[r[0]], "probability": str(r[1])})

    return return_list


def get_response(ints, dataset):
    result = "I don't Qualfied To Understand this yet"
    if len(ints) != 0:
        tag = ints[0]['intent']
        list_of_intents = dataset['intents']
        for i in list_of_intents:
            if (i['tag'] == tag):
                result = random_choice(i['responses'])
                break
    return result


# Paths
cwd = path.dirname(path.abspath(__file__))
def get_model_paths(model_name):
    model = cwd + f"/{model_name}/chatbot_model.h5"
    words = cwd + f"/{model_name}/words.pkl"
    classes = cwd + f"/{model_name}/classes.pkl"
    dataset = cwd + f"/{model_name}/{model_name}.json"
    return model, words, classes, dataset


def chatbot_response(msg, model_from_cookie="General"):
    # Get Paths
    model_path, words_path, classes_path, dataset_path = get_model_paths(model_from_cookie)

    # load files
    model = load_model(model_path)
    classes = load_pickle(open(classes_path, "rb"))
    words = load_pickle(open(words_path, 'rb'))
    dataset = load_json(open(dataset_path, encoding='utf-8').read())

    ints = predict_class(msg, model, words, classes)
    res = get_response(ints, dataset)
    return res
