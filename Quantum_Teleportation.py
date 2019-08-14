# -*- coding: utf-8 -*-
"""
Created on Thu Aug  8 20:07:59 2019

@author: Sarmed
"""
from projectq.ops import H, Measure, All, CNOT, X, Z 
from projectq.backends import CircuitDrawer
from projectq.meta import Dagger, Control
from projectq import MainEngine

def create_bell_pair(eng):
    """ returns a pair of entangled qubits"""
    # q1 is our qubit / message 
    q1 = eng.allocate_qubit()
    # q2 is the receivers qubit, will be used to re-create the message state
    q2 = eng.allocate_qubit()
    # Hadamard gate to put q1 in superposition
    H | q1
    # CNOT gate to flip q2 conditionally on the first qubit being in state |1>
    CNOT | (q1,q2)
    
    return q1,q2

def create_message(eng,q1,message_value=0):
    # qubit to send
    qs = eng.allocate_qubit() 
    if message_value == 1:
        X | qs
    # entangle the original qubit with the message qubit
    CNOT | (qs,q1)
    # 1_ put the message qubit in superposition
    # 2_ measure the 2 values to get the classical bit value
    H | qs
    Measure | qs
    Measure | q1
    
    classical_message = [int(qs),int(q1)]
    
    return classical_message

def message_receiver(eng,message,q2):
    
    if message[1] == 1:
        X | q2
    if message[0] == 1:
        Z | q2
    
    Measure | q2
    
    eng.flush()
    
    received_bit = int(q2)
    
    return received_bit
    
if __name__ == '__main__' :
    eng = MainEngine()
    
    q1 , q2 = create_bell_pair(eng)
    message = create_message(eng,q1)
    print( message_receiver(eng,message,q2) )
    