from django.forms import ModelForm
from .models import Team, Participation

class TeamForm(ModelForm):
    class Meta:
        model = Team
        fields = '__all__'
        exclude = ['leader', 'players']

    # def __init__(self, *args, **kwargs):
    #     super(TeamForm, self).__init__(*args, **kwargs)

    #     for field_name, field in self.fields.items():
    #         self.fields[field_name].widget.attrs['placeholder'] = field.label

class ParticipateForm(ModelForm):
    class Meta:
        model = Participation
        fields = "__all__"
        exclude = ['player', 'toor', 'team']
        
        