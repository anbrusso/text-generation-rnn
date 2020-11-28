from django.shortcuts import render
import tensorflow as tf
import json
import numpy
import sys
# Create your views here.
#def index(request):
def main():
    models_folder = "models/basic/"#the folder that the model information is stored within
    #eventually, change these so specific model can be received in.
    character_map = "character-map-i1.json"
    model_file = "model-i1.h5"
    text = "Do that sometimes with reddit, only time I use facebook is for group chat. Only way I justify reddit to myself is otherwise I would be completely disconnected from anything happening in the world. Don't have cable, listen to radio or any other sources of news, so that's the only way I'm going to find out whether we're bombing Syria. Also the deepfried memes."
    outputlen = 1000
    temperature = 0.04 #the temperature is used to skew the probabilities in a direction, to create more/less randomness in the output.

    #setup all the maps that will be needed for converting to and from text to the model.
    with open(models_folder + character_map) as json_file:
        int_to_char = json.load(json_file)
    int_to_char = { int(key) : value  for (key, value) in int_to_char.items()}#this is to fix the mapping so it has integer keys like it is supposed to
    char_to_int = { value : int(key) for (key, value) in int_to_char.items()}#create a reverse map, since we'll have to conver their input.
    vocab_size = len(int_to_char.keys())#the number of characters in the vocabulary

    #Take the text that has been received in, and truncate it if it is too long.
    text = text.lower()[:300]
    #we convert the letters into an array of the corresponding numbers instead.
    text = [int(char_to_int[letter]) for letter in text]

    #load the lstm model from our model file.
    model = tf.keras.models.load_model(models_folder + model_file)
    
    for i in range(outputlen):
        #we convert text to be the correct shape for the lstm, and we squish all the values to be between 0 and 1
        x = numpy.reshape(text, (1, len(text), 1))
        x = x / float(vocab_size)

        #run the input through our model.
        predictions = model.predict(x, verbose=0)
        predictions = predictions / temperature #we devide the predictions by our temparature. For higher temperatures inject more randomness into the text.
        #select the prediction randomly, by sampling according to the prediction confidence.
        predicted_char = tf.random.categorical(predictions,num_samples=1)[-1,0].numpy()

        result = int_to_char[predicted_char]

        #Add the character to our text, and bump out the first letter
        text.append(predicted_char)
        text = text[1:len(text)]
        print(result, end = '',flush=True)
    #return render(request,'index.html')

if __name__=="__main__":
    main()