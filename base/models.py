from django.db import models
from django.contrib.auth.models import User 



class Game(models.Model):
    name = models.CharField(max_length=200)
    # type = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Team(models.Model):
    leader = models.ForeignKey(User,null=True, on_delete=models.SET_NULL)
    game = models.ForeignKey(Game,null=True, on_delete=models.SET_NULL)
    code = models.IntegerField()
    name = models.CharField(max_length=200)
    players = models.ManyToManyField(User, related_name='players', blank =True )
    
    @property
    def players_list(self):
        players = self.players.all()
        return players
    
    def __str__(self):
        return self.name

class Toornament(models.Model):
    game = models.ForeignKey(Game,null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    teams = models.ManyToManyField(
        Team, related_name='teams', blank =True )
    place = models.CharField(max_length=200)
    date_time = models.CharField(max_length=200)
    prize = models.IntegerField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)


    @property
    def teams_list(self):
        teams = self.teams.all()
        return teams

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name
    


class Participation(models.Model):
    idientifier = models.IntegerField()
    player = models.ForeignKey(User,null=True, on_delete=models.SET_NULL)
    toor = models.ForeignKey(Toornament,null=True, on_delete=models.SET_NULL)
    age = models.IntegerField()
    team = models.ForeignKey(Team, null=True, on_delete=models.SET_NULL)
    def __str__(self):
        return self.idientifier