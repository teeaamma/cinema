from django.contrib import admin
from .models import Hall, Movie, Session, Seat, Reservation


@admin.register(Hall)
class HallAdmin(admin.ModelAdmin):
    pass


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    pass


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    pass


@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    pass


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    pass
