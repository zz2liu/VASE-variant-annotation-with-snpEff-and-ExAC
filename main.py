#!/usr/bin/env python3
import sys, argparse;  sys.version_info >= (3, 5) or sys.exit('Require python 3.5+')
import csv, json, subprocess
from urllib.request import urlopen
import vcf, yaml #pip install pyvcf, pyyaml

VERSION = '0.1'
config = yaml.load(open('config.yaml')) #exacServer, snpEffJar

vcfFieldNames = ['CHROM', 'POS', 'REF', 'ALT', 'QUAL', 'FILTER',
    'depthOfCoverage', 'readsOfAlt', 'percOfAlt']
def getVcfFields(x):
    """get a list of values from original vcf row."""
    depth = x.INFO['DP']
    readsAlt = x.INFO['AO'][0] #only report the first alt
    percAlt = readsAlt/(readsAlt + x.INFO['RO'])
    return [x.CHROM, x.POS, x.REF, x.ALT[0], x.QUAL, x.FILTER,
        depth, readsAlt, percAlt]

snpEffFieldNames = ['EFFECT', 'IMPACT','GENENAME', 'GENEID',
    'HGVS.c', 'HGVS.p']
def getSnpEffFields(ann):
    """get a list of values from snpEff ANN attribute

    REF: http://snpeff.sourceforge.net/SnpEff_manual.html
    """
    _, EFFECT,IMPACT,GENENAME,GENEID,_,_,_,_,HGVSc,HGVSp,_,_,_,_,_ = list(range(16))
    firstAnn = ann[0].split('|')
    return [firstAnn[EFFECT], firstAnn[IMPACT],firstAnn[GENENAME],firstAnn[GENEID],
            firstAnn[HGVSc], firstAnn[HGVSp]]

exacFieldNames = ['exacAlleleFreq']
def getExacFields(key, exacServer=config['exacServer']):
    """get a list of values from ExAC variant annotation if any"""
    url = f'{exacServer}/rest/variant/{key}'
    exac = json.load(urlopen(url))
    #breakpoint()
    AlleleFreq = exac['variant'].get('allele_freq')
    return [AlleleFreq]


def main(snpEffJar, vcfFile=sys.stdin, outfile=sys.stdout):
    """the workflow from ori VCF file to annotated csv file
    """
    # run snpEff on vcfFile, store result in annFile
    jar=config['snpEff']['jar']
    params=config['snpEff']['params']
    tmpVcf = 'tmp.ann.vcf'
    cmd = f'''java -Xmx4g -jar {jar} ann {params} GRCh37.75 \
        > {tmpVcf}'''
    subprocess.call(cmd, stdin=vcfFile, shell=True)

    # prepare result file, write the header line
    csvOut = csv.writer(outfile)
    csvOut.writerow(vcfFieldNames + snpEffFieldNames + exacFieldNames)

    # write a rec for each row from the tmpAnnVcf file
    vcf_reader = vcf.Reader(open(tmpVcf))
    for x in vcf_reader:
        vcfFields = getVcfFields(x)

        #breakpoint() #import pdb; pdb.set_trace()
        snpEffFields = getSnpEffFields(x.INFO['ANN'])

        key=f'{x.CHROM}-{x.POS}-{x.REF}-{x.ALT[0]}' #only the first alt reported
        exacFields = getExacFields(key)

        row = vcfFields + snpEffFields + exacFields
        csvOut.writerow(row)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='A simple linux tool for variant annotation using snpEff and ExAC.',
        epilog='--by Zongzhi Liu, home page: https://github.com/zz2liu/VASE-variant-annotation-with-snpEff-and-ExAC',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    #version
    parser.add_argument("--version", action="version",
        version="%(prog)s "+VERSION)

    # positional args
    parser.add_argument('vcfFile', type=argparse.FileType('r'),
        help='The original vcf file')

    #optionals
    parser.add_argument('-s', '--snpEffJar', default=config['snpEff']['jar'], 
        help='Path/to/snpEff.jar file. Default value is defined in config.yaml file.')
    parser.add_argument('-o', '--outfile', type=argparse.FileType('w'),
        default=sys.stdout, help=argparse.SUPPRESS) #'output file')

    parsed = parser.parse_args()
    main(parsed.snpEffJar, parsed.vcfFile, parsed.outfile)
