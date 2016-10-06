from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from .models import RegForm
from .forms import RegistrationForm
from django.core import serializers
from django.core.urlresolvers import reverse
from projherokureg.settings import RECAPTCHA_SECRET_KEY
import requests


# Create your views here.

def registration_added(request):
    context = {'message': 'Added, Thank You!'}
    return render(request, 'thanks.html', context=context)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def add_registration(request):
    if request.method == 'POST':

        data = request.POST
        captcha_rs = data.get('g-recaptcha-response')
        url = "https://www.google.com/recaptcha/api/siteverify"

        params = {
            'secret': RECAPTCHA_SECRET_KEY,
            'response': captcha_rs,
            'remoteip': get_client_ip(request)
        }

        print(params)

        verify_rs = requests.post(url, params=params)
        verify_rs = verify_rs.json()

        response = {}
        response["status"] = verify_rs.get("success", False)

        print(response)

        # Test captcha first
        if response['status']:
            print('Captcha was a success')
            f = RegistrationForm(data)      
            if f.is_valid():
                print('form is valid')
                registration = f.save(commit=False)
                registration.save()
                url = reverse('registration_added')                
                print(url)
                return HttpResponseRedirect(url)
                #return HttpResponseRedirect(reverse('spot_added'))
            else:
                print('not valid?!?!?')
                print (f.errors)
                return render(request, 'addgarage.html', {'form': f})
        else:
            # Failed the Captcha:
            print(verify_rs.get('error-codes', 'no error code available... weird.'))
            f = RegistrationForm(data)            
            return render(request, 'addgarage.html', {'form': f, 'captchaError':'You failed the captcha...'})
    else:
        f = RegistrationForm()
        return render(request, 'addgarage.html', {'form': f})
