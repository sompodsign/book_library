
from django.contrib import admin
from django.urls import path, include

app_name = 'account'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('library.urls', namespace='books')),
    path('account/', include('account.urls', namespace='account')),
    path('account/', include('django.contrib.auth.urls')),
]
