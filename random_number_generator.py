# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 19:34:57 2019

@author: Acer
"""

from projectq.ops import H, Measure, All, CNOT, X, Z 
from projectq import MainEngine
import matplotlib.pyplot as plt

def get_random_number(quantum_engine):
    qubit = quantum_engine.allocate_qubit()
    H | qubit
    Measure | qubit
    rand_num = int(qubit)
    return rand_num

def rand_num(N,quantum_engine):
    random_numbers_list = []
    for i in range(int(N)):
        random_numbers_list.append( get_random_number(quantum_engine))
        
        quantum_engine.flush() # Flushes the quantum engine from memory
    return random_numbers_list


if __name__ == '__main__' :
    N = 1e3
    quantum_engine = MainEngine()
    random_numbers = rand_num(N,quantum_engine)
    one = random_numbers.count(1)
    zero = N - one
    plt.bar([0,1],[zero,one])
    plt.xticks([0,1])
    #print(random_numbers)