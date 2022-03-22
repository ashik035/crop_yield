from django.shortcuts import render
def home(request):
        #    call='this page is now dynamic'
        #    response='Thanks for reading this tutorial!'
        #    context={'call':call, 'response':response}
        #    return render(request, 'home.html', context)
    return render(request, 'home.html')