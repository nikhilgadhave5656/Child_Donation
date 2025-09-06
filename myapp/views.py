from django.shortcuts import render, redirect, get_object_or_404
from .models import Contact, Child, Payment
from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import User
from django.conf import settings
import razorpay

# Razorpay client
client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


def index(request):
    children = Child.objects.all()
    return render(request, 'index.html', {'children': children})


def about(request):
    return render(request, 'about.html')


def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        Contact.objects.create(name=name, email=email, phone=phone, message=message)
        messages.success(request, "Message sent successfully!")
        return redirect('contact')
    return render(request, 'contact.html')


def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'signup.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'signup.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return render(request, 'signup.html')

        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        return redirect('home')

    return render(request, 'signup.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
            return render(request, 'login.html')

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


def child_detail(request, child_id):
    child = get_object_or_404(Child, pk=child_id)
    return render(request, 'child_detail.html', {'child': child})


def create_payment(request, child_id):
    if not request.user.is_authenticated:
        messages.error(request, "Please login to proceed for payment")
        return redirect('login')

    child = get_object_or_404(Child, id=child_id)

    if request.method == 'POST':
        try:
            amount = float(request.POST.get('amount', 100))
        except ValueError:
            messages.error(request, "Invalid amount")
            return redirect('child_detail', child_id=child.id)

        if amount < 100:
            messages.error(request, "Minimum sponsorship amount is ₹100")
            return redirect('child_detail', child_id=child.id)

        # Save payment in DB as Pending
        payment = Payment.objects.create(
            user=request.user,
            child=child,
            amount=amount,
            status='Pending'
        )

        # Create Razorpay Payment Link
        link = client.payment_link.create({
            "amount": int(amount * 100),  # convert to paise
            "currency": "INR",
            "description": f"Sponsorship for {child.name}",
            "customer": {"name": request.user.username, "email": request.user.email},
            "notify": {"sms": True, "email": True},
            "callback_url": request.build_absolute_uri('/payment-success/'),
            "callback_method": "get"
        })

        # Save Razorpay payment link ID in Payment model BEFORE redirect
        payment.payment_id = link['id']
        payment.save()

        # Redirect user to the payment link
        return redirect(link['short_url'])

    return redirect('child_detail', child_id=child.id)


def payment_success(request):
    #call back here staus
    payment_link_id = request.GET.get('razorpay_payment_link_id')   # plink_xxx
    status = request.GET.get('razorpay_payment_link_status')        # paid / failed / cancelled

    if not payment_link_id:
        messages.error(request, "Invalid payment callback.")
        return redirect('home')

    try:
        # DB save link
        payment = Payment.objects.get(payment_id=payment_link_id)

        if status == 'paid':
            payment.status = 'Completed'
            messages.success(request, "Payment successful ")
        elif status in ['failed', 'cancelled', 'expired']:
            payment.status = 'Failed'
            messages.error(request, "Payment failed ")
        else:
            payment.status = 'Pending'
            messages.warning(request, "Payment is still pending...")

        payment.save()

    except Payment.DoesNotExist:
        messages.error(request, "Payment record not found.")

    return redirect('home')
