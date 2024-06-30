from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to Elibrary-Hub Admin Panel")