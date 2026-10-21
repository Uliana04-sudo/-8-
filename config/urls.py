from django.http import JsonResponse
from django.contrib import admin
from django.urls import include, path
def healthz(request):
    return JsonResponse({"status": "ok"})
urlpatterns = [
 path('healthz/', healthz, name='healthz'),
 path('admin/', admin.site.urls),
 path('accounts/',
 include('django.contrib.auth.urls')),
 path('', include('accounts.urls')),
 path('', include('tickets.urls')),
]
