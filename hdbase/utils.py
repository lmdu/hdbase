import pyorthanc

def upload_dicoms(dicom_files):
	client = pyorthanc.Orthanc('http://localhost:8042')
	res = pyorthanc.upload(client, dicom_files)

	for item in res:
		return item['ParentStudy']

def memory_format(size):
	for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
		if size < 1024:
			break

		size /= 1024

	return "{:.2f}{}".format(size, unit)