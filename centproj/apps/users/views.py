from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from apps.users.forms import LoginForm, DynamicLoginForm, DynamicLoginPostForm, QrLoginPostForm, VoiceLoginPostForm
from apps.extras.twilioOTP import send_single_sms
from centproj.settings import twilio_account_id, twilo_auth_token, from_twilio_mobile, REDIS_HOST, REDIS_PORT
from apps.extras.random_str import generate_random
import redis
from apps.users.models import UserProfile
import qrcode


class LogoutView(View):
  def get(self,request, *args, **kwargs):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

class SendSmsView(View):
  def post(self, request, *args, **kwargs):
    send_sms_form = DynamicLoginForm(request.POST)
    re_dict = {}
    if send_sms_form.is_valid():
      mobile = "+1" + send_sms_form.cleaned_data["mobile"]
      code = generate_random(4, 0)
      re_json = send_single_sms(twilio_account_id, twilo_auth_token, from_twilio_mobile, code, to_mobile=mobile)
      if re_json:
        re_dict["status"] = "success"
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, charset="utf8", decode_responses=True)
        r.set(str(mobile), code)
        r.expire(str(mobile), 60*30) # 30 mins expired
      else:
        re_dict["msg"] = "error"
    else:
      for key, value in send_sms_form.errors.items():
        re_dict[key] = value[0]
      
    return JsonResponse(re_dict)

class LoginView(View):
  def get(self, request, *args, **kwargs):
    if request.user.is_authenticated:
      return HttpResponseRedirect(reverse("index"))

    login_form = DynamicLoginForm()
    return render(request, "login.html", {
      "login_form": login_form
    })

  def post(self, request, *args, **kwargs):
    login_form = LoginForm(request.POST)

    if login_form.is_valid():
      user_name = login_form.cleaned_data["username"]
      password = login_form.cleaned_data["password"]
      user = authenticate(username=user_name, password=password)

      if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("index"))  # make sure the url changes after redirect
      else:
        return render(request, "login.html", {"msg": "email or password incorrect", "login_form":login_form})
    else:
      return render(request, "login.html", {"login_form": login_form})

class DynamicLoginView(View):
  def post(self, request, *args, **kwargs):
    login_form = DynamicLoginPostForm(request.POST)
    if login_form.is_valid():
      mobile = login_form.cleaned_data["mobile"]
      existed_users = UserProfile.objects.filter(mobile=mobile)
      if existed_users:
        user = existed_users[0]
      else:
        # make new user
        user = UserProfile(username=mobile)
        password = generate_random(10,2) # generate password 
        user.set_password(password)
        user.mobile = mobile
        user.save()
      login(request, user)
      return HttpResponseRedirect(reverse("index"))
    else:
      return render(request, "login.html", {"login_form": login_form})

class QrLoginView(View):
  def post(self, request, *args, **kwargs):
    login_form = QrLoginPostForm(request.POST)
    
    if login_form.is_valid():

      user_name = login_form.cleaned_data["username"]
      password = login_form.cleaned_data["password"]
      user = authenticate(username=user_name, password=password)

      code = login_form.cleaned_data["code"]
      r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, charset="utf8", decode_responses=True)
      match_code = r.get(str(user_name))

      if code == match_code:
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
      else:
        return render(request, "login.html", {"QRlogin_form": login_form})
    else:
      return render(request, "login.html", {"QRlogin_form": login_form})

class CreateQRcodeView(View):
  def post(self, request, *args, **kwargs):
    re_dict = {}
    login_form = LoginForm(request.POST)

    if login_form.is_valid():
      user_name = login_form.cleaned_data["username"]
      password = login_form.cleaned_data["password"]

      user = authenticate(username=user_name, password=password)

      if user is not None:
        re_dict["status"] = "success"
        # create code
        code = generate_random(4, 0)
        re_dict["status"] = "success"
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, charset="utf8", decode_responses=True)
        r.set(str(user_name), code)
        r.expire(str(user_name), 60*30) # 30 mins expired

        #create qrcode image
        qrCodeIma = qrcode.make(str(code))
        qrCodeImaPath = "static/qrimages/" + user_name + ".jpg"
        qrCodeIma.save(qrCodeImaPath)

      else:
        re_dict["status"] = "error"
      return JsonResponse(re_dict)

class VoiceLoginView(View):
  def post(self, request, *args, **kwargs):
    login_form = VoiceLoginPostForm(request.POST)
    if login_form.is_valid():
      user_name = login_form.cleaned_data["username"]
      password = login_form.cleaned_data["password"]

      user = authenticate(username=user_name, password=password)
      user_secrect = user.voice_secrect

      input_user_secrect = login_form.cleaned_data["secrect"]

      if input_user_secrect.lower() == user_secrect:
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
      else:
        return render(request, "login.html", {"voice_login_form": login_form})
    else:
      return render(request, "login.html", {"voice_login_form": login_form})

