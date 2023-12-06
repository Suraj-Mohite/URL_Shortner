from django.shortcuts import render, redirect
from django.http import JsonResponse
from .utils import get_alias
from django.db import IntegrityError
from django.contrib.sites.shortcuts import get_current_site
from .models import URL
import json
import logging
import sys

logger = logging.getLogger(__name__)

# Create your views here.

def Dashboard(request, *args, **kwargs):

    if not request.user.is_authenticated:   
        return redirect('login')
    
    if request.method == 'POST':
        response = {}
        response['status'] = 500
        response['message'] = 'Internal server Error'
        try:
            data = json.loads(request.body)
            target_url = data.get('target_url')
            alias = data.get('alias', None)

            if not alias:
                alias = get_alias()

            try:
                request.user.url_set.create(target_url=target_url, alias=alias)
                response['status'] = 200
                response['message'] = 'Success'
                return JsonResponse(response)
            except IntegrityError as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                logger.info("Dashboard %s at %s", str(e), str(exc_tb.tb_lineno), extra={'AppName': 'Accounts'})
                logger.info("Alias already exists", extra={'AppName': 'Accounts'})
                response['status'] = 409
                response['message'] = 'Alias already exists'
                return JsonResponse(response)
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                logger.error("Dashboard %s at %s", str(e), str(exc_tb.tb_lineno), extra={'AppName': 'Accounts'})
                return JsonResponse(response)

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            logger.error("Dashboard %s at %s", str(e), str(exc_tb.tb_lineno), extra={'AppName': 'Accounts'})
            return JsonResponse(response)
        
    site = get_current_site(request)
    print(site)
    return render(request, 'dashboard.html', {'domain' : site})


def redirect_to_target_page(request, alias):
    try:
        obj = URL.objects.get(alias=alias)
        redirect_url = obj.target_url
        return redirect(redirect_url)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logger.error("redirect_to_target_page %s at %s", str(e), str(exc_tb.tb_lineno), extra={'AppName': 'Accounts'})
        return render(request, 'page404.html')