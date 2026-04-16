"""
Une Mini-blockchain  en Python
"""
import hashlib
import json
import time
from datetime import datetime

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


if __name__ == '__main__':
    print("\n=== TEST TRANSACTION ===")
    tx1 = Transaction('Alice', 'Bob', 0.5)
    tx2 = Transaction('Bob', 'Carol', 0.2)
    tx3 = Transaction('Carol', 'Dave', 0.1)

    print(tx1)
    print(tx2)
    print(tx3)

    tx_a = Transaction('Alice', 'Bob', 0.5)
    time.sleep(0.1)
    tx_b = Transaction('Alice', 'Bob', 0.5)

    print(f"\ntx_a = {tx_a.tx_id[:16]}...")
    print(f"tx_b = {tx_b.tx_id[:16]}...")
    print("Identiques ?", tx_a.tx_id == tx_b.tx_id)  # False attendu



class Block:
    """Représente un bloc dans la blockchain."""

    def __init__(self, index: int, transactions: list,
                 previous_hash: str = '0' * 64):
        self.index         = index
        self.transactions  = transactions
        self.previous_hash = previous_hash
        self.timestamp     = time.time()
        self.nonce         = 0
        self.hash          = self.calculate_hash()

    def calculate_hash(self) -> str:
        """Calcule le SHA-256 du bloc."""
        block_data = json.dumps({
            "index": self.index,
            "transactions": [tx.to_dict() for tx in self.transactions],
            "previous_hash": self.previous_hash,
            "timestamp": self.timestamp,
            "nonce": self.nonce
        }, sort_keys=True).encode()
        return hashlib.sha256(block_data).hexdigest()

    def mine_block(self, difficulty: int) -> None:
        """Proof of Work : cherche un hash commençant par N zéros."""
        target = '0' * difficulty
        start_time = time.time()
        attempts = 0

        print(f"\n    Minage du bloc #{self.index} (difficulté {difficulty})...")

        while not self.hash.startswith(target):
            self.nonce += 1
            self.hash = self.calculate_hash()
            attempts += 1

        elapsed = time.time() - start_time
        print(f"    ✓ Bloc #{self.index} miné en {elapsed:.3f}s"
              f" | nonce={self.nonce:,}"
              f" | tentatives={attempts:,}"
              f" | hash={self.hash[:16]}...")

    def __repr__(self) -> str:
        return (
            f"Block #{self.index} | "
            f"{len(self.transactions)} tx | "
            f"nonce={self.nonce} | "
            f"hash={self.hash[:12]}..."
        )


if __name__ == '__main__':
    print("\n=== TEST BLOCK + PROOF OF WORK ===")
    tx_list = [
        Transaction('Alice', 'Bob', 0.5),
        Transaction('Bob', 'Carol', 0.3),
    ]

    for diff in [2, 3]:
        b = Block(index=1, transactions=tx_list)
        b.mine_block(difficulty=diff)


class Blockchain:
    """Gère la chaîne de blocs complète."""

    def __init__(self, difficulty: int = 3):
        self.difficulty = difficulty
        self.chain      = []
        self.pending_tx = []
        self._create_genesis_block()

    def _create_genesis_block(self) -> None:
        """Crée le bloc #0 (genesis)."""
        genesis_block = Block(index=0, transactions=[], previous_hash='0' * 64)
        genesis_block.mine_block(self.difficulty)
        self.chain.append(genesis_block)

    @property
    def last_block(self) -> Block:
        return self.chain[-1]

    def add_transaction(self, tx: Transaction) -> None:
        self.pending_tx.append(tx)

    def add_block(self, miner: str = 'Miner') -> Block:
        """Mine un bloc avec toutes les transactions en attente."""
        if not self.pending_tx:
            print("[WARN] Aucune transaction en attente.")

        coinbase = Transaction('COINBASE', miner, 6.25)
        txs = [coinbase] + self.pending_tx

        new_block = Block(
            index=len(self.chain),
            transactions=txs,
            previous_hash=self.last_block.hash
        )

        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)
        self.pending_tx = []
        return new_block

    def get_balance(self, address: str) -> float:
        balance = 0.0
        for block in self.chain:
            for tx in block.transactions:
                if tx.from_ == address:
                    balance -= tx.amount
                if tx.to == address:
                    balance += tx.amount
        return balance

    def display_chain(self) -> None:
        print("\n" + "="*70)
        print(f"  BLOCKCHAIN | {len(self.chain)} blocs | difficulté={self.difficulty}")
        print("="*70)
        for block in self.chain:
            print(f"[{block.index}] hash={block.hash[:20]}... "
                  f"prev={block.previous_hash[:12]}... "
                  f"nonce={block.nonce:,} txs={len(block.transactions)}")
        print("="*70)


if __name__ == '__main__':
    print("\n=== TEST BLOCKCHAIN ===")
    bc = Blockchain(difficulty=3)

    bc.add_transaction(Transaction('Alice', 'Bob', 1.0))
    bc.add_transaction(Transaction('Alice', 'Carol', 0.5))
    bc.add_block(miner='MinerA')

    bc.add_transaction(Transaction('Bob', 'Dave', 0.3))
    bc.add_block(miner='MinerB')

    bc.display_chain()
