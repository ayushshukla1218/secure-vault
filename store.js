// store.js — In-memory data store (users, vaults, RSA keys)
const { v4: uuidv4 } = require('uuid');

const users = {};   // { userId: { id, username, masterHash, rsaPublicKey, rsaPrivateKeyEncrypted } }
const vaults = {};  // { userId: [ { id, site, username, encryptedPassword, createdAt, updatedAt } ] }

function createUser(username, masterHash, rsaPublicKey, rsaPrivateKeyEncrypted) {
  const id = uuidv4();
  users[id] = { id, username, masterHash, rsaPublicKey, rsaPrivateKeyEncrypted };
  vaults[id] = [];
  return users[id];
}

function findUserByUsername(username) {
  return Object.values(users).find(u => u.username === username) || null;
}

function findUserById(id) {
  return users[id] || null;
}

function addVaultEntry(userId, entry) {
  const record = { id: uuidv4(), ...entry, createdAt: new Date().toISOString(), updatedAt: new Date().toISOString() };
  vaults[userId].push(record);
  return record;
}

function getVaultEntries(userId) {
  return vaults[userId] || [];
}

function updateVaultEntry(userId, entryId, patch) {
  const entries = vaults[userId] || [];
  const idx = entries.findIndex(e => e.id === entryId);
  if (idx === -1) return null;
  entries[idx] = { ...entries[idx], ...patch, updatedAt: new Date().toISOString() };
  return entries[idx];
}

function deleteVaultEntry(userId, entryId) {
  const entries = vaults[userId] || [];
  const idx = entries.findIndex(e => e.id === entryId);
  if (idx === -1) return false;
  entries.splice(idx, 1);
  return true;
}

module.exports = { createUser, findUserByUsername, findUserById, addVaultEntry, getVaultEntries, updateVaultEntry, deleteVaultEntry };
