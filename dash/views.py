from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from datetime import datetime
from .forms import UserForm, UserProfileForm, LoginForm

@login_required
def index(request):
	context = RequestContext(request)	

	# Cookie information
	# Obtain the response object early to add cookie information
	response = render(request, 'dash/guac_scrape.html', context)

	# Get the number of visits to the site
	visits = int(request.COOKIES.get('visits', '0'))

	# Does the cookie last_visit exist?
	if 'last_visit' in request.COOKIES:
		#Yes
		last_visit = request.COOKIES['last_visit']
		# Cast the value to a date/time object
		last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")

		# If it's been more than one day
		if (datetime.now() - last_visit_time).days > 0:
			# reassign the value of the cookie to +1
			response.set_cookie('visits', visits+1)
			response.set_cookie('last_visit', datetime.now())
	else:
		# Cookie last_visit doesn't exist, so create current date/time
		response.set_cookie('last_visit', datetime.now())

	# Return response back to the user, updating any cookies that need changed.
	return response	
		

	
	return render(request, 'dash/guac_scrape.html')

def home(request):
	# Displays the home page
	return render(request, 'dash/home.html')


def about(request):
	# Displays the about page
	return render(request, 'dash/about.html')

def FAQs(request):
	# Displays Frequently Asked Questions page
	return render(request, 'dash/FAQs.html')

def history(request):
	# Displays History page
	return render(request, 'dash/history.html')

def contact(request):
	# Displays the contact page
	return render(request, 'dash/contact.html')


def register(request):
	# Like before, get the request's context.
	context = RequestContext(request)

	# A boolean value for telling the template whether the registration was successful.
	# Set to False initially. Code changes value to True when registration succeeds.
	registered = False	
	
	if request.method == 'POST':
		user_form = UserForm(data=request.POST)
		profile_form = UserProfileForm(data=request.POST)

		if user_form.is_valid() and profile_form.is_valid():
			#Save the user's form data to the database
			user = user_form.save()
			
			# Now hash the password and update the user object
			user.set_password(user.password)
			user.save()
			
			# Sort out the UserProfile instance. 
			profile = profile_form.save(commit=False)
			profile.user = user

			# If the user chose to upload an image...
			if 'picture' in request.FILES:
				profile.picture = request.FILES['picture']

			# Now save the UserProfile model instance
			profile.save()			
			# Update variable to confirm that the user is registered
			registered = True
	
			return render(request, 'dash/login.html', context)
		# Invalid form or forms with mistakes
		# Prints the errors to terminal and shows it to the user
		else:
			print user_form.errors, profile_form.errors
	# Not an HTTP POST, so we render our form using two ModelForm instances.
	# These forms will be blank, ready for user input.
	else:
		user_form = UserForm()
		profile_form = UserProfileForm()

	# Render the template depending on the context
	return render(request,
		'dash/register.html',
		{'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
		 context)

def user_login(request):
	#obtain context
	form = LoginForm(request.POST or None)
	# If the request is an HTTP POST, try to pull out the relevant information
	if request.POST and form.is_valid():
		# Gather the username and password provided by the user
		user = form.login(request)
		if user:
			login(request, user)
			return HttpResponseRedirect('/dash/') # Redirects to main page
	return render(request, 'dash/login.html', {'form':form})
		
	
@login_required
def user_logout(request):
	logout(request)
	return HttpResponseRedirect('/dash/')

@login_required
def get_user_profile(request):
	u = User.objects.get(username=request.user)

	return render(request,'dash/user_profile.html', {'user':u})
