from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, TemplateView, UpdateView, DetailView
from .models import Session, Reservation, Seat

from django.db.models import Q, Case, When
from django.shortcuts import get_object_or_404, redirect, reverse
from django.views.decorators.http import require_POST

from .forms import UserUpdateForm, ReservationCreateForm, MovieForm, SessionForm

User = get_user_model()


class SessionListView(ListView):
    model = Session
    template_name = 'cinema/session_list.html'
    context_object_name = 'sessions'
    paginate_by = 8

    def get_queryset(self):
        return (Session.objects.filter(start_time__gte=now())
                .order_by('start_time')
                .select_related('movie', 'hall')
                .prefetch_related('seats'))


class SessionDetailView(DetailView):
    model = Session
    template_name = 'cinema/session_detail.html'
    context_object_name = 'session'

    def get_object(self):
        return get_object_or_404(Session, id=self.kwargs['session_id'])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        session = self.get_object()

        # Создаем форму бронирования
        form = ReservationCreateForm(session=session, user=self.request.user)

        # Добавляем форму в контекст
        context['form'] = form
        return context

    def post(self, request, *args, **kwargs):
        session = self.get_object()
        seat_id = request.POST.get('seat')  # Получаем ID выбранного места
        seat = get_object_or_404(Seat, id=seat_id, session=session)

        # Проверяем, свободно ли место
        if seat.is_reserved:
            return render(request, self.template_name, {
                'session': session,
                'form': ReservationCreateForm(session=session, user=request.user),
                'error_message': "Это место уже забронировано."
            })

        # Создаем бронирование
        reservation = Reservation.objects.create(
            session=session,
            user=request.user,
            seat=seat,
            status='PENDING'
        )

        # Изменяем статус места на занятое
        seat.is_reserved = True
        seat.save()

        # Перенаправляем пользователя на страницу профиля
        return redirect('cinema:profile', username=request.user.username)


class ProfileView(TemplateView):
    template_name = 'cinema/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.kwargs['username']
        user = get_object_or_404(get_user_model(), username=username)
        context['profile'] = user

        if user.groups.filter(name='Admin').exists():
            role = 'Администратор'
        elif user.groups.filter(name='Cashier').exists():
            role = 'Кассир'
        else:
            role = 'Зритель'

        context['role'] = role

        if role == 'Кассир':
            # Для кассира добавляем пользователя в запрос
            user_reservations = (
                Reservation.objects.select_related('session', 'seat', 'session__movie', 'user')
                .order_by(
                    Case(
                        When(status='PENDING', then=0),
                        When(status='CONFIRMED', then=1),
                        When(status='CANCELLED', then=2),
                        default=3,
                    )
                )
            )
        elif role == 'Зритель':
            user_reservations = (
                Reservation.objects.filter(user=user)
                .select_related('session', 'seat', 'session__movie')
            )
        else:
            user_reservations = None

        context['user_reservations'] = user_reservations
        return context


class ProfileUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = get_user_model()
    form_class = UserUpdateForm
    template_name = 'cinema/user.html'

    def test_func(self):
        return self.request.user.id == self.get_object().id

    def handle_no_permission(self):
        user = self.get_object()
        return redirect('cinema:profile', username=user.username)

    def get_success_url(self):
        context = self.get_context_data()
        user = context['user']
        user_username = user.username
        return reverse('cinema:profile', kwargs={'username': user_username})


@login_required
@require_POST
def update_reservation_status(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    if request.user.groups.filter(name='Cashier').exists():
        status = request.POST.get('status')
        if status in dict(Reservation.STATUS_CHOICES):
            reservation.status = status
            reservation.save()
    return redirect('cinema:profile', username=request.user.username)


@login_required
def add_movie(request):
    if not request.user.groups.filter(name='Admin').exists():
        raise Http404("У вас нет прав для доступа к этой странице.")
    
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('cinema:profile', username=request.user.username)
    else:
        form = MovieForm()

    return render(request, 'cinema/add_movie.html', {'form': form})


@login_required
def add_session(request):
    if not request.user.groups.filter(name='Admin').exists():
        raise Http404("У вас нет прав для доступа к этой странице.")
    
    if request.method == 'POST':
        form = SessionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cinema:profile', username=request.user.username)
    else:
        form = SessionForm()

    return render(request, 'cinema/add_session.html', {'form': form})