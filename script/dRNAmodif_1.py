##################################
# A pipeline for ONT_dRNA_seq written by Chen X.F
##################################
#EXA={"S1R1","S1R2","S2R1","S2R2"}
#ref="RGF"
#fast5="fast"
configfile: "./configForMainTail.yaml"
EXA = config["EXA"]
ref= config["ref"]
fast5= config["fast5"]

#################################
rule all:
    input:
        directory(expand("{example}/analysis/modification/{example}_collapsed",example=EXA))


rule slow_index:
    input:
        expand("./{example}/analysis/{example}.fastq",example=EXA),
        expand("./{example}/analysis/slow5/file.blow5",example=EXA)
    output:
        "./{example}/analysis/slow5/file.slow5.idx"
    threads:16
    shell:
        "f5c_x86_64_linux_cuda index --slow5 {input[1]} {input[0]}"


rule eventalign:
    input:
        expand("{example}/analysis/{example}.fastq",example=EXA),
        expand("{example}/analysis/slow5/file.blow5",example=EXA),
        expand("{example}/analysis/mapping/{example}_transcript.bam",example=EXA),
        expand("{ref}",ref=ref)
    output:
        expand("{example}/analysis/modification/{example}_eventalign.tsv",example=EXA)
    #threads:16
    shell:
        "f5c_x86_64_linux_cuda eventalign  --print-read-names --scale-events --samples --slow5 {input[1]} -b {input[2]} -g {input[3]} -r {input[0]} -t 8 --rna > {output}"


rule collapse:
    input:
        expand("{example}/analysis/modification/{example}_eventalign.tsv",example=EXA)
    output:
        directory(expand("{example}/analysis/modification/{example}_collapsed",example=EXA))
    threads:16
    shell:
        "nanocompore eventalign_collapse -t 6 -i {input} -o {output}"
