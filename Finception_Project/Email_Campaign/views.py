from django.shortcuts import render
from django.http import HttpResponse

import time
from django.core.mail import send_mail
from django.template import loader
import multiprocessing
import django
django.setup()
from . import forms, models


def index(request):
    return render(request, "Homepage.html")

def sub_unsub(request):

    if request.method == 'POST':
        form = forms.subscribe_form(request.POST or None)
        if (form.is_valid()):
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            flag = 0
            if models.User.objects.filter(email=email).exists():
                user = models.User.objects.get(email=email)
                if models.Inactive.objects.filter(user=user).exists():

                    user_sub = models.Subscriber()
                    user_sub.user = user
                    user_sub.save()
                    models.Inactive.objects.get(user=user).delete()
                else:
                    user_inac = models.Inactive()
                    user_inac.user = user
                    user_inac.save()
                    models.Subscriber.objects.get(user=user).delete()
                    flag = -1
            else:
                user = models.User()
                user.email = email
                user.first_name = first_name
                user.save()
            return render(request, 'subscribe_page.html', {'flag': flag})


        else:
            return HttpResponse("Invalid form")



    return render(request, 'subscribe_page.html')

# send_mail(
#     'Subject here',
#     'Here is the message.',
#     'from@example.com',
#     ['to@example.com'],
#     fail_silently=False,
# )

def postBlog(request):
    if request.method == 'POST':
        form = forms.blog_form(request.POST or None)
        if form.is_valid():
            heading = form.cleaned_data['heading']
            article = form.cleaned_data['article']
            blog = models.Blog(heading=heading, article=article)
            blog.save()
            return render(request, 'post_blog.html', {'success': 1})
        else:
            return HttpResponse("Invalid Form")
    else:
        return render(request, 'post_blog.html', {'success': 0})

def all_articles(request):

    articles = models.Blog.objects.all()

    return render(request, 'all_articles.html', {"articles": articles})


def show_article(request, articleId):
    article = models.Blog.objects.get(id=articleId)
    return render(request, 'show_article.html', {"heading": article.heading, "article": article.article})

def send_email(request, articleId):
    if request.method == "POST":
        form = forms.email_form(request.POST or None)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            op_message = form.cleaned_data['op_message']
            article = models.Blog.objects.get(id=articleId)
            users = models.Subscriber.objects.all() # getting all subscribers
            users = [i.user.email for i in users] # getting mail of all subscribers
            preview_text = article.article[:20] + '...' # Taking first 20 characters
            plain_text = article.article

            html_text = loader.render_to_string('email_html.html', { 'op_message': op_message,
                                                                     'article': article,
                                                                     'preview_text': preview_text})
            nargs = [(subject, i, html_text, plain_text) for i in users]


            start_time = time.time()
            # send_email_parallel(subject, "plain_text", users, "shukla.anurag0006@gmail.com", html_text)
            cpu_count = multiprocessing.cpu_count()
            pool = multiprocessing.Pool(processes = cpu_count-1) # TODO: Keep it Dynamic
            pool.map(send_mail_parallel, nargs)
            total_time = time.time()-start_time

            return  render(request, 'results.html', {'execution_time': total_time})

    return render(request, 'send_email.html')


def send_mail_parallel(i):
    subject, to_, html_message, plain_text = i

    from_ = "#########Please Enter your email here############"
    send_mail(subject, plain_text, from_, [to_], html_message=html_message)







