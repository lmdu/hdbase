from django.db import models
from django.contrib.auth.models import User

from froala_editor.fields import FroalaField
from django_jsonform.models.fields import JSONField


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
	birthday = models.DateField(blank=True, null=True)
	weight = models.FloatField(blank=True, null=True, help_text='kg')
	height = models.PositiveSmallIntegerField(blank=True, null=True, help_text='cm')
	phone = models.CharField(max_length=20, blank=True, default='')
	address = models.CharField(max_length=255, blank=True, default='')
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	author = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return "{} {}".format(self.number, self.name)

	class Meta:
		ordering = ['-created']

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

class DicomImage(models.Model):
	filename = models.FileField(upload_to='dicom/%Y/%m/', max_length=200)
	fileuuid = models.CharField(max_length=50)
	patient = models.CharField(max_length=50, blank=True, default='')
	series = models.CharField(max_length=50, blank=True, default='')
	study = models.CharField(max_length=50, blank=True, default='')
	created = models.DateTimeField(auto_now_add=True)
	author = models.ForeignKey(User, on_delete=models.CASCADE)

class CardiomyopathyDisease(models.Model):
	FAMILY_HISTORIES = {
		0: "无",
		1: "有"
	}

	COMPLICATIONS = {
		0: "没有",
		1: "瓣膜病变",
		2: "冠脉狭窄/异常",
		3: "冠脉损害",
		4: "结构异常",
		5: "心肌炎后",
		6: "心肌梗死"
	}

	SURVIVALS = {
		0: "否",
		1: "是"
	}

	SPECIAL_TREATMENTS = {
		0: "无",
		1: "起搏器",
		2: "射频",
		3: "心脏移植"
	}

	SAMPLE_COLLECTS = {
		0: "否",
		1: "是"
	}

	SAMPLE_TYPES = {
		0: "无",
		1: "全血",
		2: "血细胞",
		3: "血浆",
		4: "组织"
	}

	disease_code = models.CharField(max_length=100, blank=True, default='', help_text="编号或测序编号")
	body_surface = models.FloatField(blank=True, null=True, help_text="体表面积")
	disease_type = models.CharField(max_length=100, blank=True, default='', help_text="心肌病分型")
	mutate_gene = models.CharField(max_length=20, blank=True, default='', help_text="突变基因")
	diagnose_age = models.FloatField(blank=True, null=True, help_text="初诊年龄")
	has_history = models.PositiveSmallIntegerField(choices=FAMILY_HISTORIES, default=0, help_text="有无家族史")
	family_history = models.CharField(max_length=100, blank=True, default='', help_text="家族史情况")
	complication = models.PositiveSmallIntegerField(choices=COMPLICATIONS, default=0, help_text="合并症")
	heart_failure = models.CharField(max_length=20, blank=True, default='', help_text="心衰评分")
	is_survival = models.PositiveSmallIntegerField(choices=SURVIVALS, default=1, help_text="是否存活")
	death_time = models.DateField(blank=True, null=True, help_text="死亡时间")
	arrhythmia_type = models.CharField(max_length=100, blank=True, default='', help_text="心律失常类型")
	special_treatment = models.PositiveSmallIntegerField(choices=SPECIAL_TREATMENTS, default=0, help_text="特殊治疗")
	hospital_visits = models.SmallIntegerField(default=0, help_text="心衰再入院次数")
	follow_time = models.DateField(blank=True, null=True, help_text="随访时间")
	sample_collect = models.PositiveSmallIntegerField(choices=SAMPLE_COLLECTS, default=0, help_text="是否采集标本")
	test_sample = models.PositiveSmallIntegerField(choices=SAMPLE_TYPES, default=0, help_text="已送检标本")
	remain_sample = models.PositiveSmallIntegerField(choices=SAMPLE_TYPES, default=0, help_text="剩余标本")
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	patient = models.ForeignKey(Patient, on_delete=models.CASCADE, help_text="患者")
	author = models.ForeignKey(User, on_delete=models.CASCADE)

	class Meta:
		ordering = ['-created']

class CardiomyopathyBloodRoutine(models.Model):
	POSITIVE_NEGATIVE = {
		0: "阴性",
		1: "阳性"
	}

	wbc = models.FloatField(blank=True, null=True, help_text="WBC (×10^9/L)")
	hgb = models.FloatField(blank=True, null=True, help_text="HGB (g/L)")
	hct = models.FloatField(blank=True, null=True, help_text="HCT (%)")
	mcv = models.FloatField(blank=True, null=True, help_text="MCV (fl)")
	mch = models.FloatField(blank=True, null=True, help_text="MCH (pg)")
	mchc = models.FloatField(blank=True, null=True, help_text="MCHC (g/L)")
	rdw = models.FloatField(blank=True, null=True, help_text="RDW (fl)")
	crp = models.FloatField(blank=True, null=True, help_text="CRP/hs-CRP (mg/L)")
	alt = models.FloatField(blank=True, null=True, help_text="ALT (U/L)")
	ast = models.FloatField(blank=True, null=True, help_text="AST (U/L)")
	alb = models.FloatField(blank=True, null=True, help_text="ALB (g/L)")
	cr = models.FloatField(blank=True, null=True, help_text="Cr (umol/L)")
	tc = models.FloatField(blank=True, null=True, help_text="TC (mmol/L)")
	tg = models.FloatField(blank=True, null=True, help_text="TG (mmol/L)")
	hdlc = models.FloatField(blank=True, null=True, help_text="HDL-C (mmol/L)")
	ldlc = models.FloatField(blank=True, null=True, help_text="LDL-C (mmol/L)")
	apoa = models.FloatField(blank=True, null=True, help_text="APO-A1 (g/L)")
	apob = models.FloatField(blank=True, null=True, help_text="APO-B (g/L)")
	glu = models.FloatField(blank=True, null=True, help_text="GLU (mmol/L)")
	rheumatism = models.PositiveSmallIntegerField(choices=POSITIVE_NEGATIVE, default=0, help_text="风湿筛查")
	autoantibody = models.PositiveSmallIntegerField(choices=POSITIVE_NEGATIVE, default=0, help_text="自身抗体")
	positive_result = models.CharField(max_length=200, blank=True, default='', help_text="阳性结果")
	tested = models.DateField(blank=True, null=True, help_text="检验时间")
	created = models.DateTimeField(auto_now_add=True)
	disease = models.ForeignKey(CardiomyopathyDisease, on_delete=models.CASCADE, related_name='bloods')
	author = models.ForeignKey(User, on_delete=models.CASCADE)

class CardiomyopathyMarker(models.Model):
	ckmb = models.FloatField(blank=True, null=True, help_text="CK-MB (ug/L)")
	ck = models.FloatField(blank=True, null=True, help_text="CK (ug/L)")
	ctni = models.FloatField(blank=True, null=True, help_text="cTnI (ug/L)")
	myo = models.FloatField(blank=True, null=True, help_text="MYo (ug/L)")
	ldh = models.FloatField(blank=True, null=True, help_text="LDH (U/L)")
	ast = models.FloatField(blank=True, null=True, help_text="AST (U/L)")
	bnp = models.FloatField(blank=True, null=True, help_text="BNP (pg/ml)")
	ntbnp = models.FloatField(blank=True, null=True, help_text="NT-BNP (pg/ml)")
	tested = models.DateField(blank=True, null=True, help_text="检验时间")
	created = models.DateTimeField(auto_now_add=True)
	disease = models.ForeignKey(CardiomyopathyDisease, on_delete=models.CASCADE, related_name='markers')
	author = models.ForeignKey(User, on_delete=models.CASCADE)

class CardiomyopathyTreatment(models.Model):
	drugs = JSONField(
		schema = {
			'type': 'dict',
			'anyOf': [
				{'type': 'number'},
				{'type': 'string'}
			]
		},
		help_text="治疗情况"
	)
	treated = models.DateField(blank=True, null=True, help_text="治疗时间")
	created = models.DateTimeField(auto_now_add=True)
	disease = models.ForeignKey(CardiomyopathyDisease, on_delete=models.CASCADE, related_name='treatments')
	author = models.ForeignKey(User, on_delete=models.CASCADE)

class CardiomyopathyUltrasound(models.Model):
	code = models.CharField(max_length=20, blank=True, default='', help_text="超声号")
	age = models.FloatField(blank=True, null=True, help_text="年龄")
	lvef = models.FloatField(blank=True, null=True, help_text="LVEF (%)")
	lvfs = models.FloatField(blank=True, null=True, help_text="LVFS (%)")
	la = models.FloatField(blank=True, null=True, help_text="LA (mm)")
	lv = models.FloatField(blank=True, null=True, help_text="LV (mm)")
	ra = models.FloatField(blank=True, null=True, help_text="RA (mm)")
	rv = models.FloatField(blank=True, null=True, help_text="RV (mm)")
	lvedd = models.FloatField(blank=True, null=True, help_text="LVEDD (mm)")
	lvesd = models.FloatField(blank=True, null=True, help_text="LVESD (mm)")
	diagnosis = models.TextField(blank=True, default='', help_text="超声诊断")
	report = models.FileField(upload_to='report/%Y/%m/', max_length=200, blank=True, null=True, help_text="报告")
	dicom = models.ForeignKey(DicomImage, blank=True, null=True, help_text="图像", on_delete=models.CASCADE)
	tested = models.DateField(blank=True, null=True, help_text="治疗时间")
	created = models.DateTimeField(auto_now_add=True)
	disease = models.ForeignKey(CardiomyopathyDisease, on_delete=models.CASCADE, related_name='ultrasounds')
	author = models.ForeignKey(User, on_delete=models.CASCADE)

class CardiomyopathyMRI(models.Model):
	POSITIVE_NEGATIVE = {
		0: "阴性",
		1: "阳性"
	}

	YES_NO = {
		0: "否",
		1: "是"
	}

	code = models.CharField(max_length=20, blank=True, default='', help_text="超声号")
	age = models.FloatField(blank=True, null=True, help_text="年龄")
	lvef = models.FloatField(blank=True, null=True, help_text="LVEF (%)")
	lvfs = models.FloatField(blank=True, null=True, help_text="LVFS (%)")
	la = models.FloatField(blank=True, null=True, help_text="LA (mm)")
	lv = models.FloatField(blank=True, null=True, help_text="LV (mm)")
	ra = models.FloatField(blank=True, null=True, help_text="RA (mm)")
	rv = models.FloatField(blank=True, null=True, help_text="RV (mm)")
	mass = models.CharField(max_length=10, blank=True, default='', help_text="心室肌质量")
	lge = models.PositiveSmallIntegerField(choices=POSITIVE_NEGATIVE, default=0)
	perfusion = models.CharField(max_length=50, default='', help_text="首过灌注")
	dema = models.PositiveSmallIntegerField(choices=YES_NO, default=0, help_text="心肌水肿")
	fibrosis = models.CharField(max_length=50, blank=True, default='', help_text="心肌纤维化")
	microcirculation = models.CharField(max_length=50, blank=True, default='', help_text="心肌微循环")
	report = models.FileField(upload_to='report/%Y/%m/', max_length=200, blank=True, null=True, help_text="报告")
	dicom = models.ForeignKey(DicomImage, blank=True, null=True, help_text="图像", on_delete=models.CASCADE)
	tested = models.DateField(blank=True, null=True, help_text="检验时间")
	created = models.DateTimeField(auto_now_add=True)
	disease = models.ForeignKey(CardiomyopathyDisease, on_delete=models.CASCADE, related_name='mris')
	author = models.ForeignKey(User, on_delete=models.CASCADE)

class CardiomyopathyECG(models.Model):
	YES_NO = {
		0: "否",
		1: "是"
	}

	age = models.FloatField(blank=True, null=True, help_text="年龄")
	stt = models.PositiveSmallIntegerField(choices=YES_NO, default=0, help_text="ST-T改变")
	cdzz = models.PositiveSmallIntegerField(choices=YES_NO, default=0, help_text="传导阻滞")
	xfcd = models.PositiveSmallIntegerField(choices=YES_NO, default=0, help_text="心房颤动")
	sxzb = models.PositiveSmallIntegerField(choices=YES_NO, default=0, help_text="室性早搏")
	fxzb = models.PositiveSmallIntegerField(choices=YES_NO, default=0, help_text="房性早搏")
	zsfd = models.PositiveSmallIntegerField(choices=YES_NO, default=0, help_text="左室肥大")
	zffd = models.PositiveSmallIntegerField(choices=YES_NO, default=0, help_text="左房肥大")
	ycqb = models.PositiveSmallIntegerField(choices=YES_NO, default=0, help_text="异常Q波")
	dxdgh = models.PositiveSmallIntegerField(choices=YES_NO, default=0, help_text="窦性心动过缓")
	dxdgs = models.PositiveSmallIntegerField(choices=YES_NO, default=0, help_text="窦性心动过速")
	fxdgs = models.PositiveSmallIntegerField(choices=YES_NO, default=0, help_text="房性心动过速")
	sxdgs = models.PositiveSmallIntegerField(choices=YES_NO, default=0, help_text="室性心动过速")
	tested = models.DateField(blank=True, null=True, help_text="检验时间")
	created = models.DateTimeField(auto_now_add=True)
	disease = models.ForeignKey(CardiomyopathyDisease, on_delete=models.CASCADE, related_name='ecgs')
	author = models.ForeignKey(User, on_delete=models.CASCADE)

class CardiomyopathyGeneReport(models.Model):
	company = models.CharField(max_length=100, blank=True, default='', help_text="检测公司")
	report = models.FileField(upload_to='report/%Y/%m/', blank=True, null=True, help_text="报告")
	tested = models.DateField(blank=True, null=True, help_text="检验时间")
	created = models.DateTimeField(auto_now_add=True)
	disease = models.ForeignKey(CardiomyopathyDisease, on_delete=models.CASCADE, related_name='reports')
	author = models.ForeignKey(User, on_delete=models.CASCADE)

class CardiomyopathyGeneMutation(models.Model):
	gene = models.CharField(max_length=50, blank=True, default='', help_text="基因")
	position = models.CharField(max_length=50, blank=True, default='', help_text="位置")
	mutation = models.FloatField(max_length=80, blank=True, default='', help_text="突变")
	gnomad = models.CharField(max_length=30, blank=True, default='', help_text="gnomAD MAF")
	acmg = models.CharField(max_length=30, blank=True, default='', help_text="ACMG")
	disease = models.CharField(max_length=80, blank=True, default='', help_text="疾病名称")
	gmode = models.CharField(max_length=10, blank=True, default='', help_text="遗传模式")
	zygote = models.CharField(max_length=100, blank=True, default='', help_text="合子类型")
	report = models.ForeignKey(CardiomyopathyGeneReport, on_delete=models.CASCADE, related_name='genes')
	

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


