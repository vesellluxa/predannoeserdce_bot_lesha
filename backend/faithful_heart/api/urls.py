from django.urls import include, path

app_name = 'api'

urlpatterns = [
    path('', include('djoser.urls'), name='djoser'),
    path('auth/', include('djoser.urls.authtoken')),
]
