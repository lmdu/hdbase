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

	name = models.CharField(max_length=30, help_text="名字")
	number = models.CharField(max_length=15, blank=True, default='', help_text="登记号")
	gender = models.PositiveSmallIntegerField(choices=GENDERS, default=0, help_text="性别")
	ethnicity = models.PositiveSmallIntegerField(choices=ETHNIC_GROUPS, default=1, help_text="民族")
	birthday = models.DateField(blank=True, null=True, help_text="出生日期")
	weight = models.FloatField(blank=True, null=True, help_text='休重(Kg)')
	height = models.PositiveSmallIntegerField(blank=True, null=True, help_text='身高(cm)')
	phone = models.CharField(max_length=20, blank=True, default='', help_text="电话")
	address = models.CharField(max_length=255, blank=True, default='', help_text="地址")
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
	drugs = models.JSONField(blank=True, default=dict, help_text="治疗情况")
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
	lvedd_z = models.FloatField(blank=True, null=True, help_text="Z值")
	lvesd = models.FloatField(blank=True, null=True, help_text="LVESD (mm)")
	lvesd_z = models.FloatField(blank=True, null=True, help_text="Z值")
	diagnosis = models.CharField(max_length=255, blank=True, default='', help_text="超声诊断")
	report = models.FileField(upload_to='report/%Y/%m/', max_length=200, blank=True, null=True, help_text="报告文件")
	dicom_file = models.FileField(upload_to='dicom/%Y/%m/', max_length=255, blank=True, null=True, help_text="影像文件")
	dicom_uuid = models.CharField(max_length=50, blank=True, default='')
	tested = models.DateField(blank=True, null=True, help_text="检查时间")
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
	lge = models.PositiveSmallIntegerField(choices=POSITIVE_NEGATIVE, default=0, help_text="LGE")
	perfusion = models.CharField(max_length=50, default='', help_text="首过灌注")
	dema = models.PositiveSmallIntegerField(choices=YES_NO, default=0, help_text="心肌水肿")
	fibrosis = models.CharField(max_length=50, blank=True, default='', help_text="心肌纤维化")
	microcirculation = models.CharField(max_length=50, blank=True, default='', help_text="心肌微循环")
	report = models.FileField(upload_to='report/%Y/%m/', max_length=200, blank=True, null=True, help_text="报告文件")
	dicom_file = models.FileField(upload_to='dicom/%Y/%m/', max_length=255, blank=True, null=True, help_text="影像文件")
	dicom_uuid = models.CharField(max_length=50, blank=True, default='')
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

	def __str__(self):
		return self.report.name.split('/')[-1]

class CardiomyopathyGeneMutation(models.Model):
	gene = models.CharField(max_length=50, blank=True, default='', help_text="基因")
	position = models.CharField(max_length=50, blank=True, default='', help_text="位置")
	mutation = models.CharField(max_length=80, blank=True, default='', help_text="突变信息")
	gnomad = models.CharField(max_length=30, blank=True, default='', help_text="gnomAD MAF")
	acmg = models.CharField(max_length=30, blank=True, default='', help_text="ACMG变异评级")
	disease = models.CharField(max_length=80, blank=True, default='', help_text="疾病名称")
	gmode = models.CharField(max_length=20, blank=True, default='', help_text="遗传模式")
	zygote = models.CharField(max_length=100, blank=True, default='', help_text="合子类型")
	report = models.ForeignKey(CardiomyopathyGeneReport, on_delete=models.CASCADE, related_name='genes')
	created = models.DateTimeField(auto_now_add=True)
	disease = models.ForeignKey(CardiomyopathyDisease, on_delete=models.CASCADE, related_name='reports')
	author = models.ForeignKey(User, on_delete=models.CASCADE)


class KawasakiDisease(models.Model):
	CHUANQI_TYPES = {
		0: "未知",
		1: "完全",
		1: "不完全"
	}

	YES_NO = {
		0: "否",
		1: "是",
		2: "-"
	}

	SAMPLE_TYPES = {
		0: "无",
		1: "全血",
		2: "血细胞",
		3: "血浆",
		4: "组织"
	}

	cqlx = models.PositiveSmallIntegerField(choices=CHUANQI_TYPES, default=0, help_text="川崎类型")
	cznl = models.FloatField(blank=True, null=True, help_text="初诊年龄")
	bqdk = models.PositiveSmallIntegerField(choices=YES_NO, default=0, help_text="丙球抵抗")
	gmsh = models.PositiveSmallIntegerField(choices=YES_NO, default=0, help_text="冠脉损害")
	cqxk = models.PositiveSmallIntegerField(choices=YES_NO, default=0, help_text="川崎休克")
	fr5ksszlwx = models.PositiveSmallIntegerField(choices=YES_NO, default=0, help_text="发热5天以上，抗生素治疗无效")
	jmcx = models.PositiveSmallIntegerField(choices=YES_NO, default=0, help_text="结膜充血")
	yms = models.PositiveSmallIntegerField(choices=YES_NO, default=0, help_text="杨梅舌")
	kcgb = models.PositiveSmallIntegerField(choices=YES_NO, default=0, help_text="口唇改变")
	pizhen = models.PositiveSmallIntegerField(choices=YES_NO, default=0, help_text="皮疹")
	jblbjzd = models.PositiveSmallIntegerField(choices=YES_NO, default=0, help_text="颈部淋巴结肿大")
	zdyj = models.PositiveSmallIntegerField(choices=YES_NO, default=0, help_text="肢端硬结/掌趾红斑")
	xjgs = models.PositiveSmallIntegerField(choices=YES_NO, default=0, help_text="心肌梗死")
	kjjzhz = models.PositiveSmallIntegerField(choices=YES_NO, default=0, help_text="卡介苗接种部位红肿硬结")
	fufa = models.PositiveSmallIntegerField(choices=YES_NO, default=0, help_text="复发")
	sfcjbb = models.PositiveSmallIntegerField(choices=YES_NO, default=0, help_text="是否采集标本")
	sjbb = models.PositiveSmallIntegerField(choices=SAMPLE_TYPES, default=0, help_text="已送检标本")
	sybb = models.PositiveSmallIntegerField(choices=SAMPLE_TYPES, default=0, help_text="剩余标本")
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
	author = models.ForeignKey(User, on_delete=models.CASCADE)

	class Meta:
		ordering = ['-created']

class KawasakiBlood(models.Model):
	xcg = models.CharField(max_length=80, blank=True, null=True, default='', help_text="血常规")
	frsj = models.CharField(max_length=30, blank=True, null=True, default='', help_text="距离发热xx时间")
	wbc = models.FloatField(blank=True, null=True, help_text="WBC")
	np = models.FloatField(blank=True, null=True, help_text="N%")
	lp = models.FloatField(blank=True, null=True, help_text="L%")
	monop = models.FloatField(blank=True, null=True, help_text="MONO%")
	lym = models.FloatField(blank=True, null=True, help_text="Lym")
	mono = models.FloatField(blank=True, null=True, help_text="MONO(单核细胞绝对值)")
	anc = models.FloatField(blank=True, null=True, help_text="ANC")
	rbc = models.FloatField(blank=True, null=True, help_text="RBC")
	hgb = models.FloatField(blank=True, null=True, help_text="HGB")
	plt = models.FloatField(blank=True, null=True, help_text="PLT")
	hct = models.FloatField(blank=True, null=True, help_text="HCT")
	rdwc = models.FloatField(blank=True, null=True, help_text="RDWC")
	rdwsd = models.FloatField(blank=True, null=True, help_text="RDWSD")
	pdw = models.FloatField(blank=True, null=True, help_text="PDW")
	mpv = models.FloatField(blank=True, null=True, help_text="MPV")
	plcr = models.FloatField(blank=True, null=True, help_text="PLCR")
	pctp = models.FloatField(blank=True, null=True, help_text="PCT%")
	crp = models.FloatField(blank=True, null=True, help_text="CRP")
	esr = models.FloatField(blank=True, null=True, help_text="ESR")
	jgsy = models.FloatField(blank=True, null=True, help_text="降钙素原")
	saa = models.FloatField(blank=True, null=True, help_text="SAA")
	tested = models.DateField(blank=True, null=True, help_text="检验时间")
	created = models.DateTimeField(auto_now_add=True)
	disease = models.ForeignKey(KawasakiDisease, on_delete=models.CASCADE, related_name='bloods')
	author = models.ForeignKey(User, on_delete=models.CASCADE)

class KawasakiBiochemistry(models.Model):
	alt = models.FloatField(blank=True, null=True, help_text="ALT")
	ast = models.FloatField(blank=True, null=True, help_text="AST")
	tb = models.FloatField(blank=True, null=True, help_text="TB")
	dbil = models.FloatField(blank=True, null=True, help_text="DBIL")
	idil = models.FloatField(blank=True, null=True, help_text="IDIL")
	alb = models.FloatField(blank=True, null=True, help_text="ALB")
	glb = models.FloatField(blank=True, null=True, help_text="GLB")
	rgt = models.FloatField(blank=True, null=True, help_text="γ-GT")
	ldh = models.FloatField(blank=True, null=True, help_text="LDH")
	pa = models.FloatField(blank=True, null=True, help_text="PA")
	alp = models.FloatField(blank=True, null=True, help_text="ALP")
	un = models.FloatField(blank=True, null=True, help_text="UN")
	jg = models.FloatField(blank=True, null=True, help_text="肌酐")
	cysc = models.FloatField(blank=True, null=True, help_text="CYSC")
	ua = models.FloatField(blank=True, null=True, help_text="UA")
	p = models.FloatField(blank=True, null=True, help_text="P")
	k = models.FloatField(blank=True, null=True, help_text="K+")
	na = models.FloatField(blank=True, null=True, help_text="Na+")
	cl = models.FloatField(blank=True, null=True, help_text="Cl-")
	ca = models.FloatField(blank=True, null=True, help_text="Ca2+")
	mg = models.FloatField(blank=True, null=True, help_text="Mg2+")
	tc = models.FloatField(blank=True, null=True, help_text="TC")
	tg = models.FloatField(blank=True, null=True, help_text="TG")
	hdlc = models.FloatField(blank=True, null=True, help_text="HDLC")
	ldlc = models.FloatField(blank=True, null=True, help_text="LDLC")
	apoa = models.FloatField(blank=True, null=True, help_text="Apoa")
	apob = models.FloatField(blank=True, null=True, help_text="Apob")
	tested = models.DateField(blank=True, null=True, help_text="检验时间")
	created = models.DateTimeField(auto_now_add=True)
	disease = models.ForeignKey(KawasakiDisease, on_delete=models.CASCADE, related_name='biochems')
	author = models.ForeignKey(User, on_delete=models.CASCADE)

class KawasakiMarker(models.Model):
	pt = models.FloatField(blank=True, null=True, help_text="PT")
	aptt = models.FloatField(blank=True, null=True, help_text="APTT")
	fg = models.FloatField(blank=True, null=True, help_text="Fg")
	tt = models.FloatField(blank=True, null=True, help_text="TT")
	ddi = models.FloatField(blank=True, null=True, help_text="DDI")
	fdp = models.FloatField(blank=True, null=True, help_text="FDP")
	atiii = models.FloatField(blank=True, null=True, help_text="ATIII")
	inr = models.FloatField(blank=True, null=True, help_text="INR")
	ctni = models.FloatField(blank=True, null=True, help_text="cTni")
	mb = models.FloatField(blank=True, null=True, help_text="Mb")
	ntbnp = models.FloatField(blank=True, null=True, help_text="NT-BNP")
	tested = models.DateField(blank=True, null=True, help_text="检验时间")
	created = models.DateTimeField(auto_now_add=True)
	disease = models.ForeignKey(KawasakiDisease, on_delete=models.CASCADE, related_name='markers')
	author = models.ForeignKey(User, on_delete=models.CASCADE)

class KawasakiOtherExamine(models.Model):
	NORMAL_TYPES = {
		0: "未做",
		1: "正常",
		2: "不正常"
	}

	HAVE_TYPES = {
		0: "无",
		1: "有"
	}

	POSITIVE_NEGATIVE = {
		0: "阴性",
		1: "阳性"
	}

	njyjc = models.PositiveSmallIntegerField(choices=NORMAL_TYPES, default=0, help_text="脑脊液检查")
	njydbz = models.FloatField(blank=True, null=True, help_text="脑脊液蛋白质")
	njyt = models.FloatField(blank=True, null=True, help_text="脑脊液糖")
	njylhw = models.FloatField(blank=True, null=True, help_text="脑脊液氯化物")
	rxjj = models.PositiveSmallIntegerField(choices=NORMAL_TYPES, default=0, help_text="溶血检查")
	krqdbss = models.PositiveSmallIntegerField(choices=POSITIVE_NEGATIVE, default=0, help_text="直接抗人球蛋白试验")
	wzhxb = models.FloatField(blank=True, null=True, help_text="网织红细胞(%)")
	dbcg = models.PositiveSmallIntegerField(choices=NORMAL_TYPES, default=0, help_text="大便常规")
	dbbxb = models.CharField(max_length=20, blank=True, null=True, default='', help_text="大便白细胞/hp")
	dbhxb = models.CharField(max_length=20, blank=True, null=True, default='', help_text="大便红细胞/hp")
	dbnxb = models.PositiveSmallIntegerField(choices=HAVE_TYPES, default=0, help_text="大便脓细胞/hp")
	xbcg = models.PositiveSmallIntegerField(choices=NORMAL_TYPES, default=0, help_text="小便常规")
	xbndb = models.FloatField(blank=True, null=True, help_text="小便尿蛋白")
	xbbxb = models.CharField(max_length=20, blank=True, null=True, default='', help_text="小便白细胞/hp")
	xbhxb = models.CharField(max_length=20, blank=True, null=True, default='', help_text="小便红细胞/hp")
	xbnxb = models.PositiveSmallIntegerField(choices=HAVE_TYPES, default=0, help_text="小便脓细胞/hp")
	xdt = models.PositiveSmallIntegerField(choices=NORMAL_TYPES, default=0, help_text="心电图")
	xdtbx = models.CharField(max_length=255, blank=True, null=True, default='', help_text="心电图具体表现")
	xp = models.PositiveSmallIntegerField(choices=NORMAL_TYPES, default=0, help_text="胸片")
	xpbx = models.CharField(max_length=255, blank=True, null=True, default='', help_text="胸片具体表现")
	created = models.DateTimeField(auto_now_add=True)
	disease = models.ForeignKey(KawasakiDisease, on_delete=models.CASCADE, related_name='examines')
	author = models.ForeignKey(User, on_delete=models.CASCADE)

class KawasakiTreatment(models.Model):
	IVIG_LOCATIONS = {
		1: "心血管科住院",
		2: "急诊",
		3: "门诊或其他住院部科室",
		4: "外院"
	}

	YES_NO = {
		0: "否",
		1: "是"
	}

	ASPL_DOSES = {
		0: "未使用",
		1: "小3-10mg/kg/d",
		2: "大30-50"
	}

	ASPL_IVIG_ORDERS = {
		0: "未知",
		1: "同时",
		2: "IVIG在前",
		3: "IVIG在后" 
	}

	KL_TREATEMENTS = {
		0: "未知",
		1: "阿司匹林",
		2: "潘生丁(双嘧达莫)",
		3: "氯吡格雷",
		4: "华法林",
		5: "低分子肝素"
	}

	dyivigdd = models.PositiveSmallIntegerField(choices=IVIG_LOCATIONS, default=1, help_text="第一次IVIG使用地点")
	dyivigsj = models.CharField(max_length=20, blank=True, null=True, default='', help_text="第一次IVIG使用时间")
	dycivig = models.PositiveSmallIntegerField(choices=YES_NO, default=0, help_text="第一次IVIG")
	dycjl = models.FloatField(blank=True, null=True, help_text="第一次剂量(g/kg)")
	ksszhtrsj = models.CharField(max_length=20, blank=True, null=True, default='', help_text="开始输注后退热时间")
	decivig = models.PositiveSmallIntegerField(choices=YES_NO, default=0, help_text="第二次IVIG")
	decjl = models.FloatField(blank=True, null=True, help_text="第二次剂量(g/kg)")
	sfsyjs = models.PositiveSmallIntegerField(choices=YES_NO, default=0, help_text="是否使用激素")
	jszl = models.CharField(max_length=30, blank=True, null=True, default='', help_text="激素种类")
	syjslfrdj = models.CharField(max_length=20, blank=True, null=True, default='', help_text="使用激素，离发热多久")
	jsyf = models.CharField(max_length=30, blank=True, null=True, default='', help_text="激素用法")
	jsyl = models.FloatField(blank=True, null=True, help_text="激素用量(mg/kg)")
	sfsyaspl = models.PositiveSmallIntegerField(choices=YES_NO, default=0, help_text="是否使用阿司匹林")
	syasplfrdj = models.CharField(max_length=20, blank=True, null=True, default='', help_text="使用阿司匹林，离发热多久")
	aspljl = models.PositiveSmallIntegerField(choices=ASPL_DOSES, default=0, help_text="阿司匹林剂量")
	aspltrsj = models.CharField(max_length=20, blank=True, null=True, default='', help_text="阿司匹林使用后退热时间")
	asplivigsx = models.PositiveSmallIntegerField(choices=ASPL_IVIG_ORDERS, default=0, help_text="阿司匹林和IVIG使用顺序")
	klzl = models.PositiveSmallIntegerField(choices=KL_TREATEMENTS, default=0, help_text="抗凝治疗")
	qtzlfa = models.CharField(max_length=200, blank=True, null=True, default='', help_text="其他治疗方案")
	created = models.DateTimeField(auto_now_add=True)
	disease = models.ForeignKey(KawasakiDisease, on_delete=models.CASCADE, related_name='treats')
	author = models.ForeignKey(User, on_delete=models.CASCADE)

class KawasakiCardiacPhenotype(models.Model):
	HAVE_TYPES = {
		0: "无",
		1: "有"
	}

	sfyxhxtzz = models.PositiveSmallIntegerField(choices=HAVE_TYPES, default=0, help_text="是否有消化系统症状")
	outu = models.PositiveSmallIntegerField(choices=HAVE_TYPES, default=0, help_text="呕吐")
	ftjzbs = models.PositiveSmallIntegerField(choices=HAVE_TYPES, default=0, help_text="腹痛/脐周不适")
	gy = models.PositiveSmallIntegerField(choices=HAVE_TYPES, default=0, help_text="肝炎")
	hd = models.PositiveSmallIntegerField(choices=HAVE_TYPES, default=0, help_text="黄疸")
	dlzd = models.PositiveSmallIntegerField(choices=HAVE_TYPES, default=0, help_text="胆囊肿大")
	yxy = models.PositiveSmallIntegerField(choices=HAVE_TYPES, default=0, help_text="胰腺炎")
	xhxtqtbx = models.CharField(max_length=200, blank=True, null=True, default='', help_text="消化系统其他表现")
	sjxtzz = models.PositiveSmallIntegerField(choices=HAVE_TYPES, default=0, help_text="神经系统症状")
	jz = models.PositiveSmallIntegerField(choices=HAVE_TYPES, default=0, help_text="惊厥")
	cc = models.PositiveSmallIntegerField(choices=HAVE_TYPES, default=0, help_text="抽搐")
	jr = models.PositiveSmallIntegerField(choices=HAVE_TYPES, default=0, help_text="激惹")
	ss = models.PositiveSmallIntegerField(choices=HAVE_TYPES, default=0, help_text="嗜睡")
	tt = models.PositiveSmallIntegerField(choices=HAVE_TYPES, default=0, help_text="头痛")
	pt = models.PositiveSmallIntegerField(choices=HAVE_TYPES, default=0, help_text="偏瘫")
	tssjsh = models.PositiveSmallIntegerField(choices=HAVE_TYPES, default=0, help_text="听视神经损害")
	qlpl = models.PositiveSmallIntegerField(choices=HAVE_TYPES, default=0, help_text="前囟膨隆")
	ngs = models.PositiveSmallIntegerField(choices=HAVE_TYPES, default=0, help_text="脑梗塞")
	ncx = models.PositiveSmallIntegerField(choices=HAVE_TYPES, default=0, help_text="脑出血")
	sw = models.PositiveSmallIntegerField(choices=HAVE_TYPES, default=0, help_text="神萎")
	sjxtqtbx = models.CharField(max_length=200, blank=True, null=True, default='', help_text="神经系统其他表现")
	sfyhxxtbx = models.PositiveSmallIntegerField(choices=HAVE_TYPES, default=0, help_text="是否有呼吸系统表现")
	ks = models.PositiveSmallIntegerField(choices=HAVE_TYPES, default=0, help_text="咳嗽")
	hxxtqtbx = models.CharField(max_length=200, blank=True, null=True, default='', help_text="呼吸系统其他表现")
	sfyjrxtbx = models.PositiveSmallIntegerField(choices=HAVE_TYPES, default=0, help_text="是否有肌肉系统表现")
	gjy = models.PositiveSmallIntegerField(choices=HAVE_TYPES, default=0, help_text="关节炎")
	gjtt = models.PositiveSmallIntegerField(choices=HAVE_TYPES, default=0, help_text="关节疼痛")
	hzgjtw = models.PositiveSmallIntegerField(choices=HAVE_TYPES, default=0, help_text="寰椎关节脱位")
	jbhdsx = models.PositiveSmallIntegerField(choices=HAVE_TYPES, default=0, help_text="颈部活动受限")
	jrxtqtbx = models.CharField(max_length=200, blank=True, null=True, default='', help_text="肌肉系统其他表现")
	sfymnxtbx = models.PositiveSmallIntegerField(choices=HAVE_TYPES, default=0, help_text="是否有泌尿生殖系统表现")
	yljs = models.PositiveSmallIntegerField(choices=HAVE_TYPES, default=0, help_text="阴囊积水")
	ndy = models.PositiveSmallIntegerField(choices=HAVE_TYPES, default=0, help_text="尿道炎")
	ndky = models.PositiveSmallIntegerField(choices=HAVE_TYPES, default=0, help_text="尿道口炎")
	ndxtqtbx = models.CharField(max_length=200, blank=True, null=True, default='', help_text="泌尿生殖系统其他表现")
	sfyqtxtbx = models.PositiveSmallIntegerField(choices=HAVE_TYPES, default=0, help_text="是否有其他系统表现")
	qtxtjtbx = models.CharField(max_length=200, blank=True, null=True, default='', help_text="其他系统具体表现")
	created = models.DateTimeField(auto_now_add=True)
	disease = models.ForeignKey(KawasakiDisease, on_delete=models.CASCADE, related_name='cardiacs')
	author = models.ForeignKey(User, on_delete=models.CASCADE)

class KawasakiUltrasound(models.Model):
	YES_NO = {
		0: "否",
		1: "是"
	}

	NORMAL_TYPES = {
		0: "未知",
		1: "正常",
		2: "不正常"
	}

	code = models.CharField(max_length=20, blank=True, default='', help_text="超声号")
	lfrjt = models.FloatField(blank=True, null=True, help_text="离发热几天")
	jtzk = models.PositiveSmallIntegerField(choices=NORMAL_TYPES, default=1, help_text="具体状况")
	efp = models.FloatField(blank=True, null=True, help_text="EF(%)")
	xbjy = models.PositiveSmallIntegerField(choices=YES_NO, default=0, help_text="心包积液")
	xzzd = models.PositiveSmallIntegerField(choices=YES_NO, default=0, help_text="心脏长大")
	bmfl = models.PositiveSmallIntegerField(choices=YES_NO, default=0, help_text="瓣膜返流")
	gmkz = models.PositiveSmallIntegerField(choices=YES_NO, default=0, help_text="冠脉扩张")
	gmxs = models.PositiveSmallIntegerField(choices=YES_NO, default=0, help_text="冠脉血栓")
	gml = models.PositiveSmallIntegerField(choices=YES_NO, default=0, help_text="冠脉瘤")
	lca = models.FloatField(blank=True, null=True, help_text="LCA")
	lad = models.FloatField(blank=True, null=True, help_text="LAD")
	lcx = models.FloatField(blank=True, null=True, help_text="LCX")
	rca = models.FloatField(blank=True, null=True, help_text="RCA")
	zdms = models.CharField(max_length=200, blank=True, null=True, default='', help_text="诊断描述")
	report = models.FileField(upload_to='report/%Y/%m/', max_length=200, blank=True, null=True, help_text="报告文件")
	dicom_file = models.FileField(upload_to='dicom/%Y/%m/', max_length=255, blank=True, null=True, help_text="影像文件")
	dicom_uuid = models.CharField(max_length=50, blank=True, default='')
	tested = models.DateField(blank=True, null=True, help_text="检查时间")
	created = models.DateTimeField(auto_now_add=True)
	disease = models.ForeignKey(KawasakiDisease, on_delete=models.CASCADE, related_name='ultrasounds')
	author = models.ForeignKey(User, on_delete=models.CASCADE)

class KawasakiMedimage(models.Model):
	IMAGE_TYPES = {
		1: "MRI",
		3: "CTA",
		2: "冠脉造影",
		0: "其他"
	}

	yxlx = models.PositiveSmallIntegerField(choices=IMAGE_TYPES, default=1, help_text="影像类型")
	code = models.CharField(max_length=20, blank=True, default='', help_text="影像号")
	zd = models.CharField(max_length=200, blank=True, default='', help_text="诊断")
	report = models.FileField(upload_to='report/%Y/%m/', max_length=200, blank=True, null=True, help_text="报告文件")
	dicom_file = models.FileField(upload_to='dicom/%Y/%m/', max_length=255, blank=True, null=True, help_text="影像文件")
	dicom_uuid = models.CharField(max_length=50, blank=True, default='')
	tested = models.DateField(blank=True, null=True, help_text="检查时间")
	created = models.DateTimeField(auto_now_add=True)
	disease = models.ForeignKey(KawasakiDisease, on_delete=models.CASCADE, related_name='medimages')
	author = models.ForeignKey(User, on_delete=models.CASCADE)

class KawasakiGeneReport(models.Model):
	company = models.CharField(max_length=100, blank=True, default='', help_text="检测公司")
	report = models.FileField(upload_to='report/%Y/%m/', blank=True, null=True, help_text="报告")
	tested = models.DateField(blank=True, null=True, help_text="检验时间")
	created = models.DateTimeField(auto_now_add=True)
	disease = models.ForeignKey(KawasakiDisease, on_delete=models.CASCADE, related_name='reports')
	author = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.report.name.split('/')[-1]

class KawasakiGeneMutation(models.Model):
	gene = models.CharField(max_length=50, blank=True, default='', help_text="基因")
	position = models.CharField(max_length=50, blank=True, default='', help_text="位置")
	mutation = models.CharField(max_length=80, blank=True, default='', help_text="突变信息")
	gnomad = models.CharField(max_length=30, blank=True, default='', help_text="gnomAD MAF")
	acmg = models.CharField(max_length=30, blank=True, default='', help_text="ACMG变异评级")
	disease = models.CharField(max_length=80, blank=True, default='', help_text="疾病名称")
	gmode = models.CharField(max_length=20, blank=True, default='', help_text="遗传模式")
	zygote = models.CharField(max_length=100, blank=True, default='', help_text="合子类型")
	report = models.ForeignKey(KawasakiGeneReport, on_delete=models.CASCADE, related_name='genes')


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


