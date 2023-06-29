from django.shortcuts import render


def profile(request):
    return render(request,'restaurant/restProfile.html')
