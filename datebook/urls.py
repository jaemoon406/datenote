from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('v1/account/', include('apps.user.urls')),
    path('v1/auth/', include('apps.auth.urls')),
    path('v1/', include('apps.book.urls')),
]
