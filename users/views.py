from django.contrib.auth.models import User
from django.contrib.auth import login
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate
from rest_framework import parsers
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import renderers
from users.serializers import AuthCustomTokenSerializer
from .forms import LoginForm


def web_authenticate(username=None, password=None):
        try:
            user = User.objects.get(email__iexact=username)
            if user.check_password(password):
                return authenticate(username=user.username, password=password)
        except User.DoesNotExist:
            return None


def web_login(request):
    if request.user.is_authenticated():
        return redirect('/dashboard/')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            pwd = form.cleaned_data['password']
            user = web_authenticate(username=email, password=pwd)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('kobocat'))
                else:
                    return render(request, 'registration/login.html', {'form':form, 'inactive':True})
            else:
                return render(request, 'registration/login.html', {'form':form, 'form_errors':True})
        else:
            return render(request, 'registration/login.html', {'form': form})
    else:
        form = LoginForm()

    return render(request, 'registration/login.html', {'form': form})

# @group_required("admin")


def auth_token(request):
    pass


class ObtainAuthToken(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (
        parsers.FormParser,
        parsers.MultiPartParser,
        parsers.JSONParser,
    )

    renderer_classes = (renderers.JSONRenderer,)

    def post(self, request):
        serializer = AuthCustomTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        content = {
            'token': unicode(token.key),
        }

        return Response(content)


# def profile_update(request):
#     if request.method == 'POST':
#         form = ProfileForm(request.POST)
#         if form.is_valid():
#             up = form.save(commit=False)
#             user = request.user
#             try:
#                 user_profile = user.profile
#                 user_profile.skype = up.skype
#                 user_profile.address = up.address
#                 user_profile.phone = up.phone
#                 user_profile.gender = up.gender
#                 user_profile.save()
#             except:
#                 up.user = user
#                 up.save()
#             messages.info(request, "Profile Updated")
#             return render(request, 'users/profile_update.html', {'form': form})
#         return render(request, 'users/profile_update.html', {'form': form})
#     else:
#         try:
#             instance = UserProfile.objects.get(user_id=request.user.id)
#             form = ProfileForm(instance=instance)
#         except:
#             form = ProfileForm()
#     return render(request, 'users/profile_update.html', {'form': form})
