##################################
# A pipeline for ONT_dRNA_seq written by Chen X.F
##################################
#EXA = "XXX"
#cfgfile = "CCC"
#ref="RGF"
#fast5="fast"
configfile: "config.yaml"
#################################
EXA = config["EXA"]
cfgfile= config["cfgfile"]
ref= config["ref"]
fast5= config["fast5"]

rule all :
    input:  
        expand("{example}/analysis/{example}.fastq",example=EXA),
        expand("{example}/analysis/nanoplot",example=EXA),
        expand("{example}/analysis/mapping/{example}_transcript.bam",example=EXA),
        expand("{example}/analysis/count/{example}_transcript_counts.csv",example=EXA),
        expand("{example}/analysis/slow5/file.blow5",example=EXA)

rule slow5_f2s:
    input:
        "{fast5}"
    output:
        "{example}/analysis/slow5/midbolw5_dir"
    shell:
        "slow5tools f2s {input} -d {output}  -p 8"

rule slow5_merge:
    input:
        "{example}/analysis/slow5/midbolw5_dir"
    output:
        "{example}/analysis/slow5/file.blow5"
    shell:
        "slow5tools merge {input} -o {output} -t 8 | rm -rf {input}"

rule slow5_split:
    input:
        "{example}/analysis/slow5/file.blow5"
    output:
        "{example}/analysis/slow5/bolw5_dir"
    shell:
        "slow5tools split {input} -d {output} -r 4000"

rule slow5_convert:
    input:
        "{example}/analysis/slow5/bolw5_dir"
    output:
        "{example}/analysis/fast5"
    shell:
        "slow5tools s2f {input} -d {output}  -p 8"


rule basecall:
    input:
        "{example}/analysis/fast5",
        expand("{cfg}.cfg",cfg=cfgfile)
    output:
        "{example}/analysis/basecall"
    shell:
        "guppy_basecaller -c {input[1]} -i {input[0]} -s {output}"

rule Fastq data management:
    input:
        "{example}/analysis/basecall"
    output:
        "{example}/analysis/{example}.fastq"
    shell:
        "pyBioTools Fastq Filter -i {input}/pass -o {output}"

rule nanoplot_visual:
    input:
        "{example}/analysis/basecall"
    output:
        "{example}/analysis/nanoplot"
    shell:
        "Nanoplot --summary {input}/sequencing_summary.txt --loglength -o {output}"
     
rule mapping:
    input:
        "{ref}",
        "{example}/analysis/{example}.fastq"
    output:
        "{example}/analysis/mapping/{example}_transcript.sam"
    shell:
        "minimap2 -ax map-ont -splice -uf -k14 -t 4 -p 0 -N 10 {input[0]} {input[1]} > {output}"

rule sam_sort:
    input:
        "{example}/analysis/mapping/{example}_transcript.sam"
    output:
        "{example}/analysis/mapping/{example}_transcript.bam"
    shell:
        "samtools sort -@ 4 -O bam -o {output} {input}"

rule transcript_count:
    input:
        "{example}/analysis/mapping/{example}_transcript.bam"
    output:
        "{example}/analysis/count/{example}_transcript_counts.csv"
    shell:
        "NanoCount -i {input} -o {output}"
