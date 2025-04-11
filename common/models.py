from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.templatetags.static import static

# Create your models here.
class Profile(models.Model):
	ROLE_NONE = 0
	ROLE_VISITOR = 1
	ROLE_EDITOR = 2
	ROLE_ADMINITOR = 10


	USER_ROLES = {
		ROLE_NONE: "未设置",
		ROLE_VISITOR: "访客",
		ROLE_EDITOR: "编辑",
		ROLE_ADMINITOR: "管理员"
	}

	USER_TITLES = {
		0: "无",
		1: "教授",
		2: "研究员",
		3: "副教授",
		4: "副研究员",
		5: "讲师",
		6: "助理研究员",
		7: "医师",
		8: "主治医师",
		9: "副主任医师",
		10: "主任医师"
	}

	USER_DEGREES = {
		0: "无",
		1: "博士",
		2: "硕士",
		3: "学士"
	}

	USER_POSITIONS = {
		0: "无",
		1: "教职工",
		2: "博士后",
		2: "学生",
	}

	USER_STATES = {
		0: "无",
		1: "在职",
		2: "离职",
		3: "在读",
		4: "毕业",
		5: "退学",
	}

	user = models.OneToOneField(User, on_delete=models.CASCADE)
	phone = models.CharField(max_length=20, blank=True, default='')
	avatar = models.ImageField(upload_to="avatars/%Y/%m", blank=True, default='')
	major = models.CharField(max_length=100, blank=True, default='')
	resume = models.TextField(blank=True, default='')
	role = models.PositiveSmallIntegerField(choices=USER_ROLES, default=0)
	title = models.PositiveSmallIntegerField(choices=USER_TITLES, default=0)
	degree = models.PositiveSmallIntegerField(choices=USER_DEGREES, default=0)
	position = models.PositiveSmallIntegerField(choices=USER_POSITIONS, default=0)
	state = models.PositiveSmallIntegerField(choices=USER_STATES, default=0)

	class Meta:
		ordering = ['-user__date_joined']

	@property
	def get_avatar(self):
		return self.avatar.url if self.avatar else static('img/doctor.svg')

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
	instance.profile.save()
