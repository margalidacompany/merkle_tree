from MT import calc_hash, combine_hashes
from insert_MT import read_merkle_info
import os
import hashlib

def find_document_position(doc_name, tree_info):
    if not os.path.exists(f'docs/{doc_name}'):
        raise ValueError(f"Doc {doc_name} no found in the docs folder")
    
    doc_hash = calc_hash(f'docs/{doc_name}', tree_info['leaf_prefix'])
    
    depth = tree_info['depth']
    for j in range(tree_info['num_docs']):
        if tree_info['nodes'].get((depth-1, j)) == doc_hash:
            return j
    
    raise ValueError(f"Doc {doc_name} is not in the tree")

def generate_proof(doc_name):
    tree_info = read_merkle_info()
    
    position = find_document_position(doc_name, tree_info)
    
    proof_nodes = []

    current_level = tree_info['depth'] - 1
    current_pos = position
    
    while current_level > 0:
        is_left = current_pos % 2 == 0
        sibling_pos = current_pos + 1 if is_left else current_pos - 1
        
        if (current_level, sibling_pos) in tree_info['nodes']:
            proof_nodes.append({
                'level': current_level,
                'position': sibling_pos,
                'hash': tree_info['nodes'][(current_level, sibling_pos)].hex(),
                'is_left': not is_left
            })
        
        current_pos = current_pos // 2
        current_level -= 1
    

    if not os.path.exists('proof'):
        os.makedirs('proof')
    
    proof_file = f'proof/proof_{doc_name}.txt'
    with open(proof_file, 'w') as f:
        f.write(f"Document: {doc_name}\n")
        f.write(f"Tree Root Hash: {tree_info['root_hash']}\n")
        f.write(f"Leaf Prefix: {tree_info['leaf_prefix']}\n")
        f.write(f"Node Prefix: {tree_info['node_prefix']}\n")
        f.write("Proof Nodes:\n")
        
        for node in proof_nodes:
            f.write(f"Level {node['level']}, Position {node['position']}, "
                   f"{'Left' if node['is_left'] else 'Right'} Node: {node['hash']}\n")
    
    print(f"Proof saved in {proof_file}")
    return proof_nodes

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Uso: python3 proof_MT.py doc_name")
        sys.exit(1)
    
    doc_name = sys.argv[1]
    
    try:
        generate_proof(doc_name)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)