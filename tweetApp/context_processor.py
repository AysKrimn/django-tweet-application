from datetime import datetime, timedelta
from .models import TweetUser as User, TweetModel


def get_current_recent_users(request):

    now = datetime.now()
    # 24 saat öncesini hesapla
    start_time = now - timedelta(days=1)
    
    new_users = User.objects.filter(date_joined__gte=start_time, date_joined__lt=now)

    return {"recent_users": new_users}


def get_total_user_tweets(request):

        if request.user.is_authenticated is False:      
              return
        
        tweets = TweetModel.objects.all()
        return {"user_tweets_count": tweets.filter(author = request.user).count()}
