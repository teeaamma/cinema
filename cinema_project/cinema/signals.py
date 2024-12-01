from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from .models import Movie, Session, Reservation

@receiver(post_migrate)
def create_user_groups(sender, **kwargs):

    # Создаем группы
    admin_group, _ = Group.objects.get_or_create(name='Admin')
    cashier_group, _ = Group.objects.get_or_create(name='Cashier')

    # Получаем ContentType для моделей
    movie_content_type = ContentType.objects.get_for_model(Movie)
    session_content_type = ContentType.objects.get_for_model(Session)
    reservation_content_type = ContentType.objects.get_for_model(Reservation)

    # Проверяем и создаем разрешения
    if not Permission.objects.filter(codename='add_movie', content_type=movie_content_type).exists():
        add_movie_permission = Permission.objects.create(
            codename='add_movie',
            name='Can add movie',
            content_type=movie_content_type,
        )
        admin_group.permissions.add(add_movie_permission)

    if not Permission.objects.filter(codename='add_session', content_type=session_content_type).exists():
        add_session_permission = Permission.objects.create(
            codename='add_session',
            name='Can add session',
            content_type=session_content_type,
        )
        admin_group.permissions.add(add_session_permission)

    if not Permission.objects.filter(codename='process_reservation', content_type=reservation_content_type).exists():
        process_reservation_permission = Permission.objects.create(
            codename='process_reservation',
            name='Can process reservation',
            content_type=reservation_content_type,
        )
        cashier_group.permissions.add(process_reservation_permission)
