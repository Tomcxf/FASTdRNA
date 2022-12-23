##################################
# A pipeline for ONT_dRNA_seq written by Chen X.F
##################################
#S1R1="S1R1"
#S1R2="S1R2"
#S2R1="S2R1"
#S2R2="S2R2"

#ref="RGF"
configfile: "config.yaml"

#################################



rule generateEvents:
    input:
        {ref}
    output:
        "AlternativeSplicing/localAS"
    shell:
        "mkdir AlternativeSplicing | mkdir AlternativeSplicing/localAS | suppa.py generateEvents -i {input} -o {output}/local -f ioe -e {SE,SS,MX,RI,FL}"

rule generateEvents2:
    input:
        "AlternativeSplicing/localAS"
    output:
        "AlternativeSplicing/localAS/allevents.ioe"
    shell：
        "awk 'FNR==1 && NR!=1 { while (/^<header>/) getline; } 1 {print}' {input}/*.ioe > output[0]"

rule joinFilesCond1:
    input:
        {S1R1},
        {S1R2}
    output:
        "AlternativeSplicing/localAS/Condition1"
    shell：
        "suppa.py joinFiles -f tpm -i {input[0]} {input[1]} -o {output}"

rule joinFilesCond1:
    input:
        {S2R1},
        {S2R2}
    output:
        "AlternativeSplicing/localAS/Condition2"
    shell：
        "suppa.py joinFiles -f tpm -i {input[0]} {input[1]} -o {output}"

rule PSI_Con1:
    input:
        "AlternativeSplicing/localAS/allevents.ioe",
        "AlternativeSplicing/localAS/Condition1"
    output:
        "AlternativeSplicing/localAS/Condition1"
    shell：
        "suppa.py psiPerEvent --ioe-file {input[0]} --expression-file {input[1]}.tpm -o {output}"

rule PSI_Con2:
    input:
        "AlternativeSplicing/localAS/allevents.ioe",
        "AlternativeSplicing/localAS/Condition2"
    output:
        "AlternativeSplicing/localAS/Condition2"
    shell：
        "suppa.py psiPerEvent --ioe-file {input[0]} --expression-file {input[1]}.tpm -o {output}"

rule diffsplice:
    input:
        "AlternativeSplicing/localAS/allevents.ioe",
        "AlternativeSplicing/localAS/Condition1",
        "AlternativeSplicing/localAS/Condition2",
        "AlternativeSplicing/localAS/Condition1",
        "AlternativeSplicing/localAS/Condition2"
    output:
        "AlternativeSplicing/localAS/Con1vs2"
    shell： 
        "suppa.py diffSplice --method empirical --input {input[0]} --psi {input[1]}.psi {input[2]}.psi --tpm {input[3]}.tpm {input[4]}.tpm --area 1000 --lower-bound 0.05 -gc -o {output}"

rule cluster:
    input:
        "AlternativeSplicing/localAS/Con1vs2"
    output:
        "AlternativeSplicing/localAS/cluster"
    shell:
        "suppa.py clusterEvents --dpsi {input}.dpsi --psivec {input}.psivec --sig-threshold 0.1 --eps 0.1 --min-pts 20 --groups 1-2,3-4 -o <output-file>" 

rule trans_gE:
    input:
        {ref}
    output:
        "AlternativeSplicing/transcript"
    shell:
        "mkdir AlternativeSplicing/transcript | suppa.py generateEvents -i {input} -o {output}/local -f ioe -e {SE,SS,MX,RI,FL}"

