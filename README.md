# btk_nanopore
Made some code for running ONT analysis with Docker.

### Make another Dockerfile to run scipt (name your image nanopore:03)
FROM nanopore:0.3

COPY nanopore.sh /opt/
RUN chmod +x /opt/nanopore.sh

ENTRYPOINT ["bash", "/opt/nanopore.sh"]

### Run docker image example
docker run \
--volume /Users/dmnemch/Projects/BTKProjects/NanoporeBTK_prj:/data:ro \
--volume /Users/dmnemch/Projects/BTKProjects/NanoporeBTK_prj:/out \
--workdir /out \
--name=porechop-fastq-PAG79814_pass_09e7ba6d_0 \
nanopore:0.1 \
porechop -i data/PAG79814_pass_09e7ba6d_0.fastq.gz -o PAG79814_pass_09e7ba6d_0.fastq.porechop.fastq.gz
