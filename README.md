# FastdRNA: a workflow for analysis of ONT direct RNA seq dataset
![未标题-1](https://github.com/Tomcxf/FASTdRNA/assets/75790226/c04de3be-20d2-4b82-ae8f-243f7a9ead9e)

FastdRNA is a pipeline written in snakemake to handle ONT direct RNA seq database. 

<h2> We have published a handbook which includes more details, please read [FdRhandbook](https://tomcxf.github.io/jekyll-gitbook/) before using it!

The analysis includes : 
- dRNAmain: a module for basecalling. mapping and transcript count.
- dRNAtail: a module for RNA poly(A) length estimate.
- dRNAmodif: a module for RNA modification detection.
- dRNAas: a module for alternative splicing analysis.

## Installation
Users need to install snakemake and conda before.

Then you can download the workflow by:
```
git clone https://github.com/Tomcxf/FASTdRNA.git
```

Required software and relative dependence can be installed through conda by typing

```
conda env create -f environment.yml
```

There're two software need to install in binary file.

- [a branch of nanopolish suitable for slow5](https://github.com/jts/nanopolish/files/9256504/nanopolish.tar.gz)

- [f5c](https://github.com/hasindu2008/f5c/releases/download/v1.1/f5c-v1.1-binaries.tar.gz)

Finally, for the reason that copyright protection, we can't supply Guppy directly. Searcher should download Guppy in Nanopore Comm

## Usage

```
 snakemake -s {dRNAmain.py / dRNAtail.py / dRNAmodif.py / dRNAas.py}
           -s the snakemake file you want to run
           --cores / -c : the number of cores to use (necessary)
           --set-threads myrule=XXX set threads XXX for running
```

### tips
To generate a offical report by snakemake, users can run
```
snakemake --report report.html
```
after pipeline finished.

## Citation
Chen X, Liu Y, Lv K, Wang M, Liu X, Li B. FASTdRNA: a workflow for the analysis of ONT direct RNA sequencing. Bioinform Adv. 2023 Jul 20;3(1):vbad099. doi: 10.1093/bioadv/vbad099. PMID: 37521311; PMCID: PMC10375421. [link](https://academic.oup.com/bioinformaticsadvances/article/3/1/vbad099/7227116)
