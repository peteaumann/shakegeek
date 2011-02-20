from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User 
from calc import hash_rcn_phone

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

class Story(models.Model):
	sharecode = models.CharField(max_length=10)
	email = models.CharField(max_length=75)
	first_name = models.CharField(max_length=30)
	last_name = models.CharField(max_length=30)	
	place = models.CharField(max_length=30)
	level = models.CharField(max_length=1, choices=LEVEL_CHOICES)
	rcn = models.IntegerField(null=True, blank=True)
	phone1 = models.IntegerField(null=True, blank=True)
	phone2 = models.IntegerField(null=True, blank=True)
	status = models.CharField(max_length=1, choices=STATUS_CHOICES)
	audiofile = models.FileField(upload_to='audio/')
	length = models.CharField(max_length=8)
	linkline = models.CharField(max_length=65)

class Feedback(models.Model):
	first_name = models.CharField(max_length=30)
	last_name = models.CharField(max_length=30)	
	email = models.CharField(max_length=75)
	comments = models.TextField()
	
class Link(models.Model):
	url = models.URLField(unique=True)
	def __unicode__(self):
		return self.url

class Bookmark(models.Model):
	title = models.CharField(max_length=200)
	user = models.ForeignKey(User)
	link = models.ForeignKey(Link)
	def __unicode__(self):
		return u'%s, %s' % (self.user.username, self.link.url)
	def get_absolute_url(self):
		return self.link.url

class Tag(models.Model):
	name = models.CharField(max_length=64, unique=True)
	bookmarks = models.ManyToManyField(Bookmark)
	def __unicode__(self):
		return self.name
		
class Wall(models.Model):
	username = models.CharField(max_length=10)
	storys = models.ManyToManyField(Story)
	def __unicode__(self):
		return self.name
		
class Playlist(models.Model):
	username = models.CharField(max_length=10)
	invite = models.CharField(max_length=20)
	title = models.CharField(max_length=30)
	storys = models.ManyToManyField(Story)
	def __unicode__(self):
		return self.title

class StoryTag(models.Model):
	name = models.CharField(max_length=200, unique=True)
	storys = models.ManyToManyField(Story)
	def __unicode__(self):
		return self.name
				
class SharedBookmark(models.Model):
	bookmark = models.ForeignKey(Bookmark, unique=True)
	date = models.DateTimeField(auto_now_add=True)
	votes = models.IntegerField(default=1)
	users_voted = models.ManyToManyField(User)
	def __unicode__(self):
		return u'%s, %s' % (self.bookmark, self.votes)

class Dossier:
	keeper = models.CharField(max_length=10)
	invite = models.CharField(max_length=20)
	email = models.EmailField()
	phone = models.CharField(max_length=15)
	intro = models.IntegerField(null=True, blank=True)	
	status = models.CharField(max_length=10)
	
class Invitation(models.Model):
	name = models.CharField(max_length=50)
	email = models.EmailField()
	code = models.CharField(max_length=20)
	sender = models.ForeignKey(User)
	def __unicode__(self):
		return u'%s, %s' % (self.sender.username, self.email)
	def send(self):
		subject = u'Invitation to join Django Bookmarks'
		link = 'http://%s/friend/accept/%s/' % (
			settings.SITE_HOST,
			self.code
		)
		template = get_template('invitation_email.txt')
		context = Context({
			'name': self.name,
			'link': link,
			'sender': self.sender.username,
		})
		message = template.render(context)
		send_mail(
			subject, message,
			settings.DEFAULT_FROM_EMAIL, [self.email]
		)
		
class Friendship(models.Model):
	from_friend = models.ForeignKey(
		User, related_name='friend_set'
	)
	to_friend = models.ForeignKey(
		User, related_name='to_friend_set'
	)
	def __unicode__(self):
		return u'%s, %s' % (
			self.from_friend.username,
			self.to_friend.username
		)
	class Meta:
		unique_together = (('to_friend', 'from_friend'), )
		


