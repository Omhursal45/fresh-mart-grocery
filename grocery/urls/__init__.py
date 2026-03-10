from django.urls import path, include

urlpatterns = [
    path('', include('grocery.urls.web')),
    path('api/', include('grocery.urls.api')),
]
