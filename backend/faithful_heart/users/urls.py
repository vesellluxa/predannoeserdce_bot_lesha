from django.urls import path
from users import views

urlpatterns = [
    path('download-excel/', views.download_excel_file, name='download_excel_file'),
    path('download_user_information/', views.show_download_page, name='show_download_page'),
]