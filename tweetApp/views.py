from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
# Tweet Modelini Çek
from .models import *
from .models import TweetUser as User

# formu çek
from .form import UserProfile

# utils
from datetime import datetime, timedelta
# Create your views here.
def Anasayfa(request):
    context = {}
    tweetInstances = {}

    tweets = TweetModel.objects.all().order_by("-createdAt")
    
    for tweet in tweets:

        tweetInstances[tweet.id] = tweet
        # 1: { name: ömer, post: dünya, likes: 12},
        # 2: {name: muhammed, post: csgo, likes 15}
    else:
        context["tweets"] = tweetInstances
        
        if request.user.is_authenticated:
            context["form"] = UserProfile(instance=request.user)

    # Şu anki zamanı al
    now = datetime.now()

    # 24 saat öncesini hesapla
    start_time = now - timedelta(days=1)
    
    new_users = User.objects.filter(date_joined__gte=start_time, date_joined__lt=now)
    context["recent_users"] = new_users


    if request.method == 'POST':
        
           tweetContent = request.POST.get('tweetContent')
           tweetAttachment = request.POST.get('tweetAttachment')

           if tweetContent:
               TweetModel.objects.create(author=request.user, tweet=tweetContent)
           elif tweetContent and tweetAttachment:
               TweetModel.objects.create(author=request.user, tweet=tweetContent, attachment=tweetAttachment)
           else:
               # bir şeyler ters gitmiştir
               context['error'] = "Birşeyler ters gitti lütfen daha sonra tekrar dene."
               return render(request, "index.html", context)
           

           return redirect('index-view')
               
    else:
        return render(request, "index.html", context)

# anasayfaya post isteği gelirse
def AnaSayfa_POST(request):

    if request.method == 'POST':

        form = UserProfile(request.POST, instance=request.user)

        if form.is_valid():

            form.save()

        # şifreleri değiştir
        oldPassword = request.POST.get('old_password')
        newPassword = request.POST.get('new_password')

        if oldPassword and newPassword:

            # şu an ki şifre eski şifre ile uyuşuyor mu?
            match_old_password = request.user.check_password(oldPassword)

            if match_old_password is False:
                print("[USER EDIT ENPOINT]: Şifreler uyuşmuyor")
                return redirect("index-view")

            # yeni şifreyi belirle
            request.user.set_password(newPassword)
            # user modelini kaydet
            request.user.save()
            print("[USER EDIT ENPOINT]: Şifre değişti")
            return redirect("index-view")

# tweeet güncelleme
def TweetGuncelle(request, tweetId):

    # kullanıcı giriş yapmamışsa engelle
    if request.user.is_authenticated == False:

        return redirect("login-view")
    
    if request.method == 'POST':
        # tweeti bul
        tweet = TweetModel.objects.filter(id = tweetId).first()

        if tweet is None:
            return redirect('index-view')
        
        
        # yetki kontrol
        if request.user.is_superuser == False or request.user.id != tweet.author.id:

            return redirect("index-view")
        
        newTweet = request.POST.get('newContent')
        tweet.tweet = newTweet
        tweet.save()

        return redirect("index-view")
        
    else:
        # get istekleri icin hep anasayfaya yonlendşir
        return redirect('index-view')



def TweetSil(request, tweetId):
        
        if request.user.is_authenticated == False:

            return redirect('login-view')
        
    
        tweet = TweetModel.objects.filter(id = tweetId).first()

        if tweet is None:
            return redirect('index-view')
        

        # yetki kontrol
        if request.user.is_superuser == False or request.user.id != tweet.author.id:

            return redirect("index-view")
        
        
        tweet.delete()

        return redirect("index-view")


def GirisYap(request):
    context = {}

    if request.user.is_authenticated:

        return redirect('index-view')
    

    if request.method == 'POST':
        
        usernameInput = request.POST.get('username')
        passwordInput = request.POST.get('password')

        # böyle bir user var mi?
        user = authenticate(request, username = usernameInput, password = passwordInput)

        if user is None:
            # böyle bi usee yok
            context["error"] = "Girdiğiniz bilgiler Geçersiz Lütfen Tekrar Deneyin."
            return render(request, "login.html", context)
        else:
            login(request, user)
            return redirect('index-view')

    else:
        return render(request, "login.html")
    

def CikisYap(request):

        logout(request)
        return redirect('index-view')



def KayitOl(request):
     
     context = {}

     if request.method == 'POST':
          
          usernameInput = request.POST.get('username')
          passwordInput = request.POST.get('password')
          password2Input = request.POST.get('password2')

          if usernameInput and passwordInput and password2Input:
              
            # bu ada sahip başka bir user var mı?
            buAdaSahipHesaplar = User.objects.filter(username = usernameInput)

            if buAdaSahipHesaplar.__len__():
                context['hata'] = "Bu hesap adı alınmış lütfen başka bir ad deneyiniz."
                return render(request, 'register.html', context)
            # şifreler aynı mı?
            if passwordInput == password2Input:
                # hesabı oluştur
                User.objects.create_user(username=usernameInput, password=password2Input)
                return redirect('login-view')
            else:
                # şifreler aynı değil
                context['hata'] = "Şifreler Uyuşmuyor"
                return render(request, 'register.html', context)
          else:
               context['hata'] = "Lütfen gerekli olan tüm alanları doldurunuz"
               return render(request, 'register.html', context)


     else:
        return render(request, "register.html")
     


def ProfilDetay(request, userId):
    context = {}
    tweetInstances = {}
    # Şu anki zamanı al
    now = datetime.now()

    # 24 saat öncesini hesapla
    start_time = now - timedelta(days=1)
    
    new_users = User.objects.filter(date_joined__gte=start_time, date_joined__lt=now)
    context["recent_users"] = new_users

    requestedUser = User.objects.filter(id = int(userId)).first()
    context["user"] = requestedUser

    # ilgili userin göndermiş oldugu tweetler
    usersTweets = TweetModel.objects.filter(author = requestedUser)

    for tweet in usersTweets:
        tweetInstances[tweet.id] = tweet

    context['tweets'] = tweetInstances
    
    return render(request, "profile.html", context)