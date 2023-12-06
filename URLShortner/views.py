from django.shortcuts import render
import logging
import sys

logger = logging.getLogger(__name__)

def HomePage(request):
    try:
        if request.user.is_authenticated:
            return render(request, 'dashboard.html')
        return render(request, 'login.html')
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        logger.error("LoginSubmitAPI %s at %s",
                        str(e), str(exc_tb.tb_lineno), extra={'AppName': 'URLShortner'})
        return render(request, 'login.html')