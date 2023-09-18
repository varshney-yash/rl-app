from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse


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

def custom_error_page(request):
    return render(request,'index/custom_error_page.html')