# merkle_tree
Merkle Tree Document Verification in Python. Python implementation of a Merkle Tree-based document verification system. This project includes tools for creating the tree, adding documents, generating proof files, and verifying document authenticity.

This project implements a **Merkle Tree-based system** for verifying document authenticity in Python. It includes scripts for creating a Merkle Tree, inserting new documents, generating proofs, and verifying document authenticity using those proofs.

## Project Structure

The project contains the following scripts:
- **`MT.py`**: Constructs the Merkle Tree and generates a record of the tree structure.
- **`insert_MT.py`**: Adds new documents to the tree, updating its structure and hash values.
- **`proof_MT.py`**: Generates a proof file for a specific document in the tree.
- **`verify_MT.py`**: Verifies the authenticity of a document using the generated proof file.

### Directory Structure
The repository should have the following structure:
├── MT.py 
├── insert_MT.py 
├── proof_MT.py 
├── verify_MT.py 
├── docs/ # Folder containing the documents to add to the Merkle Tree 
├── nodes/ # Generated folder containing node hashes 
├── proof/ # Generated folder containing proof files 
└── merkle_tree.txt # Record of the Merkle Tree structure


### ⚙ How to Use

- 1. Clone the Repository
- 2. Create your docs/ folder with your documents.
- 3. Create the Merkle Tree python3 MT.py
- 4. Add new documents to the tree with python3 insert_MT.py <path_to_new_document>
- 5. Generate a proof file with python3 proof_MT.py <document_name>
- 6. verify a document with python3 verify_MT.py <document_path> proof/proof_<document_name>.txt


### Technical Details
- Hashing Algorithm: SHA-1
- Prefixes: Separate prefixes for leaf nodes and internal nodes to mitigate second preimage attacks.
- Tree Construction 
    -Strategy: Bottom-up, starting with leaf hashes and computing parent hashes up to the root.
    -Storage: Nodes are stored as binary files in the /nodes folder.
- Proof and Verification
    -Proofs: Minimal information stored for efficient verification.
    -Verification: Recomputes the hash path from the document to the root and compares it with the recorded root hash.


