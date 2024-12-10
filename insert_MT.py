from MT import calc_hash, combine_hashes
import os
import hashlib
import shutil

def read_merkle_info():
    with open('merkle_tree.txt', 'r') as f:
        header = f.readline().strip().split(':')

        _, hash_type, leaf_prefix, node_prefix, num_docs, depth, root_hash = header #heather
        
        nodes = {}
        for line in f:
            i, j, hash_value = line.strip().split(':')
            nodes[(int(i), int(j))] = bytes.fromhex(hash_value)
            
    return {
        'hash_type': hash_type,
        'leaf_prefix': leaf_prefix,
        'node_prefix': node_prefix,
        'num_docs': int(num_docs),
        'depth': int(depth),
        'root_hash': root_hash,
        'nodes': nodes
    }

def insert_document(doc_path):
    doc_name = os.path.basename(doc_path)
    
    if not os.path.exists('./docs'):
        os.makedirs('./docs')
    shutil.copy2(doc_path, f'./docs/{doc_name}')
    
    tree_info = read_merkle_info()
    num_docs = tree_info['num_docs']
    depth = tree_info['depth']
    nodes = tree_info['nodes']
    leaf_prefix = tree_info['leaf_prefix']
    node_prefix = tree_info['node_prefix']
    
    new_hash = calc_hash(f'./docs/{doc_name}', leaf_prefix)
    
    new_leaf_pos = num_docs
    with open(f'nodes/node{depth-1}.{new_leaf_pos}', 'wb') as f:
        f.write(new_hash)
    nodes[(depth-1, new_leaf_pos)] = new_hash
    

    current_hash = new_hash
    current_pos = new_leaf_pos
    
    for level in range(depth-2, -1, -1):
        is_left = current_pos % 2 == 0
        parent_pos = current_pos // 2
        
        if is_left:
            nodes[(level, parent_pos)] = current_hash
            with open(f'nodes/node{level}.{parent_pos}', 'wb') as f:
                f.write(current_hash)
        else:
            left_hash = nodes.get((level+1, current_pos-1))
            if left_hash:
                current_hash = combine_hashes(left_hash, current_hash, node_prefix)
                nodes[(level, parent_pos)] = current_hash
                with open(f'nodes/node{level}.{parent_pos}', 'wb') as f:
                    f.write(current_hash)
        
        current_pos = parent_pos
        

    with open('merkle_tree.txt', 'w') as f:
        f.write(f"MerkleTree:{tree_info['hash_type']}:{leaf_prefix}:{node_prefix}:"
                f"{num_docs+1}:{depth}:{nodes[(0,0)].hex()}\n")
        
        for (i, j), hash_value in sorted(nodes.items()):
            f.write(f"{i}:{j}:{hash_value.hex()}\n")

    print(f"Doc '{doc_name}' has been upload to the Merkle tree. The current number of docs is: {num_docs+1}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("You have to use: python insert_MT.py NewDocuments/document_name")
        sys.exit(1)
    
    doc_path = sys.argv[1]
    
    if not os.path.exists(doc_path):
        print(f"Error: File {doc_path} does not exist")
        sys.exit(1)
        
    insert_document(doc_path)