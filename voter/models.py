from django.db import models
from voter.constants import LETTERS
from color import colorz


class Letter(models.Model):

    letter = models.CharField(max_length=1, choices=LETTERS)
    image = models.ImageField(upload_to='media/uploads')
    archived = models.BooleanField(default=False)

    def dominant_color(self):
    	return colorz(self.image, 1)[0]


    def __unicode__(self):
        return "{} - {}".format(self.letter, self.image)


class MatchUp(models.Model):

    letter_a = models.ForeignKey('Letter', related_name="left")
    letter_b = models.ForeignKey('Letter', related_name="right")

    def get_results(self):

    	a_votes = self.vote_set.filter(letter=self.letter_a).count()
    	b_votes = self.vote_set.filter(letter=self.letter_b).count()

        try:
            a_percent = (float(a_votes) / float((a_votes + b_votes)))*100

            if a_percent > 98:
                a_percent = 98

        except:
            a_percent = 0

        try:
            b_percent = (float(b_votes) / float((b_votes + a_votes)))*100

            if b_percent > 98:
                b_percent = 98
        except:
            b_percent = 0

    	return {
    		'a': {
    			'percent': a_percent,
    			'votes': a_votes
    		},
    		'b': {
    			'percent': b_percent,
    			'votes': b_votes
    		}
    	}

    def get_loser(self):

        a_votes = self.vote_set.filter(letter=self.letter_a).count()
        b_votes = self.vote_set.filter(letter=self.letter_b).count()

        if a_votes > b_votes:
            return self.letter_b
        elif a_votes < b_votes:
            return self.letter_a
        else:
            return None

    def __unicode__(self):
        return "{} ___VS___ {}".format(self.letter_a, self.letter_b)


class Vote(models.Model):

    letter = models.ForeignKey('Letter')
    matchup = models.ForeignKey('MatchUp')
