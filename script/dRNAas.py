##################################
# A pipeline for ONT_dRNA_seq written by Chen X.F
##################################
#S1R1="S1R1"
#S1R2="S1R2"
#S2R1="S2R1"
#S2R2="S2R2"

#ref="RGF"
configfile: "./configForModifAS.yaml"

#################################
S1R1= config["S1R1"]
S1R2= config["S1R2"]
S2R1= config["S2R1"]
S2R2= config["S2R2"]
gtf= config["ref"]
filetype = [".dpsi",".psivec"]
import glob
rule all:
    input:
        #"AlternativeSplicing/localAS/diff/Con1vs2.psivec",
        #"AlternativeSplicing/localAS/diff/Con1vs2.dpsi"
        #"AlternativeSplicing/localAS/allevents.ioe"
        #directory("AlternativeSplicing/localAS/diff/")
        expand("./Con1vs2{ft}",ft = filetype)
rule generateEvents:
    input:
        expand("{gtf}",gtf=gtf) 
    params:
        "AlternativeSplicing/localAS/",
        #"\{SE,SS,MX,RI,FL\}"
        #"AlternativeSplicing/localAS/*.ioe"
	ioe_files=lambda wildcards: glob.glob("AlternativeSplicing/localAS/*.ioe")
    output:
        "AlternativeSplicing/localAS/allevents.ioe"
    shell:
        #"mkdir AlternativeSplicing | mkdir AlternativeSplicing/localAS | "
        "suppa.py generateEvents -i {input} -o {params[0]} -f ioe -e {{SE,SS,MX,RI,FL}} -p | awk 'FNR==1 && NR!=1 {{ while (/^<header>/) getline; }} 1 {{print}}' {params.ioe_files} > {output}"

#rule generateEvents2:
#    input:
#        "AlternativeSplicing/localAS/*.ioe"
#    output:
#        "AlternativeSplicing/localAS/allevents.ioe"
#    shell:
#        "awk 'FNR==1 && NR!=1 {{ while (/^<header>/) getline; }} 1 {print}' {input} > {output}"

rule extractTpm:
    input:
        expand("./{S1R1}/analysis/count/{S1R1}_transcript_counts.csv",S1R1=S1R1)
    output:
        expand("./{S1R1}/analysis/count/{S1R1}_transcript_counts.tpm",S1R1=S1R1)
    shell:
        "cut -f 1,4 {input} > {output}"

rule extractTpm2:
    input:
        expand("./{S1R2}/analysis/count/{S1R2}_transcript_counts.csv",S1R2=S1R2)
    output:
        expand("./{S1R2}/analysis/count/{S1R2}_transcript_counts.tpm",S1R2=S1R2)
    shell:
        "cut -f 1,4 {input} > {output}"

rule extractTpm3:
    input:
        expand("./{S2R1}/analysis/count/{S2R1}_transcript_counts.csv",S2R1=S2R1)
    output:
        expand("./{S2R1}/analysis/count/{S2R1}_transcript_counts.tpm",S2R1=S2R1)
    shell:
        "cut -f 1,4 {input} > {output}"

rule extractTpm4:
    input:
        expand("./{S2R2}/analysis/count/{S2R2}_transcript_counts.csv",S2R2=S2R2)
    output:
        expand("./{S2R2}/analysis/count/{S2R2}_transcript_counts.tpm",S2R2=S2R2)
    shell:
        "cut -f 1,4 {input} > {output}"


rule joinFilesCond1:
    input:
        expand("./{S1R1}/analysis/count/{S1R1}_transcript_counts.tpm",S1R1=S1R1),
        expand("./{S1R2}/analysis/count/{S1R2}_transcript_counts.tpm",S1R2=S1R2)
    params:
        "AlternativeSplicing/localAS/Condition1"
    output:
        "AlternativeSplicing/localAS/Condition1.tpm"
    shell:
        "suppa.py joinFiles -f tpm -i {input[0]} {input[1]} -o {params}"

rule joinFilesCond2:
    input:
        expand("./{S2R1}/analysis/count/{S2R1}_transcript_counts.tpm",S2R1=S2R1),
        expand("./{S2R2}/analysis/count/{S2R2}_transcript_counts.tpm",S2R2=S2R2)
    params:
        "AlternativeSplicing/localAS/Condition2"
    output:
        "AlternativeSplicing/localAS/Condition2.tpm"
    shell:
        "suppa.py joinFiles -f tpm -i {input[0]} {input[1]} -o {params}"

rule PSI_Con1:
    input:
        "AlternativeSplicing/localAS/allevents.ioe",
        "AlternativeSplicing/localAS/Condition1.tpm"
    params:
        "AlternativeSplicing/localAS/Condition1"
    output:
        "AlternativeSplicing/localAS/Condition1.psi"
    shell:
        "suppa.py psiPerEvent --ioe-file {input[0]} --expression-file {input[1]} -o {params}"

rule PSI_Con2:
    input:
        "AlternativeSplicing/localAS/allevents.ioe",
        "AlternativeSplicing/localAS/Condition2.tpm"
    params:
        "AlternativeSplicing/localAS/Condition2"
    output:
        "AlternativeSplicing/localAS/Condition2.psi"
    shell:
        "suppa.py psiPerEvent --ioe-file {input[0]} --expression-file {input[1]} -o {params}"

rule diffsplice:
    input:
        "AlternativeSplicing/localAS/allevents.ioe",
        "AlternativeSplicing/localAS/Condition1.psi",
        "AlternativeSplicing/localAS/Condition2.psi",
        "AlternativeSplicing/localAS/Condition1.tpm",
        "AlternativeSplicing/localAS/Condition2.tpm"
    params:
        "Con1vs2"
    output:
        #"AlternativeSplicing/localAS/diff/Con1vs2.dpsi",
        #"AlternativeSplicing/localAS/diff/Con1vs2.psivec"
        multiext("./Con1vs2",".dpsi",".psivec")
    shell: 
        "suppa.py diffSplice --method empirical --input {input[0]} --psi {input[1]} {input[2]} --tpm {input[3]} {input[4]} --area 1000 --lower-bound 0.05 -gc -o {params}"

#rule cluster:
#    input:
#        "AlternativeSplicing/localAS/Con1vs2.psivec",
#        "AlternativeSplicing/localAS/Con1vs2.dpsi"
#    output:
#        "AlternativeSplicing/localAS/cluster"
#    shell:
#        "suppa.py clusterEvents --dpsi {input[0]} --psivec {input[1]} --sig-threshold 0.1 --eps 0.1 --min-pts 20 --groups 1-2,3-4 -o <output-file>" 

#rule trans_gE:
#    input:
#        {ref}
#    output:
#        "AlternativeSplicing/transcript"
#    shell:
#        "mkdir AlternativeSplicing/transcript | suppa.py generateEvents -i {input} -o {output}/local -f ioe -e {SE,SS,MX,RI,FL}"

