# Text Generation RNN
An RNN based model intended to replicate the style of text that I have written.

## Requirements
- [Python](https://www.python.org/)
- [Docker](https://www.docker.com/products/docker-desktop) &mdash; For testing the models
- [Jupyter Notebooks](https://jupyter.org/) &mdash; For training the models

## Submission Overview
- `report.pdf` &mdash; the project report pdf
- `/messages/` &mdash; folder containing the datasets to train on
- `/notebooks/` &mdash; folder containing the Jupyter Notebooks to use to train the model
- `/textgeneration/` &mdash; folder containing the Django web app
    - `/frontend/views.py` &mdash; code used for loading and running the models to generate text.
    - `/frontend/forms.py` &mdash; code for building the form.
    - `/frontend/templates/index.html` &mdash; html template for the web form.
    - `/frontend/models/` &mdash; the tensorflow models and token maps that are loaded for each model that is ran

## How the models have been trained
The trained models delivered with the codebase are mostly trained on a corpus of text I've gathered from my own posts on Discord, Facebook Messenger, and other written works.

## How to train the model
Since the source dataset is rather personal, I have not released the full text corpus, only the trained models for demonstration purposes. With the code, I've included a copy of shakespearean dialogues from https://www.tensorflow.org/tutorials/text/text_generation, as well as the fulltext of Alice in Wonderland from [Project Gutenberg](https://www.gutenberg.org/) which can be used to train and test the model yourself.

To train the model on your own corpus, or retrain it with the shakespearean dialogue, install [Jupyter Notebooks](https://jupyter.org/). Then you can open one of the notebooks in the notebooks directory with:

    jupyter notebook character-model.ipynb
    jupyter notebook word-model.ipynb
In the notebook, if you run all of the cells it will build and train the model, and generate some text using the model. Everything to run the models is saved in the directory `textgeneration/frontend/models/character-new` and `textgeneration/frontend/models/words-new`. These two models are automatically loaded into the testing page for testing, but additional models could be saved and added to the forms.py and views.py files.

## How to test the model
To test the models, you can either adjust the seed text in the notebook and rerun the final cell to generate something new, or use the testing page. Instructions for using the testing page are below.
### Option 1 (recommended)
The easiest way to run the testing page, requires that [Docker](https://www.docker.com/products/docker-desktop) be installed (as well as [docker compose](https://docs.docker.com/compose/install/), which comes with docker on Windows and Mac). After docker is installed, you can startup the web server by navigating to the code's root directory and running:

    docker-compose up

This will pull down a python container, build in all of the dependencies for django and tensorflow, and start up the webserver, which can be accessed at `http://localhost:8000/`. Models that have been recently built can be ran with the options Character New and Word New, which point to the directories that the two notebooks save their models in.
### Option 2
Alternatively, you can install the python requirements into an existing python install from the `requirements.txt` file:

    pip install -r requirements.txt
Then run the following command inside the `textgeneration` folder:

    python manage.py runserver 0.0.0.0:8000

This will run the django server in your existing python instance rather than from inside the docker container, which will be accessible in a browser via `http://localhost:8000/`.
