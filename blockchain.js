// blockchain.js — Immutable audit log using linked hash chain (simplified blockchain)
const crypto = require('crypto');

class Block {
  constructor(index, data, previousHash) {
    this.index = index;
    this.timestamp = new Date().toISOString();
    this.data = data;
    this.previousHash = previousHash;
    this.hash = this.calculateHash();
  }

  calculateHash() {
    const content = `${this.index}${this.timestamp}${JSON.stringify(this.data)}${this.previousHash}`;
    return crypto.createHash('sha256').update(content).digest('hex');
  }
}

class AuditBlockchain {
  constructor() {
    this.chain = [this.createGenesis()];
  }

  createGenesis() {
    return new Block(0, { event: 'GENESIS', message: 'Vault initialized' }, '0');
  }

  getLatestBlock() {
    return this.chain[this.chain.length - 1];
  }

  addBlock(data) {
    const block = new Block(this.chain.length, data, this.getLatestBlock().hash);
    this.chain.push(block);
    return block;
  }

  isChainValid() {
    for (let i = 1; i < this.chain.length; i++) {
      const current = this.chain[i];
      const previous = this.chain[i - 1];
      if (current.hash !== current.calculateHash()) return false;
      if (current.previousHash !== previous.hash) return false;
    }
    return true;
  }

  getLogs(userId) {
    return this.chain
      .filter(b => b.index > 0 && (!userId || b.data.userId === userId || b.data.userId === 'SYSTEM'))
      .map(b => ({
        index: b.index,
        timestamp: b.timestamp,
        event: b.data.event,
        detail: b.data.detail,
        userId: b.data.userId,
        hash: b.hash
      }));
  }
}

// Singleton — shared across all routes
const auditChain = new AuditBlockchain();

module.exports = { auditChain };
