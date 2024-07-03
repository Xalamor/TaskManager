from django.db import models
from django.contrib.auth.models import User


class Chapter(models.Model):
    name = models.CharField('Наименование раздела', max_length=50)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Раздел'
        verbose_name_plural = 'Разделы'


def get_default_user():
    return User.objects.first().id


class Task(models.Model):
    title = models.CharField('Название', max_length=50)
    task = models.TextField('Описание')
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=get_default_user)
    user_can_read = models.ManyToManyField(User, related_name='tasks_can_read', blank=True)
    visibility = models.CharField(max_length=20, choices=[
        ('only_me', 'Только я'),
        ('everyone', 'Все'),
        ('selected', 'Выбранные пользователи')
    ], default='only_me')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
