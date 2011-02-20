import re
from django.contrib.auth.models import User
from django import forms
from django.forms.widgets import RadioSelect

STATUS_CHOICES = (
    ('R', 'Recorded'),
    ('T', 'Transcribed'),
    ('S', 'Submitted'),
    ('C', 'Censored'),
    ('A', 'Approved'),
)

LEVEL_CHOICES = (
	('W', 'Wannabe'),
	('M', 'Master Affiliate'),
	('D', 'Director'),
	('S', 'Senior Director'),
	('A', 'Ambassador'),
	('P', 'Presidential'),
)

USERTYPE_CHOICES = (
    (1, 'I AM A RELIV BUSINESS BUILDER AND HEARD ABOUT IT THROUGH MY RELIV CONNECTIONS'),
    (2, 'I WAS SENT AN OPEN INVITE BY A FRIEND/RELATIVE/STRANGER/SOMEONE IN RELIV [EMAIL/CHAT]'),
    (3, 'I WAS TOLD ABOUT THIS WEBSITE BY A FRIEND/RELATIVE/STRANGER/SOMEONE IN RELIV'),
    (4, 'I WAS REFERRED HERE BY ANOTHER SITE [WEBSITE/BLOG]'),
    (5, 'I WAS REFERRED HERE THROUGH A SOCIAL MEDIA SITE [FACEBOOK/MYSPACE]'),
    (6, 'I FOUND THIS SITE WHILE SURFING THE INTERNET [SEARCH ENGINE/BANNER AD/FORUM LINK]'),
)

class SignUpForm(forms.Form):
	usertype = forms.CharField(
		label=u'HOW DID YOU COME TO THIS WEBSITE [PLEASE CHOOSE THE BEST ANSWER]',
		widget=forms.RadioSelect(choices=USERTYPE_CHOICES)		
		#widget=forms.ChoiceField(choices=USERTYPE_CHOICES)
	)
	
class RegistrationForm(forms.Form):	
	username = forms.CharField(label=u'Username/Sharecode')
	
	password1 = forms.CharField(
		label=u'Password',
		widget=forms.PasswordInput()
	)
	password2 = forms.CharField(
		label=u'Password (Again)',
		widget=forms.PasswordInput()
	)

	email = forms.EmailField(label=u'Email')
	
	def clean_password2(self):
		if 'password1' in self.cleaned_data:
			password1 = self.cleaned_data['password1']
			password2 = self.cleaned_data['password2']
			if password1 == password2:
				return password2
		raise forms.ValidationError('Passwords do not match.')
		
	def clean_username(self):
		username = self.cleaned_data['username']
		if not re.search(r'^\w+$', username):
			raise forms.ValidationError('Username can only contain '
				'alphanumeric characters and the underscore.')
		try:
			User.objects.get(username=username)
		except User.DoesNotExist:
			return username
		raise forms.ValidationError('Username is already taken.')

class BookmarkSaveForm(forms.Form):
	url = forms.URLField(
		label=u'URL',
		widget=forms.TextInput(attrs={'size': 64})
	)
	title = forms.CharField(
		label=u'Title',
		widget=forms.TextInput(attrs={'size': 64})
	)
	tags = forms.CharField(
		label=u'Tags',
		required=False,
		widget=forms.TextInput(attrs={'size': 64})
	)
	share = forms.BooleanField(
		label=u'Share on the main page',
		required=False
	)
	
class StorySaveForm(forms.Form):
	# sharecode = forms.CharField(label=u'Sharecode', max_length=30)
	email = forms.EmailField(label=u'Email', max_length=75)
	first_name = forms.CharField(label=u'First Name', max_length=30)
	last_name = forms.CharField(label=u'Last Name', max_length=30)
	place = forms.CharField(label=u'From', max_length=30)
	level = forms.ChoiceField(label=u'Reliv Level', choices=LEVEL_CHOICES)
	rcn = forms.IntegerField(label=u'RCN')
	phone1 = forms.IntegerField(label=u'Phone One')
	phone2 = forms.IntegerField(label=u'Phone Two', required=False)
	status = forms.ChoiceField(label=u'Status', choices=STATUS_CHOICES)
	audiofile = forms.FileField(label=u'Audio File', required=False)
	length = forms.CharField(label=u'Length (h:mm:ss)', max_length=8)
	tags = forms.CharField(
		label=u'Tags',
		required=False,
		widget=forms.TextInput(attrs={'size': 64})
	)
class FeedbackSaveForm(forms.Form):
	name = forms.CharField(label=u'Full Name', max_length=30)
	phone = forms.IntegerField(label=u'Phone (digits only)')
	email = forms.EmailField(label=u'e-mail address', max_length=75)
	comments = forms.CharField(label=u'Comments or Suggestions', widget=forms.Textarea)
	
class PlaylistSaveForm(forms.Form):
	title = forms.CharField(label=u'Description', max_length=30)
	
class SearchForm(forms.Form):
	query = forms.CharField(
		label=u'Enter sharecode to search for',
		widget=forms.TextInput(attrs={'size': 32})
	)

		

