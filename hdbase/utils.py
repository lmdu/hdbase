import pyorthanc

def upload_dicoms(dicom_files):
	client = pyorthanc.Orthanc('http://localhost:8042')
	res = pyorthanc.upload(client, dicom_files)

	for item in res:
		return item['ParentStudy']
