##################################
# A pipeline for ONT_dRNA_seq written by Chen X.F
# RNA modification module (Nanocompore sampcomp)
##################################
configfile: "./configForModifAS.yaml"

#################################
# Configuration
#   fasta      : transcriptome FASTA used by nanocompore (--fasta)
#   conditions : {condition_name: [replicate_sample, ...]}
#                replicate sample names must match the project names (EXA)
#                produced by dRNAmain / collapsed by dRNAmodif_1.
#################################
FASTA = config["fasta"]
CONDITIONS = config["conditions"]
COND_NAMES = list(CONDITIONS.keys())

# Nanocompore sampcomp compares exactly two conditions.
if len(COND_NAMES) != 2:
    raise ValueError(
        "dRNAmodif_2 sampcomp compares exactly two conditions, but config "
        "'conditions' has %d: %s" % (len(COND_NAMES), COND_NAMES)
    )
COND1, COND2 = COND_NAMES


def collapse_tsv(sample):
    """Collapsed eventalign produced by dRNAmodif_1 for one sample."""
    return ("%s/analysis/modification/%s_collapsed/"
            "out_eventalign_collapse.tsv" % (sample, sample))


def condition_collapse(condition):
    return [collapse_tsv(s) for s in CONDITIONS[condition]]


rule all:
    input:
        "modification/results/simulated_report.tsv",
        "modification/results/simulated_shift.tsv"

# Compare modification signal between the two conditions.
# file_list1/2 accept any number of replicates (comma-separated).
rule sampcomp:
    input:
        cond1 = condition_collapse(COND1),
        cond2 = condition_collapse(COND2),
        fasta = FASTA
    output:
        directory("modification/sampcomp")
    params:
        label1 = COND1,
        label2 = COND2,
        file_list1 = lambda wildcards, input: ",".join(input.cond1),
        file_list2 = lambda wildcards, input: ",".join(input.cond2)
    threads: 8
    shell:
        "nanocompore sampcomp "
        "--file_list1 {params.file_list1} --file_list2 {params.file_list2} "
        "--label1 {params.label1} --label2 {params.label2} "
        "--fasta {input.fasta} --outpath {output} --overwrite -t {threads}"

# Turn the SampComp database into a report + per-condition shift statistics.
rule follow:
    input:
        sampcomp = "modification/sampcomp",
        fasta = FASTA
    output:
        "modification/results/simulated_report.tsv",
        "modification/results/simulated_shift.tsv"
    params:
        db = "modification/sampcomp/outSampComp.db"
    script:
        "modification.py"
