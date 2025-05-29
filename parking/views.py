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
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404
from .models import ParkingSpace, Booking
from datetime import datetime

def parking_search(request):
    spot_number = request.GET.get('spot_number')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    today = datetime.today().date()

    if spot_number:
        # Пользователь выбрал конкретное место
        spot = get_object_or_404(ParkingSpace, spot_number=spot_number)
        bookings = Booking.objects.filter(
            spot=spot,
            end_date__gte=today
        ).order_by('start_date')
        is_booked = False
        if start_date and end_date:
            is_booked = Booking.objects.filter(
                spot=spot,
                start_date__lt=end_date,
                end_date__gt=start_date
            ).exists()
        context = {
            'selected_spot': spot,
            'bookings': bookings,
            'is_booked': is_booked,
            'start_date': start_date,
            'end_date': end_date,
        }
        return render(request, 'parking/spot_status.html', context)
    elif start_date and end_date:
        # Показываем все свободные места на выбранные даты
        spots = ParkingSpace.objects.all()
        free_spots = []
        for spot in spots:
            is_booked = Booking.objects.filter(
                spot=spot,
                start_date__lt=end_date,
                end_date__gt=start_date
            ).exists()
            if not is_booked:
                free_spots.append(spot)
        context = {
            'free_spots': free_spots,
            'start_date': start_date,
            'end_date': end_date,
        }
        return render(request, 'parking/free_spots.html', context)
    else:
        # Если ничего не выбрано — редирект обратно на главную
        return redirect('index')

def spot_search_view(request):
    # ваш код обработки поиска
    return render(request, 'parking/spot_search.html', {})

@csrf_exempt
def book_spot(request):
    if request.method == 'POST':
        spot_number = request.POST.get('spot_number')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        payment_method = request.POST.get('payment_method')
        spot = get_object_or_404(ParkingSpace, spot_number=spot_number)
        # Здесь можно добавить проверку, что на эти даты место всё ещё свободно!
        Booking.objects.create(
            user=request.user if request.user.is_authenticated else None,
            spot=spot,
            start_date=start_date,
            end_date=end_date,
            payment_method=payment_method
        )
        return render(request, 'parking/success.html', {
            'spot': spot,
            'start_date': start_date,
            'end_date': end_date,
            'payment_method': payment_method,
        })
    else:
        return redirect('booking_search')

def booking_search(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    context = {}

    if start_date and end_date:
        spots = ParkingSpace.objects.all()
        spot_statuses = []
        for spot in spots:
            is_booked = Booking.objects.filter(
                spot=spot,
                start_date__lt=end_date,
                end_date__gt=start_date
            ).exists()
            spot_statuses.append({
                'spot': spot,
                'status': "Занято/Забронировано" if is_booked else "Свободно",
            })
        context['spot_statuses'] = spot_statuses
        context['start_date'] = start_date
        context['end_date'] = end_date

    return render(request, 'parking/booking_search.html', context)

def index(request):
    return render(request, 'parking/index.html')

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
    if not (start_date and end_date):
        # Если даты не переданы — редирект обратно на поиск
        return redirect('booking_search')
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


def logout_view(request):
    logout(request)
    return redirect('login')

def confirm_booking(request):
    if request.method == 'POST':
        spot_id = request.POST.get('spot_id')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        payment_method = request.POST.get('payment_method')
        spot = get_object_or_404(ParkingSpace, id=spot_id)
        Booking.objects.create(
            user=request.user if request.user.is_authenticated else None,
            spot=spot,
            start_date=start_date,
            end_date=end_date,
            payment_method=payment_method
        )
        return render(request, 'parking/success.html', {
            'spot': spot,
            'start_date': start_date,
            'end_date': end_date,
            'payment_method': payment_method,
        })
    return redirect('booking_search')