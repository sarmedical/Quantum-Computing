# -*- coding: utf-8 -*-
"""
Created on Thu Aug  8 20:07:59 2019

@author: Sarmed
"""
from projectq.ops import H, Measure, All, CNOT, X, Z 
from projectq.backends import CircuitDrawer
from projectq.meta import Dagger, Control
from projectq import MainEngine

def create_bell_pair(engine):
    """ returns a pair of entangled qubits"""
    
    q1 = engine.allocate_qubit()
    q2 = engine.allocate_qubit()
    
    H | q1
    CNOT | (q1,q2)
    
    return q1,q2

def run_teleport(eng):
    # create bell pair
    q1,q2 = create_bell_pair(eng) 
    # Alice's qubit (to be teleported)
    psi = eng.allocate_qubit()                                                 
    # Entangle psi with q1 (her share of the bell-pair)
    CNOT | (q1 , psi)
    # measure two values (once in Hadamard basis) and send the bits to Bob
    H | psi
    Measure | psi
    Measure | q1 
    msg_to_Bob = [int(psi) , int(q1)]
    
    # Bob may have to apply up to two operation depending on the message sent
    # by Alice:
    with Control(eng,q1):
        X | q2
    with Control(eng,psi):
        Z | q2
        
    Measure | q2
    eng.flush()
    print ( int(q2) )
    
if __name__ == '__main__' :
    eng = MainEngine()
    run_teleport(eng)