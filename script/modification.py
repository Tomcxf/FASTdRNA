from nanocompore.SampCompDB import SampCompDB

# Load the SampComp database produced by `nanocompore sampcomp`.
db = SampCompDB(
    db_fn=snakemake.params.db,
    fasta_fn=snakemake.input.fasta,
)
print(db)
print(db.ref_id_list)

# Differential-modification report.
db.save_report(output_fn=snakemake.output[0])

# Per-condition shift statistics (mean / median / sd of intensity & dwell time).
db.save_shift_stats(output_fn=snakemake.output[1])

# Optional downstream filter (kept as a hint, run manually if wanted):
#   awk '{if($7!="nan" && $7!="1.0") print}' simulated_report.tsv \
#       > simulated_report_final.tsv
