from .models import Client, ParkingSpace, Car, Rental, Payment
from django.contrib import admin
from .models import ParkingSpace

@admin.register(ParkingSpace)
class ParkingSpaceAdmin(admin.ModelAdmin):
    list_display = ('spot_number', 'location', 'status')

admin.site.register(Client)
#admin.site.register(ParkingSpace)
admin.site.register(Car)
admin.site.register(Rental)
admin.site.register(Payment)