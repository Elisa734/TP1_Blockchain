# 🔗 Mini-Blockchain Python - M1 RIST UFHB

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Blockchain](https://img.shields.io/badge/Blockchain-Educational-orange?style=for-the-badge)

**Implémentation complète d'une blockchain en Python avec cryptographie ECDSA**

*Auteur : GNETO Schiphra Grace*  
*Master 1 RIST - UFHB 2025-2026*

</div>

---

## 📖 Table des matières

- [🎯 Objectif](#-objectif)
- [✨ Fonctionnalités](#-fonctionnalités)
- [📁 Structure du projet](#-structure-du-projet)
- [🚀 Installation](#-installation)
- [💻 Utilisation](#-utilisation)
- [🔧 Configuration](#-configuration)
- [🧪 Tests](#-tests)
- [📚 Concepts](#-concepts)
- [🔍 Exemples](#-exemples)
- [🤝 Contribuer](#-contribuer)
- [📄 License](#-license)

---

## 🎯 Objectif

Ce projet est une implémentation pédagogique d'une blockchain en Python, développée dans le cadre du TP1 du Master 1 RIST à l'UFHB. Il permet de comprendre les concepts fondamentaux de la blockchain :

- **Structure des blocs** et chaînage cryptographique
- **Proof of Work** (minage) avec difficulté ajustable
- **Transactions** et validation des soldes
- **Cryptographie ECDSA** pour les signatures numériques
- **Détection de falsification** et intégrité de la chaîne

---

## ✨ Fonctionnalités

### 🧱 Core Blockchain
- ✅ **Génération de blocs** avec hash SHA-256
- ✅ **Proof of Work** avec difficulté configurable
- ✅ **Chaînage immuable** des blocs
- ✅ **Validation d'intégrité** complète
- ✅ **Détection de falsification**

### 💰 Transactions
- ✅ **Création de transactions** avec identifiants uniques
- ✅ **Calcul des soldes** par adresse
- ✅ **Mempool** (transactions en attente)
- ✅ **Récompenses de minage** (coinbase)

### 🔐 Cryptographie (Extension)
- ✅ **Wallets ECDSA** (courbe secp256k1)
- ✅ **Signature numérique** des transactions
- ✅ **Vérification cryptographique**
- ✅ **Génération d'adresses** sécurisées

### 🛡️ Sécurité
- ✅ **Détection d'attaques** de falsification
- ✅ **Validation des signatures** numériques
- ✅ **Tests d'intégrité** complets

---

## 📁 Structure du projet

```
TP1blockchain/
├── blockchain.py          # Implémentation principale de la blockchain
├── wallet.py             # Extension avec wallets ECDSA
├── exercice.py           # Version simplifiée pour exercices
├── README.md             # Documentation (ce fichier)
└── TP1_Blockchain_MiniChaine_Python_M1_RIST.docx  # Énoncé du TP
```

### 📋 Description des fichiers

| Fichier | Description | Fonctionnalités principales |
|---------|-------------|----------------------------|
| `blockchain.py` | Implémentation complète | Blockchain + PoW + Validation |
| `wallet.py` | Extension cryptographique | Wallets ECDSA + Signatures |
| `exercice.py` | Version pédagogique | Classes de base pour exercices |

---

## 🚀 Installation

### Prérequis
- **Python 3.8+**
- **pip** (gestionnaire de paquets Python)

### Installation des dépendances

```bash
# Cloner le repository
git clone https://github.com/votre-username/TP1blockchain.git
cd TP1blockchain

# Installation des dépendances optionnelles (pour ECDSA)
pip install cryptography
```

### 📦 Dépendances

| Package | Version | Utilité |
|---------|---------|---------|
| `cryptography` | `>=3.4.8` | Cryptographie ECDSA (optionnel) |
| `hashlib` | intégré | Hash SHA-256 |
| `json` | intégré | Sérialisation |
| `time` | intégré | Timestamps et minage |

---

## 💻 Utilisation

### 🎯 Démonstration rapide

```bash
# Lancer la démonstration complète
python blockchain.py
```

### 📊 Exécuter les différentes versions

```bash
# Version complète avec wallets ECDSA
python wallet.py

# Version simplifiée pour exercices
python exercice.py
```

### 🧪 Exemple d'utilisation

```python
from blockchain import Blockchain, Transaction

# Créer une blockchain
bc = Blockchain(difficulty=3)

# Ajouter des transactions
bc.add_transaction(Transaction('Alice', 'Bob', 2.0))
bc.add_transaction(Transaction('Bob', 'Carol', 1.0))

# Miner un bloc
block = bc.add_block(miner='Miner1')

# Vérifier l'intégrité
print(f"Chaîne valide : {bc.is_chain_valid()}")

# Afficher les soldes
print(f"Solde Bob : {bc.get_balance('Bob')} BTC")
```

### 🔐 Utilisation des wallets ECDSA

```python
from wallet import Wallet, SignedTransaction

# Créer des wallets
alice = Wallet("Alice")
bob = Wallet("Bob")

# Créer une transaction signée
tx = SignedTransaction(alice, bob.address, 1.5)

# Vérifier la signature
is_valid = Wallet.verify_with_public_key(
    alice.public_key, 
    tx.signature, 
    json.dumps(tx.to_dict(), sort_keys=True).encode()
)
print(f"Signature valide : {is_valid}")
```

---

## 🔧 Configuration

### ⚙️ Paramètres ajustables

```python
# Difficulté de minage (nombre de zéros en début de hash)
bc = Blockchain(difficulty=3)  # 3 = hash commence par '000'

# Récompense de minage (par défaut 6.25 BTC)
coinbase = Transaction('COINBASE', miner, 6.25)
```

### 🎛️ Options de configuration

| Paramètre | Valeur par défaut | Description |
|-----------|-------------------|-------------|
| `difficulty` | `3` | Difficulté du Proof of Work |
| `reward` | `6.25` | Récompense de minage en BTC |
| `hash_algorithm` | `SHA-256` | Algorithme de hashage |
| `curve` | `secp256k1` | Courbe elliptique ECDSA |

---

## 🧪 Tests

### 🧪 Tests de base inclus

```bash
# Test des transactions
python exercice.py

# Test de la blockchain complète
python blockchain.py

# Test des wallets ECDSA
python wallet.py
```

### 📊 Résultats attendus

- ✅ **Validation de chaîne** : `True`
- ✅ **Détection de falsification** : Blocs corrompus identifiés
- ✅ **Signatures cryptographiques** : Validées avec succès
- ✅ **Calcul de soldes** : Précis et cohérent

---

## 📚 Concepts abordés

### 🔗 Blockchain
- **Bloc** : Structure de données avec transactions, hash, nonce
- **Chaînage** : Lien cryptographique entre blocs successifs
- **Immutabilité** : Modification détectable des blocs passés

### ⛏️ Mining
- **Proof of Work** : Recherche de hash avec difficulté
- **Nonce** : Valeur incrémentale pour trouver le bon hash
- **Difficulté** : Nombre de zéros requis en début de hash

### 💸 Transactions
- **UTXO simplifié** : Modèle de transactions entrant/sortant
- **Soldes** : Calcul par parcours de la chaîne
- **Coinbase** : Récompense de minage

### 🔐 Cryptographie
- **ECDSA** : Signatures numériques sur courbe elliptique
- **secp256k1** : Courbe utilisée par Bitcoin
- **Adresses** : Dérivées des clés publiques

---

## 🔍 Exemples de sortie

### 📊 Affichage de la chaîne

```
======================================================================
  BLOCKCHAIN  |  4 blocs  |  difficulté=3
======================================================================
  [  0] hash=000abc123def456789...  prev=000000000000000000...  nonce=1,234  txs=0
  [  1] hash=000def789abc123456...  prev=000abc123def456789...  nonce=5,678  txs=4
  [  2] hash=000456def123abc789...  prev=000def789abc123456...  nonce=9,012  txs=3
  [  3] hash=000789123def456abc...  prev=000456def123abc789...  nonce=3,456  txs=2
======================================================================
```

### ⚡ Processus de minage

```
    Minage du bloc #1 (difficulté 3)...
    ✓ Bloc #1 miné en 0.234s | nonce=5,678 | 12,345 tentatives | hash=000def789abc123...
```

### 🔍 Détection de falsification

```
=== SIMULATION ATTAQUE ===
Modification : Alice→Bob 2.0 BTC → 20.0 BTC dans le bloc #1
Chaîne valide ? False
  ⚠ Bloc #1 | Hash incohérent | Le contenu du bloc a été modifié
```

---

## 🤝 Contribuer

### 📝 Comment contribuer

1. **Fork** le repository
2. **Créer une branche** (`git checkout -b feature/amélioration`)
3. **Committer** les changements (`git commit -m 'Ajout nouvelle fonctionnalité'`)
4. **Push** vers la branche (`git push origin feature/amélioration`)
5. **Ouvrir une Pull Request**

### 🐛 Rapporter un bug

- Utiliser les **Issues** GitHub
- Décrire le bug avec **exemples de code**
- Inclure les **messages d'erreur** complets

### 💡 Suggestions d'amélioration

- [ ] Interface web avec Flask/Django
- [ ] Support multi-nœuds (réseau P2P)
- [ ] Smart contracts simples
- [ ] Tests unitaires complets
- [ ] Documentation API

---

## 📄 License

Ce projet est sous licence **MIT** - voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

## 🙏 Remerciements

- **UFHB** - Université Félix Houphouët-Boigny
- **Master 1 RIST** - Programme de formation
- **Contributeurs** à l'écosystème blockchain opensource

---

## 📞 Contact

- **Auteur** : GNETO Schiphra Grace
- **Email** : [votre-email@ufhb.edu.ci]
- **GitHub** : [@votre-username](https://github.com/votre-username)

---

<div align="center">

**⭐ N'hésitez pas à mettre une étoile si ce projet vous a été utile !**

Made with ❤️ and Python

</div>
