"""
Pool fastq files for bulk assembly
"""
import subprocess
from pathlib import Path
import os

from latch import small_task, medium_task, large_task, large_gpu_task, workflow
from latch.types import LatchFile, LatchDir
from latch.types.glob import file_glob
from typing import Optional
import glob


@small_task
def pool_task(fq_files: LatchDir, output_dir: LatchDir) -> (LatchFile, LatchFile):

    
    out_basename = str(output_dir.remote_path)
    
    read1 = glob.glob(f'{fq_files.local_path}/*_1*')
    read2 = glob.glob(f'{fq_files.local_path}/*_2*')
    full1 = []
    for i in read1:
        full1.append(i)
    full2 = []
    for i in read2:
        full2.append(i)
    
    print(full1,"buffer",full2)
    with open('root/merged_fastq_1.fastq', 'w') as outfile:
        for fname in full1:
            with open(fname) as infile:
                for line in infile:
                    outfile.write(line)

    
    with open('root/merged_fastq_2.fastq', 'w') as outfile:
        for fname in full2:
            with open(fname) as infile:
                for line in infile:
                    outfile.write(line)

    
    
    
    merge = ["merge_fastq"]
    _merge_cmd = merge + full1 + full2
    print(full1)
    print(full2)
    
		
    subprocess.run(_merge_cmd)

    return (
    LatchFile("root/merged_fastq_1.fastq",f"{out_basename}/merged_fastq_1.fastq"), 
    LatchFile("root/merged_fastq_2.fastq",f"{out_basename}/merged_fastq_2.fastq")
    )


@workflow
def pool_wf(fq_files: LatchDir, output_dir: LatchDir) -> (LatchFile, LatchFile):
    """Pool fastq files for pooled assemblies

    # Fastpool
This is a simple tool that takes a directory of paired end 
fastq reads and outputs 2 single paired end reads for use in a pooled assembly.

    __metadata__:
        display_name: Fastpool
        author: Corey Howe
            name: 
            email: coreyhowe99 at gmail dot com
            github: https://github.com/coreyhowe
        repository: https://github.com/coreyhowe/latch_fastpool
        license:
            id: 

    Args:

        fq_files:
          Directory containing all paired end fastq files. Paired end filenames must contain "_1" or "_2". 

          __metadata__:
            display_name: fastq files input

        output_dir:
          Output directory

          __metadata__:
            display_name: Output directory
    """
    return pool_task(fq_files=fq_files, output_dir=output_dir)
