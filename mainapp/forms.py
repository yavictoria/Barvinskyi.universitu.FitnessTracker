from django import forms
from .models import Workout


class WorkoutForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = ['description', 'all_sets_done', 'all_arms_done', 'all_legs_done', 'all_chest_done']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }