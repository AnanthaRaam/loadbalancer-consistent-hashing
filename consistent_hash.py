import matplotlib.pyplot as plt
import hashlib
from bisect import bisect, bisect_left, bisect_right

# server node class
class ServerNode:
    
    def __init__(self,_id = None,ip = None):
        self._id = _id
        self.ip = ip

# loadbalancer based on normal hash function 
def modn_hash(key: str,n: int):
    return sum(bytearray(key.encode("utf-8")))%n
        
# hash function defined for consistent hashing
def hash_function(key : str, ring_space: int):
    
    h = hashlib.sha256()
    h.update(bytes(key.encode("utf-8")))
    return int(h.hexdigest(),16)%ring_space
        
# load balancer class
class LoadBalancer:

    def __init__(self):
        self.keys = [] # index of nodes present in hash ring space
        self.nodes = []     # nodes present in hash ring space
        self.ring_space = 50        # size of hash ring space
    
    def add_node(self, node: ServerNode):
        
        # Exception handling when hash space is full
        if( len(self.keys) == self.ring_space ):
            raise Exception("hash ring space is full")
        
        # Get key value for given node using its ip address
        hashed_key = hash_function(node.ip,self.ring_space)
        # this key is index where node will stored in hashspace ring
        # insert the key in keys array so as to maintain the sorted order of indices
        hashed_index = bisect(self.keys,hashed_key)
        
        # if already node is present at same key or duplication raise exception
        if( hashed_index > 0 and self.keys[hashed_index-1] == hashed_key):
            raise Exception("collision occurred")
        # nodes[i] gives a node whose index in hash space is keys[i]
        self.nodes.insert(hashed_index,node)
        self.keys.insert(hashed_index,hashed_key)
        return hashed_key
        
    def remove_node(self, node: ServerNode):
        
        # if no node exists
        if( len(self.keys) == 0 ):
            raise Exception("hash ring space is empty")
        # get key or index of node in hash ring
        hashed_key = hash_function(node.ip,self.ring_space)
        # get index of node in keys array
        hashed_index = bisect_left(self.keys,hashed_key)
        
        # if requested node does not exists raise exception
        if( hashed_index >= len(self.keys) or self.keys[hashed_index] != hashed_key ):
            raise Exception("requested node does not exists")
        
        # delete the node and its index in hashring
        self.keys.pop(hashed_index)
        self.nodes.pop(hashed_index)
        
        return hashed_key
    
    def assign_task_to_node(self, item: str):
        
        hashed_key = hash_function(item,self.ring_space)
        
        # find the first node to the right of this key
        # if bisect_right returns index out of range we take modulo to go to begining
        index = bisect_right(self.keys,hashed_key)%len(self.keys)
        
        #return node present at index
        return self.nodes[index]

    # function to display association between nodes and requests
    def display_info(self,req_list: list):
        for req in req_list:
            res = "file "+req+" is assigned to node "+self.assign_task_to_node(req)._id
            print(res)

    # function to plot association between nodes and requests
    def plot_info(self,h1: list,req_list: list = None,h2: list = None):
        if(req_list):
            req_list_index=[]
            for req in req_list:
                req_list_index.append(hash_function(req,self.ring_space))
            val=[]
            for i in range(0,len(self.keys)):
                val.append(self.nodes[i]._id)
            ax = plt.subplot(111)
            plt.xlim(0,50)
            plt.xticks(self.keys,val)
            ax.bar(self.keys,h1,color='b')
            ax.bar(req_list_index,h2,color='r')
            plt.show()
        else:
            val=[]
            for i in range(0,len(self.keys)):
                val.append(self.nodes[i]._id)
            plt.xlim(0,50)
            plt.xticks(self.keys,val)
            plt.bar(self.keys,h1)
            plt.show()

# function to execute normal hash function
def normal_hash(list_of_servers):
    
    print("number of server nodes available are: "+str(len(list_of_servers)))

    req_list = ["f1.txt","f2.txt","f3.txt","f4.txt","f5.txt"]
    for req in req_list:
        res = "file "+req+" is assigned to node "+list_of_servers[modn_hash(req,5)]._id
        print(res)
    print("\n")                               

# function to execute consistent hash function
def consistent_hash(list_of_servers):
    
    lb = LoadBalancer()
    # to define height of each server node in bar graph
    h1=[]
    # to define height of each request in bar graph
    h2=[5,5,5,5,5]
    req_list = ["f1.txt","f2.txt","f3.txt","f4.txt","f5.txt"]
    for server in list_of_servers:
        lb.add_node(server)
        h1.append(10) 
    lb.plot_info(h1,req_list,h2)
    lb.display_info(req_list)
    
    # adding two nodes and displaying plot
    
    """lb.add_node(ServerNode(_id='F', ip='107.117.238.203'))
    lb.add_node(ServerNode(_id='G', ip='27.161.219.131'))
    h1.append(10)
    h1.append(10)
    lb.plot_info(h1,req_list,h2)
    lb.display_info(req_list)"""

    # removing two nodes and displayig plot
    
    """lb.remove_node(ServerNode(_id='F', ip='107.117.238.203'))
    lb.remove_node(ServerNode(_id='G', ip='27.161.219.131'))
    h1.pop()
    h1.pop()
    lb.plot_info(h1,req_list,h2)
    lb.display_info(req_list)"""

if( __name__ == "__main__" ):
    
    list_of_servers = [
    ServerNode(_id='A', ip='239.67.52.72'),
    ServerNode(_id='B', ip='137.70.131.229'),
    ServerNode(_id='C', ip='98.5.87.182'),
    ServerNode(_id='D', ip='11.225.158.95'),
    ServerNode(_id='E', ip='203.187.116.210'),]

    # normal hash function distribution for 5 nodes

    # normal_hash(list_of_servers)           
    
    # adding two nodes

    #list_of_servers.append(ServerNode(_id='F', ip='107.117.238.203'))
    #list_of_servers.append(ServerNode(_id='G', ip='27.161.219.131'))
    
    # normal hash function distribution after adding 2 nodes
    
    #normal_hash(list_of_servers)
    
    #consistent hashing distribution
    
    consistent_hash(list_of_servers)