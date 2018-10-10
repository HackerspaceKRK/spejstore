from django.shortcuts import redirect

def auth_redirect(request):
    return redirect('social:begin', 'hswaw')
