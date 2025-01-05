from pyexpat.errors import messages
from urllib import request
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import Book, BookReturned, Category, IssueBook, Person, Stuff
from django.contrib.auth import logout 
from django.views.generic import TemplateView
from django.contrib.auth.hashers import make_password
from datetime import datetime

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

        # Check if the email already exists
        if Person.objects.filter(email=data.get('email')).exists():
            return JsonResponse({'message': 'error', 'details': 'Email already exists'}, status=400)

        # Create a new person record from POST data
        Person.objects.create(**data)
        return JsonResponse({'message': 'success'})

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


# def edit_data(request, person_id):
#     """
#     Fetches a person's data by ID and returns it as JSON.
#     """
#     person = get_object_or_404(Person, id=person_id)
#     data = {
#         "id": person.id,
#         "name": person.name,
#         "mobile": person.mobile,
#         "email": person.email,
#     }
#     return JsonResponse(data)


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
        address = request.POST.get("address")
        birthdate = request.POST.get("birthdate")

        try:
            person = Person.objects.get(id=person_id)
            person.name = name
            person.mobile = mobile
            person.email = email
            person.address = address
            person.birthdate = birthdate
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

@csrf_exempt
def forget_page(request):

    return render(request,'forget-page.html')

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

        # Check if the email exists in the database
        if not Person.objects.filter(email=email).exists():
            return JsonResponse({"status": 0, "error": "Email not found in the database"}, status=404)

        # Generate a random OTP
        otp = random.randint(1000, 9999)
        print(otp)

        try:
            # Get the person object
            person = Person.objects.get(email=email)

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


@csrf_exempt
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
            request.session.pop('otp', None)
            request.session.pop('email',None)   

            return JsonResponse({"status": 1, "message": "OTP verified successfully", "email": email})
        else:
            return JsonResponse({"status": 0, "error": "Invalid OTP"}, status=400)

    
    return render(request, 'forget-page.html')
    

@csrf_exempt
def set_pass(request):
    if request.method == 'POST':
        newPassword = request.POST.get('newPassword')
        confirmPassword = request.POST.get('confirmPassword')
        email = request.POST.get("email")
        print(newPassword)

        if newPassword and confirmPassword:
            if newPassword == confirmPassword:
                try:
                    person = Person.objects.get(email=email)
                    print(person)
                    person.password = newPassword
                    person.save()  # Save the changes
                    return JsonResponse({"status": 1, "message": "Password updated successfully"})
                except Person.DoesNotExist:
                    messages.error(request, 'No user found with the provided email.')
                except Exception as e:
                    messages.error(request, f"An error occurred: {e}")
            else:
                messages.error(request, 'Passwords do not match.')
        else:
            messages.error(request, 'Both fields are required.')

    return render(request, 'forget-page.html')

def index(request):
    return render(request, 'index.html')

def all_books(request):
    books = Book.objects.all()
    print(books)
    return render(request, 'books.html', {'books': books , 'category': Category.objects.all()})

def all_category(request):
    category = Category.objects.all()
    return render(request, 'category.html', {'category': category})

def stuff(request):
    stuff = Stuff.objects.all()
    print(stuff)
    return render(request, 'stuff.html', {'stuff': stuff})
@csrf_exempt
def update_stuff(request):
    if request.method == 'POST':
        stuff_id = request.POST.get('id')
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')

        try:
            stuff = Stuff.objects.get(id=stuff_id)
            stuff.name = name
            stuff.mobile = mobile
            stuff.email = email
            stuff.save()
            return JsonResponse({'message': 'success'})
        except Stuff.DoesNotExist:
            return JsonResponse({'message': 'Stuff not found'}, status=404)
    return JsonResponse({'message': 'Invalid request method'}, status=405)

@csrf_exempt
def delete_stuff(request):
    if request.method == 'POST':
        stuff_id = request.POST.get('id')
        try:
            stuff = Stuff.objects.get(id=stuff_id)
            stuff.delete()
            return JsonResponse({'message': 'success'})
        except Stuff.DoesNotExist:
            return JsonResponse({'message': 'Stuff not found'}, status=404)
    return JsonResponse({'message': 'Invalid request method'}, status=405)


@csrf_exempt
def add_stuff(request):
    if request.method == 'POST':
        data = request.POST.dict()
        print(data, '..................data')

        # Create a new person record from POST data
        Stuff.objects.create(**data)
        return JsonResponse({'message': 'success'})

    return HttpResponse('Invalid request method', status=405)

@csrf_exempt
def add_book(request):
    if request.method == 'POST':
        data = {
            'title': request.POST.get('title'),
            'author': request.POST.get('author'),
            'category_id': request.POST.get('category'),  # Get the category ID
            'price': request.POST.get('price'),
            'date_added': request.POST.get('date_added'),
        }

        # Convert category_id to a Category instance
        try:
            category = Category.objects.get(id=data['category_id'])
            data['category'] = category
        except Category.DoesNotExist:
            return render(request, 'books.html', {'error': 'Invalid category'})

        # Remove category_id from data
        del data['category_id']

        # Create the Book object
        Book.objects.create(**data)
        return JsonResponse({'message':'success'})  # Redirect to the books page after adding the book

    return render(request, 'add_book.html')

@csrf_exempt
def delete_book(request):
    if request.method == 'POST':
        book_id = request.POST.get('id')
        try:
            book = Book.objects.get(id=book_id)
            book.delete()
            return JsonResponse({'message': 'success'})
        except Book.DoesNotExist:
            return JsonResponse({'message': 'Book not found'}, status=404)
    return JsonResponse({'message': 'Invalid request method'}, status=405)

@csrf_exempt
def edit_book(request):
    if request.method == 'POST':
        book_id = request.POST.get('id')
        title = request.POST.get('title')
        author = request.POST.get('author')
        category_id = request.POST.get('category')
        price = request.POST.get('price')
        date_added = request.POST.get('date_added')

        book = get_object_or_404(Book, id=book_id)
        book.title = title
        book.author = author
        book.category = get_object_or_404(Category, id=category_id)
        book.price = price
        book.date_added = date_added
        book.save()

        return JsonResponse({'message': 'success'})

    return JsonResponse({'message': 'Invalid request method'}, status=405)

@csrf_exempt
def add_category(request):
    if request.method == 'POST':
        category = request.POST.get('category')
        Category.objects.create(subject=category)
        return JsonResponse({'message': 'success'})
    return JsonResponse({'message': 'Invalid request method'}, status=405)

@csrf_exempt
def delete_category(request):
    if request.method == 'POST':
        category_id = request.POST.get('id')
        try:
            category = Category.objects.get(id=category_id)
            category.delete()
            return JsonResponse({'message': 'success'})
        except Category.DoesNotExist:
            return JsonResponse({'message': 'Category not found'}, status=404)
    return JsonResponse({'message': 'Invalid request method'}, status=405)

@csrf_exempt
def edit_category(request):
    if request.method == 'POST':
        category_name = request.POST.get('category')
        try:
            category = Category.objects.get(id=request.POST.get('id'))
            category.subject = category_name
            category.save()
            return JsonResponse({'message': 'success'})
        except Category.DoesNotExist:
            return JsonResponse({'message': 'Category not found'}, status=404)
    return JsonResponse({'message': 'Invalid request method'}, status=405)

@csrf_exempt
def add_student(request):
    return render(request, 'add-student.html')

@csrf_exempt
def add_staff(request):
    return render(request, 'add-staff.html')

@csrf_exempt
def edit_student(request, id):
    person = Person.objects.get(id=id)
    return render(request, 'edit-student.html', {'person': person})

@csrf_exempt
def edit_staff(request, id):
    stuff = Stuff.objects.get(id=id)
    return render(request, 'edit-staff.html', {'stuff': stuff})

@csrf_exempt
def issue_book(request):
    issue_book = IssueBook.objects.all()
    return render(request, "issue-book.html", {'issue_book':issue_book, 'persons':Person.objects.all(), 'books': Book.objects.all(), 'stuff': Stuff.objects.all()})

def issue_table(request):
    issue_book = IssueBook.objects.all()

    for issue in issue_book:
        if issue.issue_date == issue.end_date:
            end_time = datetime.now().time()
            issue_time = issue.issue_time
            end_datetime = datetime.combine(issue.issue_date, end_time)
            issue_datetime = datetime.combine(issue.issue_date, issue_time)
            diff = end_datetime - issue_datetime
            df = diff.seconds / 3600 
            issue.total_charges = int(df) * float(issue.charges)
        else:
            if datetime.now().date() > issue.end_date:
                end_date = datetime.now().date()
            else:
                end_date = issue.end_date
            issue_date = issue.issue_date
            # Calculate total charges based on days
            diff_days = (end_date - issue_date).days
            issue.total_charges = diff_days * float(issue.charges)

    return render(request, "issue-table.html", {'issue_book': issue_book, 'persons':Person.objects.all(), 'books': Book.objects.all(), 'stuff': Stuff.objects.all()})

@csrf_exempt
def save_issuedbook(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        student_id = request.POST.get('student_id')
        book_id = request.POST.get('book_id')
        staff_id = request.POST.get('staff_id')
        charges = request.POST.get('charges')
        issue_date = request.POST.get('issue_date')
        issue_time = request.POST.get('issue_time')
        end_date = request.POST.get('end_date')
        selected_value = request.POST.get('selectedValue')

        student = get_object_or_404(Person, id=student_id)
        book = get_object_or_404(Book, id=book_id)
        staff = get_object_or_404(Stuff, id=staff_id)

        issue_book = IssueBook(
            student = student,
            book = book,
            staff = staff,
            charges = charges,
            issue_date = issue_date,
            issue_time = issue_time,
            end_date = end_date,
            selected_value = selected_value
        )
        issue_book.save()

        return JsonResponse({'message': 'success'})

    return JsonResponse({'message': 'Invalid request method'}, status=405)

@csrf_exempt
def update_issuedbook(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        student_id = request.POST.get('student_id')
        book_id = request.POST.get('book_id')
        staff_id = request.POST.get('staff_id')
        charges = request.POST.get('charges')
        issue_date = request.POST.get('issue_date')
        issue_time = request.POST.get('issue_time')
        end_date = request.POST.get('end_date')
        typeOf_issue = request.POST.get('selectedValue')

        issue_book = get_object_or_404(IssueBook, id=id)
        student = get_object_or_404(Person, id=student_id)
        book = get_object_or_404(Book, id=book_id)
        staff = get_object_or_404(Stuff, id=staff_id)

        issue_book.student = student
        issue_book.book = book
        issue_book.staff = staff
        issue_book.charges = charges
        issue_book.issue_date = issue_date
        issue_book.issue_time = issue_time
        issue_book.end_date = end_date
        issue_book.typeOf_issue = typeOf_issue
        issue_book.save()

        return JsonResponse({'message': 'success'})

    return JsonResponse({'message': 'Invalid request method'}, status=405)


@csrf_exempt
def delete_issuedbook(request, id):
    if request.method == 'POST':
        issue_book = get_object_or_404(IssueBook, id=id)
        issue_book.delete()
        return JsonResponse({'message': 'success'})

    return JsonResponse({'message': 'Invalid request method'}, status=405)

@csrf_exempt
def return_status(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        book_id = request.POST.get('book_id')
        staff_id = request.POST.get('staff_id')
        issue_book_id = request.POST.get('id')
        return_date = request.POST.get('returnDate')
        return_charges = request.POST.get('returncharges')

        issue_book = get_object_or_404(IssueBook, id=issue_book_id)
        student = get_object_or_404(Person, id=student_id)
        book = get_object_or_404(Book, id=book_id)
        staff = get_object_or_404(Stuff, id=staff_id)
        
        return_book = BookReturned(
            student=student,
            book=book,
            staff=staff,
            issue_date=issue_book.issue_date,  
            returned_date=return_date,
            total_charges=return_charges,
            status='Returned'
        )
        return_book.save()
        issue_book.delete()

        return JsonResponse({'message': 'success'})

    return JsonResponse({'message': 'Invalid request method'}, status=405)

def returnbook_page(request):
    return_book = BookReturned.objects.all()
    return render(request, 'return-status.html', {'return_book':return_book})

def edit_issuedbook(request,id):
    issue_book = IssueBook.objects.all()
    issue_book = get_object_or_404(IssueBook , id=id)
    issue_book.issue_date = issue_book.issue_date.strftime('%Y-%m-%d')
    issue_book.end_date = issue_book.end_date.strftime('%Y-%m-%d')
    issue_book.issue_time = issue_book.issue_time.strftime('%H:%M')

    return render(request, "issue-booktimedit.html", {'issue_book':issue_book, 'persons':Person.objects.all(), 'books': Book.objects.all(), 'stuff': Stuff.objects.all()})