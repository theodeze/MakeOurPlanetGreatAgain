from django.forms import ModelForm, TextInput, DateTimeField
from apps.venture.models import Venture, Comment, Pledge

class VentureForm(ModelForm):

    finished_at = DateTimeField(
        widget=TextInput(     
            attrs={'type': 'date'} 
        )
    )   

    class Meta:
        model = Venture
        fields = ['name', 'summary', 'description', 'banner', 'finished_at', 'goal']

class CommentForm(ModelForm):

    class Meta:
        model = Comment
        fields = ['message']
    
class FundingForm(ModelForm):

    class Meta:
        model = Pledge
        fields = ['amount']