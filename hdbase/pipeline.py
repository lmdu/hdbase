import psutil
import subprocess
from pathlib import Path

__all__ = ['WESPipeline']

class AttrDict(dict):
	def __getattr__(self, attr):
		try:
			return self[attr]
		except KeyError:
			raise AttributeError

class BasePipeline:
	steps = []

	def __init__(self, task_id, params):
		self.task_id = task_id
		self.params = AttrDict(params)
		self.create_workspace()

	def create_workspace(self):
		self.work_space = Path(self.params.workdir) / self.task_id

		if not self.work_space.exists():
			self.work_space.mkdir()

	def run_command(self, cmd, inputs=None, block=True):
		proc = psutil.Popen(cmd,
			stdin = inputs,
			stdout = subprocess.PIPE,
			stderr = subprocess.PIPE
		)

		if block:
			out, err = proc.communicate()

			if proc.returncode != 0:
				raise Exception(err or out)
		else:
			return proc

class WESPipeline(BasePipeline):
	@property
	def steps(self):
		[
			{'step': 1, 'progress': 10, 'func': self.quality_control},
			{'step': 2, 'progress': 30, 'func': self.perform_mapping},
			{'step': 3, 'progress': 10, 'func': self.mark_duplicates},
		]

	def quality_control(self):
		self.read_file1 = self.work_space / "{}_r1.fq.gz".fomrat(self.task_id)
		self.read_file2 = self.work_space / "{}_r2.fq.gz".fomrat(self.task_id)
		qc_report = self.work_space / "{}_qc_report.json".fomrat(self.task_id)

		cmd = [
			'fastp',
			'-i', self.params.read1,
			'-I', self.params.read2,
			'-o', str(self.read_file1),
			'-O', str(self.read_file2),
			'-w', self.params.threads,
			'-q', self.params.fastp_quality_phred,
			'-u', self.params.fastp_percent_limit,
			'-j', str(qc_report)
		]

		self.run_command(cmd)

	def perform_mapping(self):
		assert self.read_file1.exists(), "经质控后的高质量测序数据不存在"
		assert self.read_file2.exists(), "经质控后的高质量测序数据不存在"
		self.mapping_file = self.work_space / "{}_mapping.bam".fomrat(self.task_id)

		align_cmd = [
			'bwa', 'mem', '-M',
			'-t', self.params.threads,
			self.params.bwa_index,
			self.read_file1,
			self.read_file2
		]
		align_proc = self.run_command(align_cmd, block=False)

		sort_cmd = [
			'samtools', 'sort',
			'-T', self.params.work_space,
			'-o', str(self.mapping_file),
			'-@', self.params.threads,
			'-'
		]
		self.run_command(sort_cmd, align_proc.stdout)

	def mark_duplicates(self):
		assert self.mapping_file.exists(), "Mapping结果文件不存在"

		self.metrics_file = self.work_space / "{}_markup_metrics.txt".fomrat(self.task_id)
		self.markdup_file = self.work_space / "{}_markup_mapping.bam".fomrat(self.task_id)

		cmd = [
			'/mnt/d/tools/gatk-4.6.2.0/gatk',
			'MarkDuplicates',
			'--INPUT', str(self.mapping_file),
			'--METRICS_FILE', str(self.metrics_file),
			'--OUTPUT', str(self.markdup_file),
			'--TMP_DIR', str(self.work_space),
			'--REMOVE_DUPLICATES', 'true',
			'--CREATE_INDEX', 'true'
		]
		self.run_command(cmd)

		#self.mapping_file.unlink(missing_ok=True)

	def add_read_groups(self):
		assert self.markdup_file.exists(), "PCR去重后的结果文件不存在"

		self.final_bam = self.work_space / "{}_final.bam".fomrat(self.task_id)

		cmd = [
			'/mnt/d/tools/gatk-4.6.2.0/gatk',
			'AddOrReplaceReadGroups',
			'--INPUT', str(self.markdup_file),
			'--OUTPUT', str(self.final_bam),
			'--RGID', 'lane1'
			'--RGLB', 'lib1',
			'--RGPL', self.params.sample_platform,
			'--RGPU', 'barcode1',
			'--RGSM', self.params.sample_code,
		]
		self.run_command(cmd)





