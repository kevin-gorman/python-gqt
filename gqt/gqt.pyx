#cython: embedsignature=True
# distutils: sources = ../lib/gqt/src.query.c
# distutils: include_dirs = ../lib

from __future__ import print_function
from cpython.mem cimport PyMem_Malloc, PyMem_Realloc, PyMem_Free
from libc.stdlib cimport free, malloc
import sys
import cython
cimport gqt




cpdef cy_query(char* i = '', char* d = '', char* c = '', char* v = '', char* t = '', char* B = '', char* O = '', char* V = '', char* G = '', char* params = ''):
    args = [i,d,c,v,t,B,O,V,G,params]
    arg_names = ['-i','-d','-c','-v','-t','-B','-O','-V','-G','-p','-g']
    cdef char **argv = <char**> PyMem_Malloc(300 * sizeof(char*))
    argv[0] = <char*> (PyMem_Malloc(sizeof('query') + 1))
    argv[0] = 'query'
    cdef int k = 1
    for t, j in zip(arg_names, enumerate(args)):
        if not (j[1] == ''):
            if (j[0] == 9):
                param_list = j[1].split("|")
                for param in param_list:
                    if param == '-p' or param == 'p':
                        argv[k] = <char*> PyMem_Malloc(3 * sizeof(char*))
                        argv[k] = "-p"
                    elif param == '-g' or param == 'g':
                        argv[k] = <char*> PyMem_Malloc(3 * sizeof(char*))
                        argv[k] = "-g"
                    else:
                        argv[k] = <char*> (PyMem_Malloc(sizeof(param) + 1))
                        argv[k] = param
                    k += 1
            else:
                argv[k] = <char*> PyMem_Malloc(3 * sizeof(char*))
                argv[k] = t
                argv[k + 1] = <char*> (PyMem_Malloc(sizeof(j[1]) + 1))
                argv[k + 1] = j[1]
                k += 2
    cdef int argc = k
    full_cmd = argv[0] + ' ';
    cdef int quote_next = 0;
    for k in range(1, argc):
        if (quote_next == 1):
            full_cmd += '\"' + argv[k] + '\" '
            quote_next = 0;
        else:
            full_cmd += argv[k] + ' '
        if ( (argv[k][1] == "p") or (argv[k][1] == "g")):
            quote_next = 1;
    '''
    print(k)
    print(argc)
    for k in range(argc):
        print(argv[int(k)])
    print(full_cmd)
    '''
    return query(argc, argv, full_cmd)
    #return 0
