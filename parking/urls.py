from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='parking/login.html'), name='login'),
    path('register/', views.register, name='register'),
    path('accounts/profile/', views.profile, name='profile'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.index, name='index'),
    path('booking/', views.booking_view, name='booking'),
    #path('book/<int:spot_id>/', views.book_spot, name='book_spot_by_id'),
    #path('confirm_booking/', views.confirm_booking, name='confirm_booking'),
    path('feedback/', views.feedback, name='feedback'),
    path('spot-search/', views.spot_search_view, name='spot_search'),
    path('booking/search/', views.booking_search, name='booking_search'),
    path('confirm_booking/', views.confirm_booking, name='confirm_booking'),
    path('parking/search/', views.parking_search, name='parking_search'),
    path('book/<int:spot_id>/', views.book_spot, name='book_spot'),
    path('payment/<int:booking_id>/', views.payment_page, name='payment_page'),
]
