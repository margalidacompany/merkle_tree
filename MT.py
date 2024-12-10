import os
import hashlib

def list_docs(folder):
    n = []
    for archivo in os.listdir(folder):
        if archivo.endswith('.pdf') or archivo.endswith('.dat'):
            n.append(archivo)
    return n

def calc_hash(archivo, prefix):
    hash_sha1 = hashlib.sha1()
    hash_sha1.update(bytes.fromhex(prefix))
    with open(archivo, 'rb') as f:
        for bloque in iter(lambda: f.read(4096), b""):
            hash_sha1.update(bloque)
    return hash_sha1.digest() 

def combine_hashes(hash1, hash2, prefix):
    hash_sha1 = hashlib.sha1()
    hash_sha1.update(bytes.fromhex(prefix))
    hash_sha1.update(hash1 + hash2)
    return hash_sha1.digest()

def almacenar_hashes(titulos, n, folder):
    LEAF_PREFIX = "3C3C3C3C"
    NODE_PREFIX = "F5F5F5F5"
    
    #altura del arbol
    altura = 0
    num_nodos = n
    while num_nodos > 1:
        num_nodos = (num_nodos + 1) // 2
        altura += 1
    
    nodos_info = []
    
    #guarda hashes de documents 
    nivel_actual = []
    for i in range(n):
        archivo_completo = os.path.join(folder, titulos[i])
        if os.path.exists(archivo_completo):
            hash_documento = calc_hash(archivo_completo, LEAF_PREFIX)
            nombre_archivo = f'nodes/node{altura}.{i}'
            with open(nombre_archivo, 'wb') as f:
                f.write(hash_documento)
            nivel_actual.append((i, hash_documento))
            nodos_info.append(f"{altura}:{i}:{hash_documento.hex()}")
        else:
            print(f"File not found: {archivo_completo}")

    root_hash = None
    for nivel in range(altura-1, -1, -1):
        nivel_siguiente = []
        for i in range(0, len(nivel_actual), 2):
            idx1, hash1 = nivel_actual[i]
            
            if i + 1 < len(nivel_actual):
                idx2, hash2 = nivel_actual[i + 1]
            else:
                hash2 = hash1
                idx2 = idx1

            hash_combined = combine_hashes(hash1, hash2, NODE_PREFIX)
            nuevo_idx = i // 2
            nombre_archivo = f'nodes/node{nivel}.{nuevo_idx}'
            
            with open(nombre_archivo, 'wb') as f:
                f.write(hash_combined)
            nivel_siguiente.append((nuevo_idx, hash_combined))
            nodos_info.append(f"{nivel}:{nuevo_idx}:{hash_combined.hex()}")
            
            if nivel == 0:
                root_hash = hash_combined

        nivel_actual = nivel_siguiente

    with open('merkle_tree.txt', 'w') as f:
        f.write(f"MerkleTree:sha1:{LEAF_PREFIX}:{NODE_PREFIX}:{n}:{altura+1}:{root_hash.hex()}\n")
        for nodo in nodos_info:
            f.write(f"{nodo}\n")

def main():
    folder = './docs'
    os.makedirs('nodes', exist_ok=True)

    titulos = list_docs(folder)
    n = len(titulos)

    almacenar_hashes(titulos, n, folder)
    print("Merkle tree done. ")
    print("A text file has been created with the MerkleTree information")

if __name__ == "__main__":
    main()