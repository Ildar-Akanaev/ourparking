from django import forms
from .models import Client, Feedback, Booking, ParkingSpace, Car

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['subject', 'email', 'content']

class RegisterForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['last_name', 'first_name', 'patronymic', 'email', 'phone_number']

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['spot', 'start_date', 'end_date']
        labels = {
            'spot': 'Парковочное место',
            'start_date': 'Дата начала',
            'end_date': 'Дата окончания',
        }
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

class SpotSearchForm(forms.Form):
    spot_number = forms.CharField(label='Номер места', max_length=10)

class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['brand', 'color', 'license_plate']
