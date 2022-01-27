from django.contrib import admin
from django.urls import include, path
from django.conf.urls.i18n import i18n_patterns

# TODO language select interface - maybe default to user pref somehow
urlpatterns = i18n_patterns(
    path('', include('lac.urls'))
)

urlpatterns += [path('admin/', admin.site.urls)]
