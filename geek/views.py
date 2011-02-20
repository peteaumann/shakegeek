# Create your views here.
from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template
from django.shortcuts import render_to_response
from django.template import RequestContext
from geek.forms import *
from geek.models import *
from django.contrib.auth.decorators import login_required
from calc import *
from django.core.mail import EmailMessage
from django.contrib.auth.views import login
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect
from django.core.paginator import Paginator, InvalidPage

def register_page(request):
	menupage = 'register'
	if request.method == 'POST':
		form = RegistrationForm(request.POST)
		if form.is_valid():
			user = User.objects.create_user(
				username=form.cleaned_data['username'],
				password=form.cleaned_data['password1'],
				email=form.cleaned_data['email'],
			)
			try:
				story = Story.objects.get(sharecode=form.cleaned_data['username'])
				user.is_authenticated = True
			except (Story.DoesNotExist):
				user.is_anonymous = True

			user.save()
			
			return HttpResponseRedirect('/register/success/')
	else:
		form = RegistrationForm()
	variables = RequestContext(request, {
		'menupage': menupage,
		'form': form
	})
	return render_to_response(
		'registration/register.html',
		{},
		variables
	)

def signup_page(request):
	invite = request.session['invite']
	keeper = request.session['keeper']
	linkline = request.session['linkline']
	page = 'signup'
	menupage = 'signup'
	if request.method == 'POST':
		form = SignUpSaveForm(request.POST)
		if form.is_valid():
			dossier = Dossier();
			dossier.intro=form.cleaned_data['intro']
			dossier.invite = invite
			dossier.keeper = keeper
			dossier.save()

			return HttpResponseRedirect('/playlist_open/?sesame=%s' % sesame)
	else:
		form = PlaylistSaveForm()
		
	variables = RequestContext(request, {
		'linkline': linkline,
		'menupage': menupage,
		'page': page,
		'form': form
	})
	return render_to_response('playlist_save.html', {}, variables)
		
def playlist_save_page(request):
	menupage = 'playlist'
	page = 'playlist'
	linkline = request.session['linkline']
					
	if request.method == 'POST':
		form = PlaylistSaveForm(request.POST)
		if form.is_valid():
			invite = User.objects.make_random_password(length=30, 
				allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789'
			)
			playlist, created = Playlist.objects.get_or_create(username=request.user.username,
				invite=invite
			)			
			playlist.title=form.cleaned_data['title']
			playlist.save()
			linklist = linkline.split(' ')
			
			for item in linklist:			
				story = Story.objects.get(sharecode=item)
				playlist.storys.add(story)
				
			playlist.save()

			return HttpResponseRedirect('/playlist_open/?invite=%s' % invite)
	else:
		form = PlaylistSaveForm()
		
	variables = RequestContext(request, {
		'linkline': linkline,
		'menupage': menupage,
		'page': page,
		'form': form
	})
	return render_to_response('playlist_save.html', {}, variables)

def playlist_open(request):
	ITEMS_PER_PAGE = 12
	invite = request.GET['invite']
	request.session['invite'] = invite
	menupage='playlist'
	linkline = request.session['linkline']
	linklist = linkline.split(' ')
	tag_name = invite
	tagline = tag_name
	
	playlist = get_object_or_404(Playlist, invite=invite)
	query_set = playlist.storys.order_by('-id')
	paginator = Paginator(query_set, ITEMS_PER_PAGE)
	try:
		page_number = int(request.GET['page'])
	except (KeyError, ValueError):
		page_number = 1
	try:
		page = paginator.page(page_number)
	except InvalidPage:
		raise Http404
	storys = page.object_list
	
	try:
		wall = Wall.objects.get(username=request.user.username)
		wall_list = wall.storys.order_by('-id')
	except (Wall.DoesNotExist):
		wall_list = []
	
	zipper = []								# bricktype, offset
	wallstory_list = []
	
	for wallpaper in wall_list:
		wallstory_list.append(wallpaper.sharecode)
		
	for story in storys:
		if story.sharecode in linklist:
			if story.sharecode in wallstory_list:
				zipper.append((story,1))			# both
			else:
				zipper.append((story,2))			# link
		else:
			if story.sharecode in wallstory_list:
				zipper.append((story,3))			# wall
			else:
				zipper.append((story,4))			# none
	
	variables = RequestContext(request, {
		'linkline': linkline,
		'page': page,
		'menupage': menupage,
		'tag_name': tag_name,
		'tagline': tagline,
		'zipper': zipper,
		'show_tags': True,
		'show_edit': True,
		'show_paginator': paginator.num_pages > 1,
		'has_prev': page.has_previous(),
		'has_next': page.has_next(),
		'page': page_number,
		'pages': paginator.num_pages,
		'next_page': page_number + 1,
		'prev_page': page_number - 1,
	})
	return render_to_response('playlist_open.html', {}, variables)
	
def home_page(request):
	menupage='home'
	variables = RequestContext(request, {
		'menupage': menupage
	})
	return render_to_response('home_page.html', {}, variables)

def guidelines_page(request):
	menupage='guidelines'
	variables = RequestContext(request, {
		'menupage': menupage
	})
	return render_to_response('guidelines_page.html', {}, variables)
	
def blog_page(request):
	menupage='blog'
	variables = RequestContext(request, {
		'menupage': menupage
	})
	return render_to_response('blog_page.html', {}, variables)



def user_page(request, username):
	ITEMS_PER_PAGE = 12
	linkline = request.session['linkline']
	menupage = 'user'
	page = 'user'
	user = get_object_or_404(User, username=username)
	query_set = user.bookmark_set.order_by('-id')
	paginator = Paginator(query_set, ITEMS_PER_PAGE)
	if request.user.is_authenticated():
		is_friend = Friendship.objects.filter(
		from_friend=request.user,
		to_friend=user
	)
	else:
		is_friend = False
	try:
		page_number = int(request.GET['page'])
	except (KeyError, ValueError):
		page_number = 1
	try:
		page = paginator.page(page_number)
	except InvalidPage:
		raise Http404
	bookmarks = page.object_list
	variables = RequestContext(request, {
		'linkline': linkline,
		'page': page,
		'menupage': menupage,
		'username': username,
		'bookmarks': bookmarks,
		'show_tags': True,
		'show_edit': username == request.user.username,
		'show_paginator': paginator.num_pages > 1,
		'has_prev': page.has_previous(),
		'has_next': page.has_next(),
		'page': page_number,
		'pages': paginator.num_pages,
		'next_page': page_number + 1,
		'prev_page': page_number - 1,
		'is_friend': is_friend,
	})
	return render_to_response('user_page.html', {}, variables)


	
def playlist_page(request, username):
	page = 'playlist'
	menupage = 'playlist'
	user = get_object_or_404(User, username=username)
	query_set = user.playlist_set.order_by('-id')
	paginator = Paginator(query_set, ITEMS_PER_PAGE)

	try:
		page_number = int(request.GET['page'])
	except (KeyError, ValueError):
		page_number = 1
	try:
		page = paginator.page(page_number)
	except InvalidPage:
		raise Http404
	playlists = page.object_list
	variables = RequestContext(request, {
		'page': page,
		'menupage': menupage,
		'username': username,
		'playlists': playlists,
		'show_tags': True,
		'show_edit': username == request.user.username,
		'show_paginator': paginator.num_pages > 1,
		'has_prev': page.has_previous(),
		'has_next': page.has_next(),
		'page': page_number,
		'pages': paginator.num_pages,
		'next_page': page_number + 1,
		'prev_page': page_number - 1,
	})
	return render_to_response('playlist_page.html', {}, variables)

from django.contrib.auth import logout

def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')

def login_page(request):
	
	#try:
	#	story = Story.objects.get(sharecode=request.user.username)		
	#	request.session['linkline'] = story.linkline
	#except (Story.DoesNotExist):
	
	request.session['linkline'] = 'NADA'
	
	try:
		wall = Wall.objects.get(username=request.user.username)
		request.user.wall = list(wall)
	except (Wall.DoesNotExist):
		request.user.wall = []
	return login(request) 

def wall_build_page(request):
	ITEMS_PER_PAGE = 12
	linkline = request.session['linkline']
	linklist = linkline.split(' ')
	page = 'wall'
	menupage = 'wall'
	BRICKWIDTH=10
	BRICKS_PER_ROW = 4
	brickrows = 0
	bricksleft = 0
	bricksper = BRICKS_PER_ROW
	brickwide = BRICKWIDTH
	wobrow = 3
	TOP_COL = BRICKS_PER_ROW * 4 + 1
	
	# option 1
	#try:
	#wall = Wall.objects.get_or_404(username=user)
	wall = get_object_or_404(Wall, username=request.user.username)
	query_set = wall.storys.order_by('-id')
	paginator = Paginator(query_set, ITEMS_PER_PAGE)
	try:
		page_number = int(request.GET['page'])
	except (KeyError, ValueError):
		page_number = 1
	try:
		page = paginator.page(page_number)
	except InvalidPage:
		raise Http404
			
	storys = page.object_list
	brickcount = len(storys)
	brickrows, bricksleft = divmod(brickcount, BRICKS_PER_ROW)
	
	# half row equals a row
	if (bricksleft > 0):
		brickrows = brickrows + 1

	capcol = range(TOP_COL)
	
	looprows = range(brickrows)				# should map to a list [27, 26, 25, . . . ,0]
	looprows.reverse()
	loopcols = range(BRICKS_PER_ROW)		# should map to a list [0, 1, 2, etc. ]

	zipped = []								# bricktype, offset
	blank = None

	zipped.append((0,-1,blank,blank,blank,blank,blank))						# <tr>
	zipped.append((6,-1,blank,blank,blank,blank,blank))						# <td></td> -> all half bricks														
	zipped.append((3,-1,blank,blank,blank,blank,blank))						# </tr>
	for row in looprows:
		zipped.append((0,-1,blank,blank,blank,blank,blank))					# <tr>
		whocares, evenodd = divmod(row, 2)
		if evenodd == 1:			
			zipped.append((1,-1,blank,blank,blank,blank,blank))				# odd row ->  <td></td> -> start with half brick
			for col in loopcols:
				brick = row * BRICKS_PER_ROW + col
				if brick >= brickcount:
					zipped.append((2,-1,blank,blank,blank,blank,blank))		# blankbrick ->  <td colspan = 2></td>
				else:
					storydex = storys[brick]
					#story = storydex.sharecode
					# fullname = "%s %s" % storydex.first_name, storydex.last_name
					fullname = "%s %s" % (storydex.first_name, storydex.last_name)
					place = "%s" % (storydex.place)
					audio = "%s" % (storydex.audiofile.url)
					sharecode = "%s" % (storydex.sharecode)
					if storydex.sharecode in linklist:
						brickcolor = 1
					else:
						brickcolor = 0
					zipped.append((4, brick,fullname,place,audio,sharecode,brickcolor))	# normal brick ->  <td colspan = 2></td>
		else:
			for col in loopcols:
				brick = row * BRICKS_PER_ROW + col
				if brick >= brickcount:
					zipped.append((2,-1,blank,blank,blank,blank,blank))		# blankbrick ->  <td colspan = 2></td>
				else:
					storydex = storys[brick]
					story = storydex.sharecode
					fullname = "%s %s" % (storydex.first_name, storydex.last_name)
					place = "%s" % (storydex.place)
					audio = "%s" % (storydex.audiofile.url)
					sharecode = "%s" % (storydex.sharecode)
					if storydex.sharecode in linklist:
						brickcolor = 1
					else:
						brickcolor = 0
					zipped.append((4, brick,fullname,place,audio,sharecode,brickcolor))	# normal brick ->  <td colspan = 2></td>
			zipped.append((1,-1,blank,blank,blank,blank,blank))				# even row ->  <td></td> -> end with half brick
		zipped.append((3,-1,blank,blank,blank,blank,blank))					# </tr>
	zipped.append((0,-1,blank,blank,blank,blank,blank))						# <tr>
	for capbrick in capcol:
		zipped.append((5,-1,blank,blank,blank,blank,blank))					# <td></td> -> all half bricks
	zipped.append((3,-1,blank,blank,blank,blank,blank))						# </tr>
		
	variables = RequestContext(request, {
		'linkline': linkline,
		'page': page,
		'menupage': menupage,
		'storys': storys,
		'brickwide': brickwide,
		'zipped': zipped,
		'show_tags': True,
		'show_edit': True,
		'show_paginator': paginator.num_pages > 1,
		'has_prev': page.has_previous(),
		'has_next': page.has_next(),
		'page': page_number,
		'pages': paginator.num_pages,
		'next_page': page_number + 1,
		'prev_page': page_number - 1,
	})
	return render_to_response('story_by_wall.html', {}, variables)

def sub_brick(request):
	sharecode = request.GET['sharecode']
	nix_brick(request)
	
	return wall_build_page(request)
	
def modify_wall(request):
	sharecode = request.GET['sharecode']

	try:
		wall = Wall.objects.get(username=request.user.username)
		wall_list = wall.storys.order_by('-id')
	except (Wall.DoesNotExist):
		wall_list = []
	
	wallstory_list = []
	
	for wallpaper in wall_list:
		wallstory_list.append(wallpaper.sharecode)
	
	if sharecode in wallstory_list:
		nix_brick(request)
	else:
		add_brick(request)
		
	back = request.META.get('HTTP_REFERER', "/") 
	if back: 
		return HttpResponseRedirect(back) 
	else: 
		return wall_build_page(request)
		
def add_brick(request):
	sharecode = request.GET['sharecode']

	try:
		# if wall exists, take story and then add to wall
		w1 = Wall.objects.get(username=request.user.username)
		s1 = Story.objects.get(sharecode=sharecode)		
		w1.storys.add(s1)
	except Wall.DoesNotExist:
		w2 = Wall(id=None, username=request.user.username)
		w2.save()
		s2 = Story.objects.get(sharecode=sharecode)	
		w2.storys.add(s2)
			
def nix_brick(request):
	sharecode = request.GET['sharecode']

	# nix brick from wall of belief
	w1 = Wall.objects.get(username=request.user.username)
	s1 = Story.objects.get(sharecode=sharecode)		
	w1.storys.remove(s1)
		
def modify_linkline(request):
	sharecode = request.GET['sharecode']
	linkline = request.session['linkline']
	
	if (linkline == 'NADA'):
		templist = []
	else:	
		templist = linkline.split(' ')
	
	#if (templist):
	try:
		position = templist.index(sharecode)
		del templist[position]
	except ValueError:
		if len(templist) < 6:
			templist.append(sharecode)
	
	if len(templist) == 0:
		request.session['linkline'] = 'NADA'
	else:
		request.session['linkline'] = ' '.join(templist)
		
	back = request.META.get('HTTP_REFERER', "/") 
	if back: 
		return HttpResponseRedirect(back) 
	else: 
		return story_cloud_page(request)
	
@login_required
def bookmark_save_page(request):
	linkline = request.session['linkline']
	page = 'savebookmark'
	if request.method == 'POST':
		form = BookmarkSaveForm(request.POST)
		if form.is_valid():
			bookmark = _bookmark_save(request, form)
			return HttpResponseRedirect(
				'/user/%s/' % request.user.username
			)
	elif 'url' in request.GET:
		url = request.GET['url']
		title = ''
		tags = ''
		try:
			link = Link.objects.get(url=url)
			bookmark = Bookmark.objects.get(
				link=link,
				user=request.user
			)
			title = bookmark.title
			tags = ' '.join(
				tag.name for tag in bookmark.tag_set.all()
			)
		except (Link.DoesNotExist, Bookmark.DoesNotExist):
			pass
		form = BookmarkSaveForm({
			'url': url,
			'title': title,
			'tags': tags
		})
	else:
		form = BookmarkSaveForm()
	variables = RequestContext(request, {
		'linkline': linkline,
		'page': page,
		'form': form
	})
	return render_to_response('bookmark_save.html', {}, variables)
	
@login_required
def story_save_page(request):
	linkline = request.session['linkline']
	page = 'savestory'
	menupage = 'savestory'
	if request.method == 'POST':
		form = StorySaveForm(request.POST, request.FILES)
		if form.is_valid():
			if 'audiofile' in request.FILES:  
				handle_uploaded_file(request.FILES['audiofile'])
			
			story = _story_save(request, form)
				
		#	msg1 = "Congratulations!  Your story has been approved by Reliv Compliance.\n"
		#	msg2 = "You can now go to www.shaketales.com and register with sharecode: %s\n\n" % story.sharecode
		#	msg3 = "For future reference, your story is registered as follows:\n\n"
		#	msg4 = "Sharecode.........: %s\n" % story.sharecode
		#	msg5 = "RCN...............: %s\n" % story.rcn
		#	msg6 = "Primary Phone.....: %s\n" % story.phone1
		#	msg7 = "Secondary Phone...: %s\n" % story.phone2
		#	msg8 = "Email.............: %s\n" % story.email
		#	msg9 = "From..............: %s\n" % story.place
		#	message = "%s%s%s%s%s%s%s%s%s" % (msg1, msg2, msg3, msg4, msg5, msg6, msg7, msg8, msg9)
			
		#	email = EmailMessage('Welcome to www.shaketales.com', message, to=[story.email, 'pete.aumann@gmail.com'])
		#	email.send()
			
			return HttpResponseRedirect(
				'/user/%s/' % request.user.username
			)
	elif 'sharecode' in request.GET:
		sharecode = request.GET['sharecode']
		try:
			story = Story.objects.get(sharecode=sharecode)
			email = story.email
			first_name = story.first_name
			last_name = story.last_name
			place = story.place
			level = story.level
			rcn = story.rcn
			phone1 = story.phone1
			phone2 = story.phone2
			status = story.status
			audiofile = story.audiofile
			length = story.length		
			tags = ' '.join(
				tag.name for tag in story.storytag_set.all()
			)
		except (User.DoesNotExist, Story.DoesNotExist):
			pass
		#first_name = ''
		#last_name = ''
		#place = ''
		#level = ''
		#rcn = ''
		#phone1 = ''
		#phone2 = ''
		#status = ''
		#audiofile = ''
		#length = ''
		#tags = ''
		#try:  
		#	user = User.objects.get(username=sharecode)
		#	first_name = user.first_name
		#	last_name = user.last_name
		#	story = Story.objects.get(sharecode=sharecode)
		#	email = story.email
		#	length = story.length		
		#	tags = ' '.join(
		#		tag.name for tag in story.tag_set.all()
		#	)
		#except (User.DoesNotExist, Story.DoesNotExist):
		#	pass
		form = StorySaveForm({
			'sharecode': sharecode,
			'email': email,
			'first_name': first_name,
			'last_name': last_name,
			'place': place,
			'level': level,
			'rcn': rcn,
			'phone1': phone1,
			'phone2': phone2,
			'audiofile': audiofile,
			'status': status,
			'length': length,
			'tags': tags
		})
		
	else:
		form = StorySaveForm()
	variables = RequestContext(request, {
		'linkline': linkline,
		'page': page,
		'menupage': menupage,
		'form': form
	})
	return render_to_response('story_save.html', {}, variables)

def handle_uploaded_file(file_to_upload):
	#destination = open('%s/audio/%s' % (MEDIA_ROOT, filename), 'wb+')
	destination = open(file_to_upload.name, 'wb+')
	for chunk in file_to_upload.chunks():
		destination.write(chunk)
	destination.close()

def feedback_page(request):
	menupage = 'feedback'
	if request.method == 'POST':
		form = FeedbackSaveForm(request.POST)
		if form.is_valid():
			feedback = Feedback()
			feedback.first_name = form.cleaned_data['first_name']
			feedback.last_name = form.cleaned_data['last_name']
			feedback.email = form.cleaned_data['email']
			feedback.comments = form.cleaned_data['comments']
			
			# Save story to database and return it.
			feedback.save()
				
			#	msg1 = "Congratulations!  Your story has been approved by Reliv Compliance.\n"
			#	msg2 = "You can now go to www.shaketales.com and register with sharecode: %s\n\n" % story.sharecode
			#	msg3 = "For future reference, your story is registered as follows:\n\n"
			#	msg4 = "Sharecode.........: %s\n" % story.sharecode
			#	msg5 = "RCN...............: %s\n" % story.rcn
			#	msg6 = "Primary Phone.....: %s\n" % story.phone1
			#	msg7 = "Secondary Phone...: %s\n" % story.phone2
			#	msg8 = "Email.............: %s\n" % story.email
			#	msg9 = "From..............: %s\n" % story.place
			#	message = "%s%s%s%s%s%s%s%s%s" % (msg1, msg2, msg3, msg4, msg5, msg6, msg7, msg8, msg9)
				
			#	email = EmailMessage('Welcome to www.shaketales.com', message, to=[story.email, 'pete.aumann@gmail.com'])
			#	email.send()
			
			return HttpResponseRedirect('/')
	else:
		form = FeedbackSaveForm()
		
	variables = RequestContext(request, {
		'menupage': menupage,
		'form': form
	})
	return render_to_response('feedback_page.html', {}, variables)

def story_tag_page(request, tag_name):
	ITEMS_PER_PAGE = 12
	linkline = request.session['linkline']
	linklist = linkline.split(' ')
	tagline = tag_name
	page = 'storytag'
	menupage = 'storytag'
	storytag = get_object_or_404(StoryTag, name=tag_name)
	query_set = storytag.storys.order_by('-id')
	paginator = Paginator(query_set, ITEMS_PER_PAGE)
	try:
		page_number = int(request.GET['page'])
	except (KeyError, ValueError):
		page_number = 1
	try:
		page = paginator.page(page_number)
	except InvalidPage:
		raise Http404
	storys = page.object_list
	
	try:
		wall = Wall.objects.get(username=request.user.username)
		wall_list = wall.storys.order_by('-id')
	except (Wall.DoesNotExist):
		wall_list = []
	
	zipper = []								# bricktype, offset
	wallstory_list = []
	
	for wallpaper in wall_list:
		wallstory_list.append(wallpaper.sharecode)
		
	for story in storys:
		if story.sharecode in linklist:
			if story.sharecode in wallstory_list:
				zipper.append((story,1))			# both
			else:
				zipper.append((story,2))			# link
		else:
			if story.sharecode in wallstory_list:
				zipper.append((story,3))			# wall
			else:
				zipper.append((story,4))			# none
	
	variables = RequestContext(request, {
		'linkline': linkline,
		'page': page,
		'menupage': menupage,
		'tag_name': tag_name,
		'tagline': tagline,
		'zipper': zipper,
		'show_tags': True,
		'show_edit': True,
		'show_paginator': paginator.num_pages > 1,
		'has_prev': page.has_previous(),
		'has_next': page.has_next(),
		'page': page_number,
		'pages': paginator.num_pages,
		'next_page': page_number + 1,
		'prev_page': page_number - 1,
	})
	return render_to_response('story_by_tag_page.html', {}, variables)
	

	
def tag_page(request, tag_name):
	linkline = request.session['linkline']
	page = 'submit'
	menupage = 'submit'
	tag = get_object_or_404(Tag, name=tag_name)
	bookmarks = tag.bookmarks.order_by('-id')
	variables = RequestContext(request, {
		'linkline': linkline,
		'page': page,
		'menupage': menupage,
		'bookmarks': bookmarks,
		'tag_name': tag_name,
		'show_tags': True,
		'show_user': True
	})
	return render_to_response('tag_page.html', {}, variables)
	
def tag_cloud_page(request):
	page = 'tag_cloud'
	menupage = 'tag_cloud'
	linkline = request.session['linkline']
	MAX_WEIGHT = 5
	tags = Tag.objects.order_by('name')
	# Calculate tag, min and max counts.
	min_count = max_count = tags[0].bookmarks.count()
	for tag in tags:
		tag.count = tag.bookmarks.count()
		if tag.count < min_count:
			min_count = tag.count
		if max_count < tag.count:
			max_count = tag.count
	# Calculate count range. Avoid dividing by zero.
	range = float(max_count - min_count)
	if range == 0.0:
		range = 1.0
	# Calculate tag weights.
	for tag in tags:
		tag.weight = int(
			MAX_WEIGHT * (tag.count - min_count) / range
		)
	variables = RequestContext(request, {
		'linkline': linkline,
		'page': page,
		'menupage': menupage,
		'tags': tags
	})
	return render_to_response('tag_cloud_page.html', {}, variables)

def story_cloud_page(request):
	linkline = request.session['linkline']
	page = 'storytag'
	menupage = 'storytag'
	MAX_WEIGHT = 5
	storytags = StoryTag.objects.order_by('name')	
	# Calculate tag, min and max counts.
	min_count = max_count = storytags[0].storys.count()
	for storytag in storytags:
		storytag.count = storytag.storys.count()
		if storytag.count < min_count:
			min_count = storytag.count
		if max_count < storytag.count:
			max_count = storytag.count
	# Calculate count range. Avoid dividing by zero.
	range = float(max_count - min_count)
	if range == 0.0:
		range = 1.0
	# Calculate tag weights.
	for storytag in storytags:
		storytag.weight = int(
			MAX_WEIGHT * (storytag.count - min_count) / range
		)
	variables = RequestContext(request, {
		'linkline': linkline,
		'page': page,
		'menupage': menupage,
		'storytags': storytags
	})
	return render_to_response('story_cloud_page.html', {}, variables)

def before_after_page(request):
	linkline = request.session['linkline']
	menupage = 'before'
	
	if 'page' in request.GET:
		page = request.GET['page']
	else:
		page = 'before'
		
	variables = RequestContext(request, {
		'linkline': linkline,
		'page': page,
		'menupage': menupage
	})
	return render_to_response('before_after.html', {}, variables)
		
def story_page(request):
	linkline = request.session['linkline']
	page =  'playlist'
	menupage =  'playlist'
	# current = PlayList.object.get(title='CURRENT')
	storys = ('AUMANN-PETE-CUT.wav','ALLSOP-ROBIN-CUT.wav','NUTTER-MAGGIE-CUT.wav','LAY-BRIT-CUT.wav','ADAMSON-KAREN-CUT.wav','OGRADY-ANN-CUT.wav')
	variables = RequestContext(request, {
		'linkline': linkline,
		'page': page,
		'menupage': menupage,
		'storys': storys
	})
	return render_to_response('story_page.html', {}, variables)

def search_page(request):
	linkline = request.session['linkline']
	page = 'search'
	menupage = 'search'
	form = SearchForm()
	bookmarks = []
	show_results = False
	if 'query' in request.GET:
		show_results = True
		query = request.GET['query'].strip()
		if query:
			form = SearchForm({'query' : query})
			bookmarks = Bookmark.objects.filter(
				title__icontains=query
			)[:10]
	variables = RequestContext(request, {
		'linkline': linkline,
		'page': page,
		'menupage': page,
		'form': form,
		'bookmarks': bookmarks,
		'show_results': show_results,
		'show_tags': True,
		'show_user': True
	})
	return render_to_response('search.html', {}, variables)
		
def _bookmark_save(request, form):
	# Create or get link.
	link, dummy = Link.objects.get_or_create(
		url=form.cleaned_data['url']
	)
	# Create or get bookmark.
	bookmark, created = Bookmark.objects.get_or_create(
		user=request.user,
		link=link
	)
	# Update bookmark title.
	bookmark.title = form.cleaned_data['title']
	# If the bookmark is being updated, clear old tag list.
	if not created:
		bookmark.tag_set.clear()
	# Create new tag list.
	tag_names = form.cleaned_data['tags'].split()
	for tag_name in tag_names:
		tag, dummy = Tag.objects.get_or_create(name=tag_name)
		bookmark.tag_set.add(tag)
	# Share on the main page if requested.
	if form.cleaned_data['share']:
		shared, created = SharedBookmark.objects.get_or_create(
			bookmark=bookmark
		)
		if created:
			shared.users_voted.add(request.user)
			shared.save()
	# Save boojkmark to database and return it.
	bookmark.save()
	return bookmark

def _story_save(request, form):
	# hash out sharecode
	sharecode = hash_rcn_phone(form.cleaned_data['rcn'], form.cleaned_data['phone1'])
	# get or create story.
	story, created = Story.objects.get_or_create(sharecode=sharecode)
	# Update story data.
	story.first_name = form.cleaned_data['first_name']
	story.last_name = form.cleaned_data['last_name']
	story.rcn = form.cleaned_data['rcn']
	story.phone1 = form.cleaned_data['phone1']
	story.phone2 = form.cleaned_data['phone2']
	story.place = form.cleaned_data['place']
	story.status = form.cleaned_data['status']
	story.audiofile = form.cleaned_data['audiofile']
	story.email = form.cleaned_data['email']
	story.length = form.cleaned_data['length']
	story.level = form.cleaned_data['level']
	# story.linkline = ''
	
	# If the story is being updated, clear old tag list.
	if not created:
		story.storytag_set.clear()
	# Create new tag list.
	tag_names = form.cleaned_data['tags'].split()
	for tag_name in tag_names:
		tag, dummy = StoryTag.objects.get_or_create(name=tag_name)
		story.storytag_set.add(tag)
	
	# Save story to database and return it.
	
	story.save()
	return story
	
def bookmark_page(request, bookmark_id):
	linkline = request.session['linkline']
	shared_bookmark = get_object_or_404(
		SharedBookmark,
		id=bookmark_id
	)
	variables = RequestContext(request, {
		'shared_bookmark': shared_bookmark
	})
	return render_to_response('bookmark_page.html', {}, variables)

@login_required
def friend_invite(request):
	linkline = request.session['linkline']
	if request.method == 'POST':
		form = FriendInviteForm(request.POST)
		if form.is_valid():
			invitation = Invitation(
				name=form.cleaned_data['name'],
				email=form.cleaned_data['email'],
				code=User.objects.make_random_password(20),
				sender=request.user
			)
			invitation.save()
			try:
				invitation.send()
				request.user.message_set.create(
					message=u'An invitation was sent to %s.' %
						invitation.email
				)
			except smtplib.SMTPException:
				request.user.message_set.create(
					message=u'An error happened when '
						u'sending the invitation.'
				)
			return HttpResponseRedirect('/friend/invite/')
	else:
		form = FriendInviteForm()
	variables = RequestContext(request, {
		'form': form
	})
	return render_to_response('friend_invite.html', {}, variables)
	
def friend_accept(request, code):
	linkline = request.session['linkline']
	invitation = get_object_or_404(Invitation, code__exact=code)
	request.session['invitation'] = invitation.id
	return HttpResponseRedirect('/register/')
	
	