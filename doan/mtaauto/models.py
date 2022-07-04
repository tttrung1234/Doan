from django.db import models


class contactForm(models.Model):
    username = models.CharField(max_length=25)
    email = models.EmailField()
    body = models.TextField()

    def __str__(self):
        return self.email


class nick(models.Model):
    uid = models.CharField(max_length=50, primary_key=True)
    action = models.BooleanField(default=False)
    live = models.BooleanField(default=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    def __str__(self):
        return self.uid


class AccountFl(models.Model):
    AcLink = models.CharField(max_length=100, primary_key=True)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.AcLink


class Post(models.Model):
    PostLink = models.CharField(max_length=50)
    accountFl = models.ForeignKey(
        "AccountFl", null=True, blank=True, on_delete=models.SET_NULL)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.PostLink


class Details(models.Model):

    post = models.ForeignKey(
        "Post", null=True, blank=True, on_delete=models.SET_NULL)
    content = models.TextField(blank=True, null=True)
    rate = models.CharField(max_length=50, blank=True, null=True)
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return "%s %s" % (str(self.post), str(self.created))


class UserInteractive(models.Model):
    idUserI = models.CharField(max_length=100)
    details = models.ForeignKey(
        "Details", null=True, blank=True, on_delete=models.SET_NULL)
    like = models.IntegerField(default=0)
    # 0 : không; 1: like; 2: haha; 3: sad; 4:tim; 5:wow; 6:thuongthuong; 7:angry
    comment = models.TextField(null=True, blank=True)
    share = models.BooleanField(default=False)
    rate = models.CharField(max_length=100, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.idUserI
