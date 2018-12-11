from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from mysite.models import Author, Recipe
from mysite.forms import RecipeForm, LoginForm, SignupForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.shortcuts import reverse
from mysite.settings import LOGOUT_REDIRECT_URL

def recipe_views(request):

    results = Recipe.objects.all()

    return render(request, 'recipe_view.html', {'data':results})

def author_views(request, id):

    results = Recipe.objects.filter(Author__id=id)
    author = Author.objects.filter(id=id)

    return render(request, 'author_view.html', {'data':results, 'author':author})

def individual_views(request, id):

    results = Recipe.objects.filter(id=id)

    return render(request, 'individual_view.html', {'data': results})

# @login_required
# def get_author(request):

#     if request.method == 'POST':

#         form = RecipeForm(request.user, request.POST)

#         if form.is_valid():
#             data = form.cleaned_data
#             Author.objects.create(
#                 Name=data['Name'],
#                 Bio=data['Bio']
#             )

#     else:

#         form = AuthorForm()
#     return render(request, 'author.html', {'form': form})

@login_required
def get_recipe(request):

    if request.method == 'POST':

        form = RecipeForm(request.user, request.POST)

        if form.is_valid():
            data = form.cleaned_data
            Recipe.objects.create(
                Title=data['Title'],
                Author=Author.objects.filter(id=data['Author']).first(),
                Description=data['Description'],
                Time_Required=data['Time_Required'],
                Instructions=data['Instructions']
            )

    else:

        form = RecipeForm(user=request.user)

    return render(request, 'recipe.html', {'form': form})

@staff_member_required
def signup_view(request):

    form = SignupForm(None or request.POST)

    if form.is_valid():
        data = form.cleaned_data
        user = User.objects.create_user(
            data['Username'], data['Email'], data['Password'])
        Author.objects.create(
            User = user,
            Name = data['Username'],
            Bio = data['Email']
        )
        login(request, user)
        return HttpResponseRedirect(reverse('homepage'))

    return render(request, 'signup.html', {'form': form})

def login_view(request):

    form = LoginForm(None or request.POST)

    if form.is_valid():
        data = form.cleaned_data
        user = authenticate(username=data['Username'], password=data['Password'])
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('homepage'))

    return render(request, 'login.html', {'form': form})

def logout_view(request):

    results = Recipe.objects.all()
    logout(request)

    return render(request, 'recipe_view.html', {'data':results})
    return HttpResponseRedirect(LOGOUT_REDIRECT_URL)