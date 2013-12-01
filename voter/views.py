from django.http import HttpResponse
from django.shortcuts import render
from django.core import serializers
from voter.models import MatchUp, Letter
from voter.forms import VoteForm, MatchUpForm
from voter.constants import LETTERS

from django.contrib.auth.decorators import login_required


def match_up(r):

    try:
        votes = r.session['votes']
    except KeyError as e:
        votes = []

    print votes

    votes = []

    matchups = MatchUp.objects.all()

    # vote_form = VoteForm(initial={'matchup': matchup})

    return render(r, 'matchup.html', locals())


def cast_vote(r):


    if r.method == 'POST':
        vote_form = VoteForm(r.POST)

        if vote_form.is_valid():
            voted = vote_form.save()

            try:
                votes = r.session['votes']

                votes.append(voted.matchup.id)

                r.session['votes'] = votes
            except KeyError as e:
                print e
                r.session['votes'] = [voted.matchup.id,]


            return render(r, 'voted.html', locals())

        else:
            return render(r, 'matchup.html', locals())


def create_matchup(r):

    if r.method == 'POST':
        matchup_form = MatchUpForm(r.POST)

        if matchup_form.is_valid():
            matchup = matchup_form.save()

            return render(r, 'matchup_created.html', locals())

        else:
            return render(r, 'create_matchup.html', locals())
    else:
        return render(r, 'create_matchup.html', locals())


def get_letters(r):

    letters = Letter.objects.all().order_by('letter')

    return HttpResponse(
        serializers.serialize('json', letters), mimetype='application/json')


def results(r):

    matchups = MatchUp.objects.all()

    return render(r, 'results.html', locals())


@login_required
def admin_console(r):

    if r.method == 'POST':

        if r.POST['action'] == 'create_matchups':

            create_matchups()

        elif r.POST['action'] == 'purge_losers':

            purge_losers()


    letters = Letter.objects.order_by('letter')
    matchups = MatchUp.objects.all()
    matchup_count = matchups.count()

    return render(r, 'admin_console.html', locals())


def purge_losers():

    matchups = MatchUp.objects.all()

    for matchup in matchups:

        loser = matchup.get_loser()

        try:
            loser.delete()
        except AttributeError as e:
            pass


def create_matchups():

    for letter in LETTERS:

        letter_objs = Letter.objects.filter(letter=letter[0]).order_by('?')

        i = 0

        while i < letter_objs.count():

            letter_a = letter_objs[i]

            i = i + 1

            try:
                letter_b = letter_objs[i]
                MatchUp.objects.create(letter_a=letter_a, letter_b=letter_b)

                i = i + 1

            except IndexError as e:
                print 'Odd # of letters'
                pass
