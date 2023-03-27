from django.shortcuts import redirect, render


def dashboard(request):
    return redirect('forbidden')

def forbidden(request):
    return render(request, 'forbidden.html', {})
