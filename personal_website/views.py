from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse
from users.models import Profile
from django.http import Http404, HttpResponse


def index(request):
    now = datetime.now()
    html = f'''
    <html>
        <body>
            <h1>Hello! Coming soon . . .</h1>
            <p>{ now }</p>
        </body>
    </html>
    '''
    return HttpResponse(html)

def email_verification(request, token):
    print(token)
    context = {}
    print('##*')
    try:
        print('##')
        profile = Profile.objects.filter(verification_token=token).first()
        if profile:
            print('**', profile)
            profile.verified = True
            profile.save()
            context['verification_successful'] = True
        else:
            context['invalid_token'] = True
        print(context, '--context')
    except Http404:
        context['invalid_token'] = True

    return render(request, 'personal_website/email_verification.html', context)
