from django import forms
from mysite.models import Author, Recipe

# class AuthorForm(forms.Form):
#     Name = forms.CharField(label='Name', max_length=50)
#     Bio = forms.CharField(label='Bio', max_length=300)


class RecipeForm(forms.Form):
    def __init__(self, user, *args, **kwargs):
        super(RecipeForm, self).__init__(*args, **kwargs)
        a = Author.objects.filter(User=user).first()
        self.fields['Author'].choices = [(a.id, a.User.username)]
    Title = forms.CharField(label='Title', max_length=100)

    # authors = [(a.id, a.Name) for a in Author.objects.all()]

    Author = forms.ChoiceField()
    Description = forms.CharField(label='Description', max_length=250)
    Time_Required = forms.CharField(label='Time Required', max_length=50)
    Instructions = forms.CharField(label='Instructions', max_length=2000)


class SignupForm(forms.Form):
    Username = forms.CharField(max_length=50)
    Email = forms.EmailField()
    Password = forms.CharField(widget=forms.PasswordInput())


class LoginForm(forms.Form):
    Username = forms.CharField(max_length=50)
    Password = forms.CharField(widget=forms.PasswordInput())


class EditTweetForm(forms.Form):
    def __init__(self, user, *args, **kwargs):
        super(EditTweetForm, self).__init__(*args, **kwargs)
        a = Author.objects.filter(User=user).first()
        # r = Recipe.objects.filter(Author=a)
        self.fields['Author'].choices = [(a.id, a.User.username)]
        # self.fields['Recipe'].choices = [
        #     (r.id, r.Title) for r in Recipe.objects.filter(Author=a)]

    # Recipe = forms.ChoiceField(widget=forms.Select)
    Title = forms.CharField(label='Title', max_length=100)
    Author = forms.ChoiceField(widget=forms.Select)
    Description = forms.CharField(label='Description', max_length=250)
    Time_Required = forms.CharField(label='Time Required', max_length=50)
    Instructions = forms.CharField(label='Instructions', max_length=2000)


