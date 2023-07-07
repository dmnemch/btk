# requirements: porechop, cutadapt, canu, minimap2

import argparse
import subprocess
import os
import glob

def get_args():
  parser = argparse.ArgumentParser(prog='run_ont', description='Pipeline for hybrid BGI and ONT')
  parser.add_argument('--ont', type=str, help='FASTQ filedir with subdirs with FASTQ files', required=True)
  parser.add_argument('--bgi', type=str, help='dir with BAM files')
  parser.add_argument('-o', '--out', type=str, help='Output dir for everything')
  parser.add_argument('-t', '--threads', type=int, default=8, help='THREADS')
  parser.add_argument('-r', '--ref', help='Genome reference .MMI file or .FA file')
  parser.add_argument('-g', '--genomesize', default="3.4g", help='GENOME_SIZE')
  return parser.parse_args()

def makedirs(sample):
  cmd = f"mkdir -p out/{sample}/"
  subprocess.run(cmd, shell=True)
    
def porechop(ont, sample, threads):
  cmd = f"porechop -i {ont}  -t {threads} -o out/{sample}/{sample}.porechop.fastq.gz"
  subprocess.run(cmd, shell=True)

def cutadapt(sample, threads):
  cmd = f"cutadapt --cores {threads} --trim-n --quality-cutoff 20,20 --minimum-length 0 -o out/{sample}/{sample}.cutadapt.porechop.fastq.gz out/{sample}/{sample}.porechop.fastq.gz"
  subprocess.run(cmd, shell=True)

def canu(sample, genome_size):
  cmd = f"canu -correct -p {sample} -d out/{sample}/ genomeSize={genome_size} minInputCoverage=0 -nanopore-trimmed out/{sample}.cutadapt.porechop.fastq.gz"
  subprocess.run(cmd, shell=True)    
    
def minimap2(ref, sample, threads):
  cmd = f"minimap2 -a {ref} out/{sample}/{sample}.canu.cutadapt.porechop.fastq.gz -t {threads} > out/{sample}/{sample}.sam"
  subprocess.run(cmd, shell=True)

def ont(ont, ref, threads, genome_size):
  sample = str(ont.split("/")[-1].split(".")[:-2]).strip("[]")
  makedirs(sample)
  porechop(ont, sample, threads)
  cutadapt(sample, threads)
  canu(sample, genome_size)
  minimap2(ref, sample, threads)
  
def main():
  args = get_args()
  for fastq in glob.glob(f'{ont}/*.fastq*'):
    ont(fastq, args.ref, args.threads, args.genomesize)
  # make parallel/pipe
  # make hybrid analysis
  # make exeption handling
  return 'Done'

if __name__ == '__main__':
  main()
