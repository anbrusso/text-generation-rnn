from django import forms
class TextGenerateForm(forms.Form):
    CHOICES=[
        ('basic','Basic -- Initial simple LSTM model (note: this is slow)'),
        ('improved','Improved -- An Improved GRU model with improved cross training, temperature adjusts, and optimizations.')
        ]
    seed_text = forms.CharField(
                            max_length=1000,
                            required=True,
                            widget=forms.TextInput(attrs={'class': 'form-control'}),
                            initial="Default Seed Text"
                            )
    output_length = forms.IntegerField(min_value=0,
                                        max_value=5000,
                                        required=True,
                                        initial=300,
                                        widget=forms.NumberInput(attrs={'class': 'form-control'})
                                        )
    temperature = forms.FloatField(initial="1",widget=forms.NumberInput(attrs={'class': 'form-control','type':'range', 'step': '.1', 'min': '0.01', 'max': '2.0'}), required=True)
    model_type = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect,initial="improved", required=True)