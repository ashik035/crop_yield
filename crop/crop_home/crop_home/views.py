from django.shortcuts import render
from django.http import JsonResponse
def home(request):
        #    call='this page is now dynamic'
        #    response='Thanks for reading this tutorial!'
        #    context={'call':call, 'response':response}
        #    return render(request, 'home.html', context)
    return render(request, 'home.html')

def get_rediction(request):
    data = {
        'payload' : request.GET,
        'status' : 'success',
        'prediction' : '75',
        'suggestion' : 'rice'
    }
    return JsonResponse(data)