from __future__ import print_function
import os
import sys
import io 
from io import IOBase
from contextlib import contextmanager
import ctypes
import tempfile
import subprocess
import boto3
libc = ctypes.CDLL(None)
import time
context = {"nothing": "nothing"}
event = {"queryStringParameters": {"i": "ch2", "d": 'http://gqt-files.s3.amazonaws.com/gqt_v1_integrated_call_samples.20130502.ALL.ped.db', "params": ["-p","Gender = 1","-g","maf()<.01","-p","Population in ('GBR','FIN')","-g", "count(HET)>50"]}}
#cmd = [prefix + 'lib/gqt/bin/gqt', 'query', '-i', 'http://gqt-files.s3.amazonaws.com/ALL.chr2.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.bcf.gqt', '-d', 'http://gqt-files.s3.amazonaws.com/gqt_v1_integrated_call_samples.20130502.ALL.ped.db', '-p', u'"Population in (\'GBR\')"', '-g', '"maf()>0.1"']
firstTime=True
libc = ctypes.CDLL(None)
c_stdout = ctypes.c_void_p.in_dll(libc, 'stdout')

is_i = False
is_d = False
is_params = False
files = ['ALL.chr1.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.bcf.gqt', 'ALL.chr10.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.bcf.gqt', 'ALL.chr11.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.bcf.gqt', 'ALL.chr12.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.bcf.gqt', 'ALL.chr13.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.bcf.gqt', 'ALL.chr14.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.bcf.gqt', 'ALL.chr15.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.bcf.gqt', 'ALL.chr16.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.bcf.gqt', 'ALL.chr17.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.bcf.gqt', 'ALL.chr18.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.bcf.gqt', 'ALL.chr19.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.bcf.gqt', 'ALL.chr2.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.bcf.gqt', 'ALL.chr20.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.bcf.gqt', 'ALL.chr21.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.bcf.gqt', 'ALL.chr22.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.bcf.gqt', 'ALL.chr3.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.bcf.gqt', 'ALL.chr4.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.bcf.gqt', 'ALL.chr5.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.bcf.gqt', 'ALL.chr6.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.bcf.gqt', 'ALL.chr7.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.bcf.gqt', 'ALL.chr8.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.bcf.gqt', 'ALL.chr9.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.bcf.gqt', 'ALL.wgs.phase3_shapeit2_mvncall_integrated_v5b.20130502.sites.bcf.gqt', 'ALL.chrMT.phase3_callmom-v0_4.20130502.genotypes.bcf.gqt', 'ALL.chrX.phase3_shapeit2_mvncall_integrated_v1b.20130502.genotypes.bcf.gqt', 'ALL.chrY.phase3_integrated_v2a.20130502.genotypes.bcf.gqt']
chs = ['ch1', 'ch10', 'ch11', 'ch12', 'ch13', 'ch14', 'ch15', 'ch16', 'ch17', 'ch18', 'ch19', 'ch2', 'ch20', 'ch21', 'ch22' 'ch3', 'ch4', 'ch5', 'ch6', 'ch7', 'ch8', 'ch9', ]
def handler(event, context):
    key = ''
    #prefix = '/home/ec2-user/environment/python-gqt/'
    prefix = '/var/task/'
    cmd = ['gqt', 'query']
    for param_key in event["queryStringParameters"].keys():
        
        if len(event["queryStringParameters"]["params"]) == 0:
            continue
        if param_key == "params":
            is_params = True
            for param in event["queryStringParameters"]["params"]:
                if param == 'g' or param == 'p':
                    param = '-' + param
                    key += param + '='
                    cmd.append(param)
                elif param == '-g' or param == '-p':
                    key += param
                    cmd.append(param)
                else:
                    if param[0] and param[-1] == '"' or param[0] and param[-1] == "'":
                        cmd.append(param)
                    else:
                        param = '\"' + param + '\"'
                        cmd.append(param)
                    key += param
        else:
            if param_key == 'i' or param_key == '-i':
                is_i = True
                if event["queryStringParameters"][param_key] in chs:
                    index = chs.index(event["queryStringParameters"][param_key])
                    if param_key == '-i':
                        cmd.extend([param_key, 'http://gqt-files.s3.amazonaws.com/' + files[index]])
                    else:
                        cmd.extend(['-' + param_key, 'http://gqt-files.s3.amazonaws.com/' + files[index]])
                    continue
            elif param_key == 'd' or param_key == '-d':
                is_d = True
            if param_key[0] != "-":
                cmd.extend(['-' + param_key, event["queryStringParameters"][param_key]])
            else:
                cmd.extend([param_key, event["queryStringParameters"][param_key]])
    #return cmd
    if not is_i:
        return("Must enter an -i parameter indicating a GQT index file. Ex: -i=\"ch2\"  or  -i=\"http://gqt-files.s3.amazonaws.com/ALL.chr2.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.bcf.gqt\". The full documentation can be found at _________")
    if not is_params:
        return("Must enter a params list indicating what query parameters you would like. Ex: params=[\"-p\",\"Gender = 1\",\"-g\",\"maf()<.01\",\"-p\",\"Population in (\'GBR\' \'FIN\')\",\"-g\",\"count(HET)>50\"]. The full documentation can be found at _________")
    if not is_d:
        cmd.extend(['-d', 'http://gqt-files.s3.amazonaws.com/gqt_v1_integrated_call_samples.20130502.ALL.ped.db'])
    key = key[:-1]
    key = key.replace(" ", "")
    key = key.replace("'", "*")
    key = key.replace('"', "*")
    key = key.replace('=', "*")
    key = key.replace('<', "*")
    key = key.replace('>', "*")
    key = '"' + key + '.txt"'
    #return key
    #sys.path.insert(1, prefix + "aws")
    #import boto3
    #cmd1 = "PYTHONPATH=" + prefix + "aws && export PYTHONPATH"
    #proc = subprocess.check_call(cmd1, shell=True)
    timeout=10
    #from gqt import gqt
    #import gqt
    #with open('file', 'w') as sys.stdout: gqt.cy_query(**event['queryStringParameters'])
    #return dir(gqt)
    #old_stdout = sys.stdout
    f = io.BytesIO()
    #with stdout_redirector(f):
    #with open('/tmp/tst_redir.txt', 'w') as f, stdout_redirected(f):
    
    #out_file_name = '/tmp/' + str(random.randint(0,sys.maxsize)) + '.out'
    
    
    '''
    bashCommand = "pwd"
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    here, error = process.communicate()
    '''
    current_directory= os.path.dirname(__file__)
    prog_file_path = os.path.join(current_directory, "lib/gqt/bin/")
    
    
    
    #cmd = '/home/ec2-user/environment/python-gqt/lib/gqt/bin/gqt query -i http://s3-us-west-2.amazonaws.com/gqt-data/test/10.1e4.var.bcf.gqt -B http://s3-us-west-2.amazonaws.com/gqt-data/test/10.1e4.var.bcf.bim -p "BCF_ID < 5" -g "count(HET)"'
    #cmd = ['/var/task/lib/gqt/bin/gqt', 'query','-i','http://s3-us-west-2.amazonaws.com/gqt-data/test/10.1e4.var.bcf.gqt','-B','http://s3-us-west-2.amazonaws.com/gqt-data/test/10.1e4.var.bcf.bim','-p',"BCF_ID < 5",'-g',"count(HET)"]
    #cmd = ['/home/ec2-user/environment/python-gqt/lib/gqt/bin/gqt', 'query','-i','http://s3-us-west-2.amazonaws.com/gqt-data/test/10.1e4.var.bcf.gqt','-p',"BCF_ID < 5",'-g',"count(HET)"]
    #cmd = ['/home/ec2-user/environment/python-gqt/lib/gqt/bin/gqt', 'query', '-i', 'http://gqt-files.s3.amazonaws.com/ALL.phase3.autosome.vcf.gz.gqt', '-d', 'http://gqt-files.s3.amazonaws.com/gqt_v1_integrated_call_samples.20130502.ALL.ped.db', '-p', u'"Population in (\'GRB\')"', '-g', '"maf()<0.01"']
    #cmd = [prefix + 'lib/gqt/bin/gqt', 'query', '-i', 'http://gqt-files.s3.amazonaws.com/ALL.chr2.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.bcf.gqt', '-d', 'http://gqt-files.s3.amazonaws.com/gqt_v1_integrated_call_samples.20130502.ALL.ped.db', '-p', u'"Population in (\'GBR\')"', '-g', '"maf()>0.1"']
    #cmd = ['/home/ec2-user/environment/python-gqt/lib/gqt/bin/gqt', 'query', '-i', 'http://gqt-files.s3.amazonaws.com/ALL.chr2.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.bcf.gqt', '-d', 'http://gqt-files.s3.amazonaws.com/gqt_v1_integrated_call_samples.20130502.ALL.ped.db', '-p', u'"Population in (\'GBR\')"', '-g', '"maf()>0.1"']
    bucket_name = 'gqt-results'
    #key = 'query_test.txt'
    
    

    os.chdir('/tmp')
    '''
    s3_resource = boto3.resource('s3')
    s3_client = boto3.client('s3')
    bucket = s3_resource.Bucket(bucket_name)
    '''
    cmd.extend(["|", "aws", "s3", "cp", "-", "s3://" + bucket_name + "/" + key, "--acl", "public-read"])
    #out_file_name = '/tmp/tst_redir.txt'
    #f = open(out_file_name, 'r+')
    #cmd = '/var/task/lib/gqt/bin/gqt query -i http://gqt-files.s3.amazonaws.com/ALL.phase3.autosome.vcf.gz.gqt -d http://gqt-files.s3.amazonaws.com/gqt_v1_integrated_call_samples.20130502.ALL.ped.db -p "Population in (\'GRB\')" -g "maf()<0.01" | aws s3 cp - s3://layer-overflow-bucket/query_test.txt'
    response = ''
    for i in cmd:
        if type(i) is list:
            for j in i:
                response += j + ' '
        else:
            response += i + ' '
    cmd = response
    try:
        proc = subprocess.Popen(cmd, shell=True, stderr=subprocess.PIPE)
        err = proc.communicate()[1]
        if err == "":
            
            return 'http://' + bucket_name + '.s3.amazonaws.com/' + key[1:-1]
        else:
            s3_resource = boto3.resource('s3')
            bucket = s3_resource.Bucket('gqt-results')
            obj = bucket.put_object(Key=key[1:-1],Body=err, ACL='public-read')
            return 'http://' + bucket_name + '.s3.amazonaws.com/' + key[1:-1]
    except Exception as e:
        
        s3_resource = boto3.resource('s3')
        bucket = s3_resource.Bucket('gqt-results')
        obj = bucket.put_object(Key=key[1:-1],Body=str(e), ACL='public-read')
        return 'http://' + bucket_name + '.s3.amazonaws.com/' + key[1:-1]
        
print(handler(event, context))

#handler(0,0)
