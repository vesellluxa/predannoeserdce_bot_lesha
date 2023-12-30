from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.shortcuts import render

from users.utils import export_users_excel


@login_required
def download_excel_file(request):
    filepath = export_users_excel()
    with open(filepath, 'rb') as f:
        response = HttpResponse(
            f.read(),
            content_type='application/vnd.ms-excel'
        )
        response['Content-Disposition'] = 'inline; filename=' + filepath
        return response


@login_required
def show_download_page(request):
    return render(request, 'users/download_excel.html')
