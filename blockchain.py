"""
╔══════════════════════════════════════════════════╗
  TP1 — Mini-Blockchain Python — M1 RIST UFHB 2025-2026          
  Auteur : GNETO Schiphra Grace                                    
╚══════════════════════════════════════════════════════════════════╝

"""
import hashlib
import json
import time
from datetime import datetime


# ==============================
# CLASSE TRANSACTION
# ============================================================
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
# PROGRAMME PRINCIPAL - DÉMONSTRATION
# ============================================================================

if __name__ == '__main__':

    print('\n' + '#' * 60)
    print('  SIMULATION BLOCKCHAIN — M1 RIST UFHB')
    print('#' * 60)

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