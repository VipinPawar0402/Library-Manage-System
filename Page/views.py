from urllib import request
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import Person
from django.contrib.auth import logout 
from django.views.generic import TemplateView


def person(request):
    """
    Handles the creation of a new person from form input.
    """
    # if request.method == "POST":
    #     name = request.POST.get('name')
    #     mobile = request.POST.get('mobile')
    #     email = request.POST.get('email')
    #     password = request.POST.get('password')

    #     # Save the new person to the database
    #     person_instance = Person(name=name, mobile=mobile, email=email, password=password)
    #     person_instance.save()

    return render(request, 'signin.html')


@csrf_exempt
def send_data(request):
    """
    Handles the creation of a new person using raw POST data.
    """
    if request.method == "POST":
        data = request.POST.dict()
        print(data, '..................data')

        # Create a new person record from POST data
        Person.objects.create(**data)
        return HttpResponse('success')

    return HttpResponse('Invalid request method', status=405)



def persondata(request):
    """
    Retrieves all persons and renders them on the person page.
    """
    persons = Person.objects.all()

    # try:
    #     specific_person = Person.objects.filter(name='rohan')
    #     print(specific_person, '...............')

    #     specific_person_by_id = Person.objects.get(id=28)
    #     print(specific_person_by_id, '...............')
    # except Person.DoesNotExist:
    #     print('Person with specified ID or name does not exist.')

    return render(request, 'person.html', {"persons": persons})


def delete_data(request, person_id):
    """
    Deletes a person record by ID.
    """
    person = get_object_or_404(Person, id=person_id)
    person.delete()
    return JsonResponse({'message': 'Item deleted'})


def edit_data(request, person_id):
    """
    Fetches a person's data by ID and returns it as JSON.
    """
    person = get_object_or_404(Person, id=person_id)
    data = {
        "id": person.id,
        "name": person.name,
        "mobile": person.mobile,
        "email": person.email,
    }
    return JsonResponse(data)


@csrf_exempt
def update_data(request):
    """
    Updates a person's data.
    """
    if request.method == "POST":
        person_id = request.POST.get("id")
        name = request.POST.get("name")
        mobile = request.POST.get("mobile")
        email = request.POST.get("email")

        try:
            person = Person.objects.get(id=person_id)
            person.name = name
            person.mobile = mobile
            person.email = email
            person.save()
            return JsonResponse({"message": "success"})
        except Person.DoesNotExist:
            return JsonResponse({"message": "Person not found"}, status=404)

    return JsonResponse({"message": "Invalid request method"}, status=405)


def show_date(request):
    """
    Renders the HTML template for showing the current date.
    """
    return render(request, 'show_date.html')


def show_time(request):
    """
    Renders the HTML template for time difference calculation.
    """
    return render(request, 'show_time.html')

@csrf_exempt
def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        # Check if the user exists and credentials match
        try:
            if Person.objects.filter(email=email,password=password).exists():
                person = Person.objects.get(email=email,password=password)
                    # Store user ID in the session to mark the user as logged in
                request.session['user_id'] = person.id ### session {}, sesstion['name'] = 'kunal',  del request.session['user_id']
                return JsonResponse({'success': True, 'userId':person.id})
            else:
                return JsonResponse({'success': False, 'message': 'Invalid credentials'})
        except Person.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'User not found'})

    return render(request, 'login.html')

def person_view(request, pid):
    persons = Person.objects.get(id=pid)
    return render(request, 'person_details.html', {"person": persons})

def logout_view(request):
    # logout(request)  # Log out the user
    if request.session.get('user_id'):
        del request.session['user_id']
    return redirect('/login') 

class HeaderView(TemplateView):
    template_name = "layouts/header.html"

class SidebarView(TemplateView):
    template_name = "layouts/sidebar.html"    

class BaseView(TemplateView):
    template_name = "layouts/base.html"  

def person_table(request):
    persons = Person.objects.all()
    return render(request, 'person_table.html',{'persons':persons})

@csrf_exempt
def login_page(request):
     if request.method == "POST":
        name = request.POST.get('username')
        password = request.POST.get('password')
        # Check if the user exists and credentials match
        try:
            if Person.objects.filter(name=name,password=password).exists():
                person = Person.objects.get(name=name,password=password)
                    # Store user ID in the session to mark the user as logged in
                request.session['user_id'] = person.id ### session {}, sesstion['name'] = 'kunal',  del request.session['user_id']
                return JsonResponse({'status': 1, 'userId':person.id})
            else:
                print('mmmmmmmmmmmmmmmmmmm')
                return JsonResponse({'status': 0, 'message': 'Invalid credentials'})
        except Person.DoesNotExist:
            return JsonResponse({'status': 0, 'message': 'User not found'})
     return render(request, 'login_page.html')

import random
from django.core.mail import send_mail
from django.conf import settings
@csrf_exempt
def send_otp(request):
    if request.method == "POST":
        # Get email from POST request
        email = request.POST.get('email')

        # Validate that the email is provided
        if not email:
            return JsonResponse({"status": 0, "error": "Email address is required"}, status=400)

        # Generate a random OTP
        otp = random.randint(1000, 9999)

        try:
            # Store OTP in session for validation
            request.session['otp'] = otp
            request.session['email'] = email  # Save the email for later validation
            
            # Send OTP via email
            send_mail(
                'Forgot Password',
                f'Your OTP is {otp}',
                settings.EMAIL_HOST_USER,
                [email]
            )
            return JsonResponse({"status": 1, "message": "OTP sent successfully"})
        except Exception as e:
            return JsonResponse({"status": 0, "error": f"Failed to send email: {str(e)}"}, status=500)

    # Handle non-POST requests
    return JsonResponse({"status": 0, "error": "Invalid request method"}, status=405)


def forget_page(request):

    return render(request,'forget-page.html')

def verify_otp(request):
    if request.method == "POST":
        # Get the OTP entered by the user
        entered_otp = request.POST.get('otp')

        # Retrieve the OTP and email from the session
        session_otp = request.session.get('otp')
        email = request.session.get('email')

        # Validate inputs
        if not entered_otp:
            return JsonResponse({"status": 0, "error": "OTP is required"}, status=400)

        if not session_otp:
            return JsonResponse({"status": 0, "error": "Session expired. Please request OTP again."}, status=400)

        # Check if the entered OTP matches the one in the session
        if str(entered_otp) == str(session_otp):  # Convert to string for comparison
            # Clear OTP from session
            del request.session['otp']
            del request.session['email']

            return JsonResponse({"status": 1, "message": "OTP verified successfully"})
        else:
            return JsonResponse({"status": 0, "error": "Invalid OTP"})

    # Render OTP verification page for GET requests
    return render(request, 'forget-page.html')

def set_pass(request):
    return render(request,'set-pass.html')
