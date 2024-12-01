from django.contrib import admin
from django.urls import include, path, reverse_lazy
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import CreateView

from cinema.forms import UserForm

handler404 = 'pages.views.page_not_found'
handler500 = 'pages.views.server_failure'

urlpatterns = [
    path('', include('cinema.urls')),
    path(
        'auth/registration/',
        CreateView.as_view(
            template_name='registration/registration_form.html',
            form_class=UserForm,
            success_url=reverse_lazy('cinema:session_list')
        ),
        name='registration'
    ),
    path('auth/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
        )
