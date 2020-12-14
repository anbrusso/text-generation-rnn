from django.shortcuts import render
import tensorflow as tf
import json
import numpy
import sys
import re
import os
from .forms import TextGenerateForm
from django.http import HttpResponse
def generate_text(seed_text="Default Seed Text",model_type="basic",temperature=1.0,output_length=1000):
    models_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)),"models/"+model_type+"/")
    #eventually, change these so specific model can be received in.
    token_map = "token-map.json"
    model_file = "model.h5"

    
    #setup all the maps that will be needed for converting to and from text to the model.
    with open(models_folder + token_map) as json_file:
        int_to_token = json.load(json_file)
    token_to_int = { v : float(i) for (i, v) in enumerate(int_to_token)}#create a reverse map, since we'll have to conver their input.
    n_vocab = len(int_to_token)#the number of characters in the vocabulary

    #load the model from our model file.
    model = tf.keras.models.load_model(models_folder + model_file, compile=False)

    #cleanup the text and get it into a usable format for pushing it through our model
    input_text = seed_text.lower()
    input_text = input_text.encode("ascii", "ignore").decode()
    if model_type in ["character","character-improved","character-new"]:
        input_text = re.sub(r"[~#$%&*+;<=>\[\\^_\]`{|}0-9@/]","",input_text)
        input_text = [token_to_int.get(c,0) for c in input_text]

        if model_type =="character":
            output_text = []
            # generate characters
            for i in range(output_length):
                x = numpy.reshape(input_text, (1, len(input_text), 1))
                x = x / float(n_vocab)
                prediction = model.predict(x, verbose=0)
                index = numpy.argmax(prediction)
                result = int_to_token[index]
                output_text.append(result)
                input_text.append(index)
                input_text = input_text[1:len(input_text)]
        elif model_type in ["character-improved","character-new"]:
            input_text = tf.expand_dims(input_text,0)

            #begin generating output
            output_text = []
            model.reset_states()
            #we have two output generation options, we either generate a specific length, or until we hit a new line.
            for i in range(output_length):
                #run the input through our model.
                predictions = model(input_text)
                predictions = tf.squeeze(predictions, 0)
                predictions = predictions  / temperature #we devide the predictions by our temparature. For higher temperatures inject more randomness into the text.
                #select the prediction randomly, by sampling according to the prediction confidence.
                predicted_int = tf.random.categorical(predictions,num_samples=1)[-1,0].numpy()
                #pass forward to next stage
                input_text = tf.expand_dims([predicted_int], 0)
                output_text.append(int_to_token[predicted_int])
    elif model_type in ["words","words-deeper","shakespeare","words-new"]:
        input_text = re.sub(r"[~#$%&*+;<=>\[\\^_\]`{|}0-9\(\)\'\"\-\"\:\/]","",input_text)#strip out some ascii characters that aren't super important.
        input_text = re.findall(r"\w+|\W",input_text)#we consider character strings, or punctuation to be "words"
        input_text = [token_to_int.get(c,0) for c in input_text]
        input_text = tf.expand_dims(input_text,0)
        output_text = []
        model.reset_states()
        for i in range(output_length):
            #run the input through our model.
            predictions = model(input_text)
            predictions = tf.squeeze(predictions, 0)
            predictions = predictions  / temperature #we devide the predictions by our temparature. For higher temperatures inject more randomness into the text.
            #select the prediction randomly, by sampling according to the prediction confidence.
            predicted_int = tf.random.categorical(predictions,num_samples=1)[-1,0].numpy()
            #pass forward to next stage
            input_text = tf.expand_dims([predicted_int], 0)
            output_text.append(int_to_token[predicted_int])
    return seed_text + ''.join(output_text).replace("\n","<br/>")

# Create your views here.
def index(request):
    if request.method == 'POST':
        form = TextGenerateForm(request.POST)
        if form.is_valid():
            output_text = { "output_text": generate_text(**form.cleaned_data)}
            return HttpResponse(json.dumps(output_text))
    else:
        form = TextGenerateForm()
    return render(request,'index.html', {'form':form})