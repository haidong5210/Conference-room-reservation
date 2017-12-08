from django.db import models

# Create your models here.


class User(models.Model):
    name = models.CharField(max_length=32,verbose_name="用户名")
    password = models.CharField(max_length=32,verbose_name="密码")

    def __str__(self):
        return self.name


class Boardroom(models.Model):
    title = models.CharField(max_length=32,verbose_name="会议室名")

    def __str__(self):
        return self.title


class Boardroom2Time2user(models.Model):
    meetTime = (
        (1,'8:00'),
        (2,'9:00'),
        (3,'10:00'),
        (4,'11:00'),
        (5,'12:00'),
        (6,'14:00'),
        (7,'15:00'),
        (8,'16:00'),
        (9,'17:00'),
        (10,'18:00'),
        (11,'19:00'),
    )
    meet_time=models.IntegerField(choices=meetTime,verbose_name="会议当天时间")
    time = models.DateField(verbose_name="会议日期")
    boardroom = models.ForeignKey(to="Boardroom",verbose_name="会议室")
    user = models.ForeignKey(to="User")

    def __str__(self):
        return self.time