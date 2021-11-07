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
    
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2-previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == "0000":
                check_proof = True
            else:
                new_proof += 1
        return new_proof

    def hash(self, block):
        encode_block = json.dump(block, sort_keys = True).encode()
        return hashlib.sha256(encode_block).hexdigest()
    
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2-previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != "0000":
                return False
            previous_block = block
            block_index += 1
        return True
                 
#Parte 2 - Minado de un Bloque de la Cadena

# 2.1 Crear una aplicación web para poder llamar desde postman
app = Flask(__name__)
    
    
# 2.2 Crear una instancia blockchain
blockchain = Blockchain()

# 2.3 Minar un nuevo bloque
@app.route('/mine_block', method=['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)
    response = {
        'message': '¡Enhorabuena, has minado un nuevo bloque!',
        'index' : block['index'],
        'timestamp' : block['timestamp'],
        'proof' :block['proof'],
        'previous_hash' : block['previous_hash']
    }
    return jsonify(response),200 
    
# Obtener la cadena de bloques completo
@app.route('/get_chain', method=['GET'])
def get_chain():
    response ={
        'chain': blockchain.chain,
        'length_chain': len(blockchain.chain)}
    return jsonify(response),200 

 #Ejecutar la app
app.run(host = '0.0.0.0', port = 5000)
