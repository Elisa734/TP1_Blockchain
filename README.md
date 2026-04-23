# 🔗 Mini-Blockchain Python

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Blockchain](https://img.shields.io/badge/Blockchain-Educational-orange?style=for-the-badge)

**Une blockchain simple en Python avec cryptographie ECDSA**

</div>

---

## 🎯 À propos

Implémentation pédagogique d'une blockchain pour comprendre les concepts fondamentaux :

- ⛏️ **Proof of Work** avec difficulté ajustable
- 🔗 **Chaînage cryptographique** immuable  
- 💰 **Transactions** et validation des soldes
- 🔐 **Wallets ECDSA** avec signatures numériques
- 🛡️ **Détection de falsification**

---

## 📁 Fichiers

| Fichier | Description |
|---------|-------------|
| `blockchain.py` | Blockchain complète avec Proof of Work |
| `wallet.py` | Extension avec wallets ECDSA |
| `exercice.py` | Version simplifiée pour apprentissage |

---

## 🚀 Installation

```bash
# Cloner
git clone https://github.com/Elisa734/TP1_Blockchain.git
cd TP1_Blockchain

# Dépendances optionnelles (pour ECDSA)
pip install cryptography
```

---

## 💻 Utilisation

```bash
# Démonstration complète
python blockchain.py

# Avec wallets cryptographiques
python wallet.py

# Version simple
python exercice.py
```

### Exemple rapide

```python
from blockchain import Blockchain, Transaction

# Créer blockchain
bc = Blockchain(difficulty=3)

# Ajouter transactions
bc.add_transaction(Transaction('Alice', 'Bob', 2.0))
bc.add_transaction(Transaction('Bob', 'Carol', 1.0))

# Miner un bloc
block = bc.add_block(miner='Miner1')

# Vérifier
print(f"Chaîne valide : {bc.is_chain_valid()}")
print(f"Solde Bob : {bc.get_balance('Bob')} BTC")
```

---

## ⚙️ Configuration

```python
# Difficulté de minage
bc = Blockchain(difficulty=3)  # hash commence par '000'

# Récompense de minage
coinbase = Transaction('COINBASE', miner, 6.25)
```

---

## 🔐 Wallets ECDSA

```python
from wallet import Wallet, SignedTransaction

# Créer wallets
alice = Wallet("Alice")
bob = Wallet("Bob")

# Transaction signée
tx = SignedTransaction(alice, bob.address, 1.5)
```

---

## 📚 Concepts

- **Blockchain** : Chaîne de blocs liés cryptographiquement
- **Mining** : Recherche de hash avec difficulté (Proof of Work)  
- **Transactions** : Transferts de valeur entre adresses
- **ECDSA** : Signatures numériques sur courbe elliptique

---

## 🧪 Tests

```bash
# Validation de chaîne : True
# Détection de falsification : Fonctionnelle
# Signatures cryptographiques : Validées
# Calcul de soldes : Précis
```

---

#

---

## 📄 License

MIT License - voir le fichier [LICENSE](LICENSE)

---

<div align="center">


</div>
