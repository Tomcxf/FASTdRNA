##################################
# A pipeline for ONT_dRNA_seq written by Chen X.F
# Alternative-splicing module (SUPPA2)
##################################
configfile: "./configForModifAS.yaml"

#################################
# Configuration
#   ref        : GTF annotation used by suppa generateEvents
#   conditions : {condition_name: [replicate_sample, ...]}
#                replicate sample names must match the project names (EXA)
#                produced by dRNAmain. Add conditions/replicates here only;
#                the rules below adapt automatically.
#################################
GTF = config["ref"]
CONDITIONS = config["conditions"]
COND_NAMES = list(CONDITIONS.keys())

# SUPPA diffSplice compares exactly two conditions.
if len(COND_NAMES) != 2:
    raise ValueError(
        "dRNAas diffSplice compares exactly two conditions, but config "
        "'conditions' has %d: %s" % (len(COND_NAMES), COND_NAMES)
    )
COND1, COND2 = COND_NAMES
COMPARISON = "%svs%s" % (COND1, COND2)

AS_DIR = "AlternativeSplicing/localAS"

wildcard_constraints:
    sample = r"[^/]+",
    condition = r"[^/]+"


def condition_tpm(wildcards):
    """All replicate .tpm files belonging to one condition."""
    return [
        "%s/analysis/count/%s_transcript_counts.tpm" % (s, s)
        for s in CONDITIONS[wildcards.condition]
    ]


rule all:
    input:
        multiext(COMPARISON, ".dpsi", ".psivec")

# Generate all AS events from the annotation and merge them into one ioe.
rule generateEvents:
    input:
        GTF
    output:
        AS_DIR + "/allevents.ioe"
    params:
        prefix = AS_DIR + "/events"
    shell:
        "suppa.py generateEvents -i {input} -o {params.prefix} -f ioe -e SE SS MX RI FL -p && "
        "awk 'FNR==1 && NR!=1 {{ while (/^<header>/) getline; }} 1' {params.prefix}*.ioe > {output}"

# One rule for every replicate: counts -> TPM (handles all samples).
rule extract_tpm:
    input:
        "{sample}/analysis/count/{sample}_transcript_counts.csv"
    output:
        "{sample}/analysis/count/{sample}_transcript_counts.tpm"
    shell:
        "cut -f 1,4 {input} > {output}"

# One rule for every condition: join its replicate TPMs.
rule join_tpm:
    input:
        condition_tpm
    output:
        AS_DIR + "/{condition}.tpm"
    params:
        prefix = AS_DIR + "/{condition}"
    shell:
        "suppa.py joinFiles -f tpm -i {input} -o {params.prefix}"

# One rule for every condition: per-event PSI.
rule psi_per_event:
    input:
        ioe = AS_DIR + "/allevents.ioe",
        tpm = AS_DIR + "/{condition}.tpm"
    output:
        AS_DIR + "/{condition}.psi"
    params:
        prefix = AS_DIR + "/{condition}"
    shell:
        "suppa.py psiPerEvent --ioe-file {input.ioe} --expression-file {input.tpm} -o {params.prefix}"

# Differential splicing between the two conditions.
rule diffsplice:
    input:
        ioe = AS_DIR + "/allevents.ioe",
        psi1 = AS_DIR + "/" + COND1 + ".psi",
        psi2 = AS_DIR + "/" + COND2 + ".psi",
        tpm1 = AS_DIR + "/" + COND1 + ".tpm",
        tpm2 = AS_DIR + "/" + COND2 + ".tpm"
    output:
        multiext(COMPARISON, ".dpsi", ".psivec")
    params:
        prefix = COMPARISON
    shell:
        "suppa.py diffSplice --method empirical --input {input.ioe} "
        "--psi {input.psi1} {input.psi2} --tpm {input.tpm1} {input.tpm2} "
        "--area 1000 --lower-bound 0.05 -gc -o {params.prefix}"

#rule cluster:
#    input:
#        "AlternativeSplicing/localAS/Con1vs2.psivec",
#        "AlternativeSplicing/localAS/Con1vs2.dpsi"
#    output:
#        "AlternativeSplicing/localAS/cluster"
#    shell:
#        "suppa.py clusterEvents --dpsi {input[0]} --psivec {input[1]} --sig-threshold 0.1 --eps 0.1 --min-pts 20 --groups 1-2,3-4 -o <output-file>"
