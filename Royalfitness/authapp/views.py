from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import stripe
from authapp.models import Contact, Enrollment, Trainer, MembershipPlan, Gallery, Attendance, about, services, free_trial
from django.conf import settings
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from Royalfitness.settings import RAZORPAY_ID,RAZORPAY_SECRET
import time

import razorpay
# Create your views here.
def Home(request):
    return render(request, 'index.html')

def create_checkout_session(request):
    if request.method == "POST":
        plan = request.POST.get("plan", "Basic")
        # Map your plan to amount in cents
        amount = 5000  # Example: 5000 = Rs. 50.00

        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'inr',
                    'product_data': {'name': plan},
                    'unit_amount': amount,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=request.build_absolute_uri('/success/'),
            cancel_url=request.build_absolute_uri('/join/'),
        )
        return redirect(session.url)

def gallery(request):
    posts=Gallery.objects.all()
    context={"posts":posts}
    return render(request,"gallery.html",context)

def profile(request):
    if not request.user.is_authenticated:
        messages.warning(request,"Please Login and Try Again")
        return redirect('/login')
    user_phone=request.user.username
    posts=Enrollment.objects.filter(PhoneNumber=user_phone)
    attendance=Attendance.objects.filter(phonenumber=user_phone)
    print(posts)
    context={"posts":posts,"attendance":attendance}
    return render(request,"profile.html",context)



def signup(request):
    if request.method == "POST":
        username=request.POST.get ('usernumber')
        email=request.POST.get ('email')
        pass1=request.POST.get ('pass1')
        pass2=request.POST.get ('pass2')
        
        if len(username)>10 or len(username)<10:
          messages.info(request, 'Phone Number must be 10 digits')
          return redirect('/signup' )
        
        
        if pass1 != pass2:
          messages.info(request, 'Password not matching')
          return redirect('/signup' )
        
        try:
           if User.objects.get(username=username):
             messages.warning(request, 'Phone Number is Taken')
             return redirect('/signup' )

        except Exception as identifier:
            pass

        try:
            if User.objects.get(email=email):
                 messages.warning(request, 'Email is Taken')
                 return redirect('/signup' )
              
        except Exception as identifier:
            pass

        myuser=User.objects.create_user(username,email,pass1)
        myuser.save()
        messages.success(request, 'Your Account has been successfully created')
        return redirect('/login' )
    
    return render(request, "signup.html")

def handlelogin(request):
    if request.method == "POST":
        username=request.POST.get ('usernumber')
        pass1=request.POST.get ('pass1')
        # Fix: authenticate with username and password, ensure username is string
        myuser=authenticate(request, username=str(username), password=pass1)
        if myuser is not None:
            login(request, myuser)
            messages.success(request, 'Successfully Logged In')
            return redirect('/' )
        else:
            messages.error(request, 'Invalid Credentials, Please try again')
            return redirect('/login' )

    return render(request, "handlelogin.html")


def handleLogout(request):
    logout(request)
    messages.success(request, 'Successfully Logged Out')
    return redirect('/login' )

def contact(request):
    if request.method == "POST":
        name=request.POST.get ('fullname')
        email=request.POST.get ('email')
        number=request.POST.get ('num')
        desc=request.POST.get ('desc')
        
        myquery=Contact(name=name, email=email, phonenumber=number, description=desc)
        myquery.save()
        messages.success(request, 'Thanks for contacting us. We will get back to you soon.')
        return redirect('/contact' )
    
    return render(request, "contact.html")



def attendance(request):
    if not request.user.is_authenticated:
        messages.warning(request,"Please Login and Try Again")
        return redirect('/login')
    SelectTrainer=Trainer.objects.all()
    context={"SelectTrainer":SelectTrainer}
    if request.method=="POST":
        phonenumber=request.POST.get('PhoneNumber')
        Login=request.POST.get('logintime')
        Logout=request.POST.get('loginout')
        SelectWorkout=request.POST.get('workout')
        TrainedBy=request.POST.get('trainer')
        query=Attendance(phonenumber=phonenumber,Login=Login,Logout=Logout,SelectWorkout=SelectWorkout,TrainedBy=TrainedBy)
        query.save()
        messages.warning(request,"Attendace Applied Success")
        return redirect('/attendance')
    return render(request,"attendance.html",context)


def enroll(request):
    if not request.user.is_authenticated:
        messages.error(request, 'You must be logged in to enroll')
        return redirect('/login')

    Membership = MembershipPlan.objects.all()
    SelectTrainer = Trainer.objects.all()
    context = {"Membership": Membership, "SelectTrainer": SelectTrainer}

    if request.method == "POST":
        FullName = request.POST.get('FullName')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        PhoneNumber = request.POST.get('PhoneNumber')
        DOB = request.POST.get('DOB')
        member_plan = request.POST.get('member')
        trainer = request.POST.get('trainer')
        reference = request.POST.get('reference')
        address = request.POST.get('address')
        request.session['enrollment_data'] = {
            'FullName': FullName,
            'Email': email,
            'Gender': gender,
            'PhoneNumber': PhoneNumber,
            'DOB': DOB,
            'SelectMembershipplan': member_plan,
            'SelectTrainer': trainer,
            'Reference': reference,
            'Address': address
        }
        
        try:
            plan_name, price_str = member_plan.split(' - ')
            amount_in_paise = int(price_str) * 100
        except (ValueError, IndexError):
            messages.error(request, "Invalid membership plan selected.")
            return redirect('/join')

        return redirect('initiate-payment')

    return render(request, "join.html", context)

def initiate_payment(request):
    enrollment_data = request.session.get('enrollment_data')
    if not enrollment_data:
        messages.error(request, "Enrollment data missing. Please try again.")
        return redirect('/join')
    
    try:
        plan_name, price_str = enrollment_data['SelectMembershipplan'].split(' - ')
        amount_in_paise = int(price_str) * 100
    except (ValueError, IndexError):
        messages.error(request, "Invalid membership plan selected.")
        return redirect('/join')

    client = razorpay.Client(auth=(RAZORPAY_ID, RAZORPAY_SECRET))
    
    receipt_id = f'receipt_{request.user.id}_{int(time.time())}'
    payment_order = client.order.create({
        "amount": amount_in_paise,
        "currency": "INR",
        "receipt": receipt_id
    })
    
    request.session['razorpay_order_id'] = payment_order['id']

    context = {
        "payment": payment_order,
        "razorpay_id": RAZORPAY_ID,
        "order_id": payment_order['id'],
        "enrollment_data": enrollment_data
    }

    return render(request, "payment.html", context)

def about(request):
    return render(request, "about.html")

def services(request):
    return render(request, "service.html")

# authapp/views.py

def free_trial(request):
    if not request.user.is_authenticated:
        messages.warning(request,"Please Login and Try Again")
        return redirect('/login')
    if request.method == "POST":
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        phonenumber = request.POST.get('phone')
        goals = request.POST.get('goals')
        myquery=free_trial(fullname=fullname, email=email, phone=phonenumber, goals=goals)
        myquery.save()
        messages.success(request, 'Thanks for .')
        return redirect('free_trial')
    return render(request, 'free-trial.html')


def payment(request,order_id):
    client=razorpay.Client(auth=(RAZORPAY_ID,RAZORPAY_SECRET))
    data={"amount":500, "currency":"INR", "receipt":f'{order_id}'}
    payment=client.order.create(data=data)
    template_name="payment.html"
    context={
        "payment":payment,
        "razorpay_id":RAZORPAY_ID,
        "order_id":order_id

    }
    return render(request,template_name,context)    

@csrf_exempt  # Razorpay posts to this URL
def payment_success(request):
    if request.method == 'POST':
        client = razorpay.Client(auth=(RAZORPAY_ID, RAZORPAY_SECRET))
        
        try:
            # Verify payment signature
            client.utility.verify_payment_signature({
                'razorpay_order_id': request.POST.get('razorpay_order_id'),
                'razorpay_payment_id': request.POST.get('razorpay_payment_id'),
                'razorpay_signature': request.POST.get('razorpay_signature')
            })

            # Retrieve enrollment data
            enrollment_data = request.session.get('enrollment_data')
            if not enrollment_data:
                messages.error(request, "Enrollment data missing. Contact support.")
                return redirect('/join')

            # Save enrollment to database
            Enrollment.objects.create(
                FullName=enrollment_data['FullName'],
                Email=enrollment_data['Email'],
                Gender=enrollment_data['Gender'],
                PhoneNumber=enrollment_data['PhoneNumber'],
                DOB=enrollment_data['DOB'],
                SelectMembershipplan=enrollment_data['SelectMembershipplan'],
                SelectTrainer=enrollment_data['SelectTrainer'],
                Reference=enrollment_data['Reference'],
                Address=enrollment_data['Address']
            )

            # Clear session data
            del request.session['enrollment_data']
            del request.session['razorpay_order_id']

            messages.success(request, "Enrollment successful! Payment completed.")
            return redirect('/enrollment-success')  # Success page

        except Exception as e:
            messages.error(request, f"Payment verification failed: {e}")
            return redirect('/join')

    # If GET request, show a generic success/failure page
    return render(request, "payment-success.html")
