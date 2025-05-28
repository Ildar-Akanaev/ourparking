from django import forms
from .models import Client
from .models import Feedback
from .models import Booking, ParkingSpace


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['subject', 'email', 'content']

class RegisterForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['last_name', 'first_name', 'patronymic', 'email', 'phone_number']

class BookingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['spot'].queryset = ParkingSpace.objects.filter(status='free')

    class Meta:
        model = Booking
        fields = ['spot', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }
class SpotSearchForm(forms.Form):
    spot_number = forms.CharField(label='Номер места', max_length=10)

#class FeedbackForm(forms.Form):
    #email = forms.EmailField(label="Ваш Email")
    #message = forms.CharField(widget=forms.Textarea, label="Сообщение")