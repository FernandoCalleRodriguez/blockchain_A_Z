# -*- coding: utf-8 -*-
"""
Created on Sat Nov  6 12:06:55 2021

@author: ferky
"""

#Módulo 1: Crear un Cadena de Bloques

# Importar las librerias
import datetime
import hashlib
import json
from flask import Flask, jsonify

#Parte 1 - Crear la Cadena de Bloques
class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_block(proof = 1, previous_hash = '0')
        
    def create_block(self, proof, previous_hash):
        block = {
            'index' : len(self.chain)+1,
            'timestamp' : str(datetime.datetime.now()),
            'proof' : proof,
            'previous_hash' : previous_hash
            }
        self.chain.append(block)
        return block
    
    def get_previous_block(self):
        return self.chain[-1]
    
#Parte 2 - Minado de un Bloque de la Cadena

        