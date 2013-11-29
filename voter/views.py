from django.http import HttpResponse
from django.shortcuts import render
from django.core import serializers
from voter.models import MatchUp, Letter
from voter.forms import VoteForm, MatchUpForm


def match_up(r):

    try:
        votes = r.session['votes']
    except KeyError as e:
        votes = []

    print votes

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
