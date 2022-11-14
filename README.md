# Diablo G25

**Diablo G25** - is a tool for conversion of VCF file into 23AndMe format and calculation of admixture scores from it
(implemented with [admix](https://github.com/stevenliuyi/admix)).

## Table of Contents
1. [Installation](#Installation)
2. [Usage](#Usage)
3. [How to convert the result into G25 scores](#how-to-convert-the-result-into-g25-scores)

## Installation

Currently, the best way to install Diablo G25 is to git clone the repository and install the dependencies with yml file:

```
git clone https://github.com/TheSergeyPixel/Diablo_G25
conda env create -f /path/to/cloned/repo/diablo_g25.yml 
```
You can also git clone the repository and manually install the required packages as follows:

```
git clone https://github.com/TheSergeyPixel/Diablo_G25
conda install pandas>=1.5.1
conda install numpy>=1.23.4
pip install admix
```


We are currently working on creating conda package.

## Usage

Diablo G25 requires basic **gzipped** VCF file (for example, HaplotypeCaller + GenotypeGVCFs output) as input. The output 
is always generated as tsv file. Run main.py from downloaded repository as follows:

```
python main.py -i /path/to/vcf/file.vcf -o /desired/output/direcotry/output.tsv -m model_name
```
```-i``` and ```-o``` arguments are always required.<br/>
<br/>
23andMe style tsv file with all genotypes will be generated in the directory of output file. <br/>
<br/>
For the ```-m``` option, enter the name of any model provided by [admix](https://github.com/stevenliuyi/admix#models).
If ```-m``` is not provided, K36 model will be used by default.

## How to convert the result into G25 scores

After you have obtained the scores for the model you chose, you can convert them into G25 scores via visiting 
[Allelocator calculator](https://allelocator.ovh/simulatedg25.html) and performing following steps:

1. Paste your result from the Diablo G25 output into **Calculator results** field
2. Choose the model you used from **Linear regression matrix** field
3. **Simulated G25 coordinates** field will auto generate your simulated G25 scores
4. You can proceed to [Vahaduo admixture calculator](https://vahaduo.github.io/vahaduo/) to estimate admixture 
proportions and calculate Euclidean distances. 

When you open Vahaduo admixture calculator, you would need to paste your G25 coordinates into **target** field, 
G25 populations (can be downloaded from another [Vahaduo tool](https://vahaduo.github.io/g25download/)) into **source** 
field followed by choice of desired options and running the tool at **single** tab if you have one 
sample (line) in your target field or **multi** if you have multiple samples.

https://user-images.githubusercontent.com/68028950/201698698-eb22e5dd-4478-4b62-9c74-62e4a29b5d5a.mp4







