from django import forms
class TextGenerateForm(forms.Form):
    #The options for the different models. These correspond to the different options that will run in views.py You will need to add to this list for them to show up in the form, and then
    #add them to views.py for them to actually be generateable.
    CHOICES=[
        ('character','Character -- Initial character based LSTM model (note: this is slow)'),
        ('character-improved','Character Improved -- Improved GRU model using Many to Many LSTM with cross training, temperature adjusts, and optimizations'),
        ('character-new','Character New -- The most recently generated model fresh from character notebook'),
        ('words','Words -- Similar to character improved, but utilizes word base tokenization instead of characters'),
        ('words-deeper','Words Deeper -- Words based LSTM with reduced vocabulary and deeper RNN'),
        ('words-new','Word New -- The most recently generated model fresh from the word notebook'),
        ('shakespeare','Shakespeare -- Words improved, but ran on all of Shakespeare''s plays')
        ]
    seed_text = forms.CharField(
                            max_length=1000,
                            required=True,
                            widget=forms.TextInput(attrs={'class': 'form-control'}),
                            initial="My goal as a text generator is"
                            )
    output_length = forms.IntegerField(min_value=0,
                                        max_value=5000,
                                        required=True,
                                        initial=150,
                                        widget=forms.NumberInput(attrs={'class': 'form-control'})
                                        )
    temperature = forms.FloatField(initial=".5",widget=forms.NumberInput(attrs={'class': 'form-control','type':'range', 'step': '.1', 'min': '0.01', 'max': '2.0'}), required=True)
    model_type = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect,initial="words", required=True)
