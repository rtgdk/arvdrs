from django import forms
from .models import SignUp

class UploadFileForm(forms.Form):
	file = forms.FileField()
	def clean(self):
		files = self.cleaned_data.get("file")
		if files:
            		filename = files.name
            		if filename.endswith('.xls') or filename.endswith('.xlsx') or filename.endswith('.csv'):
                		return files
           		else:
                		raise forms.ValidationError("Unsupported File type.")

        	return files
		
	class meta:
		('file',)
class SignUpForm(forms.ModelForm):
	def clean(self):
		email = self.cleaned_data.get('email')
		reg_user = SignUp.objects.filter()
		for i in reg_user:
			if (email==i.email):
				raise forms.ValidationError("Email already registered")
				break
		return self.cleaned_data
	class Meta:
	        model = SignUp
	        fields = ('email',)
	        
	        
