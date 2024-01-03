##################################
# A pipeline for ONT_dRNA_seq written by Chen X.F
##################################
S1R1="AAA"
S1R2="BBB"
S2R1="CCC"
S2R2="DDD"
ref="RGF"
sample1="111"
sample2="222"
#################################
rule all:
    input:
        "modification/results/simulated_report.tsv",
        "modification/results/simulated_shift.tsv",
        "modification/results/simulated_sig_positions.bed"
rule sampcomp:
    input:
        expand("{Sa1Re1}/analysis/modification/{Sa1Re1}_collapsed.tsv",Sa1Re1=S1R1),
        expand("{Sa1Re2}/analysis/modification/{Sa1Re2}_collapsed.tsv",Sa1Re2=S1R2),
        expand("{Sa2Re1}/analysis/modification/{Sa2Re1}_collapsed.tsv",Sa2Re1=S2R1),
        expand("{Sa2Re2}/analysis/modification/{Sa2Re2}_collapsed.tsv",Sa2Re2=S2R2),
        "{ref}"
    output:
        "modification"
    params:
        {sample1},
        {sample2}
    shell:
        "nanocompore sampcomp --file_list1 {input[0]} , {input[1]} --file_list2 {input[2]} , {input[3]} --label1 {params[0]} --label2 {params[1]} --fasta {input[4]} --outpath {output}"

rule follow:
    input:
        "modification",
        "{ref}"
    output:
        "modification/results/simulated_report.tsv",
        "modification/results/simulated_shift.tsv",
        "modification/results/simulated_sig_positions.bed"
    script:
        "modification.py"
