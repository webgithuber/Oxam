from django.shortcuts import render , redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import Candidate , Image
from django.contrib import messages
from django.contrib.auth import login, authenticate , logout
from django.contrib.auth.forms import AuthenticationForm
from django.core.files.base import ContentFile
import datetime
import base64
import json
from PIL import Image as pil
from io import BytesIO
def allow_cors(view_func):
    def wrapped_view(request, *args, **kwargs):
        response = view_func(request, *args, **kwargs)
        response["Access-Control-Allow-Origin"] = "https://www.hackerearth.com"
        response["Access-Control-Allow-Methods"] = "POST"
        response["Access-Control-Allow-Headers"] = "Content-Type"
        return response
    return wrapped_view

# Create your views here.

def dashboard(request):
    pass

@allow_cors
@csrf_exempt
def starttest(request):
    print("start test")
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        email = data.get('email')
        code = data.get('code')
        print(name,email,code)
        if name and email and code:
            if Candidate.objects.filter(email=email,activation_code=code).count()==0:
                Candidate(name=name,email=email,activation_code=code).save()
            return JsonResponse({'status': 'success'})
        else:
           return JsonResponse({'status': 'error'})
    else:
        return JsonResponse({'status': 'error'})
    

@allow_cors
@csrf_exempt
def saveimg(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            image_data = data.get('image')
            email = data.get('email')
            code = data.get('code')
            today=datetime.datetime.now()
            print("image => ", email,code)
            if image_data:
                # Save image data to the database
                image_model = Image(image_data=image_data, activation_code=code, email=email,created_at=today)
                image_model.save()
            return JsonResponse({'status': 'success'})
        else:
            raise Exception("Invalid request method.")
    except Exception as e:
        print("Error occurred: ", str(e))
        return JsonResponse({'status': 'error'})
    



def show_image(request, image_id):
    if not request.user.is_authenticated:
        return redirect("dashboard:admin_login")
    image = Image.objects.get(id=image_id)
    image=image.image_data
    image=image[image.index(',')+1:]
    bytes_decoded=base64.b64decode(image)
    img=pil.open(BytesIO(bytes_decoded))
    image_buffer = BytesIO()
    img.save(image_buffer, format='PNG')
    response = HttpResponse(image_buffer.getvalue(), content_type='image/png')
    return response
    
    


def list(request):
    if not request.user.is_authenticated:
        return redirect("dashboard:admin_login")
    candidates=Candidate.objects.all()
    return render(request,"dashboard/list.html",{"candidates":candidates,"home":1})


def detail(request,email,code):
    if not request.user.is_authenticated:
        return redirect("dashboard:admin_login")
    images=Image.objects.filter(email=email,activation_code=code)
    lst=[]
    for img in images:
        lst.append(img)
    return render(request,"dashboard/candidate.html",{"images":lst,"home":1})

    return render(request,'dashboard/candidate.html')

def admin_login(request):
    error=''
    if request.user.is_authenticated:
        return redirect("dashboard:list")
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            print(user)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("dashboard:list")
            else:
               error="Invalid username or password."
        else:
           error="Invalid username or password."
    return render(request,'dashboard/admin_login.html',{"error":error})


def logout_request(request):
    if not request.user.is_authenticated:
        return redirect("dashboard:admin_login")
    logout(request)
    return redirect('dashboard:admin_login')

    
