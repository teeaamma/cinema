from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

User = get_user_model()


class Hall(models.Model):
    name = models.CharField("Название", max_length=200)
    capacity = models.PositiveIntegerField("Вместимость")

    class Meta:
        verbose_name = "Кинозал"
        verbose_name_plural = "Кинозалы"

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField("Название", max_length=200)
    description = models.TextField("Описание")
    duration = models.DurationField("Продолжительность")
    poster = models.ImageField("Постер", upload_to='posters')

    class Meta:
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"

    def __str__(self):
        return self.title


class Session(models.Model):
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        verbose_name="Фильм",
        related_name="sessions"
    )
    hall = models.ForeignKey(
        Hall,
        on_delete=models.CASCADE,
        verbose_name="Кинозал",
        related_name="sessions"
    )
    start_time = models.DateTimeField()

    class Meta:
        verbose_name = "Сеанс"
        verbose_name_plural = "Сеансы"

    def __str__(self):
        return f"Фильм: {self.movie.title} в зале: {self.hall.name} в {self.start_time}"

    def get_available_seats(self):
        reserved_seats = self.reservations.values_list(
            'seat__number',
            flat=True
            )
        return [
            seat for seat in range(1, self.hall.capacity + 1)
            if seat not in reserved_seats
            ]
    
    def get_absolute_url(self):
        # Возвращаем URL для детальной страницы сеанса
        return reverse('cinema:session_detail', kwargs={'session_id': self.id})


class Seat(models.Model):
    session = models.ForeignKey(
        Session,
        on_delete=models.CASCADE,
        verbose_name="Сеанс",
        related_name="seats"
    )
    number = models.PositiveIntegerField("Номер места")
    is_reserved = models.BooleanField(
        default=False,
        verbose_name="Занято ли место"
        )

    class Meta:
        verbose_name = "Место"
        verbose_name_plural = "Места"

    def __str__(self):
        return f"Место {self.number}"


class Reservation(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "Ожидает"),
        ("CONFIRMED", "Подтверждено"),
        ("CANCELLED", "Отменено"),
    ]
    session = models.ForeignKey(
        Session,
        on_delete=models.CASCADE,
        verbose_name="Сеанс",
        related_name="reservations"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Зритель",
        related_name="reservations"
    )
    seat = models.ForeignKey(
        Seat,
        on_delete=models.CASCADE,
        verbose_name="Место",
        related_name="reservations"
    )
    status = models.CharField(
        "Статус",
        max_length=10,
        choices=STATUS_CHOICES,
        default="PENDING"
    )

    class Meta:
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"

    def __str__(self):
        return (f"Фильм: {self.session.movie.title}"
                f"(Место {self.seat.number})"
                )
