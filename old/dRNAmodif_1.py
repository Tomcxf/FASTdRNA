##################################
# A pipeline for ONT_dRNA_seq written by Chen X.F
##################################
#EXA={"S1R1","S1R2","S2R1","S2R2"}
#ref="RGF"
#fast5="fast"
configfile: "config.yaml"
#################################
rule all:
    input:
        expand("{example}/analysis/modification/{example}_collapsed.tsv",example=EXA)

rule eventalign:
    input:
        expand("{example}/analysis/{example}.fastq",example=EXA),
        expand("{example}/analysis/slow5/file.blow5",example=EXA),
        expand("{example}/analysis/mapping/{example}_transcript.bam",example=EXA),
        "{ref}"
    output:
        expand("{example}/analysis/modification/{example}_eventalign.tsv",example=EXA)
    shell：
        "nanopolish index {input[0]} --slow5 {input[1]}| nanopolish eventalign --reads {input[0]} --bam {input[2]}  --genome {input[3]} --print-read-names --scale-events --samples > {output}"


rule collapse:
    input:
        expand("{example}/analysis/modification/{example}_eventalign.tsv",example=EXA)
    output:
        expand("{example}/analysis/modification/{example}_collapsed.tsv",example=EXA)
    shell:
        "nanocompore eventalign_collapse -t 6 -i {input} -o {output}"
