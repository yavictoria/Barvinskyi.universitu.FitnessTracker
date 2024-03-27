from django import forms
from .models import Workout
from .models import FitnessGoal


class WorkoutForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = ['description', 'all_sets_done', 'all_arms_done', 'all_legs_done', 'all_chest_done']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }


class FitnessGoalForm(forms.ModelForm):
    class Meta:
        model = FitnessGoal
        fields = ['goal_type', 'description', 'target_value']


class FitnessRecordForm(forms.ModelForm):
    class Meta:
        model = FitnessGoal
        fields = ['achieved_value']


class FitnessGoalSelectionForm(forms.Form):
    goal = forms.ModelChoiceField(queryset=FitnessGoal.objects.all(), empty_label=None, to_field_name="id")