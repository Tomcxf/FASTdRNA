from nanocompore.SampCompDB import SampCompDB, jhelp
db = SampCompDB (db_fn = snakemake.input[0]/simulated_SampComp.db,
    fasta_fn = snakemake.input[1])
print (db)
print (db.ref_id_list)

db.save_report (output_fn=snakemake.output[0])
#downstream edition
awk '{if($7!="nan"&&$7!="1.0")print}' simulated_report.tsv > simulated_report_final.tsv

####### save_shift_stats : Save the mean, median and sd intensity and dwell time for each condition and for each position.
db.save_shift_stats (output_fn=snakemake.output[1])

####### save_to_bed
db.save_to_bed (output_fn=snakemake.output[2])
