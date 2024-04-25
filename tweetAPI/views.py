from django.shortcuts import render
from .models import TweetLikes

# JSON kütüphanesi
from django.http import JsonResponse

from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required(login_url="login-view")
def Begen(request, tweetId):
    
    message = {}

    try:
        # bu user bu postu daha önce beğenmiş mi?
        isLiked = TweetLikes.objects.filter(post_id = int(tweetId), user=request.user).first()

        # kişi bu postu zaten beğenmişse o zaman like kaldır.
        if isLiked:
            
            isLiked.delete()

            message["api_message"] = {

                "status": "Unlike Yapıldı",
                "total_likes": TweetLikes.objects.filter(post_id=tweetId).count()
            }

        else:
            
            # like oluştur
            tweet = TweetLikes.objects.create(post_id = int(tweetId), user = request.user)
            message["api_message"] = {

                "status": "Like Eklendi",
                "total_likes": TweetLikes.objects.filter(post_id=tweetId).count()
            }


    except Exception as e:
        
        print("apı da hata:", e)

        message["api_message"] = {

            "status": "Bir hata meydana geldi lütfen daha sonra tekrar dene",
        }


    # JSON mesaj dön
    return JsonResponse(message)