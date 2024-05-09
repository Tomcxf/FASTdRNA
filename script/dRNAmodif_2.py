##################################
# A pipeline for ONT_dRNA_seq written by Chen X.F
##################################
#S1R1="AAA"
#S1R2="BBB"
#S2R1="CCC"
#S2R2="DDD"
#ref="RGF"
#sample1="111"
#sample2="222"
configfile: "./configForModifAS.yaml"
#################################
S1R1= config["S1R1"]
S1R2= config["S1R2"]
S2R1= config["S2R1"]
S2R2= config["S2R2"]
ref= config["ref"]
sample1= config["sample1"]
sample2= config["sample2"]

rule all:
    input:
        "./modification/results/simulated_report.tsv",
        "./modification/results/simulated_shift.tsv",
        #"./modification/results/simulated_sig_positions.bed"
rule sampcomp:
    input:
        expand("./{Sa1Re1}/analysis/modification/WT1_collapsed/out_eventalign_collapse.tsv",Sa1Re1=S1R1),
        expand("./{Sa1Re2}/analysis/modification/WT2_collapsed/out_eventalign_collapse.tsv",Sa1Re2=S1R2),
        expand("./{Sa2Re1}/analysis/modification/{Sa2Re1}_collapsed/out_eventalign_collapse.tsv",Sa2Re1=S2R1),
        expand("./{Sa2Re2}/analysis/modification/{Sa2Re2}_collapsed/out_eventalign_collapse.tsv",Sa2Re2=S2R2),
        expand("{ref}",ref=ref)
    output:
        directory("./modification/sampcomp"),
        #"./modification/sampcomp/simulated_SampComp.db"
    params:
        {sample1},
        {sample2}
    threads:
        8
    shell:
        "nanocompore sampcomp --file_list1 {input[0]},{input[1]} --file_list2 {input[2]},{input[3]} --label1 {params[0]} --label2 {params[1]} --fasta {input[4]} --outpath {output[0]} --overwrite -t 8"

rule follow:
    input:
        "./modification/sampcomp/",
        expand("{ref}",ref=ref)
    output:
        "./modification/results/simulated_report.tsv",
        "./modification/results/simulated_shift.tsv",
        #"./modification/results/simulated_sig_positions.bed"
    params:
        "./modification/sampcomp/outSampComp.db"
    script:
        "./modification.py"
