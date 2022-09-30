# 多群体基因组加-显亲缘关系矩阵构建软件V1.0用户手册

## 软件介绍

本软件是一种畜禽群体的基因组亲缘关系矩阵计算软件，其可实现对于多个无关群体及其杂交后代的亲缘关系的整合计算，建立无关群体间、群体和杂交后裔之间的遗传联系，同时本软件基于加-显效应进行设计，可以同时计算加性亲缘关系矩阵和显性亲缘关系矩阵。

本软件计算结果可供DMU、PIBLUP等软件导入使用，有助于提高遗传评估的准确性，提供对多群体个体信息的综合利用能力，有助于大幅提升育种选育效率和全产业链的生产效率。

## 安装说明

本程序是在CentOS Linux release 7.9.2003平台上开发的，并基于Linux version 3.10.0-1127.19.1.el7.x86_64内核版本，其应可以运行在任何类Unix系统上。

考虑到本程序主要基于C语言进行开发，重新编译后其应该亦可以运行在Windows或macOS等系统上。

本软件进行常规群体亲缘关系计算时需保证系统内存在10GB以上，对于大规模群体，需要根据群体规模提供更充足的系统内存。常规arm64系统下，本软件最多接受系谱记录2,147,483,647条，最多接受基因组数据65,535条，如果需要更多数据导入，可以修改代码重新编译。

本软件在使用时，需要依赖于Intel® oneAPI Math Kernel Library科学计算库（无版本要求），Python (3.6及其以上版本)，需要用户保证运行环境中上述依赖的存在。同时，本软件编译时依赖python3-devel函数库，如需自行编译可以通过如下方式进行安装：

    apt-get depends python3-dev

或

    yum install python3-devel

如果用户的Python为完整编译安装，应已经存在此依赖库，无需另行安装。但如用户需要使用完整编译安装的Python的依赖库，需要保证Python版本低于3.9。

## 快速上手

请注意，如无特殊说明，以下的所有操作全部是在Linux命令行模式下操作进行。

### 安装

本软件提供了预编译的二进制文件，可以直接下载使用：

    tar zxvf CCPMatrix.tar.gz
    cd CCPMatrix
    chmod 755 ./bin/ccpmatrix

要的MakeFile文件，可以直接使用：

    tar zxvf CCPMatrix.tar.gz
    cd CCPMatrix
    make

进行编译。本软件推荐使用gcc v8.x 之上版本进行编译。

同时，也可以使用```make debug```获得debug模式的软件，此模式下本软件会输出更多的报错信息，可以有助于定位软件错误原因。

在安装完成后，为了方便使用，可以将本软件的执行命令目录放置到系统的全局环境变量下，例如：

    echo 'export PATH=$HOME/CCPMatrix/bin/:$PATH' >> ~/.bashrc
或

    ln -s $HOME/CCPMatrix/bin/ccpmatrix ~/.local/bin/ccpmatrix


### 软件运行

运行本软件时，只需在命令行里输入相关命令即可：

    ccpmatrix --pedigree=string --gene=string [options] ...

pedigree参数指定软件所需要的系谱文件，gene参数指定软件所需要的基因组文件，此两个参数是软件运行所必须的，可以使用相对路径或者绝对路径。

输入文件应该是ASCII格式的文件，使用空格或者制表符表示间隔，文件为dos格式或unix格式是不重要的，但是仍然推荐使用unix格式，这会让软件的运行更加稳定。文件不应该包括表头，更详细的输入文件的格式需要请参阅第四章文件格式部分。

### 软件其他相关参数介绍

软件的其他相关参数使用如下命令可查询：

    ccpmatrix -h

相关信息如下图所示：

各参数具体的介绍如下：

    -p, --pedigree    pedigree file path (string)
    指定系谱文件，可以使用相对路径和绝对路径。

    -g, --gene        gene file path (string)
    指定基因组文件，可以使用相对路径和绝对路径。

    -o, --output      output file prefix (string [=output])
    指定输出文件前缀，不能使用路径，默认值为output。

    -O, --out-dir     output file dicectionary (string [=./output])
    指定输出文件夹，可以使用相对路径和绝对路径，默认为./output。

    -A, --AMatrix     output A matrix
    额外输出系谱亲缘关系矩阵，默认为否。

    -G, --GMatrix     output G matrix
    额外输出基因组亲缘关系矩阵，默认为否。

    ,  --add         only calculate additive kinship matrix
    只计算加性亲缘关系矩阵，与dom参数矛盾。

    ,  --dom         only calculate dominance kinship matrix
    只计算显性亲缘关系矩阵，与add参数矛盾。

    -M, --Matrix      Output original matrix or inverse matrix (string [=all])
    输出的矩阵模式，可供选择的参数包括：

    original：只输出原矩阵

    inverse：只输出逆矩阵

    all：和全部输出。

    ,   --MFs         use metafounders
    强制使用元建立者模式。

    ,  --no-cMFs     don't use metafounders of multiple breeds
    强制不使用元建立者模式。

    -b, --breed       only calculate the breed (string [=all])
    指定所需要计算的品种，默认为全部计算。

    -f, --full        use full storge output type
    输出结果改变为矩阵的全存储模式，默认为半存储模式。

    -a, --all         use full storge and half storge output type
    同时输出矩阵的全存储模式和半存储模式，会覆盖--full参数。

    -m, --maf         minor allele frequency (int [=0])
    指定最小等位基因频率，默认为0。

    -c, --course      keep process files
    保留计算过程的中间文件。

    -v, --version     print version message
    打印软件版本并退出。

    -q, --quite       do not output to stdout
    关闭标准输出，不会影响日志输出。

    -d, --debug       output debug information
    启用debug模式。

    -h, --help        print this message
    打印帮助信息并退出。

## 文件说明

相关文件包括所需的系谱文件、基因型文件。文件应该是ASCII格式文件，其由一个或数个空格（或换行符）分隔。分类的变量名可以包含英文字母和数字。个体号在不同的文件中应一致。

### 系谱文件

系谱文件用于确定加性遗传关系。本软件所需要的系谱文件应该包括五列：

    1：ID
    模型中随机效应（遗传效应）的个体号。

    2：Sire ID
    公畜号，当公畜未知时，为0。

    3：Dam ID
    母畜号，当母畜未知时，为0。

    4：SORT
    个体顺序，可以使用数值化的出生日期或世代，可以全部使用0，软件将计算世代数并使用。如需导入所有个体均需要指定。

    5：BREED
    品种信息，使用单字母编码指定，杂交个体使用0指定，但需要父母均存在于系谱中，父母不存在的杂种个体将会被丢弃。

系谱文件不应该包括表头，任何的数据必须包含全部的五列，缺失的数据可以使用0进行指代。一个典型的包含多个群体及其杂交后代的系谱如下所示：

    Pedigree file – ped （示例）
    1 0 0 0 A
    2 0 0 0 A
    3 1 2 0 A
    4 0 0 0 B
    5 0 0 0 B
    6 4 5 0 B
    7 2 6 0 0
    8 3 6 0 0

### 基因组文件

基因型文件用于构建基因组关系矩阵，个体所有标记的基因型被列在一行，个体号在第一列，后面一列是每个标记的基因型编码，个体号需要与系谱中指定的个体号相同，任何不存在于系谱中的基因组信息将会被丢弃，对于不具有系谱的个体，若想保留基因组信息，可以于系谱中增加个体，并将父母均指定为缺失。

基因型编码时，0和2代表两个纯合子，1、3、4代表杂合子。3、4分别表示杂合子的优势基因来自父本和母本，1表示杂合子基因起源不确定，仅能在纯种个体中使用，5表示缺失值。

一个典型的包含多个群体及其杂交后代的基因组文件如下所示：

    Gene file – gene （示例）
    1 12021022012
    2 1022120122
    3 0210102210
    4 0221020212
    5 1021210212
    6 2131012212
    7 3000304202
    8 2033202430

在一般情况下，本软件所需要的基因组文件可以通过plink格式使用如下命令生成：

    plink --bfile $1 --recodeA --out $1.q
    awk '{$1="";$3="";$4="";$5="";$6="";print $0}' $1.q.raw | sed '1d' | sed "s/NA/5/g" > $1.genotype.txt
    paste -d " " <( awk '{print $1}' $1.genotype.txt) <( awk '{$1="";print $0}' $1.genotype.txt | sed  "s/ //g") > $1.geno.txt

### 输出文件

默认情况下本软件输出半存储模式的亲缘关系矩阵，即只输出亲缘关系矩阵的对角线元素和下三角矩阵，如果有需要可以通过参数```--full```或者```--all```输出全存储模式的亲缘关系矩阵。

结果文件默认输出为亲缘关系矩阵的逆矩阵，如需输出原矩阵，请修改```--Matrix```参数配置。

输出文件的每行表示一个矩阵元素，并使用制表符进行分割，其格式为:```IdRow IdCol value```，这里```IdRow```和```IdCol```代表对应行和列的个体号。

一个典型的输出文件可能如下所示：

    Output file – output_A_ahim_half（示例）
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

根据软件运行的参数选项，软件会产生多种不同的亲缘关系矩阵输出，其通过后缀进行区别，其文件命名安装如下形式```<prefix>_<breed>_<mat>_<storage>.txt```。```prefix```为用户通过参数指定的前缀，默认状态下为```output```；```breed```为用户系谱信息中导入的品种信息，除非通过```--breed```参数进行了指定，每个品种都会输出单独的亲缘关系矩阵文件；```storage```表示结果文件的格式是全存储（full）或者半存储（half）的；```mat```为矩阵的格式文件，声明了矩阵是加性矩阵或是显性矩阵，原矩阵或是逆矩阵等信息，其具体包含如下种类：

    aprm 系谱加性亲缘关系矩阵
    apim 系谱加性亲缘关系矩阵的逆矩阵
    agrm 基因组加性亲缘关系矩阵
    agim 基因组加性亲缘关系矩阵的逆矩阵
    ahrm 加性H矩阵
    ahim 加性H矩阵的逆矩阵
    dprm 系谱显性亲缘关系矩阵
    dpim 系谱显性亲缘关系矩阵的逆矩阵
    dgrm 基因组显性亲缘关系矩阵
    dgim 基因组显性亲缘关系矩阵的逆矩阵
    dhrm 显性H矩阵
    dhim 显性H矩阵的逆矩阵

## 典型示例

示例数据集可在example文件夹下找到。

### 默认参数运算

    ccpmatrix --pedigree ped.dat --gene gene.dat

软件调用```ped.dat```中的系谱文件和```gene.dat```中的基因组文件，输出结果包含两类文件:```output_{breed}_ahim_half.txt```包含加性H矩阵的逆矩阵信息，```output_{breed}_dhim_half.txt```包含显性H矩阵的逆矩阵信息，文件均为三列:个体号、个体号、值。

### 改变输出路径和输出前缀

    ccpmatrix --pedigree ped.dat --gene gene.dat --output test --out-dir ~/test

输出结果包含两类文件: ```test_{breed}_ahim_half.txt```包含加性H矩阵的逆矩阵信息，```test_{breed}_dhim_half.txt```包含显性H矩阵的逆矩阵信息，输出文件和日志将位于```~/test```文件夹下。

### 额外输出系谱亲缘关系矩阵和基因组亲缘关系矩阵

    ccpmatrix --pedigree ped.dat --gene gene.dat -A -G

输出结果包含六类文件:

```output_{breed}_apim_half.txt```包含系谱加性亲缘关系矩阵的逆矩阵信息；

```output_{breed}_agim_half.txt```包含基因组加性亲缘关系矩阵的逆矩阵信息；

```output_{breed}_ahim_half.txt```包含加性H矩阵的逆矩阵信息；

```output_{breed}_dpim_half.txt```包含系谱显性亲缘关系矩阵的逆矩阵信息；

```output_{breed}_dgim_half.txt```包含基因组显性亲缘关系矩阵的逆矩阵信息；

```output_{breed}_dhim_half.txt```包含显性H矩阵的逆矩阵信息，

所有文件均为三列:个体号、个体号、值。

### 仅计算加性亲缘关系

    ccpmatrix --pedigree ped.dat --gene gene.dat --add

输出结果包含一类文件: ```output_{breed}_ahim_half.txt```包含加性H矩阵的逆矩阵信息，文件均为三列:个体号、个体号、值。

### 仅计算特定品种

    ccpmatrix --pedigree ped.dat --gene gene.dat --breed A

输出结果包含两个文件: ```output_A_ahim_half.txt```包含加性H矩阵的逆矩阵信息，```output_A_dhim_half.txt```包含显性H矩阵的逆矩阵信息，文件均为三列:个体号、个体号、值。

### 额外输出原矩阵

    cpmatrix --pedigree ped.dat --gene gene.dat --Matrix all

输出结果包含四类文件: ```output_{breed}_ahrm_half.txt```包含加性H矩阵信息，```output_{breed}_ahim_half.txt```包含加性H矩阵的逆矩阵信息，```output_{breed}_dhrm_half.txt```包含显性H矩阵信息，```output_{breed}_dhim_half.txt```包含显性H矩阵的逆矩阵信息，文件均为三列:个体号、个体号、值。

### 输出改为全存储模式

    ccpmatrix --pedigree ped.dat --gene gene.dat --full

输出结果包含两类文件: ```output_{breed}_ahim_full.txt```包含加性H矩阵的逆矩阵信息，```output_{breed}_dhim_full.txt```包含显性H矩阵的逆矩阵信息，文件均为三列:个体号、个体号、值。

### 输出本软件可能的全部结果

    ccpmatrix --pedigree ped.dat --gene gene.dat -A -G --Matrix all --all

不同的参数可以协同使用，本示例会输出软件全部的24种结果文件，在此不再赘述。
