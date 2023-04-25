from django.shortcuts import render, redirect 
from django.forms import inlineformset_factory
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from .decorators import *

@unauthenticated_user
def registerPage(request):

	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, 'Account was created for ' + username)
			return redirect('login')
		

	context = {'form':form}
	return render(request, 'accounts/register.html', context)

@unauthenticated_user
def loginPage(request):

	if request.method == 'POST':
		username = request.POST.get('username')
		password =request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('home')
		else:
			messages.info(request, 'Username OR password is incorrect')

	context = {}
	return render(request, 'accounts/login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('login')

@login_required(login_url='login')
@admin_only
def home(request):
	patients=Patient.objects.all()
	appointments=Appointment.objects.all()
	total_appointments = appointments.count()

	context = {'total_appointments':total_appointments , 'patients':patients,'appointments':appointments}
	return render(request, 'accounts/dashboard.html', context)

def userPage(request):
	appointments=Appointment.objects.all()
	userr=request.user

	use=User.objects.get(id=userr.id)
	use1=Patient.objects.get(name=use.username)
	appointments=Appointment.objects.filter(patient=use1.id)
	context = {'appointments':appointments, 'total_appointments':appointments.count()}
	return render(request, 'accounts/user.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','patient'])
def Doctors(request):
	Doctors = Doctor.objects.all()
	context={'doctors':Doctors}
	return render(request, 'accounts/Doctors.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def patient(request, pk):
	patient=Patient.objects.get(id=pk)
	userr=User.objects.get(username=patient.name)
	appointments=Appointment.objects.all()

	context = {'patient':userr,'appointments':appointments}
	return render(request, 'accounts/patient.html',context)

@login_required(login_url='login')
def available(request):
	appointments=Appointment.objects.all()

	context = {'appointments':appointments}
	return render(request, 'accounts/available.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['patient'])
def CreateAPT(request, pk):
	day = request.session.get('day')
	time= request.session.get('time_slot')
	OrderFormSet = inlineformset_factory(Patient, Appointment, fields=('Doctor','day','time_slot',), extra=1 )
	userr=User.objects.get(id=pk)
	patient = Patient.objects.get(name=userr.username)

	formset = OrderFormSet(queryset=Appointment.objects.none(),instance=patient)
	if request.method == 'POST':
		day = request.POST.get('appointment_set-0-day',False)
		time = request.POST.get('appointment_set-0-time_slot',False)
		doctor = request.POST.get('appointment_set-0-Doctor',False)
		request.session['day'] = day
		request.session['Doctor'] = doctor
		request.session['time_slot'] = time
		request.session.modified = True
		formset = OrderFormSet(request.POST, instance=patient)
		if formset.is_valid():
			if Appointment.objects.filter(Doctor=doctor, day=day, time_slot=time).count()>=1:
				messages.info(request, "The Selected Time Has Already Been Booked!")
			else:
				formset.save()
				return redirect('/')
	
	context = {'form':formset}
	return render(request, 'accounts/order_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['patient','admin'])
def updateAPT(request, pk):
	order = Appointment.objects.get(id=pk)
	form = OrderForm(instance=order)
	if request.method == 'POST':
		day = request.POST.get('day')
		time = request.POST.get('time_slot')
		doctor = request.POST.get('Doctor',False)
		form = OrderForm(request.POST, instance=order)
		if form.is_valid():
			if Appointment.objects.filter(Doctor=doctor, day=day, time_slot=time).count()>=1:
				messages.info(request, "The Selected Time Has Been Reserved Before!")
				context = {'form':form}
			else:
				form.save()
				return redirect('/')

	context = {'form':form}
	return render(request, 'accounts/order_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','patient'])
def cancelAPT(request, pk):
	order = Appointment.objects.get(id=pk)
	if request.method == "POST":
		order.delete()
		return redirect('/')

	context = {'item':order}
	return render(request, 'accounts/delete.html', context)