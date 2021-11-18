from django.shortcuts import render, redirect , reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from .models import Post
from .forms import PostForm
from profiles.models import Profile

from  itertools import chain 



def get_author(user):
	qs = Profile.objects.filter(user=user)
	if qs.exists():
		qs[0]
	return None	

def index(request):
	objects = Post.objects.all()
	context = {'objects':objects,}
	return render(request, 'posts/index.html', context )

@login_required
def post_of_friends_profiles(request):
	#paginator
	objects = Profile.objects.all()
	paginator = Paginator(objects, 2)
	page_request_var = 'page'
	page = request.GET.get(page_request_var)
	try:
		paginated_queryset = paginator.page(page)
	except PageNotAnInteger:
		paginated_queryset = paginator.page(1)
	except EmptyPage:
		paginated_queryset = paginator.page(paginator.num_page)

	#followers posts :)
	profile = Profile.objects.get(user=request.user)
	following =  Profile.objects.all()
	users=[user for user in profile.friends.all()]

	posts = []
	qs = []
 
	for u in users:
		p  = Profile.objects.get(user=u)
		p_post = p.post_set.all()
		posts.append(p_post)

	my_posts = profile.profiles_posts()
	posts.append(my_posts)

	if len(posts)>0:
		qs = sorted(chain(*posts), reverse=True, key= lambda obj: obj.created)
	context = {
	'page_request_var':page_request_var,
	'queryset':paginated_queryset,
	'my_posts':my_posts,
	'posts':qs,
	'profile':profile,
	'following':following
	}
	return render(request, 'posts/main.html', context )

@login_required
def create_post(request):
	posts  =  Post.objects.all()[:3]
	form = PostForm(request.POST or None , request.FILES or None)
	author = Profile.objects.get(user=request.user)
	if request.method == 'POST':
		if form.is_valid():
			form.instance.author = author
			form.save()
			return redirect('posts-profile')
		else:
			form = PostForm
			return redirect('create-post')
	context = {
	'form':form,
	'posts': posts,
	}
	return render(request, 'posts/create_post.html', context)
@login_required
def detail_post(request, pk):
	objects = Post.objects.get(pk=pk)
	return render(request, 'posts/detail_post.html', {'objects': objects})


@login_required
def update_post(request, id):
	posts = get_object_or_404(Post, id=id)
	form = PostForm(
		request.POST or None,
	 	request.FILES or None,
	 	instance=posts)
	author = get_author(request.user)
	if request.method == 'POST':
		if form.is_valid():
			# form.instance.author = author
			form.save()
			return redirect('posts-profile')
	context = {
	'form': form,
	'posts': posts
	}
	return render(request, 'posts/update_post.html', context)
@login_required
def delete_post(request, pk):
	objects = Post.objects.get(pk=pk)
	objects.delete()
	return redirect("posts-profile")