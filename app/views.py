from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .models import Account, Transaction, User
from django.http import HttpResponse as H

# Create your views here.

def base(request):
    return render(request,'base.html')

def profile(request):
    return render(request,'profile.html')

# User Registration
def register(request):
    if request.method == "POST":
        usn = request.POST["username"]
        em = request.POST["email"]
        fn = request.POST["first_name"]
        ln = request.POST["last_name"]
        ftn = request.POST["father_name"]
        add = request.POST["address"]
        c = request.POST["city"]
        s = request.POST["state"]
        pc = request.POST["postal_code"]
        ph = request.POST["phone"]
        aa = request.POST["aadhar"]
        pn = request.POST["pan"]
        bb = request.POST["bank_balance"]
        p1 = request.POST["password1"]
        p2 = request.POST["password2"]

        if p1 != p2:
            return H("Passwords do not match!")

        if User.objects.filter(username=usn).exists():
            return H("Username already taken!")
        if User.objects.filter(email=em).exists():
            return H("Email already registered!")

        user = User.objects.create_user(
            username=usn, email=em, password=p1, first_name=fn,
            last_name=ln, father_name=ftn, address=add,
            city=c, state=s, postal_code=pc, phone=ph,
            aadhar=aa, pan=pn, bank_balance=bb
        )
        Account.objects.create(user=user, balance=bb)

        return H('<h1>User is register successfully....😊😊😊</h1>')

    return render(request, "register.html")

# User Login
def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            return H("Invalid username or password!")

    return render(request, "login.html")

# Logout View
def user_logout(request):
    logout(request)
    return redirect("login")

# Dashboard
@login_required
def dashboard(request):
    account = Account.objects.get(user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by("-timestamp")
    return render(request, "dashboard.html", {"account": account, "transactions": transactions})

# Transactions (Deposit & Withdraw)
@login_required
def transaction(request):
    account = Account.objects.get(user=request.user)

    if request.method == "POST":
        amount = int(request.POST["amount"])
        transaction_type = request.POST["transaction_type"]

        if transaction_type == "Withdraw" and amount > account.balance:
            return render(request, "transaction.html", {"error": "Insufficient Balance", "account": account})

        if transaction_type == "Deposit":
            account.balance += amount
        else:
            account.balance -= amount

        account.save()
        Transaction.objects.create(account=account, amount=amount, transaction_type=transaction_type)

        return redirect("dashboard")

    return render(request, "transaction.html", {"account": account})
