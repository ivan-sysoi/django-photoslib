from django.urls import path, include

urlpatterns = [
    path('photo-lib-api/', include('photoslib.urls'))
]
