from django.urls import path, include

urlpatterns = [
    # ... other patterns ...
    path('api/', include('api.urls')),  # Include the api.urls module
]
