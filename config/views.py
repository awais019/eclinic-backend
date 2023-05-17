from django.shortcuts import render

def check_server(request):
    return render(request, 'server.html')