from django.contrib import admin
from django.urls import include, path
from django.conf.urls.i18n import i18n_patterns

urlpatterns = i18n_patterns(
    path('', include('lac.urls'))
)

# TODO language select interface on non-prefixed root - maybe default to user pref somehow
from lac.views import index as lac_index
urlpatterns += [path('', lac_index),
                path('admin/', admin.site.urls)]
