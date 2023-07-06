from datetime import date, datetime, time
from django.db import models

from accounts.models import User, UserProfile
from accounts.utils import send_notification

class Restaurant(models.Model):
    user=models.OneToOneField(User,related_name='user',on_delete=models.CASCADE)
    user_profile=models.OneToOneField(UserProfile,related_name='userprofile',on_delete=models.CASCADE)
    restaurant_name=models.CharField(max_length=50)
    restaurant_slug=models.SlugField(max_length=100,unique=True)
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
    
    def is_open(self):
        today_date=date.today()
        today=today_date.isoweekday()  #monday->1...  
        today_opening_hours=OpeningHour.objects.filter(restaurant=self,day=today)

        now=datetime.now()
        current_time=now.strftime("%H:%M:%S")

        is_open=False
        
        for hour in today_opening_hours:
            try:
                start_time=str(datetime.strptime(hour.from_hour,'%I:%M %p').time()) 
                end_time=str(datetime.strptime(hour.to_hour,'%I:%M %p').time())

                if current_time>start_time and current_time<end_time:
                    is_open=True
                    break
            except:
                is_open=False
                break
        
        return is_open
    



DAYS=[(1,("Monday")),
      (2,("Tuesday")),
      (3,("Wednesday")),
      (4,("Thursday")),
      (5,("Friday")),
      (6,("Saturday")),
      (7,("Sunday")),
      ]

HOURS_OF_DAY=[(time(h,m).strftime('%I:%M %p'),time(h,m).strftime('%I:%M %p')) for h in range (0,24) for m in (0,30)]

class OpeningHour(models.Model):
    restaurant=models.ForeignKey(Restaurant,on_delete=models.CASCADE)
    day=models.IntegerField(choices=DAYS)
    from_hour=models.CharField(choices=HOURS_OF_DAY,max_length=10,blank=True)
    to_hour=models.CharField(choices=HOURS_OF_DAY,max_length=10,blank=True)
    is_closed=models.BooleanField(default=False)

    class Meta:
        ordering= ('day','-from_hour')
        unique_together= ('restaurant','day','from_hour','to_hour')  

    

    def __str__(self):
        return self.get_day_display()
    
    
       