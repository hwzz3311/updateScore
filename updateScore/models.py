from django.db import models

# Create your models here.
class Score(models.Model):
	clientNum = models.TextField(max_length=100,verbose_name="客户端号")
	score = models.IntegerField(verbose_name='得分')

	class Meta:
		ordering = ('score',)