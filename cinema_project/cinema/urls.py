from django.contrib import admin
from django.urls import path

from . import views

app_name = "cinema"

urlpatterns = [
    path(
        '',
        views.SessionListView.as_view(),
        name='session_list'
        ),
    path(
        'sessions/<session_id>/',
        views.SessionDetailView.as_view(),
        name='session_detail'
        ),
    path(
        'reservation/<int:pk>/update/',
        views.update_reservation_status,
        name='update_reservation_status'
        ),
    path('add_movie/', views.add_movie, name='add_movie'),
    path('add_session/', views.add_session, name='add_session'),
    # path(
    #     'session/<int:session_id>/reserve/',
    #     views.reserve_seat,
    #     name='reserve_seat'
    #     ),
    # path(
    #     'reservation/<int:reservation_id>/confirmation/',
    #     views.reservation_confirmation,
    #     name='reservation_confirmation'
    #     ),
    # path(
    #     'reservations/<int:session_id>/create/',
    #     views.ReservationCreateView.as_view(),
    #     name='reservation_create'
    #     ),
    # path(
    #     'reservations/<int:pk>/detail/',
    #     views.ReservationDetailView.as_view(),
    #     name='reservation_detail'
    #     ),
    path('profile/<int:pk>/edit/',
         views.ProfileUpdateView.as_view(),
         name='edit_profile'
         ),
    path(
        'profile/<str:username>/',
        views.ProfileView.as_view(),
        name='profile'
        ),
    
]
