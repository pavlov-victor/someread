from django.contrib import admin
from django.urls import path, include

api_urls = [
    path('api/v1/', include('books.urls'))
]

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += api_urls
