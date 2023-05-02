from django.http import HttpResponse

def check_server(request):
    return HttpResponse('Server is up and running')