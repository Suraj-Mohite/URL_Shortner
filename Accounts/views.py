from django.shortcuts import render, redirect
from django.http import JsonResponse

from django.contrib.auth.models import User
from django.contrib import auth

from .utils import remove_html_tags

import json
import logging
import sys

logger = logging.getLogger(__name__)

# Create your views here.

def login(request):

    if request.user.is_authenticated:   
        return redirect('/dashboard')
    
    if request.method == 'POST':
        response = {}
        response['status'] = 500
        response['message'] = 'Internal server Error'
        try:
            data = json.loads(request.body)
            username = data.get('username')
            username = remove_html_tags(username)
            password = data.get('password')
        
            if username and password:
                user = auth.authenticate(request, username=username, password=password)
                logger.info("user %s", user, extra={'AppName': 'Accounts'})
                if user:
                    auth.login(request, user)
                    response['status'] = 200
                    response['message'] = 'Success'
                    return JsonResponse(response)
                response['status'] = 404
                response['message'] = 'User not found'
                return JsonResponse(response)
            response['status'] = 400
            response['message'] = 'Bad Request'
            return JsonResponse(response)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("LoginSubmitAPI %s at %s", str(e), str(exc_tb.tb_lineno), extra={'AppName': 'Accounts'})
            return JsonResponse(response)
     
    return render(request, "login.html")

def register(request):

    if request.user.is_authenticated:   
        return redirect('/')

    if request.method == 'POST':
        response = {}
        response['status'] = 500
        response['message'] = 'Internal server Error'
        try:
            data = json.loads(request.body)
            username = data.get('username')
            username = remove_html_tags(username)
            email = data.get('email')
            email = remove_html_tags(email)
            password = data.get('password')
        
            if username and email and password:
                if User.objects.filter(username=username).exists():
                    response['status'] = 409
                    response['message'] = 'Username already exists'
                    return JsonResponse(response)
                
                if User.objects.filter(email=email).exists():
                    response['status'] = 409
                    response['message'] = 'Email already exists'
                    return JsonResponse(response)
                
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                auth.login(request, user)
                response['status'] = 200
                response['message'] = 'Success'
                return JsonResponse(response)
                    
            response['status'] = 400
            response['message'] = 'Bad Request'
            return JsonResponse(response)
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("RegisterAPI %s at %s", str(e), str(exc_tb.tb_lineno), extra={'AppName': 'Accounts'})
            return JsonResponse(response)
        
    return render(request, "register.html")


def logout(request):
    try:
        auth.logout(request)
        return redirect('/auth/login/')
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logger.error("RegisterAPI %s at %s", str(e), str(exc_tb.tb_lineno), extra={'AppName': 'Accounts'})