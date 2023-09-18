from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import userRegisterForm,UserUpdateForm,ProfileUpdateForm
from .models import Profile
from django.views.generic import DetailView

def register(request):
    if request.method == 'POST':
        form = userRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f'Thanks for joining, {username}. Please login to continue!')
            return redirect('user-login')
    else:
        form = userRegisterForm()
    context = {'form':form}
    return render(request,'users/register.html',context)

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        bio_form = ProfileUpdateForm(request.POST,instance=request.user.profile)
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm()
        bio_form = ProfileUpdateForm(instance=request.user.profile)

    if u_form.is_valid():
        u_form.save()
    if p_form.is_valid():
        p_form.save()
    if bio_form.is_valid():
        bio_form.save()

    context = {
        'u_form':u_form,
        'p_form':p_form,
        'bio_form':bio_form
    }

    return render(request,'users/profile.html',context)

class ProfileDetailView(DetailView):
    model = Profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.object.user  # Access the associated User object
        return context

# test image upload
from .models import Profile
def upload_image(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the form data to create a new Profile instance with the uploaded image
            form.save()
    else:
        form = ProfileUpdateForm()
    
    return render(request, 'users/upload_image.html', {'form': form})