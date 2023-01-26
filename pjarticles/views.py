from curses.ascii import HT
from gc import get_objects
from genericpath import commonprefix
from django.db.models.fields import CommaSeparatedIntegerField
from django.shortcuts import redirect, render, get_object_or_404
from django.http.response import HttpResponse
from .models import PJArticles, PJComments
from .forms import PJArticleForm, CommentForm, ContactForm

from django.contrib.auth import authenticate, login as www, logout
from django.contrib import messages

from django.contrib.auth.decorators import login_required

from django.db.models import ProtectedError

from django.core.mail import send_mail, BadHeaderError
from django.conf import settings

# Create your views here.

def main_view(request):
    user = request.user
    art = PJArticles.objects.filter(important=True, status = True)
    art_last = PJArticles.objects.filter(status = True).order_by('-pub_data')[:3]
    art_status = set(art)
    art_last_status = set(art_last)
    status_count = len(art_status | art_last_status)
    return render(request, 'articles.html', {'login' : user, 'art_last' : art_last, 'art' : art, 'status_count' : status_count})


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        print(user)
        if user is not None:
            www(request, user)

            return redirect('/articles/add_article')
        else:
            messages.error(request, 'Nieprawidłowy login lub hasło! Spróbuj ponownie')

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    user = request.user
    print(user)
    art = PJArticles.objects.filter(important=True)
    art_last = PJArticles.objects.all().order_by('-pub_data')[:3]
    return render(request, 'articles.html', {'login' : user, 'art_last' : art_last, 'art' : art})


def article_view(request, a_id):
    user = request.user
    art = PJArticles.objects.get(id=a_id)
    adcom = PJComments.objects.filter(article=a_id)
    print(adcom)
    return render(request, 'article.html', {'login': user,'art' : art, 'adcom' : adcom})


def article_acc(request):
    art = PJArticles.objects.filter(status = False)
    return render(request, 'article_accept.html', {'art' : art})


def article_pub(request, article_id):
    art = PJArticles.objects.all()
    a_object = PJArticles.objects.get(id=article_id)
    try:
        a_object.status = True
        a_object.save()
        return redirect('/articles/article_accept/')
    except ProtectedError:
        print('Bład')
        return render(request, 'articles_accept.html', {'error' : 'Nie można zmienic statusu'})
    return render(request, 'articles_accept.html', {'art' : art})   


@login_required
def add_article(request):
    user = request.user

    if request.method == 'POST':
        form = PJArticleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect ('/articles/main/')
        else:
            return render(request, 'add_article.html', {'form' : form})
    else:
        form = PJArticleForm()
        return render(request, 'add_article.html', {'form' : form})
    return render(request, 'add_article.html')


def add_comment(request, article_id):
    art = PJArticles.objects.get(id=article_id)

    if request.method == 'POST':
        cform = CommentForm(request.POST)
        if cform.is_valid():
            c = cform.save(commit=False)
            c.article = art
            c.save()
            return redirect ('/articles/main/')
        else:
            return render(request, 'add_comment.html', {'form' : cform})
    else:
        cform = CommentForm()
        return render(request, 'add_comment.html', {'form' : cform, 'art': art})


def article_edit(request, a_id):
    a_object = get_object_or_404(PJArticles, pk=a_id)
    a_form = PJArticleForm(request.POST or None, instance=a_object)
    if request.method == 'POST':
        if a_form.is_valid():
            a_form.save()
            return redirect ('/articles/main/')
        else:
            return render(request, 'article_editor.html', {'form' : a_form})
    else:
        return render(request, 'article_editor.html', {'form' : a_form})


def article_del(request, a_id):
    a_object = PJArticles.objects.get(id=a_id)
    art = PJArticles.objects.filter(important=True)
    art_last = PJArticles.objects.all().order_by('-pub_data')[:3]
    try:
        a_object.delete()
        return redirect ('/articles/article_accept/')
    except ProtectedError:
        return render(request, 'articles.html', {'art_last' : art_last, 'art' : art, 'error': 'Nie można usunąć artykułu!'})


def contact(request):
    if request.method == 'POST':
        c_form = ContactForm(request.POST)
        if c_form.is_valid():
            subject = 'Wiadomość z systemu CMS'
            body = {
                'first_name' : c_form.cleaned_data['first_name'],
                'last_name' : c_form.cleaned_data['last_name'],
                'mail' : c_form.cleaned_data['c_mail'],
                'text' : c_form.cleaned_data['text'],
                'klauzula': 'Taki sam tekst dla każdej wiadomości',
            }
            message = "\n".join(body.values())
            try:
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [c_form.cleaned_data['c_mail'], 'programistac3@gmail.com'])
            except BadHeaderError:
                return HttpResponse("Wystąpił błąd wiadomości")
            return redirect ('/articles/main/')
    c_form = ContactForm()
    return render(request, 'contact.html', { 'form' : c_form })