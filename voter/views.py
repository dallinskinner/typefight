from django.http import HttpResponse
from django.shortcuts import render
from django.core import serializers
from voter.models import MatchUp, Letter
from voter.forms import VoteForm, MatchUpForm
from voter.constants import LETTERS

from django.contrib.sessions.models import Session

from django.contrib.auth.decorators import login_required


def get_matchup(votes):

    matchups = MatchUp.objects.all().order_by('?')

    for matchup in matchups:

        if matchup.id not in votes:

            return matchup

    return None


def match_up(r):

    try:
        votes = r.session['votes']
    except KeyError as e:
        votes = []

    print votes

    matchup = get_matchup(votes)

    return render(r, 'matchup.html', {'matchup': matchup})



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


    matchup = get_matchup(r.session['votes'])


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

        elif r.POST['action'] == 'clear_results':

            clear_results()


    letters = Letter.objects.filter(archived=False).order_by('letter')
    archived = Letter.objects.filter(archived=True).order_by('letter')
    matchups = MatchUp.objects.all()
    matchup_count = matchups.count()

    return render(r, 'admin_console.html', locals())


def purge_losers():

    matchups = MatchUp.objects.all()

    for matchup in matchups:

        loser = matchup.get_loser()

        try:
            loser.archived = True
            loser.save()
            matchup.delete()
            
        except AttributeError as e:
            pass

    Session.objects.all().delete()


def create_matchups():

    for letter in LETTERS:

        letter_objs = Letter.objects.filter(letter=letter[0], archived=False).order_by('?')

        # get them random but then put them in a list so they don't keep shuffling 
        letter_list = [letter_obj for letter_obj in letter_objs]

        i = 0

        while i < letter_objs.count():

            letter_a = letter_list[i]

            i = i + 1

            try:
                letter_b = letter_list[i]
                MatchUp.objects.create(letter_a=letter_a, letter_b=letter_b)

            except IndexError as e:
                pass

            i = i + 1


def clear_results():

    letters = Letter.objects.all()

    for letter in letters:

        letter.archived = False
        letter.save()
