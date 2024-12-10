from MT import calc_hash, combine_hashes
import os
import hashlib

def read_proof_file(proof_file):
    with open(proof_file, 'r') as f:
        lines = f.readlines()
        
    doc_name = lines[0].split(': ')[1].strip()
    root_hash = lines[1].split(': ')[1].strip()
    leaf_prefix = lines[2].split(': ')[1].strip()
    node_prefix = lines[3].split(': ')[1].strip()
    
    proof_nodes = []
    for line in lines[5:]:  
        parts = line.strip().split(', ')
        level = int(parts[0].split(' ')[1])
        position = int(parts[1].split(' ')[1])
        is_left = "Left" in parts[2]
        hash_value = parts[2].split(': ')[1]
        
        proof_nodes.append({
            'level': level,
            'position': position,
            'is_left': is_left,
            'hash': hash_value
        })
    
    return {
        'doc_name': doc_name,
        'root_hash': root_hash,
        'leaf_prefix': leaf_prefix,
        'node_prefix': node_prefix,
        'proof_nodes': proof_nodes
    }

def verify_proof(doc_path, proof_file):
    proof_info = read_proof_file(proof_file)
    
    if not os.path.exists(doc_path):
        raise ValueError(f"Doc {doc_path} not found")
    
    current_hash = calc_hash(doc_path, proof_info['leaf_prefix'])
    print(f"\nHash of the document: {current_hash.hex()}")
    

    for node in proof_info['proof_nodes']:
        node_hash = bytes.fromhex(node['hash'])
        if node['is_left']:
            current_hash = combine_hashes(node_hash, current_hash, proof_info['node_prefix'])
        else:
            current_hash = combine_hashes(current_hash, node_hash, proof_info['node_prefix'])
        print(f"Level {node['level']}: {current_hash.hex()}")
    

    calculated_root = current_hash.hex()
    expected_root = proof_info['root_hash']
    
    print("\nVerification result:")
    print(f"Calculated hash: {calculated_root}")
    print(f"Expected root hash:  {expected_root}")
    
    if calculated_root == expected_root:
        print("\nSuccessful verification! The document belongs to the tree.")
        return True
    else:
        print("\nVerification failed! The document does not belong to the tree or the proof is invalid.")
        return False

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Use: python3 verify_MT.py <document_path> <proof_document_path>")
        sys.exit(1)
    
    doc_path = sys.argv[1]
    proof_file = sys.argv[2]
    
    try:
        verify_proof(doc_path, proof_file)
    except Exception as e:
        print(f"Error during verification: {e}")
        sys.exit(1)