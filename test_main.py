#!/usr/bin/env python3
import main

def test_getSnpEffFields():
    input = ['T|downstream_gene_variant|MODIFIER|HES4|ENSG00000188290|transcript|ENST00000428771|protein_coding||c.*3046C>A|||||2949|',
       'T|downstream_gene_variant|MODIFIER|HES4|ENSG00000188290|transcript|ENST00000304952|protein_coding||c.*3046C>A|||||2951|',
        'T|downstream_gene_variant|MODIFIER|HES4|ENSG00000188290|transcript|ENST00000481869|retained_intron||n.*2953C>A|||||2953|',
          'T|non_coding_transcript_exon_variant|MODIFIER|RP11-54O7.17|ENSG00000272512|transcript|ENST00000606034|lincRNA|1/1|n.2039C>A||||||']
    res = main.getSnpEffFields(input)
    assert res == \
        ['downstream_gene_variant', 'MODIFIER', 'HES4', 'ENSG00000188290', 'c.*3046C>A', '']


