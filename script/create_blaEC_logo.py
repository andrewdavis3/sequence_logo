# import packages
from weblogo import *
from Bio import Entrez
import argparse
from Bio.Align.Applications import ClustalOmegaCommandline
import os
import shutil


# pull sequences from NCBI
def pullSequence(emailAddress,outputFolder):
    Entrez.email = emailAddress 
    # get sequences IDs from Entrez
    handle = Entrez.esearch(db="protein", retmax=50, term='(blaEC) AND "Escherichia coli"[porgn:__txid562]', idtype="acc")
    record = Entrez.read(handle)
    outputFile=outputFolder+'blaEC.fasta'
    with open(outputFile,'w') as output:
        for idNum in record['IdList']:
            # Fetch sequences
            efetchHandle = Entrez.efetch(db="protein", id=idNum, rettype="fasta")
            output.write(efetchHandle.read())
    return outputFile

# generate clustalo alignment
def clustal(fastaFile):
    outAlnFile=fastaFile.replace(".fasta","")+"_aln.fasta"
    # run clustalo
    cline = ClustalOmegaCommandline( 
    infile=fastaFile, outfile=outAlnFile,outfmt="fasta",force=True)
    stdout, stderr = cline()
    print(stdout, stderr)
    return outAlnFile

# create sequence logo
def seqLogo(inFile,outputFolder):
    fileIn = open(inFile)
    seqs = read_seq_data(fileIn)
    # define sequence Logo options
    logodata = LogoData.from_seqs(seqs)
    logooptions = LogoOptions()
    logooptions.logo_title = "blaEC"
    logoformat = LogoFormat(logodata, logooptions)
    png = png_formatter(logodata, logoformat)
    # produce sequence Logo output
    with open(outputFolder+'blaEC_seqLogo.png', 'wb') as f:
        f.write(png)


def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("--email", type=str, help="email address for NCBI request")
    args = parser.parse_args()
    return args

def main():

    parseArgs=getArgs()
    # create output folder
    outFolder='example_data/'
    if  not os.path.exists(outFolder):
        os.makedirs(outFolder)
    # pull sequences from NCBI
    outFile=pullSequence(parseArgs.email,outFolder)
    # run clustalo
    outAln=clustal(outFile)
    # generate sequence logo
    seqLogo(outAln,outFolder)



if __name__ == '__main__':
	main()
