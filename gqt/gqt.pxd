#cython: embedsignature=True
from __future__ import print_function
from libc.stdint cimport uint32_t
from libc.stdlib cimport free
import sys
import locale
    
cdef extern from "query.h":
    int query(int argc, char** argv, char* full_cmd);
    
cpdef cy_query(char* i = *, char* d = *, char* c = *, char* v = *, char* t = *, char* B = *, char* O = *, char* V = *, char* G = *, char* params = *);

    