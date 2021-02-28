from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from .models import Category, Page, UserProfile
from .forms import CategoryForm, PageForm, UserForm, UserProfileForm
from django.contrib.auth.decorators import login_required
from datetime import datetime
from registration.backends.simple.views import RegistrationView
from django.contrib.auth.models import User
from rango_app.templatetags.rango_app_template_tags import get_category_list
from django.views import View
from django.utils.decorators import method_decorator

def index(request):
    """The Home Page for Rango"""
    # request.session.set_test_cookie()
    category_list = Category.objects.order_by("-likes")[:6]
    page_list = Page.objects.order_by("-views")[:6]
    context_dict = {'categories': category_list, 'pages': page_list}

    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']
    response = render(request,'rango_app/index.html',context=context_dict)
    return response

def show_category(request, category_name_slug):
    """Navigate to each category"""
    context_dict = {}
    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category).order_by('-views')
        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['pages'] = None

    return render(request, 'rango_app/category.html', context_dict)

@login_required
def add_category(request):
    """Allowing adding new categories"""
    form = CategoryForm

    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return index(request)
        else:
            print(form.errors)

    return render(request, 'rango_app/add_category.html', {'form': form})

@login_required
def add_page(request, category_name_slug):
    """Allow adding pages to existing categories"""
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    form = PageForm()
    if request.method == "POST":
        form = PageForm(request.POST)
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                return show_category(request, category_name_slug)
        else:
            print(form.errors)

    context_dict = {'form': form, 'category': category}
    return render(request, 'rango_app/add_page.html', context_dict)

def about(request):
    """The About Page for Rango"""
    # if request.session.test_cookie_worked():
    #    print('TEST COOKIE WORKED!')
    #     request.session.delete_test_cookie()
    return render(request, 'rango_app/about.html', {})


@login_required
def restricted(request):
    message = f"Welcome {request.user.username.title()}! "
    message += f"You can view this content because you are logged in."
    message += f"\nYou can always leave me feedback or express concerns"
    message += f" at francomania23@live.com. Enjoy!"
    message += f"\nSpecial regards, FrankOlum."
    context_dict = {'message': message}
    return render(request, 'rango_app/restricted.html', context_dict)

# Define a helper function client cookies
def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val

def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request,'visits','1'))

    last_visit_cookie = get_server_side_cookie(
            request, 'last_visit', str(datetime.now())
        )
    last_visit_time =datetime.strptime(
            last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S'
        )
    if (datetime.now()-last_visit_time).days > 0:
        visits += 1
        request.session['last_visit'] = str(datetime.now())
    else:
        visits = 1
        request.session['last_visit'] = last_visit_cookie
    request.session['visits'] = visits

def search_page(request):
    search_text = request.GET['query']
    pages = Page.objects.filter(title__contains=search_text)
    context_dict = {'pages': pages}
    return render(request, 'rango_app/search.html', context_dict)

def track_url(request):
    page_id = None
    url = '/'
    if request.method == "GET":
        if 'page_id' in request.GET:
            page_id = request.GET['page_id']
            if page_id:
                page = Page.objects.get(id=page_id)
                page.views += 1
                page.save()
                url = page.url
            else:
                pass

    return HttpResponseRedirect(url)

@login_required
def register_profile(request):
    form = UserProfileForm()
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()
            
            return redirect("/")
        else:
            print(form.errors)
    
    context_dict = {'form': form}
    return render(request, 'rango_app/profile_registration.html', context_dict)

# Using Class-Based View
class ProfileView(View):
    def get_user_details(self, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None
        
        user_profile = UserProfile.objects.get_or_create(user=user)[0]
        form = UserProfileForm({'website': user_profile.website,
                                'picture': user_profile.picture,
                                'message': user_profile.message})
        
        return (user, user_profile, form)
    
    @method_decorator(login_required)
    def get(self, request, username):
        try:
            (user, user_profile, form) = self.get_user_details(username)
        except TypeError:
            return redirect("/")
        
        context_dict = {'user_profile': user_profile,
                        'selected_user': user,
                        'form': form}
        
        return render(request, 'rango_app/profile.html', context_dict)
    
    @method_decorator(login_required)
    def post(self, request, username):
        try:
            (user, user_profile, form) = self.get_user_details(username)
        except TypeError:
            return redirect("/")
        
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        
        if form.is_valid():
            form.save(commit=True)
            return redirect("/")
        else:
            print(form.errors)
        
        context_dict = {'user_profile': user_profile,
                        'selected_user': user,
                        'form': form}
        
        return render(request, 'rango_app/profile.html', context_dict)
        
            
class ListProfilesView(View):
    @method_decorator(login_required)
    def get(self, request):
        profiles = UserProfile.objects.all()
        
        return render(request,
                      'rango_app/list_profiles.html',
                      {'userprofile_list': profiles})

@login_required
def like_category(request):
    cat_id = None
    if request.method == 'GET':
        cat_id = request.GET.get('category_id')
        likes=0
        if cat_id:
            cat = Category.objects.get(id=int(cat_id))
            if cat:
                likes = cat.likes + 1
                cat.likes = likes
                cat.save()
    return HttpResponse(likes)

def suggest_category(request):
    cat_list= []
    starts_with = ''
    if request.method == 'GET':
        starts_with = request.GET['suggestion']
    cat_list = get_category_list(7, starts_with)
    return render(request, 'rango_app/cats.html', {'cats': cat_list})

