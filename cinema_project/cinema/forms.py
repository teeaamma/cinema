from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import Movie, Session, Reservation, Seat


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'description', 'duration', 'poster']
        widgets = {
            'duration': forms.TimeInput(attrs={'type': 'time'}),
        }


class SessionForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ['movie', 'hall', 'start_time']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


class ReservationCreateForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['seat']

    def __init__(self, *args, **kwargs):
        session = kwargs.pop('session', None)
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.session = session
        self.user = user

    def save(self, commit=True):
        reservation = super().save(commit=False)
        reservation.session = self.session
        reservation.user = self.user
        if commit:
            reservation.save()
        return reservation



class UserForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name',
                  'email', "password1", "password2",)


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name',
                  'email',)
