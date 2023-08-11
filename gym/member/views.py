from django.shortcuts import render, redirect
from .models import Members, Payment,GymReport
from .forms import MemberForm
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from gym import settings
from django.core.mail import send_mail,EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from .token import generate_token
def create_member(request):
    if request.method == 'POST':
        form = MemberForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('base')
    else:
        form = MemberForm()
    return render(request, 'create_member.html', {'form': form})

def dashboard(request):
    members = Members.objects.all().order_by('fee_date')
    payments = Payment.objects.all()
    total_member=members.count()
    context={
        'members': members,
        'payments': payments,
        'total_member':total_member,

    }
    return render(request, 'base.html', context)

def generate_report(request):
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        start_date=timezone.datetime.strptime(start_date,'%Y-%m-%d').date()
        end_date = timezone.datetime.strptime(end_date, '%Y-%m-%d').date()
        revenue=0
        payments = Payment.objects.filter(payment_date__range=(start_date, end_date))
        for payment in payments:
            revenue += payment.amount
        report=GymReport(start_date=start_date,end_date=end_date,revenue=revenue)
        report.save()
        return redirect('report_details',report_id=report.id)



    return render(request, 'report.html')
def report_details(request,report_id):
    report=GymReport.objects.get(id=report_id)
    return render(request,'report_details.html',{'report':report})
def make_payment(request,member_id):
    if request.method == 'POST':
        member=Members.objects.get(id=member_id)
        amount=float(request.POST['amount'])
        payment_date=timezone.now().date()
        payment=Payment(amount=amount,member=member,payment_date=payment_date)
        payment.save()
        return redirect('base')
    member=Members.objects.get(id=member_id)
    return render(request,'make_payment.html',{'member':member})
def update_member(request,pk):
    member=Members.objects.get(id=pk)
    form=MemberForm(instance=member)
    if request.method == 'POST':
        form=MemberForm(request.POST,instance=member)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {
        'form':form,
    }

    return render(request,'create_member.html',context)
def deleteOrder(request,pk):
    member=Members.objects.get(id=pk)
    if request.method == 'POST':
        member.delete()
        return redirect('/')
    context={
        'member':member
    }
    return render(request,'delete.html',context)
def SignUp(request):
    if request.method == 'POST':
        username=request.POST['username']
        fname=request.POST['fname']
        lname=request.POST['lname']
        email=request.POST['email']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']
        if User.objects.filter(username=username):
            messages.error(request,'Username already exist')
            return redirect('base')

        if User.objects.filter(email=email):
            messages.error(request,'Email already exist')
            return redirect('base')
        if len(username)>10:
            messages.error(request,'User must be under 10 character')
        if pass1 != pass2:
            messages.error(request,'password does not match')
        if not username.isalnum():
            messages.error(request,'username must be in alphabets')
            return redirect('base')

        myuser=User.objects.create_user(username,email,pass1)
        myuser.first_name= fname
        myuser.last_name=lname
        myuser.is_active=False
        myuser.save()
        messages.success(request,'Your Account Has been Ssuccesfully Created')
        subject="Welcome to django project"
        message="Hello" +myuser.first_name+"!! \n" +"Welcome to Gym manaegment system \n Thanks for visiting our website"
        from_email=settings.EMAIL_HOST_USER
        to_list=[myuser.email]
        send_mail(subject,message,from_email,to_list,fail_silently=True)
        uid=urlsafe_base64_encode(force_bytes(myuser.pk))
        print(uid)
        token=generate_token.make_token(myuser)
        print(token)
        current_site=get_current_site(request)
        email_subject="Confirm your email @ gym -Django"
        message2=render_to_string('email.html',{
            'name':myuser.first_name,
            'domain':current_site.domain,
            'uid':urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token':generate_token.make_token(myuser)
        })

        email=EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [myuser.email],

        )
        email.fail_silently=True
        email.send()

        return redirect('signin')






    return render(request,'SignUp.html')
def SignIn(request):
    if request.method == 'POST':
        username=request.POST['username']
        pass1=request.POST['pass1']
        user=authenticate(username=username,password=pass1)
        if user is not None:
            login(request,user)
            fname=user.first_name
            return render(request,'base.html',{'fname':fname})
        else:
            messages.error(request,'Bad Crediential')
            return redirect('base')


    return render(request,'SignIn.html')
def SignOut(request):
    logout(request)
    messages.success(request,"Log out Successfully")
    return redirect('base')
def activate(request,uidb64,token):
    try:
        uid=force_text(urlsafe_base64_decode(uidb64))
        myuser=User.objects.get(pk=uid)
    except (TypeError,OverflowError,ValueError,User.DoesNotExist):
        myuser=None
    if myuser is not None and generate_token.check_token(myuser,token):

        myuser.is_active=True
        myuser.save()
        login(request,myuser)
        return redirect('base')
    else:
        return render(request,'email.html')