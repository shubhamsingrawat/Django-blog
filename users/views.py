from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .form import UserRegisterForm,ProfileUpdatedForm,UserUpdatedForm

def register(request):
    if request.method=='POST':
        form=UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data.get('username')
            messages.success(request, f'You can now login {username}')
            return redirect('login')
    else:
        form=UserRegisterForm()
    return render(request,'users/register.html',{'form':form})

@login_required
def profile(request):
    if request.method=='POST':
        u_form = UserUpdatedForm(request.POST,instance=request.user)
        p_form = ProfileUpdatedForm(request.POST,
                                    request.FILES,
                                    instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('profile')
    else:
        u_form = UserUpdatedForm(instance=request.user)
        p_form = ProfileUpdatedForm(instance=request.user.profile)
        context={
            'u_form':u_form,
            'p_form':p_form
        }
        return render(request,'users/profile.html',context)
