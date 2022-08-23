##################################
# A pipeline for ONT_dRNA_seq written by Chen X.F
##################################
ref="analysis/RGF"
EXA = "XXX"
##################################
rule all:
    input:
        "analysis/polyA_estimate/polyA_estimate.tsv"


rule polyA_estimate:
    input:
        expand("analysis/{example}.fastq",example=EXA),
        "analysis/slow5/midbolw5_dir",
        expand("analysis/mapping/{example}_transcript.bam",example=EXA)",
        "{ref}"
    output:
        "analysis/polyA_estimate/polya_results.tsv"
    shell:
        "nanopolish index {input[0]} --slow5 {input[1]} | nanopolish polya --reads {input[0]} --bam {input[2]} --genome {input[3]} > {output}"
rule polyA_mid_results_1:
    input:
        "analysis/polyA_estimate/polya_results.tsv"
    output:
        "analysis/polyA_estimate/polya_results.pass_only.tsv"
    shell:
        "grep 'PASS' {input} > {output}"

rule polyA_mid_results_2:
    input:
        "analysis/polyA_estimate/polya_results.tsv"
    output:
        "analysis/polyA_estimate/header.tsv"
    shell:
        "head -1 {input} > {output}"

rule polyA_results:
    input:
        "analysis/polyA_estimate/header.tsv",
        "analysis/polyA_estimate/polya_results.pass_only.tsv"
    output:
        "analysis/polyA_estimate/polyA_estimate.tsv"
    shell:
        "cat {input[0]} {input[1]} > {output}"
