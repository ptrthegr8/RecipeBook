from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from mysite.models import Author, Recipe
from mysite.forms import RecipeForm, LoginForm, SignupForm, EditTweetForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.shortcuts import reverse
from mysite.settings import LOGOUT_REDIRECT_URL


def recipe_views(request):

    results = Recipe.objects.all()

    return render(request, 'recipe_view.html', {'data': results})


def author_views(request, id):

    results = Recipe.objects.filter(Author__id=id)
    author = Author.objects.get(id=id)
    author_favorites = author.Favorites.all()

    return render(
        request,
        'author_view.html',
        {
            'data': results,
            'author': author,
            'author_favorites': author_favorites
        }
    )


def individual_views(request, id):

    results = Recipe.objects.filter(id=id)
    
    return render(
        request,
        'individual_view.html',
        {
            'data': results,
            "is_current_user": True if request.user.id is results.first().Author.id else False
        }
    )

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


def edit_recipe(request, id):
    current_user = User.objects.get(id=request.user.id)
    recipe = Recipe.objects.get(id=id)
    data = {
        "Title": recipe.Title,
        "Description": recipe.Description,
        "Time_Required": recipe.Time_Required,
        "Instructions": recipe.Instructions
    }
    if request.method == "POST":
        form = EditTweetForm(current_user, request.POST)
        if form.is_valid():
            data = form.cleaned_data
            recipe = recipe
            recipe.Title = data["Title"]
            recipe.Author = current_user.author
            recipe.Description = data["Description"]
            recipe.Time_Required = data["Time_Required"]
            recipe.Instructions = data["Instructions"]
            print(recipe)
            recipe.save()
            return(HttpResponseRedirect(reverse('homepage')))
    else:
        form = EditTweetForm(user=current_user, initial=data)
    return render(request, 'recipe_edit.html', {'form': form, 'id': id})


@staff_member_required
def signup_view(request):

    form = SignupForm(None or request.POST)

    if form.is_valid():
        data = form.cleaned_data
        user = User.objects.create_user(
            data['Username'], data['Email'], data['Password'])
        Author.objects.create(
            User=user,
            Name=data['Username'],
            Bio=data['Email']
        )
        login(request, user)
        return HttpResponseRedirect(reverse('homepage'))

    return render(request, 'signup.html', {'form': form})


def login_view(request):
    form = LoginForm(None or request.POST)

    if form.is_valid():
        data = form.cleaned_data
        user = authenticate(
            username=data['Username'], password=data['Password'])
        if user is not None:
            login(request, user)

            return HttpResponseRedirect(reverse('homepage'))

    return render(request, 'login.html', {'form': form})


def logout_view(request):

    results = Recipe.objects.all()
    logout(request)

    return render(request, 'recipe_view.html', {'data': results})
    return HttpResponseRedirect(LOGOUT_REDIRECT_URL)


def favorite_view(request, id):
    current_author = Author.objects.get(User=request.user)
    targeted_recipe = Recipe.objects.get(id=id)
    recipe_collection = current_author.Favorites.all()
    data = {
        "test": current_author,
        "recipe": targeted_recipe,
        "recipe_collection": recipe_collection
    }
    print(data)
    current_author.Favorites.add(targeted_recipe)
    return render(request, 'favorite_view.html', data)
