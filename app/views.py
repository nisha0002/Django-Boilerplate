from django.shortcuts import render,HttpResponse

# Create your views here.
def index(request):
    # Write your code
    return render(request,'index.html')