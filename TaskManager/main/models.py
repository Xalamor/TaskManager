from django.db import models
from django.contrib.auth.models import User


def get_default_user():
    return User.objects.first().id
class Task(models.Model):
    title = models.CharField('Название', max_length=50)
    task = models.TextField('Описание')
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=get_default_user)

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'