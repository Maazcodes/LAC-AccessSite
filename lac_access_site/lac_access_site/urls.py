from django.contrib import admin
from django.urls import include, path
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _

urlpatterns = i18n_patterns(
    path('', include('lac.urls'))
)

# TODO language select interface on non-prefixed root - maybe default to user pref somehow
from lac.views import index as lac_index
urlpatterns += [path('', lac_index)]

# admin setup
admin.site.site_header = _('LAC Web Archive Admin')
urlpatterns += [path('admin/', admin.site.urls)]
