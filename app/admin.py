from django.contrib import admin
from app.models import ClinicType,Patient,Admin,Operator,SMSModel
admin.site.register(ClinicType)
admin.site.register(Patient)
admin.site.register(Admin)
admin.site.register(Operator)
admin.site.register(SMSModel)
# Register your models here.
