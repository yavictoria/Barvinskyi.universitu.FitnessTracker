from django import forms
from .models import Workout, Activity, Comment, CompletedGoals
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


class ActivityForm(forms.ModelForm):
    completed_goal = forms.ModelChoiceField(queryset=CompletedGoals.objects.none(), required=False)

    class Meta:
        model = Activity
        fields = ['content', 'completed_goal']

    def __init__(self, user, *args, **kwargs):
        super(ActivityForm, self).__init__(*args, **kwargs)
        self.fields['completed_goal'].queryset = CompletedGoals.objects.filter(user=user)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_text']