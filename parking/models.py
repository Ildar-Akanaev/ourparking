from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='client', null=True, blank=True)
    last_name = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    patronymic = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

class ParkingSpace(models.Model):
    STATUS_CHOICES = (
        ('free', 'Свободно'),
        ('occupied', 'Занято'),
        ('reserved', 'Зарезервировано'),
    )

    spot_number = models.CharField(max_length=10)
    location = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    def __str__(self):
        return f"Место #{self.spot_number} — {self.location}"

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    spot = models.ForeignKey(ParkingSpace, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"Бронь #{self.id} — {self.spot} ({self.start_date} — {self.end_date})"

class Rental(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='rentals')
    parking_space = models.ForeignKey(ParkingSpace, on_delete=models.CASCADE, related_name='rentals')
    start_date = models.DateField()
    end_date = models.DateField()
    price = models.IntegerField()

    def __str__(self):
        return f"Rental {self.id} for {self.client} at {self.parking_space}"

class Car(models.Model):
    license_plate = models.CharField(max_length=20)
    brand = models.CharField(max_length=24)
    color = models.CharField(max_length=24, blank=True, null=True)
    rental = models.OneToOneField(Rental, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.brand} ({self.license_plate})"

class Payment(models.Model):
    rental = models.ForeignKey(Rental, on_delete=models.CASCADE)
    amount = models.IntegerField()
    payment_date = models.DateField()
    payment_method = models.CharField(max_length=255)

    def __str__(self):
        return f"Payment {self.id} of {self.amount} by {self.payment_method} on {self.payment_date}"

class Feedback(models.Model):
    subject = models.CharField(max_length=255, verbose_name='Тема письма')
    email = models.EmailField(max_length=255, verbose_name='Электронный адрес (email)')
    content = models.TextField(verbose_name='Содержимое письма')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата отправки')
    ip_address = models.GenericIPAddressField(verbose_name='IP отправителя', blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Пользователь')

    def __str__(self):
        return f"{self.subject} ({self.email})"


