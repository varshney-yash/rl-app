from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import userRegisterForm,UserUpdateForm,ProfileUpdateForm, BioUpdateForm
from .models import Profile
from django.views.generic import DetailView
import smtplib, random, string
from email.message import EmailMessage

SMTP_SERVER = "smtp-relay.brevo.com"
SMTP_PORT = 587
SMTP_USERNAME = "17yashvarshney@gmail.com"
SMTP_PASSWORD = "fcI5rm6Gk02aZ3dB"

def generate_random_token():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(16))


def register(request):
    if request.method == 'POST':
        form = userRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            user = form.instance
            messages.success(request,f'Thanks for joining, {username}. Please login to continue!')

            profile = Profile.objects.get(user=user)
            profile.verification_token = generate_random_token()
            profile.save()
            verification_link = f"http://{request.get_host()}/verify/{profile.verification_token}/"

            msg = EmailMessage()
            msg.set_content(f"Hi, {username}! Here is your verification link:- {verification_link}. \n\n\n Made with ❤️ by Yash Varshney")
            msg["Subject"] = "Welcome to YVblogs!"
            msg["From"] = SMTP_USERNAME
            msg["To"] = form.cleaned_data.get('email')
        
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                server.starttls()
                server.login(SMTP_USERNAME, SMTP_PASSWORD)
                server.send_message(msg)
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
        bio_form = BioUpdateForm(request.POST,instance=request.user.profile)
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm()
        bio_form = BioUpdateForm(instance=request.user.profile)

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
