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
    
    avatar = models.FileField(("Avatar"), upload_to=None, max_length=100, blank=True, null=True)
    birthday = models.DateTimeField(("Doğum Tarihi"), auto_now=False, auto_now_add=False, blank=True, null=True)
    location = models.CharField(("Yaşadığı Yer"), max_length=50, blank=True, null=True)
    relation = models.CharField(("İlişki Durumu"), max_length=50, choices=iliski_durumu_secenekler, null=True, blank=True)





# tweet model
class TweetModel(models.Model):

    # id
    author = models.ForeignKey(TweetUser, verbose_name=("Tweet Yazarı"), on_delete=models.CASCADE)
    tweet = models.TextField(("Tweet"))
    tweetLikes = models.ForeignKey("tweetAPI.TweetLikes", verbose_name=("Beğeniler"), on_delete=models.CASCADE, null=True)
    attachment = models.FileField(("Ek"), upload_to=None, max_length=100, blank=True)   # """blank = True = Opsiyonel"""
    createdAt = models.DateTimeField(("Tarih"), auto_now=True, auto_now_add=False)
    updatedAt = models.DateTimeField(("Güncellenme Tarih"), auto_now=False, auto_now_add=True)


    def __str__(self) -> str:
        return f"Yazar: {self.author.username} Post: {self.tweet}"
    

    def show_likes(self):
        return TweetLikes.objects.filter(post_id = self.id).count()
    
