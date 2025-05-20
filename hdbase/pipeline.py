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
			{'step': 1, 'progress': 10, 'message': "质量控制", 'func': self.quality_control},
			{'step': 2, 'progress': 30, 'message': "Mapping", 'func': self.perform_mapping},
			{'step': 3, 'progress': 35, 'message': "去除PCR重复", 'func': self.mark_duplicates},
			{'step': 4, 'progress': 40, 'message': "添加reads分组信息", 'func': self.add_read_groups},
			{'step': 5, 'progress': 60, 'message': "重校对碱基质量", 'func': self.recalibrate_base_quality},
			{'step': 6, 'progress': 80, 'message': "应用重校对碱基", 'func': self.apply_base_recalibrator},
			{'step': 7, 'progress': 100, 'message': "搜索变异位点", 'func': self.call_variants},
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
			'gatk',
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

		self.fixed_bam = self.work_space / "{}_fixed.bam".fomrat(self.task_id)

		cmd = [
			'gatk',
			'AddOrReplaceReadGroups',
			'--INPUT', str(self.markdup_file),
			'--OUTPUT', str(self.fixed_bam),
			'--RGID', 'lane1'
			'--RGLB', 'lib1',
			'--RGPL', self.params.sample_platform,
			'--RGPU', 'barcode1',
			'--RGSM', self.params.sample_code,
			'--CREATE_INDEX', 'true',
			'--TMP_DIR', str(self.work_space)
		]
		self.run_command(cmd)

		#self.markdup_file.unlink(missing_ok=True)

	def recalibrate_base_quality(self):
		assert self.fixed_bam.exists(), "修复后的比对结果文件不存在"

		self.recal_table = self.work_space / "{}_recal.table".fomrat(self.task_id)

		cmd = [
			'gatk',
			'BaseRecalibrator',
			'--input', str(self.fixed_bam),
			'--output', str(self.recal_table),
			'--reference', self.params.reference,
		]
		self.run_command(cmd)

	def apply_base_recalibrator(self):
		assert self.recal_table.exists(), "碱基质量分数重校对表格不存在"

		self.final_bam = self.work_space / "{}_final.bam".fomrat(self.task_id)

		cmd = [
			'gatk',
			'ApplyBQSR',
			'--reference', self.params.reference,
			'--input', str(final_bam),
			'--bqsr-recal-file', str(recal_table),
			'--output', str(self.final_bam)
		]
		self.run_command(cmd)

	def call_variants(self):
		self.vcf_file = self.work_space / "{}.vcf.gz".fomrat(self.task_id)

		cmd = [
			'gatk',
			'HaplotypeCaller',
			'--reference', self.params.reference,
			'--input', str(self.final_bam),
			'--output', str(self.vcf_file)
		]
		self.run_command(cmd)

	def select_variants(self):
		pass








