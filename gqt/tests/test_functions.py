from __future__ import print_function
import os
import sys

def test_query():
    from gqt import gqt
    gqt.cy_query(i = 'http://gqt-files.s3.amazonaws.com/ALL.chr1.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.bcf.gqt', d = 'http://gqt-files.s3.amazonaws.com/gqt_v1_integrated_call_samples.20130502.ALL.ped.db',  params = '-p|Gender = 1|-g|maf()>0.1|-p|Population in (\'YRI\')|-g|maf()>0.9999')
test_query()