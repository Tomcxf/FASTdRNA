##################################
# A pipeline for ONT_dRNA_seq written by Chen X.F
##################################
#ref="analysis/RGF"
#EXA = "XXX"
configfile: "./configForMainTail.yaml"
##################################
EXA = config["EXA"]
cfgfile= config["cfgfile"]
ref= config["ref"]
fast5= config["fast5"]



rule all:
    input:
        expand("./{example}/analysis/polyA_estimate/polyA_estimate.tsv",example=EXA)

rule samtools_index:
    input:
        expand("./{example}/analysis/mapping/{example}_transcript.bam",example=EXA)
    output:
        expand("./{example}/analysis/mapping/{example}_transcript.bam.bai",example=EXA)
    shell:
        "samtools index {input}"

rule slow_index:
    input:
        expand("./{example}/analysis/{example}.fastq",example=EXA),
        expand("./{example}/analysis/slow5/file.blow5",example=EXA)
    output:
        "./{example}/analysis/slow5/file.slow5.idx"
    threads:16
    benchmark:
        "./{example}/analysis/polyA_estimate/slow5_index.txt"
    shell:
        "/home/chenxf/tools/nanopolish index {input[0]} --slow5 {input[1]}"

rule polyA_estimate:
    input:
        expand("./{example}/analysis/{example}.fastq",example=EXA),
        expand("./{example}/analysis/mapping/{example}_transcript.bam",example=EXA),
        expand("{ref}",ref=ref)
    output:
        "./{example}/analysis/polyA_estimate/polya_results.tsv"
    threads:16
    benchmark:
        "./{example}/analysis/polyA_estimate/polyA_estimate_record.txt"
    shell:
        "/home/chenxf/tools/nanopolish polya --reads {input[0]} --bam {input[1]} --genome {input[2]} > {output}"
rule polyA_mid_results_1:
    input:
        "./{example}/analysis/polyA_estimate/polya_results.tsv"
    output:
        "./{example}/analysis/polyA_estimate/polya_results.pass_only.tsv",
        "./{example}/analysis/polyA_estimate/header.tsv"
    shell:
        "grep 'PASS' {input} > {output[0]} | head -1 {input} > {output[1]}"

#rule polyA_mid_results_2:
#    input:
#        "./{example}/analysis/polyA_estimate/polya_results.tsv"
#    output:
#        "./{example}/analysis/polyA_estimate/header.tsv"
#    shell:
#        "head -1 {input} > {output}"

rule polyA_results:
    input:
        "./{example}/analysis/polyA_estimate/header.tsv",
        "./{example}/analysis/polyA_estimate/polya_results.pass_only.tsv"
    output:
        "./{example}/analysis/polyA_estimate/polyA_estimate.tsv"
    shell:
        "cat {input[0]} {input[1]} > {output}"

rule R_drawing:
    input:
        "./{example}/analysis/polyA_estimate/polyA_estimate.tsv"
    output:
        "./{example}/analysis/polyA_estimate/polyA_estimate.pdf"
    script:
        "./Tail.R"

