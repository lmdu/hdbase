import numpy
import pandas
import datetime

from .models import *

def parse_date(t):
	date = t.strip().split()[0]

	if '/' in date:
		cols = date.split('/')

	elif '.' in date:
		cols = date.split('.')

	else:
		cols = date.split('-')

	if len(cols) == 2:
		year, month = cols
		day = 1

	elif len(cols) == 1:
		year = cols[0][0:4]
		month = cols[0][4:6]
		day = cols[0][6:]

	else:
		year, month, day = cols

	date = datetime.date(int(year), int(month), int(day))
	return date

def load_data_into_patient(infile, author):
	dtypes = {
		1: str,
		4: str,
		5: float,
		6: float,
		7: str
	}
	table = pandas.read_excel(infile, sheet_name=0, dtype=dtypes)

	gender_mapping = {
		'男': 1,
		'女': 2,
		'1': 1,
		'2': 2,
		1: 1,
		2: 2
	}

	ethnic_mapping= {v: k for k, v in Patient.ETHNIC_GROUPS.items()}

	patient_list = []
	for row in table.itertuples(index=False, name=None):
		params = dict(
			name = row[0].strip(),
			number = row[1].strip()
		)

		if pandas.notna(row[2]):
			params['gender'] = gender_mapping.get(row[3], 0)

		if pandas.notna(row[3]):
			params['ethnicity'] = ethnic_mapping.get(row[4], 0)

		if pandas.notna(row[4]):
			params['birthday'] = parse_date(row[4])

		if pandas.notna(row[5]):
			params['height'] = row[5]

		if pandas.notna(row[6]):
			params['weight'] = row[6]

		if pandas.notna(row[7]):
			params['phone'] = row[7].strip()

		params['author'] = author
		patient_list.append(Patient(**params))

	objs = Patient.objects.bulk_create(patient_list,
		update_conflicts=True,
		unique_fields = ['number'],
		update_fields = ['name']
	)
	return {obj.number : obj for obj in objs}

def load_data_into_table(mclass, dtypes, fields, fdates, fgets, infile, sheet, author, patients=None, diseases=None):
	table = pandas.read_excel(infile, sheet_name=sheet, dtype=dtypes)

	item_list = []
	for row in table.itertuples(index=False, name=None):
		params = {}

		for i, f in enumerate(fields):
			if f is None or pandas.isna(row[i]):
				continue

			if f in fdates:
				params[f] = parse_date(row[i])

			elif f in fgets:
				if dtypes[i] is str:
					params[f] = fgets[f][row[i].strip()]
				else:
					params[f] = fgets[f][row[i]]

			elif dtypes[i] is str:
				params[f] = row[i].strip()

			else:
				params[f] = row[i]

		if params:
			params['author'] = author

			if patients:
				params['patient'] = patients[row[1].strip()]

			if diseases:
				params['disease'] = diseases[row[1].strip()]

			item_list.append(mclass(**params))

	return mclass.objects.bulk_create(item_list)

def load_data_into_cardiomyopathy(infile, author):
	patients = load_data_into_patient(infile, author)

	sheet = 1
	dtypes = {0: str, 1: str, 2: float, 3: str, 4: str, 5: float, 6: str,
		7: str, 8: str, 9: str, 10: str, 11: str, 12: str, 13: str, 14: float,
		15: str, 16: str, 17: str, 18: str
	}
	fields = [None, None, 'body_surface', 'disease_type', 'mutate_gene', 'diagnose_age',
		'has_history', 'family_history', 'complication', 'heart_failure', 'is_survival',
		'death_time', 'arrhythmia_type', 'special_treatment', 'hospital_visits',
		'follow_time', 'sample_collect', 'test_sample', 'remain_sample']
	fdates = ['death_time', 'follow_time']

	disease_types = {v: k for k, v in CardiomyopathyDisease.DISEASE_TYPES.items()}
	disease_types.update({str(k): k for k, v in CardiomyopathyDisease.DISEASE_TYPES.items()})
	special_treats = {v: k for k, v in CardiomyopathyDisease.SPECIAL_TREATMENTS.items()}
	special_treats.update({str(k): k for k, v in CardiomyopathyDisease.SPECIAL_TREATMENTS.items()})

	family_histories = {
		'无': 0,
		'有': 1,
		'0': 0,
		'1': 1
	}

	yes_or_no = {
		'是': 1,
		'否': 2,
		'1': 1,
		'2': 2
	}

	sample_types = {v: k for k, v in CardiomyopathyDisease.SAMPLE_TYPES.items()}
	sample_types.update({str(k): k for k, v in CardiomyopathyDisease.SAMPLE_TYPES.items()})

	fgets = {'disease_type': disease_types, 'special_treatment': special_treats,
		'has_history': family_histories, 'is_survival': yes_or_no,
		'sample_collect': yes_or_no, 'test_sample': sample_types,
		'remain_sample': sample_types}

	objs = load_data_into_table(CardiomyopathyDisease, dtypes, fields, fdates, fgets, infile, sheet, author, patients=patients)
	diseases = {obj.patient.number : obj for obj in objs}


	sheet = 2
	dtypes = {0: str, 1: str, 2: float, 3: float, 4: float, 5: float, 6: float,
		7: float, 8: float, 9: float, 10: float, 11: float, 12: float, 13: float,
		14: float, 15: float, 16: float, 17: float, 18: float, 19: float, 20: float,
		21: str, 22: str, 23: str
	}
	fields = [None, None, 'wbc', 'hgb', 'hct', 'mcv', 'mch', 'mchc', 'rdw','crp',
		'alt', 'ast', 'alb', 'cr', 'tc', 'tg', 'hdlc', 'ldlc', 'apoa', 'apob', 'glu',
		'rheumatism', 'autoantibody', 'positive_result']
	fdates = []
	yes_or_no = {'阴性': 0, '阳性': 1, '0': 0, '1': 1}
	fgets = {'rheumatism': yes_or_no, 'autoantibody': yes_or_no}

	load_data_into_table(CardiomyopathyBloodRoutine, dtypes, fields, fdates, fgets, infile, sheet, author, diseases=diseases)


	sheet = 3
	dtypes = {0: str, 1: str, 2: str, 3: float, 4: float, 5: float,
		6: float, 7: float, 8: float, 9: str, 10: float, 11: str,
		12: float
	}
	fields = [None, None, 'tested', 'ckmb', 'ck', 'ctni', 'myo', 'ldh', 'ast',
		'bnpjysj', 'bnp', 'ntbnpjysj', 'ntbnp'
	]
	fdates = ['tested', 'bnpjysj', 'ntbnpjysj']
	fgets = {}

	load_data_into_table(CardiomyopathyMarker, dtypes, fields, fdates, fgets, infile, sheet, author, diseases=diseases)

	sheet = 4
	dtypes = {0: str, 1: str, 2: str, 3: str, 4: str, 5: str, 6: str,
		7: str, 8: str, 9: str}
	fields = [None, None, 'eglj', 'lnj', 'aceiarni', 'bstzdj', 'qtyw', 'kxlsc', 'kbkn', 'tszl']
	fdates = []
	yes_or_no = {
		'无': 0,
		'有': 1,
		'0': 0,
		'1': 1
	}
	fgets = {'eglj': yes_or_no, 'kxlsc': yes_or_no, 'kbkn': yes_or_no}
	load_data_into_table(CardiomyopathyTreatment, dtypes, fields, fdates, fgets, infile, sheet, author, diseases=diseases)

	sheet = 5
	dtypes = {0: str, 1: str, 2: str, 3: str, 4: str, 5: float, 6: float,
		7: float, 8: float, 9: float, 10: float, 11: float, 12: str,
		13: float, 14: str, 15: str}
	fields = [None, None, 'tested', 'code', 'age', 'lvef', 'lvfs', 'la', 'lv',
		'ra', 'rv', 'lvedd', 'lvedd_z', 'lvesd', 'lvesd_z', 'diagnosis']
	fdates = ['tested']
	fgets = {}

	load_data_into_table(CardiomyopathyUltrasound, dtypes, fields, fdates, fgets, infile, sheet, author, diseases=diseases)

	sheet = 6
	dtypes = {0: str, 1: str, 2: str, 3: str, 4: float, 5: float, 6: float,
		7: float, 8: float, 9: float, 10: float, 11: float, 12: str, 13: str,
		14: str, 15: str}
	fields = [None, None, 'tested', 'code', 'age', 'lvef', 'lvfs', 'lv', 'la',
		'rv', 'ra', 'mass', 'perfusion', 'dema', 'lge', 'microcirculation']
	fdates = ['tested']

	yes_or_no = {
		"阴性": 0,
		"阳性": 1,
		"可疑": 2,
		"是": 1,
		"否": 0,
		'0': 0,
		'1': 1,
		'2': 2
	}

	fgets = {'perfusion': yes_or_no, 'dema': yes_or_no, 'lge': yes_or_no,
		'microcirculation': yes_or_no}

	load_data_into_table(CardiomyopathyMRI, dtypes, fields, fdates, fgets, infile, sheet, author, diseases=diseases)

	sheet = 7
	dtypes = {0: str, 1: str, 2: str, 3: str, 4: float, 5: float, 6: float,
		7: float, 8: float, 9: float, 10: float, 11: str, 12: str, 13: str,
		14: str, 15: str, 16: str, 17: str, 18: str, 19: str, 20: str, 21: str, 
		22: str, 23: str, 24: str, 25: str}
	fields = [None, None, 'tested', 'age', 'xsl', 'pr', 'rv5sv1', 'qrs', 'pms', 'rv5_sv1', 'qtc',
		'cdzzlx', 'fxxlsc', 'sxxlsc', 'stt', 'cdzz', 'xfcd', 'sxzb', 'fxzb', 'zsfd', 'zffd', 'ycqb',
		'dxdgh', 'dxdgs', 'fxdgs', 'sxdgs']
	fdates = ['tested']
	yes_or_no = {
		"否": 0,
		"是": 1,
		"0": 0,
		"1": 1
	}
	cdzz_types = {v: k for k, v in CardiomyopathyECG.CDZZ_TYPES.items()}
	cdzz_types.update({str(k): k for k, v in CardiomyopathyECG.CDZZ_TYPES.items()})
	fxxlsc_types = {v: k for k, v in CardiomyopathyECG.FXXLSC_TYPES.items()}
	fxxlsc_types.update({str(k): k for k, v in CardiomyopathyECG.FXXLSC_TYPES.items()})
	sxxlsc_types = {v: k for k, v in CardiomyopathyECG.SXXLSC_TYPES.items()}
	sxxlsc_types.update({str(k): k for k, v in CardiomyopathyECG.SXXLSC_TYPES.items()})
	fgets = {'cdzzlx': cdzz_types, 'fxxlsc': fxxlsc_types, 'sxxlsc': sxxlsc_types, 'stt': yes_or_no,
		'cdzz': yes_or_no, 'xfcd': yes_or_no, 'sxzb': yes_or_no, 'fxzb': yes_or_no, 'zsfd':yes_or_no,
		'zffd': yes_or_no, 'ycqb': yes_or_no, 'dxdgh': yes_or_no, 'dxdgs': yes_or_no, 'fxdgs': yes_or_no,
		'sxdgs': yes_or_no}

	load_data_into_table(CardiomyopathyECG, dtypes, fields, fdates, fgets, infile, sheet, author, diseases=diseases)

	sheet = 8
	dtypes = {0: str, 1: str, 2: str, 3: str}
	fields = [None, None, 'company', 'tested']
	fdates = ['tested']
	fgets = {}
	objs = load_data_into_table(CardiomyopathyGeneReport, dtypes, fields, fdates, fgets, infile, sheet, author, diseases=diseases)
	gene_reports = {obj.disease.patient.number: obj for obj in objs}

	sheet = 9
	dtypes = {0: str, 1: str, 2: str, 3: str, 4: str, 5: str, 6: str, 7: str}
	fields = [None, 'report', 'gene', 'mutation', 'gnomad', 'acmg', 'gmode', 'zygote']
	fdates = []
	fgets = {'report': gene_reports}
	load_data_into_table(CardiomyopathyGeneMutation, dtypes, fields, fdates, fgets, infile, sheet, author, diseases=diseases)



	






























