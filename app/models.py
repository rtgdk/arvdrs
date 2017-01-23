from __future__ import unicode_literals

from django.db import models

# Create your models here.
class ClinicType(models.Model):
	name =  models.CharField(max_length=64)
	key = models.CharField(max_length=64,null=True)
	def __str__(self):
		return (self.key+"-"+self.name)
class Patient(models.Model):
	stype=(('Male','Male'),('Female','Female'),('Other','Other'))
	name = models.CharField(max_length=64)
	address = models.CharField(max_length=128)
	age = models.IntegerField(blank=True,null=True,default=0)
	sex = models.CharField(choices=stype,max_length=16)
	mob = models.CharField(max_length=64,verbose_name="Mobile No")
	age = models.IntegerField(blank=True,null=True,default=0)
	email = models.CharField(max_length=64)
	clinic = models.CharField(max_length=64,verbose_name="Clinic")
	bite = models.CharField(max_length=64,verbose_name="Location of Bite")
	reg_date = models.DateField(blank=False)
	remarks = models.CharField(max_length=64,verbose_name="Special Remarks")
	key = models.CharField(max_length=32) #first letter of name+uniqid
	day1_status = models.CharField(max_length=32)
	day1 = models.DateField(blank=True)
	real_day1 = models.DateField(blank=True,null=True)
	msg_day1 = models.CharField(max_length=64,blank="False")
	day2_status = models.CharField(max_length=32)
	day2 = models.DateField(blank=True)
	real_day2 = models.DateField(blank=True,null=True)
	msg_day2 = models.CharField(max_length=64,blank="False")
	day3_status = models.CharField(max_length=32)
	day3 = models.DateField(blank=True)
	real_day3 = models.DateField(blank=True,null=True)
	msg_day3 = models.CharField(max_length=64,blank="False")
	day4_status = models.CharField(max_length=32)
	day4 = models.DateField(blank=True)
	real_day4 = models.DateField(blank=True,null=True)
	msg_day4 = models.CharField(max_length=64,blank="False")
	status = models.CharField(max_length=64,blank=False) #1=Registered 2=day1 done 3=day2done 4=day3done 5=day4done
	def __str__(self):
		return (self.name +" " +self.mob)
		
class Admin(models.Model):
	username = models.CharField(max_length=64)
	password = models.CharField(max_length=64)
	def __str__(self):
		return self.username

class Operator(models.Model):
	username = models.CharField(max_length=64)
	password = models.CharField(max_length=64)
	def __str__(self):
		return self.username

class SMSModel(models.Model):
	name = models.CharField(max_length=16)
	no = models.IntegerField(default=0)
