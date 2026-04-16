"""
╔══════════════════════════════════════════════════════════════════╗
║  TP1 — Mini-Blockchain Python — M1 RIST UFHB 2025-2026          ║
║  Auteur : GNETO Schiphra Grace                                   ║
║  Extension : Wallet ECDSA (Question TP1.8)                       ║
╚══════════════════════════════════════════════════════════════════╝

Une blockchain simple en python avec signatures numériques ECDSA.
"""
import hashlib
import json
import time
from datetime import datetime

# ============================================================================
# IMPORTS POUR LE WALLET ECDSA (Question TP1.8)
# ============================================================================
# Nécessite : pip install cryptography
# ============================================================================
try:
    from cryptography.hazmat.primitives.asymmetric import ec
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.exceptions import InvalidSignature
    CRYPTO_AVAILABLE = True
except ImportError:
    print("[WARN] Cryptography non installée. Wallet ECDSA désactivé.")
    print("       Installez avec : pip install cryptography")
    CRYPTO_AVAILABLE = False


# ============================================================================
# CLASSE TRANSACTION
# ============================================================================

class Transaction:
    """Représente une transaction simplifiée dans la blockchain."""

    def __init__(self, from_: str, to: str, amount: float):
        self.from_ = from_
        self.to = to
        self.amount = amount
        self.timestamp = time.time()
        self.tx_id = self._calculate_id()

    def _calculate_id(self) -> str:
        """Calcule le SHA-256 de la transaction — identifiant unique."""
        tx_data = json.dumps({
            "from": self.from_,
            "to": self.to,
            "amount": self.amount,
            "timestamp": self.timestamp
        }, sort_keys=True).encode()
        return hashlib.sha256(tx_data).hexdigest()

    def to_dict(self) -> dict:
        """Sérialise la transaction en dictionnaire."""
        return {
            "from": self.from_,
            "to": self.to,
            "amount": self.amount,
            "timestamp": self.timestamp,
            "tx_id": self.tx_id
        }

    def __repr__(self) -> str:
        dt = datetime.fromtimestamp(self.timestamp).strftime('%H:%M:%S')
        return (f"Tx[{self.tx_id[:8]}...] "
                f"{self.from_} → {self.to} : {self.amount:.4f} BTC @ {dt}")


# ============================================================================
# CLASSE BLOCK
# ============================================================================

class Block:
    """Représente un bloc dans la blockchain."""

    def __init__(self, index: int, transactions: list,
                 previous_hash: str = '0' * 64):
        self.index = index
        self.transactions = transactions  # liste de Transaction
        self.previous_hash = previous_hash
        self.timestamp = time.time()
        self.nonce = 0  # sera incrémenté lors du minage
        self.hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        """
        Calcule le SHA-256 du bloc.
        Inclut TOUS les champs : index, transactions, previous_hash,
        timestamp et nonce.
        """
        block_data = json.dumps({
            "index": self.index,
            "transactions": [tx.to_dict() for tx in self.transactions],
            "previous_hash": self.previous_hash,
            "timestamp": self.timestamp,
            "nonce": self.nonce
        }, sort_keys=True).encode()
        return hashlib.sha256(block_data).hexdigest()

    def mine_block(self, difficulty: int) -> None:
        """
        Proof of Work : mine le bloc jusqu'à trouver un hash
        commençant par 'difficulty' zéros.
        """
        target = '0' * difficulty
        start_time = time.time()
        attempts = 0

        print(f'    Minage du bloc #{self.index} (difficulté {difficulty})...')

        while not self.hash.startswith(target):
            self.nonce += 1
            self.hash = self.calculate_hash()
            attempts += 1

        elapsed = time.time() - start_time
        print(f'    ✓ Bloc #{self.index} miné en {elapsed:.3f}s'
              f' | nonce={self.nonce:,}'
              f' | {attempts:,} tentatives'
              f' | hash={self.hash[:16]}...')

    def __repr__(self) -> str:
        return (f"Block #{self.index} | "
                f"{len(self.transactions)} tx | "
                f"nonce={self.nonce} | "
                f"hash={self.hash[:12]}...")


# ============================================================================
# CLASSE BLOCKCHAIN
# ============================================================================

class Blockchain:
    """Gère la chaîne de blocs complète."""

    def __init__(self, difficulty: int = 3):
        self.difficulty = difficulty
        self.chain = []
        self.pending_tx = []  # transactions en attente de confirmation
        self._create_genesis_block()

    def _create_genesis_block(self) -> None:
        """Crée le bloc #0 (genesis) avec un previous_hash conventionnel."""
        genesis_block = Block(index=0, transactions=[], previous_hash='0' * 64)
        genesis_block.mine_block(self.difficulty)
        self.chain.append(genesis_block)

    @property
    def last_block(self) -> Block:
        """Retourne le dernier bloc de la chaîne."""
        return self.chain[-1]

    def add_transaction(self, tx: Transaction) -> None:
        """Ajoute une transaction dans la file d'attente (mempool)."""
        self.pending_tx.append(tx)

    def add_block(self, miner: str = 'Miner') -> Block:
        """
        Mine un nouveau bloc avec toutes les transactions en attente.
        Ajoute automatiquement une transaction coinbase (récompense mineur).
        """
        if not self.pending_tx:
            print('[WARN] Aucune transaction en attente, bloc vide créé.')

        # Transaction coinbase : récompense du mineur
        coinbase = Transaction('COINBASE', miner, 6.25)
        txs = [coinbase] + self.pending_tx

        new_block = Block(
            index=len(self.chain),
            transactions=txs,
            previous_hash=self.last_block.hash
        )

        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)
        self.pending_tx = []  # Vider la mempool
        return new_block

    def get_balance(self, address: str) -> float:
        """Calcule le solde d'une adresse en parcourant toutes les transactions."""
        balance = 0.0
        for block in self.chain:
            for tx in block.transactions:
                if tx.from_ == address:
                    balance -= tx.amount
                if tx.to == address:
                    balance += tx.amount
        return balance

    def is_chain_valid(self) -> bool:
        """Vérifie l'intégrité complète de la blockchain."""
        for i in range(1, len(self.chain)):
            curr = self.chain[i]
            prev = self.chain[i - 1]

            # Vérification 1 : cohérence du hash
            if curr.hash != curr.calculate_hash():
                return False

            # Vérification 2 : chaînage avec le bloc précédent
            if curr.previous_hash != prev.hash:
                return False

        return True

    def detect_tampering(self) -> list:
        """
        Parcourt la chaîne et retourne la liste des blocs corrompus.
        Retourne une liste vide si la chaîne est valide.
        """
        corrupted = []
        for i in range(1, len(self.chain)):
            curr = self.chain[i]
            prev = self.chain[i - 1]

            if curr.hash != curr.calculate_hash():
                corrupted.append((curr.index, "Hash incohérent",
                                  "Le contenu du bloc a été modifié"))
            elif curr.previous_hash != prev.hash:
                corrupted.append((curr.index, "Chaînage rompu",
                                  "Le hash du bloc précédent ne correspond pas"))

        return corrupted

    def display_chain(self) -> None:
        """Affiche la chaîne complète de façon lisible."""
        print('\n' + '=' * 70)
        print(f'  BLOCKCHAIN  |  {len(self.chain)} blocs  |  difficulté={self.difficulty}')
        print('=' * 70)
        for block in self.chain:
            print(f'  [{block.index:3d}] hash={block.hash[:20]}...'
                  f'  prev={block.previous_hash[:12]}...'
                  f'  nonce={block.nonce:,}'
                  f'  txs={len(block.transactions)}')
        print('=' * 70 + '\n')


# ============================================================================
# CLASSE WALLET - EXTENSION ECDSA (Question TP1.8)
# ============================================================================

if CRYPTO_AVAILABLE:
    
    class Wallet:
        """Wallet Bitcoin simplifié avec clés ECDSA (courbe secp256k1)."""
        
        def __init__(self, name: str = ""):
            """
            Crée un nouveau wallet avec une paire de clés ECDSA.
            
            Args:
                name: Nom optionnel du propriétaire (pour l'affichage)
            """
            self.name = name
            # Générer une clé privée sur la courbe secp256k1 (celle de Bitcoin)
            self.private_key = ec.generate_private_key(ec.SECP256K1())
            self.public_key = self.private_key.public_key()
            self.address = self._derive_address()

        def _derive_address(self) -> str:
            """Dérive une adresse simplifiée à partir de la clé publique."""
            pub_bytes = self.public_key.public_bytes(
                serialization.Encoding.X962,
                serialization.PublicFormat.CompressedPoint
            )
            # Dans le vrai Bitcoin : RIPEMD160(SHA256(pub_bytes))
            # Ici version simplifiée : SHA256 seulement
            return hashlib.sha256(pub_bytes).hexdigest()[:40]

        def sign(self, data: bytes) -> bytes:
            """Signe des données avec la clé privée."""
            return self.private_key.sign(
                data,
                ec.ECDSA(hashes.SHA256())
            )

        def verify(self, signature: bytes, data: bytes) -> bool:
            """Vérifie une signature avec la clé publique de CE wallet."""
            try:
                self.public_key.verify(
                    signature,
                    data,
                    ec.ECDSA(hashes.SHA256())
                )
                return True
            except InvalidSignature:
                return False

        @staticmethod
        def verify_with_public_key(public_key, signature: bytes, data: bytes) -> bool:
            """Vérifie une signature avec une clé publique donnée."""
            try:
                public_key.verify(
                    signature,
                    data,
                    ec.ECDSA(hashes.SHA256())
                )
                return True
            except InvalidSignature:
                return False

        def get_public_key_bytes(self) -> bytes:
            """Retourne la clé publique au format bytes (pour partage)."""
            return self.public_key.public_bytes(
                serialization.Encoding.X962,
                serialization.PublicFormat.CompressedPoint
            )

        def __repr__(self) -> str:
            name_str = f" ({self.name})" if self.name else ""
            return f"Wallet{name_str} | address={self.address[:12]}..."

else:
    # Fallback si cryptography n'est pas installée
    class Wallet:
        """Version simplifiée sans cryptographie (fallback)."""
        def __init__(self, name: str = ""):
            self.name = name
            self.address = hashlib.sha256(f"{name}{time.time()}".encode()).hexdigest()[:40]
        
        def sign(self, data: bytes) -> bytes:
            return hashlib.sha256(data).digest()
        
        def verify(self, signature: bytes, data: bytes) -> bool:
            return signature == hashlib.sha256(data).digest()
        
        def __repr__(self) -> str:
            name_str = f" ({self.name})" if self.name else ""
            return f"Wallet{name_str} (SIMULÉ) | address={self.address[:12]}..."


# ============================================================================
# TRANSACTION SIGNÉE (Extension pour utiliser les wallets)
# ============================================================================

class SignedTransaction(Transaction):
    """Transaction avec signature cryptographique."""
    
    def __init__(self, from_wallet: Wallet, to_address: str, amount: float):
        super().__init__(from_wallet.address, to_address, amount)
        self.from_wallet = from_wallet
        self.signature = None
        self.sign()
    
    def sign(self) -> None:
        """Signe la transaction avec le wallet de l'expéditeur."""
        tx_data = json.dumps(self.to_dict(), sort_keys=True).encode()
        self.signature = self.from_wallet.sign(tx_data)
    
    def verify(self, public_key) -> bool:
        """Vérifie la signature de la transaction."""
        tx_data = json.dumps(self.to_dict(), sort_keys=True).encode()
        return Wallet.verify_with_public_key(public_key, self.signature, tx_data)
    
    def to_dict(self) -> dict:
        """Sérialise la transaction signée en dictionnaire."""
        d = super().to_dict()
        if self.signature:
            d["signature"] = self.signature.hex()[:32] + "..."
        return d


# ============================================================================
# PROGRAMME PRINCIPAL - DÉMONSTRATION COMPLÈTE
# ============================================================================

if __name__ == '__main__':

    print('\n' + '#' * 70)
    print('  SIMULATION BLOCKCHAIN — M1 RIST UFHB')
    print('  Auteur : GNETO Schiphra Grace')
    print('#' * 70)

    # ========================================================================
    # PARTIE 1 : TEST DU WALLET ECDSA (Question TP1.8)
    # ========================================================================
    
    print('\n' + '=' * 70)
    print('  PARTIE 1 : TEST WALLET ECDSA (Question TP1.8)')
    print('=' * 70)
    
    if CRYPTO_AVAILABLE:
        print('\n[INFO] Cryptography installée — Wallet ECDSA actif (secp256k1)')
        
        # Créer des wallets pour Alice et Bob
        alice = Wallet("Alice")
        bob = Wallet("Bob")
        
        print(f'\n=== WALLETS CRÉÉS ===')
        print(f'  {alice}')
        print(f'  {bob}')
        
        # Alice crée une transaction
        print(f'\n=== CRÉATION D\'UNE TRANSACTION SIGNÉE ===')
        tx = SignedTransaction(alice, bob.address, 1.5)
        print(f'  {tx}')
        
        # Vérifier la signature avec la clé publique d'Alice
        is_valid = Wallet.verify_with_public_key(
            alice.public_key,
            tx.signature,
            json.dumps(tx.to_dict(), sort_keys=True).encode()
        )
        print(f'\n=== VÉRIFICATION DE LA SIGNATURE ===')
        print(f'  Signature valide avec clé publique d\'Alice ? {is_valid}')
        
        # Test avec une fausse transaction (fraude)
        print(f'\n=== TEST DE FRAUDE ===')
        fake_tx_data = b"transaction trafiquee"
        is_valid_fake = Wallet.verify_with_public_key(
            alice.public_key,
            tx.signature,
            fake_tx_data
        )
        print(f'  Transaction falsifiée acceptée ? {is_valid_fake}')
        
        # Test : Bob essaie de vérifier une transaction qu'il n'a pas signée
        print(f'\n=== TEST USURPATION D\'IDENTITÉ ===')
        fake_tx = SignedTransaction(bob, alice.address, 100.0)
        is_valid_usurpation = Wallet.verify_with_public_key(
            alice.public_key,
            fake_tx.signature,
            json.dumps(fake_tx.to_dict(), sort_keys=True).encode()
        )
        print(f'  Bob se fait passer pour Alice ? {is_valid_usurpation}')
        
    else:
        print('\n[WARN] Cryptography NON installée — Wallet SIMULÉ')
        alice = Wallet("Alice")
        bob = Wallet("Bob")
        print(f'  {alice}')
        print(f'  {bob}')

    # ========================================================================
    # PARTIE 2 : DÉMONSTRATION BLOCKCHAIN
    # ========================================================================
    
    print('\n' + '=' * 70)
    print('  PARTIE 2 : DÉMONSTRATION BLOCKCHAIN')
    print('=' * 70)

    # 1. Créer la blockchain (difficulté 3 = hash commence par '000')
    bc = Blockchain(difficulty=3)
    print(f'\n[INFO] Blockchain initialisée | Genesis : {bc.chain[0].hash[:20]}...')

    # 2. Simuler des transactions
    print('\n=== BLOC 1 — Transactions Alice, Bob, Carol ===')
    bc.add_transaction(Transaction('Alice', 'Bob', 2.0))
    bc.add_transaction(Transaction('Alice', 'Carol', 1.0))
    bc.add_transaction(Transaction('Bob', 'Dave', 0.5))
    bloc1 = bc.add_block(miner='PoolAntMiner')

    print('\n=== BLOC 2 — Transactions Dave, Carol ===')
    bc.add_transaction(Transaction('Dave', 'Alice', 0.2))
    bc.add_transaction(Transaction('Carol', 'Bob', 0.3))
    bloc2 = bc.add_block(miner='PoolBTC.com')

    print('\n=== BLOC 3 — Transaction unique ===')
    bc.add_transaction(Transaction('Bob', 'Eve', 0.1))
    bloc3 = bc.add_block(miner='PoolViaBTC')

    # 3. Afficher la chaîne complète
    bc.display_chain()

    # 4. Vérifier l'intégrité
    print(f'Chaîne intègre ? {bc.is_chain_valid()}')  # True

    # 5. Afficher les soldes
    print('\n=== SOLDES ===')
    for addr in ['Alice', 'Bob', 'Carol', 'Dave', 'Eve',
                 'PoolAntMiner', 'PoolBTC.com', 'PoolViaBTC']:
        bal = bc.get_balance(addr)
        if bal != 0:
            print(f'  {addr:20s} : {bal:+.4f} BTC')

    # 6. Attaque de falsification
    print('\n=== SIMULATION ATTAQUE ===')
    print('Modification : Alice→Bob 2.0 BTC → 20.0 BTC dans le bloc #1')
    bc.chain[1].transactions[1].amount = 20.0
    print(f'Chaîne valide ? {bc.is_chain_valid()}')
    corrupted = bc.detect_tampering()
    for idx, reason, detail in corrupted:
        print(f'  ⚠ Bloc #{idx} | {reason} | {detail}')

    # 7. Bonus : visualiser l'impact de la difficulté
    print('\n=== BENCHMARK DIFFICULTÉ ===')
    for diff in [2, 3, 4]:
        test_bc = Blockchain(difficulty=diff)
        t0 = time.time()
        test_bc.add_transaction(Transaction('Test', 'Node', 1.0))
        test_bc.add_block(miner='BenchMiner')
        print(f'  Difficulté {diff} : {time.time() - t0:.3f}s')

    # ========================================================================
    # FIN
    # ========================================================================
    
    print('\n' + '#' * 70)
    print('  FIN DE LA DÉMONSTRATION')
    print('  TP1 — Mini-Blockchain Python — M1 RIST UFHB 2025-2026')
    print('#' * 70 + '\n')