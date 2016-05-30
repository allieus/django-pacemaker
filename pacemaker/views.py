import os
import re
from io import StringIO
from django.contrib import messages
from django.db.utils import OperationalError
from django.shortcuts import redirect, resolve_url, render
from django.contrib.auth import get_user_model
from django.core.management import call_command
from .forms import SuperuserCreationForm


User = get_user_model()


def check_first_superuser(is_ignore_exception=False):
    def wrapper(view_fn):
        def inner(request, *args, **kwargs):
            try:
                request.first_superuser = User.objects.filter(is_superuser=True).first()
            except OperationalError as e:
                if is_ignore_exception:
                    request.first_superuser = None
                else:
                    if 'no such table' in str(e):
                        return redirect('migrate')
                    raise

            return view_fn(request, *args, **kwargs)
        return inner
    return wrapper


@check_first_superuser(is_ignore_exception=True)
def migrate(request):
    if request.first_superuser and not request.user.is_superuser:
        messages.info(request, '이미 Superuser를 생성하셨습니다.')
        return redirect(resolve_url('admin:login') + '?next=' + request.path)

    if request.method == 'POST':
        result_io = StringIO()
        call_command('migrate', stdout=result_io)
        result = re.sub(r'\x1b\[[\d;]+m', '', result_io.getvalue())
    else:
        result = None

    return render(request, 'pacemaker/migrate.html', {
        'result': result,
        'DJANGO_SETTINGS_MODULE': os.environ['DJANGO_SETTINGS_MODULE'],
    })


@check_first_superuser()
def createsuperuser(request):
    if request.first_superuser is None:
        if request.method == 'POST':
            form = SuperuserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Superuser를 생성했습니다.')
                return redirect('admin:login')
        else:
            form = SuperuserCreationForm()
    else:
        form = None

    return render(request, 'pacemaker/createsuperuser.html', {
        'first_superuser': request.first_superuser,
        'form': form,
        'DJANGO_SETTINGS_MODULE': os.environ['DJANGO_SETTINGS_MODULE'],
    })

