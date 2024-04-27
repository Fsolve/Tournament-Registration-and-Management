from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .forms import TeamForm, ParticipateForm
from django.contrib.auth.models import User 
from .models import Toornament, Game, Team, Participation


# Create your views here.

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')  
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User Does Not Exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
    
        else:
            messages.error(request, 'Username or Password Does not exist')

    context = {'page':page}
    return render(request, 'base/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')




def home(request):
    # q = request.GET.get('q') if request.GET.get('q') != None else ''
    # print(q)
    # tours = Toornament.objects.filter(
    #     Q(topic__name__icontains=q)|
    #     Q(name__icontains=q)|
    #     Q(description__icontains=q)
    #     )
    teams = Team.objects.all()
    
    # for t in teams:
    #     for p in t.players_list:
    #         print(p.username)
    toors = Toornament.objects.all()
    games = Game.objects.all()
    toor_count = toors.count()

    context = {'toors': toors, 'games': games, 'toor_count':toor_count, 'teams':teams}
    return render(request, 'base/home.html', context)


def registerPage(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        for f in form:
            print(f)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration')
    context = {'form':form}
    return render(request, 'base/login_register.html', context)


@login_required(login_url='login')
def createTeam(request):
    form = TeamForm()
    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            team = form.save(commit=False)
            team.leader = request.user
            team.save()
            team.players.add(request.user)
            team.save()
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration')
    context = {'form': form}
    return render(request, 'base/team_form.html', context)

@login_required(login_url='login')
def participate(request, pk):
    form = ParticipateForm()
    toor = Toornament.objects.get(id = pk)
    teams = Team.objects.filter(game = toor.game)
    if request.method == 'POST':
        team_name = request.POST.get('teams')
        team = Team.objects.get(name = team_name)
        code = request.POST.get('code')
        print(team, team.pk)
        print(code, '==?', team.code)
        if int(code) == int(team.code):
            form = ParticipateForm(request.POST)
            if form.is_valid():
                participation = form.save(commit=False)
                participation.player = request.user
                participation.toor = Toornament.objects.get(name = toor.name)
                participation.save()
                toor.teams.add(team)
                toor.save()
                if request.user != team.leader:
                    team.players.add(request.user)
                    team.save()
                return redirect('home')
            else:
                messages.error(request, 'An error occured during registration')
        else:
            messages.error(request, 'The code doesn\'t match the chosen team')

    context = {'form': form, 'toor':toor, 'teams':teams}
    return render(request, 'base/participate_page.html', context)


def toornament(request, pk):
    toor = Toornament.objects.get(id = pk) 
    toor_id = toor.pk
    teams = toor.teams
    teams_num = toor.teams.count()
    context = {'toor':toor, 'teams':teams, 'toor_id':toor_id, 'teams_num':teams_num}
    return render(request, 'base/toornament.html', context)


