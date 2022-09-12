import hashlib
import json
import os
from time import time
from urllib.parse import urlparse
import threading
from threading import Timer
import requests

class Smart_Blockchain:
    def __init__(self):
        self.current_information = []        
        self.chain = []
        self.chain2 = []
        self.nodes = set()

        # Create the genesis block
        self.new_block(previous_hash='1')


    def smart_chain(self):
        """
        All nodes can receive the smart_chain
        """
        response = requests.get(f'http://tin-server:5000/chain')
        
        if response.status_code == 200:
            chain = response.json()['chain']
            if len(chain) - len(self.chain) > 4: 
                requests.get(os.environ['WEBHOOK'])
            self.chain = chain


    def new_block(self, previous_hash):
        """
        Create a new Block in the Smart Blockchain
        :param previous_hash: Hash of previous Block
        :return: New Block
        """

        block = {
            'index2': len(self.chain2) + 1,
            'timestamp': time(),
            'information': self.current_information,
            'previous_hash': previous_hash or self.hash(self.chain2[-1]),
        }

        # Reset the current list of transactions
        self.current_information = []

        self.chain2.append(block)
        return block


    @property
    def last_block(self):
        return self.chain2[-1]


    @staticmethod
    def hash(block):
        """
        Creates a SHA-256 hash of a Block
        :param block: Block
        """

        # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()


# Instantiate the Smart_Blockchain
blockchain = Smart_Blockchain()

def check():
    print('checking chain ...')
    threading.Timer(int(os.environ['CHECK_DELAY']), check).start()
    blockchain.smart_chain()

check()
