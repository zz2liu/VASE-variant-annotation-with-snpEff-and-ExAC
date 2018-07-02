# VASE: A simple *V*ariant *A*nnotation tool using *S*npEff and *E*xAC.

## Installation
- Download and Install snpEff [link] (Java is required) and download the data for GRCh37.75
    ```bash
    wget http://sourceforge.net/projects/snpeff/files/snpEff_latest_core.zip
    unzip snpEff_latest_core.zip
    # download hg19 with Ensembl annotation
    cd snpEff
    #java -jar snpEff.jar databases | grep GRCh37
    java -jar snpEff.jar download GRCh37.75
    cd ..
    ```
- Install python 3.7+ [link] and install the vcf parser `pip3.7 install pyvcf`
- Download and extract this package to a folder
- For a quick test, go to the package folder and run
```bash
    cd tests
    python3.7 main.py test.vcf > out.csv
```

## Usage, from the package folder
- modify config.yaml with a text editor if necessary
- then
```bash
vase <vcffile> -o <outFile>
```

## Implementation Notes
- Depth of coverage (DP), Number of reads supporting the variants(AO), and Percentage of reads supporting the variant (AO/(AO+RO)) are extracted from the original VCF file from the variant caller (freebayes).
- snpEff is used for first-line annotation to get the type of the variation, genename, geneid, etc.  Only the first ANN fields (the most deleterious one) are reported.
- For simplification
    - only the first variants (if there are multiple possibilities) are used to fetch results from ExAC
    - only the allele freq of the variant is fetched from ExAC.
    - the genome version of the input VCF file is assumed to be hg19/GRCh37 (no check)


