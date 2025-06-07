from django.db import models
from django.contrib.auth.models import User

from froala_editor.fields import FroalaField

# Create your models here.
class Option(models.Model):
	name = models.CharField(max_length=50)
	values = models.JSONField(blank=True, default=dict)

class Disease(models.Model):
	name = models.CharField(max_length=50)
	comment = models.TextField(blank=True, default='')
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	author = models.ForeignKey(User, on_delete=models.CASCADE)

class Diagnose(models.Model):
	pass
	

class Hospitalization(models.Model):
	enter_time = models.DateField(blank=True, null=True)

class Patient(models.Model):
	GENDERS = {
		1: '男',
		2: '女',
		0: '未知',
	}

	ETHNIC_GROUPS = {
		1: '汉族',
		2: '蒙古族',
		3: '回族',
		4: '藏族',
		5: '维吾尔族',
		6: '苗族',
		7: '彝族',
		8: '壮族',
		9: '布依族',
		10: '朝鲜族',
		11: '满族',
		12: '侗族',
		13: '瑶族',
		14: '白族',
		15: '土家族',
		16: '哈尼族',
		17: '哈萨克族',
		18: '傣族',
		19: '黎族',
		20: '傈僳族',
		21: '佤族',
		22: '畲族',
		23: '高山族',
		24: '拉祜族',
		25: '水族',
		26: '东乡族',
		27: '纳西族',
		28: '景颇族',
		29: '柯尔克孜族',
		30: '土族',
		31: '达斡尔族',
		32: '仫佬族',
		33: '羌族',
		34: '布朗族',
		35: '撒拉族',
		36: '毛南族',
		37: '仡佬族',
		38: '锡伯族',
		39: '阿昌族',
		40: '普米族',
		41: '塔吉克族',
		42: '怒族',
		43: '乌孜别克族',
		44: '俄罗斯族',
		45: '鄂温克族',
		46: '德昂族',
		47: '保安族',
		48: '裕固族',
		49: '京族',
		50: '塔塔尔族',
		51: '独龙族',
		52: '鄂伦春族',
		53: '赫哲族',
		54: '门巴族',
		55: '珞巴族',
		56: '基诺族',
		0: '其他',
	}

	name = models.CharField(max_length=30)
	number = models.CharField(max_length=15, blank=True, default='', help_text="register number")
	gender = models.PositiveSmallIntegerField(choices=GENDERS, default=0)
	ethnicity = models.PositiveSmallIntegerField(choices=ETHNIC_GROUPS, default=1)
	age = models.FloatField(blank=True, null=True)
	weight = models.FloatField(blank=True, null=True, help_text='kg')
	height = models.PositiveSmallIntegerField(blank=True, null=True, help_text='cm')
	phone = models.CharField(max_length=20, blank=True, default='')
	address = models.CharField(max_length=255, blank=True, default='')
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	author = models.ForeignKey(User, on_delete=models.CASCADE)

class Dataset(models.Model):
	DATASET_TYPES = {
		1: 'WES',
		2: 'WGS',
		0: '其他',
	}

	PLATFORMS = {
		1: 'ILLUMINA',
		2: 'DNBSEQ',
		3: 'PACBIO',
		4: 'ONT',
		5: 'CAPILLARY',
		6: 'ELEMENT',
		7: 'HELICOS',
		8: 'IONTORRENT',
		9: 'LS454',
		10: 'SINGULAR',
		11: 'SOLID',
		12: 'ULTIMA',
		0: 'UNKNOWN'
	}

	name = models.CharField(max_length=100)
	code = models.CharField(max_length=50, blank=True, default='')
	tissue = models.CharField(max_length=30, blank=True, default='')
	first = models.CharField(max_length=200, help_text="file one")
	second = models.CharField(max_length=200, blank=True, default='', help_text="file two")
	type = models.PositiveSmallIntegerField(choices=DATASET_TYPES, default=0)
	platform = models.PositiveSmallIntegerField(choices=PLATFORMS, default=0)
	comment = models.TextField(blank=True, default='')
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	patient = models.ForeignKey(Patient, on_delete=models.CASCADE, blank=True, null=True)
	author = models.ForeignKey(User, on_delete=models.CASCADE)

	class Meta:
		ordering = ['-created']

class DicomMedia(models.Model):
	filename = models.CharField(max_length=255)
	fileuuid = models.CharField(max_length=50)
	patient = models.CharField(max_length=50, blank=True, default='')
	series = models.CharField(max_length=50, blank=True, default='')
	study = models.CharField(max_length=50, blank=True, default='')
	created = models.DateTimeField(auto_now_add=True)
	author = models.ForeignKey(User, on_delete=models.CASCADE)

class CardiomyopathyDisease(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
	author = models.ForeignKey(User, on_delete=models.CASCADE)

	class Meta:
		ordering = ['-created']

class KawasakiDisease(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
	author = models.ForeignKey(User, on_delete=models.CASCADE)

	class Meta:
		ordering = ['-created']

class CongenitalHeartDisease(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
	author = models.ForeignKey(User, on_delete=models.CASCADE)

	class Meta:
		ordering = ['-created']

class RadiofrequencyAblation(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
	author = models.ForeignKey(User, on_delete=models.CASCADE)

	class Meta:
		ordering = ['-created']

class Job(models.Model):
	FAILURE = 0
	SUCCESS = 1
	RUNNING = 2
	WAITING = 3
	STOPPED = 4

	STATUS_CHOICES = {
		FAILURE: 'FAILURE',
		SUCCESS: 'SUCCESS',
		RUNNING: 'RUNNING',
		WAITING: 'WAITING',
		STOPPED: 'STOPPED'
	}

	COMMAND_CHOICES = {
		1: '全外显子组分析',
		0: '模拟任务测试',
	}

	short_id = models.CharField(max_length=10, blank=True, default='')
	long_id = models.CharField(max_length=40, blank=True, default='')
	name = models.CharField(max_length=200, blank=True, default='')
	command = models.PositiveSmallIntegerField(choices=COMMAND_CHOICES, default=0)
	status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=3)
	progress = models.PositiveSmallIntegerField(default=0)
	step = models.PositiveSmallIntegerField(default=0)
	message = models.TextField(blank=True, default='')
	created = models.DateTimeField(auto_now_add=True)
	started = models.DateTimeField(blank=True, null=True)
	stopped = models.DateTimeField(blank=True, null=True)
	dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)
	author = models.ForeignKey(User, on_delete=models.CASCADE)

	class Meta:
		ordering = ['-created']


