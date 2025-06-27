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
	jbmc = models.CharField(max_length=80, blank=True, default='', help_text="疾病名称")
	gmode = models.CharField(max_length=20, blank=True, default='', help_text="遗传模式")
	zygote = models.CharField(max_length=100, blank=True, default='', help_text="合子类型")
	report = models.ForeignKey(CardiomyopathyGeneReport, on_delete=models.CASCADE, related_name='genes', help_text="来源报告")
	created = models.DateTimeField(auto_now_add=True)
	disease = models.ForeignKey(CardiomyopathyDisease, on_delete=models.CASCADE, blank=True, null=True)
	author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)


class KawasakiDisease(models.Model):
	CHUANQI_TYPES = {
		0: "未知",
		1: "完全",
		2: "不完全"
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

	disease_code = models.CharField(max_length=100, blank=True, default='', help_text="编号或测序编号")
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
	patient = models.ForeignKey(Patient, on_delete=models.CASCADE, help_text="患者")
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
	report = models.ForeignKey(KawasakiGeneReport, on_delete=models.CASCADE, related_name='genes', help_text="来源报告")
	created = models.DateTimeField(auto_now_add=True)
	disease = models.ForeignKey(KawasakiDisease, on_delete=models.CASCADE, blank=True, null=True)
	author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

class ArrhythmiaDisease(models.Model):
	YES_NO = {
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
	xlscbx = models.CharField(max_length=80, blank=True, default='', help_text="心律失常表型")
	cznl = models.CharField(max_length=20, blank=True, null=True, default='', help_text="初诊年龄(岁/孕周)")
	sqzd = models.CharField(max_length=200, blank=True, null=True, default='', help_text="术前诊断")
	sqyy = models.CharField(max_length=100, blank=True, null=True, default='', help_text="术前用药")
	yyjl = models.CharField(max_length=30, blank=True, null=True, default='', help_text="药物剂量")
	shzd = models.CharField(max_length=200, blank=True, null=True, default='', help_text="术后诊断")
	sssj = models.DateField(blank=True, null=True, help_text="手术时间")
	ssfs = models.CharField(max_length=80, blank=True, null=True, default='', help_text="手术方式")
	ssch = models.PositiveSmallIntegerField(choices=YES_NO, default=1, help_text="存活")
	sfsj = models.DateField(blank=True, null=True, help_text="随访时间")
	sfcjbb = models.PositiveSmallIntegerField(choices=YES_NO, default=1, help_text="是否采集标本")
	sjbb = models.PositiveSmallIntegerField(choices=SAMPLE_TYPES, default=0, help_text="已送检标本")
	sybb = models.PositiveSmallIntegerField(choices=SAMPLE_TYPES, default=0, help_text="剩余标本")
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	patient = models.ForeignKey(Patient, on_delete=models.CASCADE, help_text="患者")
	author = models.ForeignKey(User, on_delete=models.CASCADE)

class ArrhythmiaBlood(models.Model):
	xcg = models.CharField(max_length=80, blank=True, null=True, default='', help_text="血常规")
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
	hctp = models.FloatField(blank=True, null=True, help_text="HCT(%)")
	rdwcv = models.FloatField(blank=True, null=True, help_text="RDW-CV%")
	rdwsd = models.FloatField(blank=True, null=True, help_text="RDWSD")
	pdw = models.FloatField(blank=True, null=True, help_text="PDW")
	mpv = models.FloatField(blank=True, null=True, help_text="MPV")
	plcr = models.FloatField(blank=True, null=True, help_text="PLCR")
	pctp = models.FloatField(blank=True, null=True, help_text="PCT%")
	crp = models.FloatField(blank=True, null=True, help_text="CRP")
	tested = models.DateField(blank=True, null=True, help_text="检验时间")
	created = models.DateTimeField(auto_now_add=True)
	disease = models.ForeignKey(ArrhythmiaDisease, on_delete=models.CASCADE, related_name='bloods')
	author = models.ForeignKey(User, on_delete=models.CASCADE)

class ArrhythmiaBiochemistry(models.Model):
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
	urea = models.FloatField(blank=True, null=True, help_text="Urea")
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
	disease = models.ForeignKey(ArrhythmiaDisease, on_delete=models.CASCADE, related_name='biochems')
	author = models.ForeignKey(User, on_delete=models.CASCADE)

class ArrhythmiaMarker(models.Model):
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
	disease = models.ForeignKey(ArrhythmiaDisease, on_delete=models.CASCADE, related_name='markers')
	author = models.ForeignKey(User, on_delete=models.CASCADE)

class ArrhythmiaOtherExamine(models.Model):
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

	dbcg = models.PositiveSmallIntegerField(choices=NORMAL_TYPES, default=0, help_text="大便常规")
	dbbxb = models.CharField(max_length=20, blank=True, null=True, default='', help_text="大便白细胞/hp")
	dbhxb = models.CharField(max_length=20, blank=True, null=True, default='', help_text="大便红细胞/hp")
	dbnxb = models.PositiveSmallIntegerField(choices=HAVE_TYPES, default=0, help_text="大便脓细胞/hp")
	xbcg = models.PositiveSmallIntegerField(choices=NORMAL_TYPES, default=0, help_text="小便常规")
	xbndb = models.FloatField(blank=True, null=True, help_text="小便尿蛋白")
	xbbxb = models.CharField(max_length=20, blank=True, null=True, default='', help_text="小便白细胞/hp")
	xbhxb = models.CharField(max_length=20, blank=True, null=True, default='', help_text="小便红细胞/hp")
	xbnxb = models.PositiveSmallIntegerField(choices=HAVE_TYPES, default=0, help_text="小便脓细胞/hp")
	created = models.DateTimeField(auto_now_add=True)
	disease = models.ForeignKey(ArrhythmiaDisease, on_delete=models.CASCADE, related_name='examines')
	author = models.ForeignKey(User, on_delete=models.CASCADE)

class ArrhythmiaCardiogram(models.Model):
	YES_NO = {
		0: "否",
		1: "是"
	}

	HEART_RHYTHM = {
		1: "窦",
		2: "室",
		3: "房"
	}

	RHYTHM_TYPES = {
		1: "左束支",
		2: "右束支"
	}

	jcxl = models.PositiveSmallIntegerField(choices=HEART_RHYTHM, default=1, help_text="基础心律")
	cdzz = models.PositiveSmallIntegerField(choices=YES_NO, default=0, help_text="传导阻滞")
	xllx = models.PositiveSmallIntegerField(choices=RHYTHM_TYPES, default=0, help_text="类型")
	sxzb = models.PositiveSmallIntegerField(choices=YES_NO, default=0, help_text="室性早搏")
	sxfzcs = models.FloatField(blank=True, null=True, help_text="发作次数(次/24h)")
	sxzbp = models.FloatField(blank=True, null=True, help_text="室性占比(%)")
	fxzb = models.PositiveSmallIntegerField(choices=YES_NO, default=0, help_text="房性早搏")
	fxfzcs = models.FloatField(blank=True, null=True, help_text="发作次数(次/24h)")
	fxzbp = models.FloatField(blank=True, null=True, help_text="房性占比(%)")
	fxxdgs = models.PositiveSmallIntegerField(choices=YES_NO, default=0, help_text="房性心动过速")
	fxfzpc = models.CharField(max_length=100, blank=True, null=True, default='', help_text="房性发作频次")
	sxxdgs = models.PositiveSmallIntegerField(choices=YES_NO, default=0, help_text="室性心动过速")
	sxfzpc = models.CharField(max_length=100, blank=True, null=True, default='', help_text="室性发作频次")
	ssxdgs = models.PositiveSmallIntegerField(choices=YES_NO, default=0, help_text="室上性心动过速")
	ssfzpc = models.CharField(max_length=100, blank=True, null=True, default='', help_text="室上发作频次")
	sdnn = models.FloatField(blank=True, null=True, help_text="SDNN")
	fzsqrs = models.FloatField(blank=True, null=True, help_text="发作时QRS宽度")
	dlsqrs = models.FloatField(blank=True, null=True, help_text="窦律时QRS宽度")
	pbkd = models.FloatField(blank=True, null=True, help_text="P波宽度")
	prjq = models.FloatField(blank=True, null=True, help_text="PR间期")
	qtcjq = models.FloatField(blank=True, null=True, help_text="QTc间期")
	pjjq = models.FloatField(blank=True, null=True, help_text="PJ间期")
	dzpzjd = models.FloatField(blank=True, null=True, help_text="电轴偏转角度")
	tbrpjq = models.FloatField(blank=True, null=True, help_text="体表心电图RP间期")
	created = models.DateTimeField(auto_now_add=True)
	disease = models.ForeignKey(ArrhythmiaDisease, on_delete=models.CASCADE, related_name='cardiograms')
	author = models.ForeignKey(User, on_delete=models.CASCADE)

class ArrhythmiaSurgery(models.Model):
	sscxsj = models.FloatField(blank=True, null=True, help_text="手术持续时间(min)")
	xxbgl = models.FloatField(blank=True, null=True, help_text="X线曝光量(Gy)")
	xrnlgl = models.FloatField(blank=True, null=True, help_text="消融能量及功率")
	xrggbd = models.FloatField(blank=True, null=True, help_text="消融巩固靶点个数")
	glwk = models.CharField(max_length=50, blank=True, null=True, default='', help_text="功率/温控")
	scfbjsssj = models.CharField(max_length=50, blank=True, null=True, default='', help_text="首次发病距手术时间")
	fzsplsq = models.FloatField(blank=True, null=True, help_text="发作时频率(术前)")
	fzsplsz = models.FloatField(blank=True, null=True, help_text="发作时频率(术中)")
	yfms = models.CharField(max_length=50, blank=True, null=True, default='', help_text="诱发模式")
	yfsj = models.FloatField(blank=True, null=True, help_text="诱发时间")
	dfjhfsj = models.FloatField(blank=True, null=True, help_text="窦房结恢复时间")
	pbqdhcj = models.FloatField(blank=True, null=True, help_text="P波起点到HIS/CS近端A波间期")
	csabjdkd = models.FloatField(blank=True, null=True, help_text="CS上A波激动跨度")
	csvbjdkd = models.FloatField(blank=True, null=True, help_text="CS上V波激动跨度")
	pajq = models.FloatField(blank=True, null=True, help_text="PA间期")
	ahjq = models.FloatField(blank=True, null=True, help_text="AH间期")
	hvjq = models.FloatField(blank=True, null=True, help_text="HV间期")
	ahjqfz = models.FloatField(blank=True, null=True, help_text="AH间期(发作时)")
	hvjqfz = models.FloatField(blank=True, null=True, help_text="HV间期(发作时)")
	vajqfz = models.FloatField(blank=True, null=True, help_text="VA间期(发作时)")
	fsjqcbyq = models.FloatField(blank=True, null=True, help_text="房室结前传不应期")
	xfbyq = models.FloatField(blank=True, null=True, help_text="心房不应期")
	fsjlcbyq = models.FloatField(blank=True, null=True, help_text="房室结逆传不应期")
	xsbyq = models.FloatField(blank=True, null=True, help_text="心室不应期")
	bddwtqcd = models.FloatField(blank=True, null=True, help_text="靶点电位提前程度")
	bddwcxsj = models.FloatField(blank=True, null=True, help_text="靶点电位持续时间")
	djxt = models.CharField(max_length=50, blank=True, null=True, default='', help_text="单极形态")
	operated = models.DateField(blank=True, null=True, default='', help_text="手术时间")
	created = models.DateTimeField(auto_now_add=True)
	disease = models.ForeignKey(ArrhythmiaDisease, on_delete=models.CASCADE, related_name='surgerys')
	author = models.ForeignKey(User, on_delete=models.CASCADE)

class ArrhythmiaUltrasound(models.Model):
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
	csnl = models.FloatField(blank=True, null=True, help_text="年龄")
	lvef = models.FloatField(blank=True, null=True, help_text="LVEF(%)")
	lvfs = models.FloatField(blank=True, null=True, help_text="LVFS(%)")
	lv = models.FloatField(blank=True, null=True, help_text="LV(mm)")
	la = models.FloatField(blank=True, null=True, help_text="LA(mm)")
	rv = models.FloatField(blank=True, null=True, help_text="RV(mm)")
	ra = models.FloatField(blank=True, null=True, help_text="RA(mm)")
	tapse = models.FloatField(blank=True, null=True, help_text="TAPSE")
	ivs = models.FloatField(blank=True, null=True, help_text="IVS")	
	xbjy = models.PositiveSmallIntegerField(choices=YES_NO, default=0, help_text="心包积液")
	xzzd = models.PositiveSmallIntegerField(choices=YES_NO, default=0, help_text="心脏长大")
	bmfl = models.PositiveSmallIntegerField(choices=YES_NO, default=0, help_text="瓣膜返流")
	gmyc = models.PositiveSmallIntegerField(choices=YES_NO, default=0, help_text="冠脉异常")
	xnxs = models.PositiveSmallIntegerField(choices=YES_NO, default=0, help_text="心内血栓")
	fdmgy = models.PositiveSmallIntegerField(choices=YES_NO, default=0, help_text="肺动脉高压")
	cszd = models.CharField(max_length=200, blank=True, null=True, default='', help_text="超声诊断")
	report = models.FileField(upload_to='report/%Y/%m/', max_length=200, blank=True, null=True, help_text="报告文件")
	dicom_file = models.FileField(upload_to='dicom/%Y/%m/', max_length=255, blank=True, null=True, help_text="影像文件")
	dicom_uuid = models.CharField(max_length=50, blank=True, default='')
	tested = models.DateField(blank=True, null=True, help_text="检查时间")
	created = models.DateTimeField(auto_now_add=True)
	disease = models.ForeignKey(ArrhythmiaDisease, on_delete=models.CASCADE, related_name='ultrasounds')
	author = models.ForeignKey(User, on_delete=models.CASCADE)

class ArrhythmiaMRI(models.Model):
	code = models.CharField(max_length=20, blank=True, default='', help_text="影像号")
	zd = models.CharField(max_length=200, blank=True, default='', help_text="诊断")
	report = models.FileField(upload_to='report/%Y/%m/', max_length=200, blank=True, null=True, help_text="报告文件")
	dicom_file = models.FileField(upload_to='dicom/%Y/%m/', max_length=255, blank=True, null=True, help_text="影像文件")
	dicom_uuid = models.CharField(max_length=50, blank=True, default='')
	tested = models.DateField(blank=True, null=True, help_text="检查时间")
	created = models.DateTimeField(auto_now_add=True)
	disease = models.ForeignKey(ArrhythmiaDisease, on_delete=models.CASCADE, related_name='mris')
	author = models.ForeignKey(User, on_delete=models.CASCADE)

class ArrhythmiaGeneReport(models.Model):
	company = models.CharField(max_length=100, blank=True, default='', help_text="检测公司")
	report = models.FileField(upload_to='report/%Y/%m/', blank=True, null=True, help_text="报告")
	tested = models.DateField(blank=True, null=True, help_text="检验时间")
	created = models.DateTimeField(auto_now_add=True)
	disease = models.ForeignKey(ArrhythmiaDisease, on_delete=models.CASCADE, related_name='reports')
	author = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.report.name.split('/')[-1]

class ArrhythmiaGeneMutation(models.Model):
	gene = models.CharField(max_length=50, blank=True, default='', help_text="基因")
	position = models.CharField(max_length=50, blank=True, default='', help_text="位置")
	mutation = models.CharField(max_length=80, blank=True, default='', help_text="突变信息")
	gnomad = models.CharField(max_length=30, blank=True, default='', help_text="gnomAD MAF")
	acmg = models.CharField(max_length=30, blank=True, default='', help_text="ACMG变异评级")
	disease = models.CharField(max_length=80, blank=True, default='', help_text="疾病名称")
	gmode = models.CharField(max_length=20, blank=True, default='', help_text="遗传模式")
	zygote = models.CharField(max_length=100, blank=True, default='', help_text="合子类型")
	report = models.ForeignKey(ArrhythmiaGeneReport, on_delete=models.CASCADE, related_name='genes', help_text="来源报告")
	created = models.DateTimeField(auto_now_add=True)
	disease = models.ForeignKey(ArrhythmiaDisease, on_delete=models.CASCADE, blank=True, null=True)
	author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

class CongenitalSurgeryDisease(models.Model):
	YES_NO = {
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
	xxbbx = models.CharField(max_length=80, blank=True, default='', help_text="先心病表型")
	cznl = models.FloatField(blank=True, null=True, help_text="初诊年龄")
	sssj = models.DateField(blank=True, null=True, help_text="手术时间")
	ssfs = models.CharField(max_length=80, blank=True, null=True, default='', help_text="手术方式")
	ssch = models.PositiveSmallIntegerField(choices=YES_NO, default=1, help_text="存活")
	sfsj = models.DateField(blank=True, null=True, help_text="随访时间")
	sfcjbb = models.PositiveSmallIntegerField(choices=YES_NO, default=1, help_text="是否采集标本")
	sjbb = models.PositiveSmallIntegerField(choices=SAMPLE_TYPES, default=0, help_text="已送检标本")
	sybb = models.PositiveSmallIntegerField(choices=SAMPLE_TYPES, default=0, help_text="剩余标本")
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	patient = models.ForeignKey(Patient, on_delete=models.CASCADE, help_text="患者")
	author = models.ForeignKey(User, on_delete=models.CASCADE)

class CongenitalSurgeryPreBlood(models.Model):
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
	hctp = models.FloatField(blank=True, null=True, help_text="HCT(%)")
	rdwcv = models.FloatField(blank=True, null=True, help_text="RDW-CV%")
	rdwsd = models.FloatField(blank=True, null=True, help_text="RDWSD")
	pdw = models.FloatField(blank=True, null=True, help_text="PDW")
	mpv = models.FloatField(blank=True, null=True, help_text="MPV")
	plcr = models.FloatField(blank=True, null=True, help_text="PLCR")
	pctp = models.FloatField(blank=True, null=True, help_text="PCT%")
	crp = models.FloatField(blank=True, null=True, help_text="CRP")
	tested = models.DateField(blank=True, null=True, help_text="检验时间")
	created = models.DateTimeField(auto_now_add=True)
	disease = models.ForeignKey(CongenitalSurgeryDisease, on_delete=models.CASCADE, related_name='prebloods')
	author = models.ForeignKey(User, on_delete=models.CASCADE)

class CongenitalSurgeryPreBiochemistry(models.Model):
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
	urea = models.FloatField(blank=True, null=True, help_text="Urea")
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
	disease = models.ForeignKey(CongenitalSurgeryDisease, on_delete=models.CASCADE, related_name='prebiochems')
	author = models.ForeignKey(User, on_delete=models.CASCADE)

class CongenitalSurgeryPreCruor(models.Model):
	pt = models.FloatField(blank=True, null=True, help_text="PT")
	aptt = models.FloatField(blank=True, null=True, help_text="APTT")
	fg = models.FloatField(blank=True, null=True, help_text="Fg")
	tt = models.FloatField(blank=True, null=True, help_text="TT")
	ddi = models.FloatField(blank=True, null=True, help_text="DDI")
	fdp = models.FloatField(blank=True, null=True, help_text="FDP")
	atiii = models.FloatField(blank=True, null=True, help_text="ATIII")
	inr = models.FloatField(blank=True, null=True, help_text="INR")
	tested = models.DateField(blank=True, null=True, help_text="检验时间")
	created = models.DateTimeField(auto_now_add=True)
	disease = models.ForeignKey(CongenitalSurgeryDisease, on_delete=models.CASCADE, related_name='precruors')
	author = models.ForeignKey(User, on_delete=models.CASCADE)

class CongenitalSurgeryPreExamine(models.Model):
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

	dbcg = models.PositiveSmallIntegerField(choices=NORMAL_TYPES, default=0, help_text="大便常规")
	dbbxb = models.CharField(max_length=20, blank=True, null=True, default='', help_text="大便白细胞/hp")
	dbhxb = models.CharField(max_length=20, blank=True, null=True, default='', help_text="大便红细胞/hp")
	dbnxb = models.PositiveSmallIntegerField(choices=HAVE_TYPES, default=0, help_text="大便脓细胞/hp")
	xbcg = models.PositiveSmallIntegerField(choices=NORMAL_TYPES, default=0, help_text="小便常规")
	xbndb = models.FloatField(blank=True, null=True, help_text="小便尿蛋白")
	xbbxb = models.CharField(max_length=20, blank=True, null=True, default='', help_text="小便白细胞/hp")
	xbhxb = models.CharField(max_length=20, blank=True, null=True, default='', help_text="小便红细胞/hp")
	xbnxb = models.PositiveSmallIntegerField(choices=HAVE_TYPES, default=0, help_text="小便脓细胞/hp")
	created = models.DateTimeField(auto_now_add=True)
	disease = models.ForeignKey(CongenitalSurgeryDisease, on_delete=models.CASCADE, related_name='prexamines')
	author = models.ForeignKey(User, on_delete=models.CASCADE)

class CongenitalSurgeryPreLung(models.Model):
	YES_NO = {
		0: "否",
		1: "是"
	}

	NORMAL_TYPES = {
		0: "不正常",
		1: "正常",

	}

	fzsl = models.PositiveSmallIntegerField(choices=YES_NO, default=0, help_text="术前有无肺脏受累")
	sqxp = models.PositiveSmallIntegerField(choices=NORMAL_TYPES, default=1, help_text="术前胸片")
	jtbx = models.CharField(max_length=255, blank=True, null=True, default='', help_text="具体表现")
	created = models.DateTimeField(auto_now_add=True)
	disease = models.ForeignKey(CongenitalSurgeryDisease, on_delete=models.CASCADE, related_name='prelungs')
	author = models.ForeignKey(User, on_delete=models.CASCADE)

class CongenitalSurgeryPreCardiogram(models.Model):
	YES_NO = {
		0: "否",
		1: "是"
	}

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
	jtbg = models.CharField(max_length=200, blank=True, null=True, default='', help_text="具体报告")
	tested = models.DateField(blank=True, null=True, help_text="检验时间")
	created = models.DateTimeField(auto_now_add=True)
	disease = models.ForeignKey(CongenitalSurgeryDisease, on_delete=models.CASCADE, related_name='precards')
	author = models.ForeignKey(User, on_delete=models.CASCADE)

class CongenitalSurgeryPostPH(models.Model):
	pc02 = models.FloatField(blank=True, null=True, help_text="pC02")
	p02 = models.FloatField(blank=True, null=True, help_text="p02")
	beecf = models.FloatField(blank=True, null=True, help_text="BE(ecf)/细胞外剩余碱")
	beb = models.FloatField(blank=True, null=True, help_text="BE(b)/剩余碱")
	hc03 = models.FloatField(blank=True, null=True, help_text="HCO3-act(实际碳酸氢根离子)")
	k = models.FloatField(blank=True, null=True, help_text="K+")
	na = models.FloatField(blank=True, null=True, help_text="Na+")
	ca = models.FloatField(blank=True, null=True, help_text="Ca2+")
	hct = models.FloatField(blank=True, null=True, help_text="Hct(红细胞比积)")
	chgb = models.FloatField(blank=True, null=True, help_text="cHgb(总血红蛋白)g/dL")
	glu = models.FloatField(blank=True, null=True, help_text="Glu(葡萄糖)mmol/L")
	lact = models.FloatField(blank=True, null=True, help_text="Lact(乳酸)mmol/L")
	s02 = models.FloatField(blank=True, null=True, help_text="SO2(血氧饱和度)%")
	crea = models.FloatField(blank=True, null=True, help_text="Crea(肌酐 umol/L)")
	cl = models.FloatField(blank=True, null=True, help_text="Cl-")
	ag = models.FloatField(blank=True, null=True, help_text="AG(阴离子间隙)")
	created = models.DateTimeField(auto_now_add=True)
	disease = models.ForeignKey(CongenitalSurgeryDisease, on_delete=models.CASCADE, related_name='postphs')
	author = models.ForeignKey(User, on_delete=models.CASCADE)

class CongenitalSurgeryPostBlood(models.Model):
	YES_NO = {
		0: "否",
		1: "是"
	}

	xysl = models.PositiveSmallIntegerField(choices=YES_NO, default=0, help_text="术后有无血液系统受累")
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
	hctp = models.FloatField(blank=True, null=True, help_text="HCT(%)")
	rdwcv = models.FloatField(blank=True, null=True, help_text="RDW-CV%")
	rdwsd = models.FloatField(blank=True, null=True, help_text="RDWSD")
	pdw = models.FloatField(blank=True, null=True, help_text="PDW")
	mpv = models.FloatField(blank=True, null=True, help_text="MPV")
	plcr = models.FloatField(blank=True, null=True, help_text="PLCR")
	pctp = models.FloatField(blank=True, null=True, help_text="PCT%")
	crp = models.FloatField(blank=True, null=True, help_text="CRP")
	created = models.DateTimeField(auto_now_add=True)
	disease = models.ForeignKey(CongenitalSurgeryDisease, on_delete=models.CASCADE, related_name='postbloods')
	author = models.ForeignKey(User, on_delete=models.CASCADE)

class CongenitalSurgeryPostLiver(models.Model):
	YES_NO = {
		0: "否",
		1: "是"
	}

	liver = models.PositiveSmallIntegerField(choices=YES_NO, default=0, help_text="术后有无肝脏受累")
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
	kidney = models.PositiveSmallIntegerField(choices=YES_NO, default=0, help_text="术后有无肾脏受累")
	urea = models.FloatField(blank=True, null=True, help_text="Urea")
	jg = models.FloatField(blank=True, null=True, help_text="肌酐")
	cysc = models.FloatField(blank=True, null=True, help_text="CYSC")
	ua = models.FloatField(blank=True, null=True, help_text="UA")
	created = models.DateTimeField(auto_now_add=True)
	disease = models.ForeignKey(CongenitalSurgeryDisease, on_delete=models.CASCADE, related_name='postlivers')
	author = models.ForeignKey(User, on_delete=models.CASCADE)

class CongenitalSurgeryPostCruor(models.Model):
	YES_NO = {
		0: "否",
		1: "是"
	}

	cruor = models.PositiveSmallIntegerField(choices=YES_NO, default=0, help_text="术后有无凝血功能障碍")
	pt = models.FloatField(blank=True, null=True, help_text="PT")
	aptt = models.FloatField(blank=True, null=True, help_text="APTT")
	fg = models.FloatField(blank=True, null=True, help_text="Fg")
	tt = models.FloatField(blank=True, null=True, help_text="TT")
	ddi = models.FloatField(blank=True, null=True, help_text="DDI")
	fdp = models.FloatField(blank=True, null=True, help_text="FDP")
	atiii = models.FloatField(blank=True, null=True, help_text="ATIII")
	inr = models.FloatField(blank=True, null=True, help_text="INR")
	tested = models.DateField(blank=True, null=True, help_text="检验时间")
	created = models.DateTimeField(auto_now_add=True)
	disease = models.ForeignKey(CongenitalSurgeryDisease, on_delete=models.CASCADE, related_name='postcruors')
	author = models.ForeignKey(User, on_delete=models.CASCADE)

class CongenitalSurgeryPostLung(models.Model):
	YES_NO = {
		0: "否",
		1: "是"
	}

	NORMAL_TYPES = {
		0: "不正常",
		1: "正常",

	}

	fzsl = models.PositiveSmallIntegerField(choices=YES_NO, default=0, help_text="术后有无肺脏受累")
	sqxp = models.PositiveSmallIntegerField(choices=NORMAL_TYPES, default=1, help_text="术后胸片")
	jtbx = models.CharField(max_length=255, blank=True, null=True, default='', help_text="具体表现")
	zssjsl = models.PositiveSmallIntegerField(choices=YES_NO, default=0, help_text="术后有无中枢神经系统受累")
	zssjtbx = models.CharField(max_length=255, blank=True, null=True, default='', help_text="具体表现")
	created = models.DateTimeField(auto_now_add=True)
	disease = models.ForeignKey(CongenitalSurgeryDisease, on_delete=models.CASCADE, related_name='postlungs')
	author = models.ForeignKey(User, on_delete=models.CASCADE)

class CongenitalSurgeryPostCardiogram(models.Model):
	YES_NO = {
		0: "否",
		1: "是"
	}

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
	jtbg = models.CharField(max_length=200, blank=True, null=True, default='', help_text="具体报告")
	tested = models.DateField(blank=True, null=True, help_text="检验时间")
	created = models.DateTimeField(auto_now_add=True)
	disease = models.ForeignKey(CongenitalSurgeryDisease, on_delete=models.CASCADE, related_name='postcards')
	author = models.ForeignKey(User, on_delete=models.CASCADE)

class CongenitalSurgeryOperation(models.Model):
	YES_NO = {
		0: "否",
		1: "是"
	}

	DEATH_LIVE = {
		0: "死亡",
		1: "生存"
	}

	sssj = models.DateField(blank=True, null=True, help_text="手术时间")
	ssnl = models.FloatField(blank=True, null=True, help_text="手术年龄")
	ssfs = models.CharField(max_length=30, blank=True, null=True, default='', help_text="手术方式")
	twxhsj = models.FloatField(blank=True, null=True, help_text="体外循环时间(min)")
	zdmzdsj = models.FloatField(blank=True, null=True, help_text="主动脉阻断时间(min)")
	txhsj = models.FloatField(blank=True, null=True, help_text="停循环时间(min)")
	xzxngz = models.PositiveSmallIntegerField(choices=YES_NO, default=0, help_text="选择性脑灌注方式")
	xzxngzsj = models.FloatField(blank=True, null=True, help_text="选择性脑灌注时间")
	shzg = models.PositiveSmallIntegerField(choices=DEATH_LIVE, default=1, help_text="术后转归")
	created = models.DateTimeField(auto_now_add=True)
	disease = models.ForeignKey(CongenitalSurgeryDisease, on_delete=models.CASCADE, related_name='operates')
	author = models.ForeignKey(User, on_delete=models.CASCADE)

class CongenitalSurgeryVentilator(models.Model):
	YES_NO = {
		0: "否",
		1: "是"
	}

	sqychxj = models.PositiveSmallIntegerField(choices=YES_NO, default=0, help_text="术前有创呼吸机")
	sqychxjsysj = models.FloatField(blank=True, null=True, help_text="术前有创呼吸机使用时间(h)")
	sqwchxj = models.PositiveSmallIntegerField(choices=YES_NO, default=0, help_text="术前无创呼吸机")
	sqwchxjsysj = models.FloatField(blank=True, null=True, help_text="术前无创呼吸机使用时间(h)")
	shychxj = models.PositiveSmallIntegerField(choices=YES_NO, default=0, help_text="术后有创呼吸机")
	shychxjsysj = models.FloatField(blank=True, null=True, help_text="术后有创呼吸机使用时间(h)")
	shwchxj = models.PositiveSmallIntegerField(choices=YES_NO, default=0, help_text="术后无创呼吸机")
	shwchxjsysj = models.FloatField(blank=True, null=True, help_text="术后无创呼吸机使用时间(h)")
	created = models.DateTimeField(auto_now_add=True)
	disease = models.ForeignKey(CongenitalSurgeryDisease, on_delete=models.CASCADE, related_name='vents')
	author = models.ForeignKey(User, on_delete=models.CASCADE)

class CongenitalSurgeryTreatment(models.Model):
	OPERATION_TYPES = {
		1: "术前",
		2: "术后",
	}

	sqsh = models.PositiveSmallIntegerField(choices=OPERATION_TYPES, default=0, help_text="手术期")
	shsj = models.FloatField(blank=True, null=True, help_text="术后时间(小时)")
	dba = models.FloatField(blank=True, null=True, help_text="多巴胺最大剂量(ug/kg/mim)")
	dbada = models.FloatField(blank=True, null=True, help_text="多巴胺丁胺最大剂量(ug/kg/mim)")
	ssxs = models.FloatField(blank=True, null=True, help_text="肾上腺素最大剂量(ug/kg/mim)")
	qjssxs = models.FloatField(blank=True, null=True, help_text="去甲肾上腺素最大剂量(ug/kg/mim)")
	bssxs = models.FloatField(blank=True, null=True, help_text="苯甲肾上腺素最大剂量(ug/kg/mim)")
	xgsys = models.FloatField(blank=True, null=True, help_text="血管升压素最大剂量(ug/kg/mim)")
	tljys = models.FloatField(blank=True, null=True, help_text="特利加压素最大剂量(ug/kg/mim)")
	yjjl = models.FloatField(blank=True, null=True, help_text="亚甲基蓝最大剂量(ug/kg/mim)")
	mln = models.FloatField(blank=True, null=True, help_text="米力农最大剂量(ug/kg/mim)")
	apln = models.FloatField(blank=True, null=True, help_text="奥普力农最大剂量(ug/kg/mim)")
	zxmd = models.FloatField(blank=True, null=True, help_text="左西孟旦最大剂量(ug/kg/mim)")
	vispf = models.FloatField(blank=True, null=True, help_text="VIS评分")
	created = models.DateTimeField(auto_now_add=True)
	disease = models.ForeignKey(CongenitalSurgeryDisease, on_delete=models.CASCADE, related_name='treats')
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	
class CongenitalSurgeryUltrasound(models.Model):
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
	age = models.FloatField(blank=True, null=True, help_text="年龄")
	lvef = models.FloatField(blank=True, null=True, help_text="LVEF(%)")
	lvfs = models.FloatField(blank=True, null=True, help_text="LVFS(%)")
	xbjy = models.PositiveSmallIntegerField(choices=YES_NO, default=0, help_text="心包积液")
	xzzd = models.PositiveSmallIntegerField(choices=YES_NO, default=0, help_text="心脏长大")
	bmfl = models.PositiveSmallIntegerField(choices=YES_NO, default=0, help_text="瓣膜返流")
	gmyc = models.PositiveSmallIntegerField(choices=YES_NO, default=0, help_text="冠脉异常")
	xnxs = models.PositiveSmallIntegerField(choices=YES_NO, default=0, help_text="心内血栓")
	fdmgy = models.PositiveSmallIntegerField(choices=YES_NO, default=0, help_text="肺动脉高压")
	zdms = models.CharField(max_length=200, blank=True, null=True, default='', help_text="超声诊断")
	report = models.FileField(upload_to='report/%Y/%m/', max_length=200, blank=True, null=True, help_text="报告文件")
	dicom_file = models.FileField(upload_to='dicom/%Y/%m/', max_length=255, blank=True, null=True, help_text="影像文件")
	dicom_uuid = models.CharField(max_length=50, blank=True, default='')
	tested = models.DateField(blank=True, null=True, help_text="检查时间")
	created = models.DateTimeField(auto_now_add=True)
	disease = models.ForeignKey(CongenitalSurgeryDisease, on_delete=models.CASCADE, related_name='ultrasounds')
	author = models.ForeignKey(User, on_delete=models.CASCADE)

class CongenitalSurgeryMedimage(models.Model):
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
	disease = models.ForeignKey(CongenitalSurgeryDisease, on_delete=models.CASCADE, related_name='medimages')
	author = models.ForeignKey(User, on_delete=models.CASCADE)

class CongenitalSurgeryGeneReport(models.Model):
	company = models.CharField(max_length=100, blank=True, default='', help_text="检测公司")
	report = models.FileField(upload_to='report/%Y/%m/', blank=True, null=True, help_text="报告")
	tested = models.DateField(blank=True, null=True, help_text="检验时间")
	created = models.DateTimeField(auto_now_add=True)
	disease = models.ForeignKey(CongenitalSurgeryDisease, on_delete=models.CASCADE, related_name='reports')
	author = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.report.name.split('/')[-1]

class CongenitalSurgeryGeneMutation(models.Model):
	gene = models.CharField(max_length=50, blank=True, default='', help_text="基因")
	position = models.CharField(max_length=50, blank=True, default='', help_text="位置")
	mutation = models.CharField(max_length=80, blank=True, default='', help_text="突变信息")
	gnomad = models.CharField(max_length=30, blank=True, default='', help_text="gnomAD MAF")
	acmg = models.CharField(max_length=30, blank=True, default='', help_text="ACMG变异评级")
	disease = models.CharField(max_length=80, blank=True, default='', help_text="疾病名称")
	gmode = models.CharField(max_length=20, blank=True, default='', help_text="遗传模式")
	zygote = models.CharField(max_length=100, blank=True, default='', help_text="合子类型")
	report = models.ForeignKey(CongenitalSurgeryGeneReport, on_delete=models.CASCADE, related_name='genes', help_text="来源报告")
	created = models.DateTimeField(auto_now_add=True)
	disease = models.ForeignKey(CongenitalSurgeryDisease, on_delete=models.CASCADE, blank=True, null=True)
	author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

class CongenitalInterveneDisease(models.Model):
	VSD_TYPES = {
		1: "膜周",
		2: "肌部",
		3: "干下",
		4: "其他",
	}

	YES_NO = {
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
	sjgqsbx = models.PositiveSmallIntegerField(choices=VSD_TYPES, default=1, help_text="室间隔缺损表型")
	cznl = models.FloatField(blank=True, null=True, help_text="初诊年龄")
	ssrq = models.DateField(blank=True, null=True, help_text="手术日期")
	wkqcfdq = models.PositiveSmallIntegerField(choices=YES_NO, default=1, help_text="外科取出封堵器")
	zyqjcyfl = models.PositiveSmallIntegerField(choices=YES_NO, default=1, help_text="住院期间残余分流")
	zyqjrx = models.PositiveSmallIntegerField(choices=YES_NO, default=1, help_text="住院期间溶血")
	shxdtyc = models.PositiveSmallIntegerField(choices=YES_NO, default=1, help_text="术后心电图异常")
	sfsj = models.DateField(blank=True, null=True, help_text="随访时间")
	sfcjbb = models.PositiveSmallIntegerField(choices=YES_NO, default=1, help_text="是否采集标本")
	sjbb = models.PositiveSmallIntegerField(choices=SAMPLE_TYPES, default=0, help_text="已送检标本")
	sybb = models.PositiveSmallIntegerField(choices=SAMPLE_TYPES, default=0, help_text="剩余标本")
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	patient = models.ForeignKey(Patient, on_delete=models.CASCADE, help_text="患者")
	author = models.ForeignKey(User, on_delete=models.CASCADE)

class CongenitalIntervenePreUltrasound(models.Model):
	YES_NO = {
		0: "否",
		1: "是"
	}

	sjgqsbx = models.CharField(max_length=30, blank=True, null=True, default='', help_text="室间隔缺损表型")
	rukou = models.FloatField(blank=True, null=True, help_text="入口")
	chukou = models.FloatField(blank=True, null=True, help_text="出口")
	ja0jl = models.FloatField(blank=True, null=True, help_text="距AO距离")
	szw = models.FloatField(blank=True, null=True, help_text="时钟位")
	fdmgy = models.PositiveSmallIntegerField(choices=YES_NO, default=0, help_text="肺动脉高压")
	fdmyl = models.FloatField(blank=True, null=True, help_text="肺动脉压力")
	zdmbtc = models.PositiveSmallIntegerField(choices=YES_NO, default=0, help_text="主动脉瓣脱垂")
	bmfl = models.PositiveSmallIntegerField(choices=YES_NO, default=0, help_text="瓣膜反流")
	bmfljtbx = models.CharField(max_length=200, blank=True, null=True, default='', help_text="瓣膜反流具体表型")
	zszd = models.PositiveSmallIntegerField(choices=YES_NO, default=0, help_text="左室长大")
	zsdx = models.FloatField(blank=True, null=True, help_text="左室大小(mm)")
	zszd = models.PositiveSmallIntegerField(choices=YES_NO, default=0, help_text="左房长大")
	zsdx = models.FloatField(blank=True, null=True, help_text="左房大小(mm)")
	created = models.DateTimeField(auto_now_add=True)
	disease = models.ForeignKey(CongenitalInterveneDisease, on_delete=models.CASCADE, related_name="presounds")
	author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

class CongenitalInterveneCardiogram(models.Model):
	YES_NO = {
		0: "否",
		1: "是"
	}

	OPERATION_TYPES = {
		1: "术前",
		2: "术后",
	}

	sqsh = models.PositiveSmallIntegerField(choices=OPERATION_TYPES, default=0, help_text="手术期")
	sqxdtgb = models.PositiveSmallIntegerField(choices=YES_NO, default=0, help_text="心电图改变")
	ecgzd = models.CharField(max_length=30, blank=True, null=True, default='', help_text="ECG诊断")
	xinlv = models.FloatField(blank=True, null=True, help_text="心率")
	pr = models.FloatField(blank=True, null=True, help_text="PR")
	qrs = models.FloatField(blank=True, null=True, help_text="QRS")
	pz = models.FloatField(blank=True, null=True, help_text="P轴")
	rz = models.FloatField(blank=True, null=True, help_text="R轴")
	tz = models.FloatField(blank=True, null=True, help_text="T轴")
	qt = models.FloatField(blank=True, null=True, help_text="QT")
	qtc = models.FloatField(blank=True, null=True, help_text="QTC")
	iipk = models.FloatField(blank=True, null=True, help_text="II P宽")
	iipg = models.FloatField(blank=True, null=True, help_text="II P高")
	rv5 = models.FloatField(blank=True, null=True, help_text="RV5")
	sv1 = models.FloatField(blank=True, null=True, help_text="SV1")
	v1 = models.CharField(max_length=50, blank=True, null=True, default='', help_text="V1图形")
	v5 = models.CharField(max_length=50, blank=True, null=True, default='', help_text="V5图形")
	qrszddy = models.FloatField(blank=True, null=True, help_text="QRS最大电压")
	e1 = models.FloatField(blank=True, null=True, help_text="额I")
	e2 = models.FloatField(blank=True, null=True, help_text="额II")
	e3 = models.FloatField(blank=True, null=True, help_text="额III")
	e4 = models.FloatField(blank=True, null=True, help_text="额IV")
	h1 = models.FloatField(blank=True, null=True, help_text="横I")
	h2 = models.FloatField(blank=True, null=True, help_text="横II")
	h3 = models.FloatField(blank=True, null=True, help_text="横III")
	h4 = models.FloatField(blank=True, null=True, help_text="横IV")
	ert = models.FloatField(blank=True, null=True, help_text="额R-T")
	hrt = models.FloatField(blank=True, null=True, help_text="横R-T")
	yrt = models.FloatField(blank=True, null=True, help_text="右R-T")
	tested = models.DateField(blank=True, null=True, help_text="检测时间")
	created = models.DateTimeField(auto_now_add=True)
	disease = models.ForeignKey(CongenitalInterveneDisease, on_delete=models.CASCADE, related_name="precards")
	author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

class CongenitalInterveneOperate(models.Model):
	QG_TYPES = {
		1: "传送鞘",
		2: "动脉鞘",
		3: "静脉鞘",
	}

	FDQ_COMPANY = {
		1: "深圳",
		2: "上海",
		3: "北京",
		4: "进口",
		5: "ADO-II",
		6: "西安",
	}

	FDQ_TYPES = {
		1: "对称",
		2: "ADOII",
		3: "偏心",
	}

	YES_NO = {
		0: "否",
		1: "是"
	}

	sssj = models.FloatField(blank=True, null=True, help_text="手术时间(min)")
	qglx = models.PositiveSmallIntegerField(choices=QG_TYPES, default=0, help_text="鞘管类型")
	qgdx = models.FloatField(blank=True, null=True, help_text="鞘管大小(F)")
	fdqcj = models.PositiveSmallIntegerField(choices=FDQ_COMPANY, default=0, help_text="封堵器厂家")
	fdqdx = models.FloatField(blank=True, null=True, help_text="封堵器大小")
	fdqlx = models.PositiveSmallIntegerField(choices=FDQ_COMPANY, default=0, help_text="封堵器类型")
	fdfs = models.CharField(max_length=200, blank=True, null=True, default='', help_text="封堵方式")
	fdqgs = models.FloatField(blank=True, null=True, help_text="封堵器个数")
	szdsms = models.PositiveSmallIntegerField(choices=YES_NO, default=0, help_text="术中额外地塞米松使用")
	dsmssycs = models.FloatField(blank=True, null=True, help_text="地塞米松使用次数")
	fdmssy = models.FloatField(blank=True, null=True, help_text="肺动脉收缩压")
	fdmszy = models.FloatField(blank=True, null=True, help_text="肺动脉舒张压")
	fdmpjy = models.FloatField(blank=True, null=True, help_text="肺动脉平均压")
	yxsssy = models.FloatField(blank=True, null=True, help_text="右心室收缩压")
	yxsszy = models.FloatField(blank=True, null=True, help_text="右心室舒张压")
	yxspjy = models.FloatField(blank=True, null=True, help_text="右心室平均压")
	tested = models.DateField(blank=True, null=True, help_text="手术时间")
	created = models.DateTimeField(auto_now_add=True)
	disease = models.ForeignKey(CongenitalInterveneDisease, on_delete=models.CASCADE, related_name="operates")
	author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

class CongenitalInterveneUltrasound(models.Model):
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
	age = models.FloatField(blank=True, null=True, help_text="年龄")
	lvef = models.FloatField(blank=True, null=True, help_text="LVEF(%)")
	lvfs = models.FloatField(blank=True, null=True, help_text="LVFS(%)")
	xbjy = models.PositiveSmallIntegerField(choices=YES_NO, default=0, help_text="心包积液")
	xzzd = models.PositiveSmallIntegerField(choices=YES_NO, default=0, help_text="心脏长大")
	bmfl = models.PositiveSmallIntegerField(choices=YES_NO, default=0, help_text="瓣膜返流")
	gmyc = models.PositiveSmallIntegerField(choices=YES_NO, default=0, help_text="冠脉异常")
	xnxs = models.PositiveSmallIntegerField(choices=YES_NO, default=0, help_text="心内血栓")
	fdmgy = models.PositiveSmallIntegerField(choices=YES_NO, default=0, help_text="肺动脉高压")
	zdms = models.CharField(max_length=200, blank=True, null=True, default='', help_text="超声诊断")
	report = models.FileField(upload_to='report/%Y/%m/', max_length=200, blank=True, null=True, help_text="报告文件")
	dicom_file = models.FileField(upload_to='dicom/%Y/%m/', max_length=255, blank=True, null=True, help_text="影像文件")
	dicom_uuid = models.CharField(max_length=50, blank=True, default='')
	tested = models.DateField(blank=True, null=True, help_text="检查时间")
	created = models.DateTimeField(auto_now_add=True)
	disease = models.ForeignKey(CongenitalInterveneDisease, on_delete=models.CASCADE, related_name='ultrasounds')
	author = models.ForeignKey(User, on_delete=models.CASCADE)

class CongenitalInterveneMedimage(models.Model):
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
	disease = models.ForeignKey(CongenitalInterveneDisease, on_delete=models.CASCADE, related_name='medimages')
	author = models.ForeignKey(User, on_delete=models.CASCADE)

class CongenitalInterveneGeneReport(models.Model):
	company = models.CharField(max_length=100, blank=True, default='', help_text="检测公司")
	report = models.FileField(upload_to='report/%Y/%m/', blank=True, null=True, help_text="报告")
	tested = models.DateField(blank=True, null=True, help_text="检验时间")
	created = models.DateTimeField(auto_now_add=True)
	disease = models.ForeignKey(CongenitalInterveneDisease, on_delete=models.CASCADE, related_name='reports')
	author = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.report.name.split('/')[-1]

class CongenitalInterveneGeneMutation(models.Model):
	gene = models.CharField(max_length=50, blank=True, default='', help_text="基因")
	position = models.CharField(max_length=50, blank=True, default='', help_text="位置")
	mutation = models.CharField(max_length=80, blank=True, default='', help_text="突变信息")
	gnomad = models.CharField(max_length=30, blank=True, default='', help_text="gnomAD MAF")
	acmg = models.CharField(max_length=30, blank=True, default='', help_text="ACMG变异评级")
	disease = models.CharField(max_length=80, blank=True, default='', help_text="疾病名称")
	gmode = models.CharField(max_length=20, blank=True, default='', help_text="遗传模式")
	zygote = models.CharField(max_length=100, blank=True, default='', help_text="合子类型")
	report = models.ForeignKey(CongenitalInterveneGeneReport, on_delete=models.CASCADE, related_name='genes', help_text="来源报告")
	created = models.DateTimeField(auto_now_add=True)
	disease = models.ForeignKey(CongenitalInterveneDisease, on_delete=models.CASCADE, blank=True, null=True)
	author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)


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


