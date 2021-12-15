import hashlib
import json
from logging import exception
from time import time
from urllib.parse import urlparse
from uuid import uuid4
import io
import requests
from flask import Flask, jsonify, request

from argparse import ArgumentParser
import urllib.parse
from requests.models import Response
from flask import Flask, Request
import os
import sys




def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)



app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000
# values = json.loads('' or 'null')
parser = ArgumentParser()
parser.add_argument('-cl','--chainlength',type=int)
parser.add_argument('-noc','--noofcertificate', type=int)
parser.add_argument('-p', '--port', default=3000, type=int, help='port to listen on')
args = parser.parse_args()
port = args.port
cl = args.chainlength
noofcertificates = args.noofcertificate

class Blockchain:
    def __init__(self):
        self.current_transactions = []
        self.chain = []
        self.chainMaxLength = cl # max number of blocks
        self.nodes = set() # no of active nodes, nodes set display
        self.transactionsPerBlock = noofcertificates # no of certificates to be stored in one block 
        self.currentTransactionscount = 0

        # Create the genesis block
        self.new_block(previous_hash='1', proof=100)

    def register_node(self, address):
        """
        Add a new node to the list of nodes

        :param address: Address of node. Eg. 'http://192.168.0.5:5000'
        """

        parsed_url = urlparse(address)
        if parsed_url.netloc:
            self.nodes.add(parsed_url.netloc)
        elif parsed_url.path:
            # Accepts an URL without scheme like '192.168.0.5:5000'.
            self.nodes.add(parsed_url.path)
        else:
            raise ValueError('Invalid URL')


    def valid_chain(self, chain):
        """
        Determine if a given blockchain is valid

        :param chain: A blockchain
        :return: True if valid, False if not
        """

        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            print(f'{last_block}')
            print(f'{block}')
            print("\n-----------\n")
            # Check that the hash of the block is correct
            last_block_hash = self.hash(last_block)
            if block['previous_hash'] != last_block_hash:
                return False

            # Check that the Proof of Work is correct
            if not self.valid_proof(last_block['proof'], block['proof'], last_block_hash):
                return False

            last_block = block
            current_index += 1

        return True

    def resolve_conflicts(self):
        """
        This is our consensus algorithm, it resolves conflicts
        by replacing our chain with the longest one in the network.

        :return: True if our chain was replaced, False if not
        """

        neighbours = self.nodes
        new_chain = None

        # We're only looking for chains longer than ours
        max_length = len(self.chain)

        # Grab and verify the chains from all the nodes in our network
        for node in neighbours:
            response = requests.get(f'http://{node}/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                # Check if the length is longer and the chain is valid
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        # Replace our chain if we discovered a new, valid chain longer than ours
        if new_chain:
            self.chain = new_chain
            return True

        return False

    def new_block(self, proof, previous_hash):
        """
        Create a new Block in the Blockchain

        :param proof: The proof given by the Proof of Work algorithm
        :param previous_hash: Hash of previous Block
        :return: New Block
        """

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        # Reset the current list of transactions
        self.current_transactions = []

        self.chain.append(block)
        return block

    def new_transaction(self, certifiacteName, certificateData):
        """
        Creates a new transaction to go into the next mined Block

        :param sender: Address of the Sender
        :param recipient: Address of the Recipient
        :param amount: Amount
        :return: The index of the Block that will hold this transaction
        """
        self.current_transactions.append({
            'certificateName' : certifiacteName,
            'certificateData' : certificateData
        })

        return self.last_block['index'] + 1

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def hash(block):
        """
        Creates a SHA-256 hash of a Block

        :param block: Block
        """

        # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self, last_block):
        """
        Simple Proof of Work Algorithm:

         - Find a number p' such that hash(pp') contains leading 4 zeroes
         - Where p is the previous proof, and p' is the new proof
         
        :param last_block: <dict> last Block
        :return: <int>
        """

        last_proof = last_block['proof']
        last_hash = self.hash(last_block)

        proof = 0
        while self.valid_proof(last_proof, proof, last_hash) is False:
            proof += 1

        return proof

    @staticmethod
    def valid_proof(last_proof, proof, last_hash):
        """
        Validates the Proof

        :param last_proof: <int> Previous Proof
        :param proof: <int> Current Proof
        :param last_hash: <str> The hash of the Previous Block
        :return: <bool> True if correct, False if not.

        """

        guess = f'{last_proof}{proof}{last_hash}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"


# Instantiate the Node
app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()


@app.route('/mine', methods=['GET'])
def mine():
    # We run the proof of work algorithm to get the next proof...
    if blockchain.chainMaxLength > len(blockchain.chain):
        last_block = blockchain.last_block
        proof = blockchain.proof_of_work(last_block)

        # We must receive a reward for finding the proof.
        # The sender is "0" to signify that this node has mined a new coin.
        # blockchain.new_transaction(
        #     sender="0",
        #     recipient=node_identifier,
        #     amount=1,
        #     certifiacteName="empty.png",
        #     certificateData=""
        # )

        # Forge the new Block by adding it to the chain
        previous_hash = blockchain.hash(last_block)
        block = blockchain.new_block(proof, previous_hash)

        response = {
            'message': "New Block Forged",
            'index': block['index'],
            'transactions': block['transactions'],
            'proof': block['proof'],
            'previous_hash': block['previous_hash'],
        }
        return jsonify(response), 200

    else:
        return "Error"


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    print("post started")
    #values = request.get_json()
    try:
    # Check that the required fields are in the POST'ed data
        required = ['certificateName','certificateData']
        values = json.loads(request.data)
        with open(resource_path('data.json'), 'w', encoding='utf-8') as f:
            json.dump(values, f, ensure_ascii=False, indent=4)
        # tb = urllib.parse.unquote_to_bytes(values["certificateData"])
        # print(tb)
        # file = open("temp.pdf","wb")
        # file.write(io.BytesIO(tb).getbuffer())
        # file.close()
        

    except exception as e:
        print(e)
    #print(jsonify(request.data))
    # print(values)
    print("certi generated")
    if not all(k in values for k in required):
        return 'Missing values', 400

    # Create a new Transaction
    print("current count ",blockchain.currentTransactionscount)
    print("block count ",blockchain.transactionsPerBlock)
    if(blockchain.currentTransactionscount <= blockchain.transactionsPerBlock - 1):
        index = blockchain.new_transaction(values['certificateName'],values['certificateData'])

        response = {'message': f'Transaction will be added to Block {index}'}
        blockchain.currentTransactionscount = blockchain.currentTransactionscount + 1
        return jsonify(response), 201
    else:
        mine()
        index = blockchain.new_transaction(values['certificateName'],values['certificateData'])

        response = {'message': f'New Block create and transaction will be added to Block {index}'}
        blockchain.currentTransactionscount = 1
        return jsonify(response), 201



@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200


@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    try:
        values = request.get_json()

        nodes = values.get('nodes')
        if nodes is None:
            return "Error: Please supply a valid list of nodes", 400

        for node in nodes:
            blockchain.register_node(node)
    except exception as e:
        print(e)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201


@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.chain
        }

    return jsonify(response), 200

@app.route('/getlivestatus',methods=['GET'])
def getlivestatus():
    Response = {
        "Number of blocks mined" : len(blockchain.chain),
        "Certificate count" : (len(blockchain.chain) -1 ) + blockchain.currentTransactionscount
    }
    return jsonify(Response), 200

@app.route('/getactivenodes',methods=['GET'])
def getactivenodes():
    Response = {
        "Number of active nodes" : len(blockchain.nodes),
        "Active nodes are" : str(blockchain.nodes)
    }
    return jsonify(Response), 200

@app.route('/gettransferfile',methods=['POST'])
def get_file():
    try:
        with open(resource_path("data.json"), "r") as read_file:
            data = json.load(read_file)
        # values = json.loads(request.data)
        # print(values)
        tb = urllib.parse.unquote_to_bytes(data["certificateData"])
        file = open(resource_path("temp.pdf"),"wb+")
        file.write(io.BytesIO(tb).getbuffer())
        file.close()
    except Exception as e:
        print(e)
    # Response = {
    #     "message": "successful",
    # #     "Number of active nodes" : len(blockchain.nodes),
    #     "Active nodes are" : str(blockchain.nodes)
    # }

    response = {'message': 'Downloaded file'}
    return jsonify(response), 200

# @app.route('/getnodes',method=['POST'])
# def getnodes():
#     response = {
#         'nodes': blockchain.node,
#         'length': len(blockchain.node),
#     }
#     return jsonify(response), 200



if __name__ == '__main__':
    
    app.run(host='0.0.0.0', port=port)