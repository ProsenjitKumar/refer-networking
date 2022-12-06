from django.shortcuts import render, redirect
from .models import Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User

# Create your views here.


def signup_view(request):
    profile_id = request.session.get('ref_profile')
    print('profile_id', profile_id)
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        if profile_id is not None:
            recommended_by_profile = Profile.objects.get(id=profile_id)

            instance = form.save()
            registered_user = User.objects.get(id=instance.id)
            registered_profile = Profile.objects.get(user=registered_user)
            registered_profile.recommended_by = recommended_by_profile.user
            registered_profile.save()
        else:
            form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('main_view')
    context = {
        'form': form
    }
    return render(request, 'index/signup.html', context)


def main_view(request, *args, **kwargs):
    code = str(kwargs.get('ref_code'))
    try:
        profile = Profile.objects.get(code=code)
        request.session['ref_profile'] = profile.id
        print('id', profile.id)
    except:
        pass
    print(request.session.get_expiry_date())
    return render(request, 'index/index.html')


def my_recommendations_view(request):
    total_network = Profile.objects.all()
    print('------------Total Parents **************')
    all_parents = []
    for parent in total_network:
        if parent.recommended_by is None:
            print(all_parents.append(parent))
            print(parent)
    print(all_parents)
    print('------------Total Network* *************')
    print(total_network)
    # all_parent_profile = Profile.objects.get(user=user)
    profile = Profile.objects.get(user=request.user)
    print("--------------Current Profile--------------")
    print(profile)
    my_recs =  profile.get_recommended_profiles()
    context = {
        'my_recs': my_recs
    }
    print('---------------ALl Recommendations------------------')
    print(context)
    return render(request, 'index/recommendations.html', context)


def newprofile(request):
    return render(request, 'profile/index.html')


