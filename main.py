import hashlib
import json
from time import time
from urllib.parse import urlparse
import threading
from threading import Timer
import requests
import os
from flask import Flask, jsonify, request,  render_template
from flask_cors import CORS

class Smart_Blockchain:
    def __init__(self):
        self.current_transactions = []
        self.chain = []
        self.nodes = set()

        # Create the genesis block
        self.new_block(previous_hash='1')


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


    def smart_chain(self):
        """
        All nodes can receive the smart_chain
        """
        
        schain = None       
        response = requests.get(f'http://127.0.0.1:5000/chain')
        
        if response.status_code == 200:
            chain = response.json()['chain']                
            schain = chain

        # Replace our chain
        if schain:
            self.chain = schain
            return True

        return False


    def new_block(self, previous_hash):
        """
        Create a new Block in the Smart Blockchain
        :param previous_hash: Hash of previous Block
        :return: New Block
        """

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        # Reset the current list of transactions
        self.current_transactions = []

        self.chain.append(block)
        return block

   

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

    
# Instantiate the Node
app = Flask(__name__)
CORS(app)

# Instantiate the Smart_Blockchain
blockchain = Smart_Blockchain()


@app.route('/')
def renderIndex():
    return render_template('index.html')


def mine():
    last_block = blockchain.last_block

    # Forge the new Block by adding it to the chain
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(previous_hash)



@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200


@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()

    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201


@app.route('/smart/chain', methods=['GET'])
def smart_chain():
    replaced = blockchain.smart_chain()

    if replaced:    
        response = {
            'message': 'Smart chain update by bpsc',
            'smart chain': blockchain.chain,
            'length': len(blockchain.chain)
        }
    else:
        response = {
            'message': 'Unsuccessful: Please try again',
            'old chain': blockchain.chain,
            'length': len(blockchain.chain)            
        }
        
    return jsonify(response), 200

@app.route('/nodes', methods=['GET'])
def get_node():
    nodes = blockchain.nodes

    if len(nodes)>=0:    
        response = {
            'nodes': list(blockchain.nodes),
            'length': len(list(blockchain.nodes)),
        }
    else:
        return jsonify('error'), 400
        
    return jsonify(response), 200

blockchain.register_node("http://tin-node:5001")
def add_node():
    print("add 1")
    mine()
    timer = Timer(1, add_node)
    timer.start()

if __name__ == '__main__':
    add_node()
    app.run(host='0.0.0.0', port=5000)

