""" 
Основная модель BaseSites для хранения в БД информации о сайтах удобных для быстрого перехода
Указывается название и ссылка. 
Данные сайты доступны для всех пользователей в одинаковом варианнте (у пользователя нет функций
CRUD)
Реализация через admin
"""


from django.db import models


class BaseSites(models.Model):
    title = models.CharField(("title"), max_length=50)
    url_sites = models.URLField(("url_sites"), max_length=200)
    
    class Meta:
        verbose_name = 'Информация об основных сайтах'
        verbose_name_plural = 'Информация об основных сайтах'