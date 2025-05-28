from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
from .models import ParkingSpace, Booking
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .forms import FeedbackForm
from .forms import BookingForm
from django.shortcuts import render
from .forms import SpotSearchForm
from .models import ParkingSpace

def spot_search_view(request):
    spot_status = None
    spot_statuses = []
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    spot_number = request.GET.get('spot_number')

    if request.method == 'GET':
        if spot_number and start_date and end_date:
            # Поиск по номеру и датам
            try:
                spot = ParkingSpace.objects.get(spot_number=spot_number)
                is_booked = Booking.objects.filter(
                    spot=spot,
                    start_date__lt=end_date,
                    end_date__gt=start_date
                ).exists()
                spot_status = "Занято или зарезервировано" if is_booked else "Свободно"
            except ParkingSpace.DoesNotExist:
                spot_status = "Место не найдено"
        elif start_date and end_date:
            # Поиск по датам — список всех мест
            spots = ParkingSpace.objects.all()
            for spot in spots:
                is_booked = Booking.objects.filter(
                    spot=spot,
                    start_date__lt=end_date,
                    end_date__gt=start_date
                ).exists()
                spot_statuses.append({
                    'spot': spot,
                    'status': "Занято или зарезервировано" if is_booked else "Свободно",
                })
    return render(request, 'parking/spot_search.html', {
        'spot_status': spot_status,
        'spot_statuses': spot_statuses,
        'spot_number': spot_number,
        'start_date': start_date,
        'end_date': end_date,
    })


def feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.ip_address = request.META.get('REMOTE_ADDR')
            if request.user.is_authenticated:
                feedback.user = request.user
            feedback.save()

            send_mail(
                subject=feedback.subject,
                message=f'От: {feedback.email}\nСообщение: {feedback.content}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.ADMIN_EMAIL],
                fail_silently=False,
            )

            messages.success(request, 'Ваше сообщение отправлено!')
            return redirect('feedback')
    else:
        form = FeedbackForm()
    return render(request, 'parking/feedback.html', {'form': form})



def index(request):
    return render(request, 'parking/index.html')

#def booking_view(request):
    #if request.method == 'POST':
        #form = BookingForm(request.POST)
        #if form.is_valid():
            #booking = form.save(commit=False)
            #if request.user.is_authenticated:
                #booking.user = request.user
            #booking.save()
            #return redirect('booking')
    #else:
        #form = BookingForm()
    #return render(request, 'parking/booking.html', {'form': form})
def booking_view(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            if request.user.is_authenticated:
                booking.user = request.user
            booking.save()
            # Меняем статус места на "зарезервировано"
            booking.spot.status = 'reserved'
            booking.spot.save()
            messages.success(request, 'Бронь успешно создана!')
            return redirect('booking')
    else:
        form = BookingForm()
    return render(request, 'parking/booking.html', {'form': form})

def book_spot(request, spot_id):
    spot = get_object_or_404(ParkingSpace, id=spot_id)
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    return render(request, 'parking/book_spot.html', {
        'spot': spot,
        'start_date': start_date,
        'end_date': end_date,
    })


def confirm_booking(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        spot_id = request.POST.get('spot_id')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        spot = get_object_or_404(ParkingSpace, id=spot_id)
        Booking.objects.create(
            user=request.user,
            spot=spot,
            start_date=start_date,
            end_date=end_date,
        )
        return render(request, 'parking/success.html', {
            'spot': spot,
            'start_date': start_date,
            'end_date': end_date,
        })
    return redirect('booking_view')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'parking/register.html', {'form': form})

def login_view(request):
    return render(request, 'parking/login.html')

def profile(request):
    return render(request, 'parking/profile.html')

def feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            # Логика отправки сообщения или сохранения в БД
            return redirect('index')
    else:
        form = FeedbackForm()
    return render(request, 'parking/feedback.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')
