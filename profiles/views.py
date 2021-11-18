from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView , CreateView
from django.db.models import  Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


from .models import Profile
from .forms import ProfileForm, ProfileCreationForm

class Signup(CreateView):
	model = Profile
	form_class = ProfileCreationForm
	template_name = 'profiles'



def search(request):
	queryset =  Profile.objects.all()
	query = request.GET.get('q')
	if query:
		queryset = queryset.filter(
		Q(user__username__iexact=query)|
		Q(first_name__icontains=query)).distinct()
	context = {
	'queryset':queryset
	}
	return render(request, 'profiles/search_results.html', context)


@login_required
def my_profile(request):
	profile = Profile.objects.get(user=request.user)
	form = ProfileForm(request.POST or None, request.FILES or None ,instance=profile )
	config = False

	if request.method == 'POST':
		if form.is_valid():
			form.save()
			config = True
	context ={
	'profile':profile,
	'form': form,
	'config':config
	}	
	return render(request, 'profiles/myprofile.html', context)

@login_required
def follow_and_unfollow(request):
	my_profile = Profile.objects.get(user=request.user)
	pk = request.POST.get('profile_pk')
	obj = Profile.objects.get(pk=pk)

	if obj.user in my_profile.friends.all():
		my_profile.friends.remove(obj.user)
	else:
		my_profile.friends.add(obj.user)
	return redirect(request.META.get('HTTP_REFERER'))
	return redirect('profiles:profile-list')


class ProfileListView(LoginRequiredMixin,ListView):
	model = Profile
	template_name = 'profiles/profile-list.html'

	def get_queryset(self):
		profile = Profile.objects.all().exclude(user=self.request.user)
		return profile



class ProfileDetailView(LoginRequiredMixin,DetailView):
	model = Profile
	template_name = 'profiles/profile_detail.html'

	def get_object(self, *args, **kwargs):
		pk = self.kwargs.get('pk')
		view_profile = Profile.objects.get(pk=pk)
		return view_profile

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(**kwargs)
		my_profile = Profile.objects.get(user=self.request.user)
		view_profile = self.get_object()
		if view_profile.user in my_profile.friends.all():
			follow = False
		else:
			follow = True
		context['follow']=follow
		return context


