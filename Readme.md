<!--
 * @Author: Zhuo Yue
 * @LastEditTime: 2023-10-22 13:36
 * @FilePath: \MAGE\Readme.md
-->
# MAGE: Metafounders Assisted Genomic Estimation

Multi-group Genomic Additive-Dominance Relationship Matrix Building Software V1.0 User Manual

## Software Introduction

This software is a genomic relationship matrix calculation tool designed for livestock and poultry populations. It can perform integrated calculations for the kinship relationships of multiple unrelated populations and their hybrid offspring. The software establishes genetic connections between unrelated groups, between groups and their hybrid offspring, and is designed based on additive-dominance effects. It can calculate both additive and dominance relationship matrices simultaneously.

The calculation results of this software can be imported into software like DMU, PIBLUP, etc., helping to improve the accuracy of genetic evaluation. It offers the ability to make comprehensive use of information from multiple populations, thereby significantly improving the efficiency of breeding selection and the overall production efficiency of the industry.

## Installation Instructions

The program was developed on the `CentOS Linux release 7.9.2003` platform and is based on Linux version `3.10.0-1127.19.1.el7.x86_64` kernel version. It should be able to run on any Unix-like system.

Considering that the program is mainly developed in C language, it should also be runnable on Windows or macOS systems after recompilation.

For routine kinship calculations in this software, it is essential to ensure that the system has more than 10 GiB of memory. For large-scale populations, more system memory will be needed based on the size of the population. On a conventional arm64 system, the software accepts a maximum of `2,147,483,647` pedigree records and a maximum of `65,535` genomic data records. If you need to import more data, you can modify the code and recompile.

This software relies on the `Intel® oneAPI Math Kernel Library` for scientific calculations (no version requirement), and Python (version 3.6 or above). Users need to ensure the existence of these dependencies in their runtime environment. Additionally, the software compilation depends on the python3-devel library, which can be installed as follows:

```bash
apt-get depends python2-dev
apt-get depends python3-dev
```

or

```bash
yum install python2-devel
yum install python3-devel
```

If the user's Python is fully compiled and installed, this dependency should already exist and no separate installation is necessary. However, if users need to use the dependency library of the fully compiled and installed Python, they need to ensure that the Python version is below 3.9.

## Quick Start

Please note that, unless otherwise specified, all of the following operations are carried out in Linux command-line mode.

### Installation

The software provides pre-compiled binary files that can be directly downloaded and used:

```bash
tar zxvf mage.tar.gz
cd mage
chmod 755 ./bin/mage
```

### Running the Software

To run the software, simply enter the relevant commands in the command line:

```bash
mage --pedigree=string --gene=string [options] ...
```
The pedigree parameter specifies the pedigree file needed by the software, and the gene parameter specifies the genomic file needed by the software. These two parameters are mandatory for running the software and can be specified using either relative or absolute paths.

Input files should be in ASCII format, with spaces or tabs used as delimiters. Whether the files are in DOS format or UNIX format is not crucial, although using UNIX format is recommended for more stable software operation. Files should not include headers. For more detailed information on the format of the input files, please refer to the Chapter about File Formats.

### Introduction to Other Relevant Parameters of the Software

Other relevant parameters for the software can be queried using the following command:

```bash
mage -h
```
The specific details of each parameter are as follows:

- `-p, --pedigree`: pedigree file path (string)
    - Specifies the pedigree file, which can be either a relative or an absolute path.

- `-g, --gene`: gene file path (string)
    - Specifies the genomic file, which can be either a relative or an absolute path.

- `-o, --output`: output file prefix (string [=output])
    - Specifies the prefix for the output files. Paths are not allowed, and the default value is 'output'.

- `-O, --out-dir`: output file directory (string [=./output])
    - Specifies the output directory, which can be either a relative or an absolute path. The default is './output'.

- `-A, --AMatrix`: output A matrix
	- Additionally outputs the pedigree kinship matrix; off by default.

- `-G, --GMatrix`: output G matrix
	- Additionally outputs the genomic kinship matrix; off by default.

- `--add`: only calculate additive kinship matrix
	- Calculates only the additive kinship matrix. Conflicts with the dom parameter.

- `--dom`: only calculate dominance kinship matrix
	- Calculates only the dominance kinship matrix. Conflicts with the add parameter.

- `-M, --Matrix`: Output original matrix or inverse matrix (string [=all])
	- Specifies the matrix output mode. Options include:
      - original: Outputs only the original matrix.
      - inverse: Outputs only the inverse matrix.
      - all: Outputs both.

- `--MFs`: use metafounders
	- Enforces the use of the metafounder model.

- `--no-cMFs`: don't use metafounders of multiple breeds
	- Forces the program not to use the metafounder model.

- `-b, --breed`: only calculate the breed (string [=all])
	- Specifies the breed to be calculated. The default is to calculate for all breeds.

- `-f, --full`: use full storage output type
	- Changes the output to a full-storage matrix format, by default it's in half-storage format.

- `-a, --all`: use full storage and half storage output type
	- Outputs both full-storage and half-storage matrix formats, overriding the --full parameter.

- `-m, --maf`: minor allele frequency (int [=0])
	- Specifies the minor allele frequency, with a default value of 0.

- `-c, --course`: keep process files
	- Retains intermediate files used during the calculation process.

- `-v, --version`: print version message
	- Prints the software version and exits.

- `-q, --quite`: do not output to stdout
	- Suppresses standard output; doesn't affect log output.

- `-d, --debug`: output debug information
	- Enables debug mode.

- `-h, --help`: print this message
	- Prints the help message and exits.

## File Description

The relevant files include the required pedigree files and genotype files. Files should be ASCII-formatted files, separated by one or multiple spaces (or newline characters). The variable names for categories can include English letters and numbers. The individual numbers should be consistent across different files.

### Pedigree File
The pedigree file is used to determine additive genetic relationships. The pedigree file required by this software should include five columns:

1. ID
   - The individual number for random effects (genetic effects) in the model.

2. Sire ID
   - The sire number; if unknown, use 0.

3. Dam ID
   - The dam number; if unknown, use 0.

4. SORT
   - The order of the individuals, which can be numerical birth dates or generations. You can use 0 for all, and the software will calculate and use the number of generations. All individuals must be specified if imported.

5. BREED
   - Breed information, specified using single-letter encoding. For crossbred individuals, use 0, but both parents must exist in the pedigree. Crossbred individuals without both parents in the pedigree will be discarded.


The pedigree file should not include headers, and any data must include all five columns. Missing data can be represented with 0. A typical pedigree that includes multiple groups and their crossbred offspring is shown below:

    Pedigree file – ped (example)
    1 0 0 0 A
    2 0 0 0 A
    3 1 2 0 A
    4 0 0 0 B
    5 0 0 0 B
    6 4 5 0 B
    7 2 6 0 0
    8 3 6 0 0

### Genome File
The genotype file is used to construct the genomic relationship matrix. The genotypes of all markers for each individual are listed in one row. The individual number is in the first column, followed by the genotype encoding for each marker. The individual numbers must match those specified in the pedigree. Any genomic information not existing in the pedigree will be discarded. For individuals without a pedigree, if you wish to keep the genomic information, you can add the individual to the pedigree and specify both parents as missing.

In genotype encoding, 0 and 2 represent the two homozygotes, while 1, 3, and 4 represent heterozygotes. 3 and 4 indicate that the dominant allele in the heterozygote comes from the sire and dam, respectively. 1 indicates that the origin of the heterozygous genes is uncertain and can only be used in purebred individuals. 5 represents missing values.

A typical genome file that includes multiple groups and their crossbred offspring is shown below:

    Gene file – gene (example)
    1 12021022012
    2 1022120122
    3 0210102210
    4 0221020212
    5 1021210212
    6 2131012212
    7 3000304202
    8 2033202430

In general, the genome file required by this software can be generated in PLINK format using the following command:
```bash
plink --bfile $1 --recodeA --out $1.q
awk '{$1="";$3="";$4="";$5="";$6="";print $0}' $1.q.raw | sed '1d' | sed "s/NA/5/g" > $1.genotype.txt
paste -d " " <( awk '{print $1}' $1.genotype.txt) <( awk '{$1="";print $0}' $1.genotype.txt | sed  "s/ //g") > $1.geno.txt
```
### Output Files
By default, the software outputs the kinship matrix in semi-storage mode, i.e., only the diagonal elements and the lower triangular matrix of the kinship matrix are output. If needed, the full-storage mode of the kinship matrix can be output by using the --full or --all parameters.

The result file is output as the inverse of the kinship matrix by default. To output the original matrix, please modify the --Matrix parameter setting.

Each row of the output file represents a matrix element and is separated by a tab. The format is: IdRow IdCol value, where IdRow and IdCol represent the individual numbers corresponding to the rows and columns, respectively.

A typical output file might look like the following:

    Output file – output_A_ahim_half (example)
    1 1 1.5
    2 1 0.5
    2 2 3.64235
    3 1 -1
    3 2 -2.39239
    3 3 3.84481
    8 1 0
    8 2 0
    8 3 -2
    8 8 4
    7 1 0
    7 2 -1.84346
    7 3 0.781411
    7 8 0
    7 7 3.10575

Parameter-based Output Files
Based on the parameter options set during software operation, the software will produce various types of kinship matrix outputs. These are distinguished through suffixes, with the file names following the format `<prefix>_<breed>_<mat>_<storage>.txt`.

prefix: Specified by the user as a parameter; defaults to output.
breed: Corresponds to the breed information imported into the user's pedigree, unless specified by the --breed parameter. Each breed will have its separate kinship matrix file.
storage: Indicates whether the result file is in full-storage (full) or semi-storage (half) format.
mat: Indicates the matrix format, specifying whether the matrix is additive or dominant, the original matrix or its inverse, etc.
The specific types include:

- aprm
    - Pedigree Additive Relationship Matrix
- apim
    - Inverse of Pedigree Additive Relationship Matrix
- agrm
    - Genomic Additive Relationship Matrix
- agim
    - Inverse of Genomic Additive Relationship Matrix
- ahrm
    - Additive H Matrix
- ahim
    - Inverse of Additive H Matrix
- dprm
    - Pedigree Dominant Relationship Matrix
- dpim
    - Inverse of Pedigree Dominant Relationship Matrix
- dgrm
    - Genomic Dominant Relationship Matrix
- dgim
    - Inverse of Genomic Dominant Relationship Matrix
- dhrm
    - Dominant H Matrix
- dhim
    - Inverse of Dominant H Matrix


## Typical Examples

Sample datasets can be found in the example folder.

### Calculation with Default Parameters

```bash
mage --pedigree ped.dat --gene gene.dat
```

The software will use the pedigree file `ped.dat` and the genome file `gene.dat`. The output will include two types of files: `output_{breed}_ahim_half.txt` containing the inverse matrix information of the additive H matrix, and output_`{breed}_dhim_half.txt` containing the inverse matrix information of the dominant H matrix. Both files will have three columns: individual number, individual number, and value.

### Changing the Output Path and Prefix

```bash
mage --pedigree ped.dat --gene gene.dat --output test --out-dir ~/test
```

The output will include two types of files: `test_{breed}_ahim_half.txt` containing the inverse matrix information of the additive H matrix, and `test_{breed}_dhim_half.txt` containing the inverse matrix information of the dominant H matrix. Output files and logs will be located in the `~/test` folder.

### Additional Output of Pedigree and Genomic Kinship Matrices

```bash
mage --pedigree ped.dat --gene gene.dat -A -G
```

The output will include six types of files:

- `output_{breed}_apim_half.txt`
    - Contains the inverse matrix information of the pedigree additive kinship matrix.
- `output_{breed}_agim_half.txt`
    - Contains the inverse matrix information of the genomic additive kinship matrix.
- `output_{breed}_ahim_half.txt`
    - Contains the inverse matrix information of the additive H matrix.
- `output_{breed}_dpim_half.txt`
    - Contains the inverse matrix information of the pedigree dominant kinship matrix.
- `output_{breed}_dgim_half.txt`
    - Contains the inverse matrix information of the genomic dominant kinship matrix.
- `output_{breed}_dhim_half.txt`
    - Contains the inverse matrix information of the dominant H matrix.

All files have three columns: individual ID, individual ID, value.

### Calculate Additive Relationship Only

```bash
mage --pedigree ped.dat --gene gene.dat --add
```

The output includes one type of file: `output_{breed}_ahim_half.txt` contains information of the inverse matrix of the additive H matrix. The file has three columns: individual ID, individual ID, value.

### Calculate for Specific Breed Only

```bash
mage --pedigree ped.dat --gene gene.dat --breed A
```

The output includes two types of files: `output_A_ahim_half.txt` contains information of the inverse matrix of the additive H matrix, and `output_A_dhim_half.txt` contains information of the inverse matrix of the dominant H matrix. Both files have three columns: individual ID, individual ID, value.

### Additionally Output the Original Matrix

```bash
cpmatrix --pedigree ped.dat --gene gene.dat --Matrix all
```

The output includes four types of files: `output_{breed}_ahrm_half.txt` contains information of the additive H matrix, output_{breed}_ahim_half.txt contains information of the inverse matrix of the additive H matrix, `output_{breed}_dhrm_half.txt` contains information of the dominant H matrix, `output_{breed}_dhim_half.txt` contains information of the inverse matrix of the dominant H matrix. All files have three columns: individual ID, individual ID, value.

### Output in Full Storage Mode

```bash
mage --pedigree ped.dat --gene gene.dat --full
```

The output includes two types of files: `output_{breed}_ahim_full.txt` contains information of the inverse matrix of the additive H matrix, `output_{breed}_dhim_full.txt` contains information of the inverse matrix of the dominant H matrix. Both files have three columns: individual ID, individual ID, value.

### Output All Possible Results from this Software

```bash
mage --pedigree ped.dat --gene gene.dat -A -G --Matrix all --all
```

Different parameters can be used in combination. This example will output all 24 types of result files from the software, which are not detailed here.
