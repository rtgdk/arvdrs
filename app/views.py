from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect,HttpResponseBadRequest, JsonResponse
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
import urllib2
#addddddd
from django import forms
from django.template import RequestContext
#import django_excel as excel
from datetime import datetime,date,timedelta
from django.core.mail import send_mail,send_mass_mail
from django.views.decorators.cache import cache_control
#mail
#from django.core.mail import EmailMultiAlternatives
from django.core.mail import EmailMessage
from django.core.mail import send_mail
#excel
import xlsxwriter
import django_excel as excel
#excel date
import re
#autocomplete
import json

from .models import ClinicType,Patient,Admin,Operator,SMSModel
def unique_id():
	from time import time
	return (hex(int(time()*10000000))[9:])

def smsincr(count):
	sms = SMSModel.objects.get(name ="ARVDRS")
	sms.no += count
	sms.save()
def index(request):
	context_dict={}
	if (('primaryadmin' in request.session) or ('operator' in request.session)):
		try:
			sms = SMSModel.objects.get(name ="ARVDRS")
		except:
			sms=""
			pass
		context_dict['sms']=sms
		if request.method == 'POST':
			name=request.POST['name']
			mob=request.POST['mob']
			key=request.POST['key']
			p=Patient.objects.filter(name__icontains=name,mob__icontains=mob,key__icontains=key)
			context_dict['patient']=p
			context_dict['searchname']=name
			context_dict['searchmob']=mob
			context_dict['searchkey']=key
			return render(request, 'app/index.html',context_dict)
		else :
			return render(request, 'app/index.html',context_dict)
	else :
		return render(request, 'app/index.html',context_dict)


	
def logout(request):
	if 'primaryadmin' in request.session:
		request.session.flush()
		return HttpResponseRedirect("/app/admin/login/")
   	elif 'operator' in request.session:
		request.session.flush()
		return HttpResponseRedirect("/app/operator/login/")
	else:
		request.session.flush()
		return HttpResponseRedirect("/app/")
    
def admin_login(request):
	context_dict={}
	if request.method == 'POST':
		username=request.POST['username']
		password=request.POST['password']
		try:
			user = Admin.objects.get(username=username)
			if password == user.password:
				request.session['primaryadmin']=user.username
				return HttpResponseRedirect("/app/")
			else :
				context_dict["notlogin"]="Invalid Credentials"
				return render(request, 'app/admin_login.html',context_dict)
		except:
			context_dict["notlogin"]="Invalid Credentials"
			return render(request, 'app/admin_login.html',context_dict)
	else :
		return render(request, 'app/admin_login.html')
def operator_login(request):
	context_dict={}
	if request.method == 'POST':
		username=request.POST['username']
		password=request.POST['password']
		try:
			user = Operator.objects.get(username=username)
			if password == user.password:
				request.session['operator']=user.username
				return HttpResponseRedirect("/app/")
			else :
				context_dict["notlogin"]="Invalid Credentials"
				return render(request, 'app/operator_login.html',context_dict)
		except:
			context_dict["notlogin"]="Invalid Credentials"
			return render(request, 'app/operator_login.html',context_dict)
	else :
		return render(request, 'app/operator_login.html')
	

def op_patient_register(request):
	context_dict={}
	if (('primaryadmin' in request.session) or ('operator' in request.session)):
		clinic = ClinicType.objects.filter()
		context_dict['clinic']= clinic
		if request.method == 'POST':
			name = request.POST['name']
			age = request.POST['age']
			sex = request.POST['sex']
			mob = request.POST['mob']
			address = request.POST['address']
			email = request.POST['email']
			if (email == "" ):
				email = ""
			clinic = request.POST['clinic']
			bite = request.POST['bite']
			if (bite == "" ):
				bite = ""
			remarks = request.POST['remarks']
			if (remarks == "" ):
				remarks = ""
			"""for i in reg_user :
				if (i.email==email):
					context_dict["done"]=2
					return render(request, 'app/signup.html',context_dict)"""
			key=str(name)[:1]+str(unique_id())
			date= datetime.now()
			day1=date.strftime("%Y-%m-%d")
			day2=date+timedelta(days=3)
			day3=date+timedelta(days=7)
			day4=date+timedelta(days=28)
			thisdaystatus="Attended on " +str(datetime.now().strftime("%b-%d-%Y"))
			otherdaystatus="Yet to attend"
			othermsgstatus="Yet to send"
			a=Patient.objects.create(reg_date = day1,name=name,age=age,sex=sex,mob=mob,address=address, email=email,clinic=clinic,bite=bite,remarks=remarks,key=key,day1=day1,day2=day2,day3=day3,day4=day4,day1_status = otherdaystatus , day2_status = otherdaystatus ,day3_status = otherdaystatus, day4_status = otherdaystatus, msg_day1 = othermsgstatus,
			msg_day2 = othermsgstatus,msg_day3 = othermsgstatus,msg_day4 = othermsgstatus,status="1")
			a.save()
			messagesendurl = "https://control.msg91.com/api/sendhttp.php?authkey=96244AsR6Os06Hs562e546f&mobiles=91"
			messagesendurl += str(a.mob)
			messagesendurl += "&message="
			messagesendurl += str(a.name).upper()
			messagesendurl += ",%20your%20unique%20key%20for%20ARVDRS%20is%20"
			messagesendurl += str(a.key)
			messagesendurl += "&sender=ARVDRS&route=4&country=0&campaign=signupweb"
			req = urllib2.Request(messagesendurl)
			print urllib2.urlopen(req)
			context_dict["done"]=1
			smsincr(1)
			return render(request, 'app/patient_reg.html',context_dict)
		else :
			clinic = ClinicType.objects.all()
			context_dict["clinic"]=clinic
			context_dict["done"]=0
			return render(request, 'app/patient_reg.html',context_dict)
	else :
		return HttpResponseRedirect("/app/")

def patient_mark_attendance(request,patient_id,status):
	if (('primaryadmin' in request.session) or ('operator' in request.session)):
		try:
			patient=Patient.objects.get(key=patient_id)
			if status=="1":
				patient.day1_status="Attended on " + str(datetime.now().strftime("%b-%d-%Y"))
				patient.real_day1 = datetime.now().strftime("%Y-%m-%d")
				patient.status="2"
				patient.save()
			elif status=="2":
				patient.day2_status="Attended on " + str(datetime.now().strftime("%b-%d-%Y"))
				patient.real_day2 = datetime.now().strftime("%Y-%m-%d")
				patient.status="3"
				patient.save()
			elif status=="3":
				patient.day3_status="Attended on " + str(datetime.now().strftime("%b-%d-%Y"))
				patient.real_day3 = datetime.now().strftime("%Y-%m-%d")
				patient.status="4"
				patient.save()
			elif status=="4":
				patient.day4_status="Attended on " + str(datetime.now().strftime("%b-%d-%Y"))
				patient.real_day4 = datetime.now().strftime("%Y-%m-%d")
				patient.status="5"
				patient.save()
			else :
				return HttpResponseRedirect("/app/patient/"+str(patient_id)+"/")
			return HttpResponseRedirect("/app/patient/"+str(patient_id)+"/")
		except :
			return HttpResponseRedirect("/app/")
	else :
		return HttpResponseRedirect("/app/")
def patient(request,patient_id):
	context_dict={}
	if (('primaryadmin' in request.session) or ('operator' in request.session)):
		try:
			patient=Patient.objects.get(key=patient_id)
			context_dict['patient']=patient
			check = int(patient.status)
			context_dict['check'] = check
			return render(request, 'app/patient_page.html',context_dict)
		except :
			return HttpResponseRedirect("/app/")
	else :
		return HttpResponseRedirect("/app/")

def report_generator(request):
	context_dict={}
	if (('primaryadmin' in request.session) or ('operator' in request.session)):
		if request.method == 'POST':
			clinic= request.POST['clinic']
			if clinic=="":
				from_date= request.POST['demo1_2']
				to_date= request.POST['demo2_2']
				context_dict['fdate']=from_date
				context_dict['tdate']=to_date
				patient = Patient.objects.filter(reg_date__range=[from_date, to_date])
				context_dict['patient']=patient
				#return HttpResponse("here")
				#return render(request, 'app/report.html',context_dict)
				#excel
				workbook = xlsxwriter.Workbook('app/media/'+'All'+'_'+from_date+'to'+to_date+'_list.xlsx')
				context_dict['link']= 'All'+'_'+from_date+'to'+to_date+'_list.xlsx'
				worksheet = workbook.add_worksheet()
				worksheet.set_column('A:A', 15)
				worksheet.set_column('B:B', 25)
				worksheet.set_column('C:C', 15)
				worksheet.set_column('D:D', 15)
				worksheet.set_column('E:E', 15)
				worksheet.set_column('F:F', 15)
				bold = workbook.add_format({'bold': 1})
				worksheet.write('A1', 'Clinic', bold)
				worksheet.write('B1', 'Name', bold)
				worksheet.write('C1', 'Day1', bold)
				worksheet.write('D1', 'Day2', bold)
				worksheet.write('E1', 'Day3', bold)
				worksheet.write('F1', 'Day4', bold)
				row = 1
				col = 0
				for i in patient:
					worksheet.write_string  (row, col,i.clinic )
					worksheet.write_string(row, col + 1, i.name )
					worksheet.write_string  (row, col + 2,str(i.day1))
					worksheet.write_string  (row, col+3,str(i.day2) )
					worksheet.write_string(row, col + 4, str(i.day3))
					worksheet.write_string  (row, col + 5, str(i.day4) )
					row += 1
				workbook.close()
				return render(request, 'app/report.html',context_dict)
			else :
				from_date= request.POST['demo1_2']
				to_date= request.POST['demo2_2']
				context_dict['fdate']=from_date
				context_dict['tdate']=to_date
				patient = Patient.objects.filter(clinic=clinic, reg_date__range=[from_date, to_date])
				context_dict['patient']=patient
				#return HttpResponse("here")
				#return render(request, 'app/report.html',context_dict)
				#excel
				workbook = xlsxwriter.Workbook('app/media/'+clinic+'_'+from_date+'to'+to_date+'_list.xlsx')
				context_dict['link']= clinic+'_'+from_date+'to'+to_date+'_list.xlsx'
				worksheet = workbook.add_worksheet()
				worksheet.set_column('A:A', 15)
				worksheet.set_column('B:B', 25)
				worksheet.set_column('C:C', 15)
				worksheet.set_column('D:D', 15)
				worksheet.set_column('E:E', 15)
				worksheet.set_column('F:F', 15)
				bold = workbook.add_format({'bold': 1})
				worksheet.write('A1', 'Clinic', bold)
				worksheet.write('B1', 'Name', bold)
				worksheet.write('C1', 'Day1', bold)
				worksheet.write('D1', 'Day2', bold)
				worksheet.write('E1', 'Day3', bold)
				worksheet.write('F1', 'Day4', bold)
				row = 1
				col = 0
				for i in patient:
					worksheet.write_string  (row, col,i.clinic )
					worksheet.write_string(row, col + 1, i.name )
					worksheet.write_string  (row, col + 2,str(i.day1))
					worksheet.write_string  (row, col+3,str(i.day2) )
					worksheet.write_string(row, col + 4, str(i.day3))
					worksheet.write_string  (row, col + 5, str(i.day4) )
					row += 1
				workbook.close()
				return render(request, 'app/report.html',context_dict)
		else:
			return render(request, 'app/report.html',context_dict)
	else :
		return HttpResponseRedirect("/app/")

def sendmsg(request):
	if (('primaryadmin' in request.session) or ('operator' in request.session)):
		d = date.today()
		e = timedelta(days=1)
		f = d + e
		p = Patient.objects.all()
		count=0
		messagesendurl = "https://control.msg91.com/api/sendhttp.php?authkey=96244AsR6Os06Hs562e546f&mobiles="
		for i in p :
			if (i.status!="5"):
				if (i.status=="2" and (i.day2==d or i.day2==e)):
					messagesendurl += "91"+str(i.mob) +","
					i.msg_day2 == "Sent"
					i.save()
					count+=1
				elif (i.status=="3" and (i.day3==d or i.day3==e)):
					messagesendurl += "91"+str(i.mob) +","
					i.msg_day3 == "Sent"
					i.save()
					count+=1
				elif (i.status=="4" and (i.day4==d or i.day4==e)):
					messagesendurl += "91"+str(i.mob) +","
					i.msg_day4 == "Sent"
					i.save()
					count+=1
				else :
					pass
		messagesendurl += "&message="
		messagesendurl += "%20Your%20vacciation%20is%20scheduled%20today%20"
		messagesendurl += "&sender=ARVDRS&route=4&country=0&campaign=signupweb"
		req = urllib2.Request(messagesendurl)
		print urllib2.urlopen(req)
		smsincr(count)
		return HttpResponse("Sent "+str(count) +" messages")
	else :
		return HttpResponseRedirect("/app/")
def admin_add_clinic(request):
	if ('primaryadmin' in request.session):
		context_dict={}
		clinic= ClinicType.objects.all()
		context_dict['clinic']=clinic
		if request.method == 'POST':
			name = request.POST['name']
			if (len(ClinicType.objects.filter(name=name))>0):
				context_dict["done"]=2
				return render(request, 'app/add_clinic.html',context_dict)
			a = ClinicType.objects.create(name=name)
			a.key = str(a.id) +"-"+ a.name
			a.save()
		
			context_dict["done"]=1
			return render(request, 'app/add_clinic.html',context_dict)
		else :
			context_dict["done"]=0
			return render(request, 'app/add_clinic.html',context_dict)
	else :
		return HttpResponseRedirect("/app/")
def patient_delete(request,patient_id):
	context_dict={}
	if (('primaryadmin' in request.session) or ('operator' in request.session)):
		try:
			patient=Patient.objects.get(key=patient_id)
			patient.delete()
			return HttpResponseRedirect("/app/")
		except :
			return HttpResponseRedirect("/app/")
	else :
		return HttpResponseRedirect("/app/")
		
		
		
def admin_add_operator(request):
	context_dict={}
	if ('primaryadmin' in request.session):
		context_dict={}
		operator= Operator.objects.all()
		context_dict['operator']=operator
		if request.method == 'POST':
			name = request.POST['name']
			if (len(Operator.objects.filter(username=name))>0):
				context_dict["done"]=2
				return render(request, 'app/add_operator.html',context_dict)
			pwd = request.POST['pwd']
			a = Operator.objects.create(username=name,password=pwd)
			a.save()
			context_dict["done"]=1
			return render(request, 'app/add_operator.html',context_dict)
		else :
			context_dict["done"]=0
			return render(request, 'app/add_operator.html',context_dict)
	else :
		return HttpResponseRedirect("/app/")
#ajax
def autocompleteModel(request):
    if 'term' in request.GET:
        tags = ClinicType.objects.filter(key__icontains=request.GET['term']).values_list('key',flat=True)[:5]
        
        return HttpResponse( json.dumps( [ tag for tag in tags ] ) )
    return HttpResponse()
def autocompleteModel2(request):
    if 'term' in request.GET:
        tags = Patient.objects.filter(name__icontains=request.GET['term']).values_list('name',flat=True).distinct()[:5]
        
        return HttpResponse( json.dumps( [ tag for tag in tags ] ) )
    return HttpResponse()
def autocompleteModel3(request):
    if 'term' in request.GET:
        tags = Patient.objects.filter(mob__icontains=request.GET['term']).values_list('mob',flat=True).distinct()[:5]
        
        return HttpResponse( json.dumps( [ tag for tag in tags ] ) )
    return HttpResponse()
def autocompleteModel4(request):
    if 'term' in request.GET:
        tags = Patient.objects.filter(key__icontains=request.GET['term']).values_list('key',flat=True).distinct()[:5]
        
        return HttpResponse( json.dumps( [ tag for tag in tags ] ) )
    return HttpResponse()

