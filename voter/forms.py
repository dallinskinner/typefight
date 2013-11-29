from django.forms import ModelForm
from voter.models import *


class LetterForm(ModelForm):

    class Meta:
        model = Letter


class VoteForm(ModelForm):

    class Meta:
        model = Vote
        fields = ['letter', 'matchup']


class MatchUpForm(ModelForm):

    class Meta:
        model = MatchUp
        fields = ['letter_a', 'letter_b']
