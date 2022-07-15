FROM 812206152185.dkr.ecr.us-west-2.amazonaws.com/latch-base:02ab-main

RUN apt-get install -y curl unzip

RUN pip install merge-fastq

COPY merged_fastq_R1.fastq root/merged_fastq_R1.fastq
COPY merged_fastq_R2.fastq root/merged_fastq_R2.fastq



# STOP HERE:
# The following lines are needed to ensure your build environement works
# correctly with latch.
COPY wf /root/wf
ARG tag
ENV FLYTE_INTERNAL_IMAGE $tag
RUN python3 -m pip install --upgrade latch
WORKDIR /root
