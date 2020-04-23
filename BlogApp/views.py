from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout,get_user
from .forms import registerUser,getLogin,ArticleModelForm
from django.contrib.auth.models import User
from django.views import View
from .models import article,category
from django.views.generic import CreateView,FormView,ListView,DetailView,DeleteView,UpdateView,TemplateView
from django.contrib.auth.views import LoginView,LogoutView
from django.utils import timezone
from django.db.models import Count
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.conf import settings
from hitcount.views import HitCountDetailView

from django.contrib import messages


from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes,force_text,DjangoUnicodeDecodeError
from .tokens import generate_token
from django.core.mail import EmailMessage,send_mail
from django.http import HttpResponse


from django.db.models import Q
from django.shortcuts import render_to_response
from django.template.context import RequestContext

from BlogApp.tasks import send_verification_mail_task
# Create your views here.


class UserAuthorMixin(object):
	def dispatch(self, request, *args, **kwargs):
		handler = super().dispatch(request, *args, **kwargs)
		user = request.user
		post = self.get_object()
		if not (post.article_author == user):
			raise PermissionDenied
		return handler


class getRegister(CreateView):
	template_name='register.html'
	form_class=registerUser

	def get(self, request, *args, **kwargs):
		if self.request.user.is_authenticated:
			return redirect('/')
		else:
			return render(request, self.template_name, {'form': self.form_class})

	def post(self,request):
		form=self.form_class(request.POST or None)
		
		if form.is_valid():

			user=form.save(commit=False)
			user.is_active=False
			user.save()
			current_site=get_current_site(request)
			email_subject="Ativate Your Account"
			message=render_to_string('account_activation.html',{
				'user':user,
				'domain': current_site.domain,
				'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
				'token':generate_token.make_token(user)
			})

			to_email=form.cleaned_data.get('email')
			
			send_verification_mail_task.delay(email_subject,message,to_email)
			#return HttpResponse('Please confirm your email address to complete the registration.')
			messages.add_message(request,messages.SUCCESS,'account created succesfully')
			return render(request,'verified.html')
		return HttpResponse('Please confirm your email address to complete the registration.')



class ActivateAccountView(View):
	def get(self,request,uidb64,token):
		try:
			uid=force_text(urlsafe_base64_decode(uidb64))
			user=User.objects.get(pk=uid)
		except Exception as identifire:
			user=None

		if user is not None and generate_token.check_token(user,token):
			user.is_active=True
			user.save()
			messages.add_message(request,messages.SUCCESS,'account activated sucesfully')
			return redirect('login')


class loginfunction(FormView):
	template_name='login.html'
	form_class=getLogin

	def get(self, request, *args, **kwargs):
		if self.request.user.is_authenticated:
			return redirect('/')
		else:
			return render(request, self.template_name, {'form': self.form_class})

	def post(self,request):
		form=self.form_class(request.POST)
		if form.is_valid():
			username=form.cleaned_data['username']
			password=form.cleaned_data['password']
			user=authenticate(username=username,password=password)
			if user:
				login(request,user)
				return redirect('/')
			else:
				return redirect('login')


class logoutfunction(View):
	def get(self,request):
		if self.request.user.is_authenticated:
			logout(self.request)
			return redirect('/')
		else:
			return redirect('/')



class getArticle(ListView):
	template_name='index.html'
	model=article
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)    
		context['category'] = category.objects.all().annotate(articles_count=Count('article'))
		context['popular_articles']=article.objects.order_by("-hit_count_generic__hits")[:3]
		return context

class ArticleDetails(HitCountDetailView):
	template_name='single.html'
	model=article
	count_hit = True
	def get_context_data(self, **kwargs):
		context = super(ArticleDetails,self).get_context_data(**kwargs) 
		context.update({
        'popular_articles': article.objects.order_by('-hit_count_generic__hits')[:3],
        })  
		context['category'] = category.objects.all().annotate(articles_count=Count('article'))
		return context

class CategoryPost(ListView):
	template_name='category.html'
	model=article

	def get_queryset(self):
		self.category=get_object_or_404(category,pk=self.kwargs['pk'])
		return article.objects.filter(category=self.category.pk)

	def get_context_data(self, **kwargs):
		context = super(CategoryPost,self).get_context_data(**kwargs)
		context['category_post']=self.category    
		context['category'] = category.objects.all().annotate(articles_count=Count('article'))
		context['popular_articles']=article.objects.order_by("-hit_count_generic__hits")[:3]
		return context


class getProfile(LoginRequiredMixin,ListView):
	template_name='profile.html'
	model=article
	context_object_name='articles'
	login_url='/login/'
	def get_queryset(self):
		return article.objects.filter(article_author=self.request.user.id)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)    
		context['category'] = category.objects.all().annotate(articles_count=Count('article'))
		context['popular_articles']=article.objects.order_by("-hit_count_generic__hits")[:3]
		return context


class DeleteArticle(UserAuthorMixin,DeleteView):
	model=article
	template_name='delete_confirmation.html'
	success_url=reverse_lazy('profile')

class CreateArticle(LoginRequiredMixin,CreateView):
	template_name='create_article.html'
	login_url='/login/'
	model=article
	form_class=ArticleModelForm
	success_url='profile'
	def form_valid(self,form):
		form.instance.article_author=self.request.user
		return super(CreateArticle,self).form_valid(form)

class UpdateArticle(UserAuthorMixin,UpdateView):
	template_name='article_update.html'
	model=article
	form_class=ArticleModelForm
	success_url=reverse_lazy('profile')
	def form_valid(self,form):
		return super().form_valid(form)




class ArticleSorting(ListView):
	template_name='archives.html'
	model=article

	def get_queryset(self):
		return article.objects.filter(posted_on__year=self.kwargs['year'],posted_on__month=self.kwargs['month'])

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)    
		context['category'] = category.objects.all().annotate(articles_count=Count('article'))
		context['popular_articles']=article.objects.order_by("-hit_count_generic__hits")[:3]
	
		return context



class ArticleSearch(View):

	def get(self,request):
		if self.request.is_ajax():
			keyword=self.request.GET.get('keyword')
			if keyword is not None:
				results=article.objects.filter(
					Q(title__contains=keyword)|
					Q(body__contains=keyword)
			)

				return render_to_response('results.html',{'results':results})



class getAbout(TemplateView):
	template_name='about.html'

class getContact(TemplateView):
	template_name='contact.html'
