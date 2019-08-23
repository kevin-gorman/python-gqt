# python-gqt
A python wrapper for https://github.com/ryanlayer/gqt for querying large-scale genotype data.

### Usage
See [GQT](https://github.com/ryanlayer/gqt) for more detailed descriptions of how to use the software. With this, you can perform queries as described there in python scripts.
```
from gqt import gqt
gqt.cy_query(i = 'http://gqt-files.s3.amazonaws.com/ALL.chr1.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.bcf.gqt', d = 'http://gqt-files.s3.amazonaws.com/gqt_v1_integrated_call_samples.20130502.ALL.ped.db',  params = '-p|Gender = 1|-g|maf()>0.1|-p|Population in (\'YRI\')|-g|maf()>0.9999')
```

### Installation
Make sure you have liz, libcurl, libcrypto, libbz2 and liblzma installed.
```
git clone --recursive https://github.com/kevin-gorman/python-gqt.git
cd python-gqt
python setup.py test
python setup.py install
```
