from django.db import models

from accounts.models import User, UserProfile
from accounts.utils import send_notification

class Restaurant(models.Model):
    user=models.OneToOneField(User,related_name='user',on_delete=models.CASCADE)
    user_profile=models.OneToOneField(UserProfile,related_name='userprofile',on_delete=models.CASCADE)
    restaurant_name=models.CharField(max_length=50)
    restaurant_license=models.ImageField(upload_to='restaurant/license')
    is_approved=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    modified_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.restaurant_name 
    
    def save(self,*args,**kwargs):
        if self.pk is not None: #Update not create 
            orig=Restaurant.objects.get(pk=self.pk)
            if orig.is_approved!=self.is_approved:
                if self.is_approved==True:
                    mail_subject="Restaurent approval success"
                    mail_template='accounts/emails/admin_approval_email.html'
                    context={
                        'user':self.user,
                    }
                    send_notification(mail_subject,mail_template,context)
            
        return super(Restaurant,self).save(*args,**kwargs)