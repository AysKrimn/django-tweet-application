from django.db import models
from django.contrib.auth.models import AbstractUser
from tweetAPI.models import TweetLikes

class TweetUser(AbstractUser):

    iliski_durumu_secenekler = (

        ("1", "Evli"),
        ("2", "Bekar"),
        ("3", "Dul"),
        ("4", "İlişkisi Var"),
        ("5","İlişkisi Yok"),
        ("6", "Karışık"),
        ("7", "Belirtmek İstemiyorum")
    )
    
    avatar = models.FileField(("Avatar"), upload_to="Profile_Avatar", default="Profile_Avatar/defaultAvatar.png", max_length=100, blank=True, null=True)
    birthday = models.DateTimeField(("Doğum Tarihi"), auto_now=False, auto_now_add=False, blank=True, null=True)
    location = models.CharField(("Yaşadığı Yer"), max_length=50, blank=True, null=True)
    relation = models.CharField(("İlişki Durumu"), max_length=50, choices=iliski_durumu_secenekler, null=True, blank=True)
    followers = models.ManyToManyField("tweetApp.UserFollowers", verbose_name=("Takipçiler"))


# takipci
class UserFollowers(models.Model):

        user = models.ForeignKey(TweetUser, verbose_name=("Takipçi"), on_delete=models.CASCADE)

        def __str__(self):
            return self.user.username
        

# tweet model
class TweetModel(models.Model):

    # id
    author = models.ForeignKey(TweetUser, verbose_name=("Tweet Yazarı"), on_delete=models.CASCADE)
    tweet = models.TextField(("Tweet"))
    tweetLikes = models.ForeignKey("tweetAPI.TweetLikes", verbose_name=("Beğeniler"), on_delete=models.CASCADE, null=True)
    attachment = models.FileField(("Ek"), upload_to="Tweet_Uploads", max_length=100, blank=True)   # """blank = True = Opsiyonel"""
    createdAt = models.DateTimeField(("Tarih"), auto_now=True, auto_now_add=False)
    updatedAt = models.DateTimeField(("Güncellenme Tarih"), auto_now=False, auto_now_add=True)
    # comments = [yorum 1, yorum 2]


    def __str__(self) -> str:
        return f"Yazar: {self.author.username} Post: {self.tweet}"
    

    def show_likes(self):
        return TweetLikes.objects.filter(post_id = self.id).count()
    
# yorum şeması
class TweetCommentModel(models.Model):
     
     author = models.ForeignKey(TweetUser, verbose_name=("Yorum Yapan"), on_delete=models.CASCADE)
     post = models.ForeignKey(TweetModel, related_name="comments", verbose_name=("Tweet"), on_delete=models.CASCADE)
     message = models.TextField(("Yorum"))
     createdAt = models.DateTimeField(("Tarih"), auto_now=True, auto_now_add=False)
     updatedAt = models.DateTimeField(("Güncellenme Tarih"), auto_now=False, auto_now_add=True)

     def __str__(self) -> str:
        return self.message