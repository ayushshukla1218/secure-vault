// routes.js — All API endpoints
const express = require('express');
const router = express.Router();
const { hashMaster, encryptAES, decryptAES, generateRSAKeyPair, encryptWithRSA, decryptWithRSA, signData, verifySignature } = require('./crypto');
const { createUser, findUserByUsername, findUserById, addVaultEntry, getVaultEntries, updateVaultEntry, deleteVaultEntry } = require('./store');
const { auditChain } = require('./blockchain');

// --- Auth ---
router.post('/register', (req, res) => {
  const { username, masterPassword } = req.body;
  if (!username || !masterPassword) return res.status(400).json({ error: 'Missing fields' });
  if (findUserByUsername(username)) return res.status(409).json({ error: 'User exists' });

  const masterHash = hashMaster(masterPassword);
  const { publicKey, privateKey } = generateRSAKeyPair();
  // RSA private key is itself encrypted with masterPassword using AES
  const rsaPrivateKeyEncrypted = encryptAES(privateKey, masterPassword);
  const user = createUser(username, masterHash, publicKey, rsaPrivateKeyEncrypted);

  auditChain.addBlock({ event: 'REGISTER', detail: `User ${username} registered`, userId: user.id });
  res.json({ message: 'Registered successfully', userId: user.id, rsaPublicKey: publicKey });
});

router.post('/login', (req, res) => {
  const { username, masterPassword } = req.body;
  const user = findUserByUsername(username);
  if (!user || user.masterHash !== hashMaster(masterPassword)) {
    return res.status(401).json({ error: 'Invalid credentials' });
  }
  auditChain.addBlock({ event: 'LOGIN', detail: `User ${username} logged in`, userId: user.id });
  res.json({ message: 'Login successful', userId: user.id, rsaPublicKey: user.rsaPublicKey });
});

// --- Vault CRUD ---
router.post('/vault', (req, res) => {
  const { userId, masterPassword, site, username, password } = req.body;
  const user = findUserById(userId);
  if (!user || user.masterHash !== hashMaster(masterPassword)) return res.status(401).json({ error: 'Unauthorized' });

  const encryptedPassword = encryptAES(password, masterPassword);
  const entry = addVaultEntry(userId, { site, username, encryptedPassword });
  auditChain.addBlock({ event: 'ADD_PASSWORD', detail: `Added entry for ${site}`, userId });
  res.json({ message: 'Password saved', entry: { ...entry, encryptedPassword: undefined } });
});

router.get('/vault/:userId', (req, res) => {
  const { masterPassword } = req.query;
  const { userId } = req.params;
  const user = findUserById(userId);
  if (!user || user.masterHash !== hashMaster(masterPassword)) return res.status(401).json({ error: 'Unauthorized' });

  const entries = getVaultEntries(userId).map(e => ({
    id: e.id,
    site: e.site,
    username: e.username,
    password: decryptAES(e.encryptedPassword, masterPassword),
    createdAt: e.createdAt,
    updatedAt: e.updatedAt
  }));
  auditChain.addBlock({ event: 'VIEW_VAULT', detail: 'Vault accessed', userId });
  res.json({ entries });
});

router.put('/vault/:userId/:entryId', (req, res) => {
  const { userId, entryId } = req.params;
  const { masterPassword, site, username, password } = req.body;
  const user = findUserById(userId);
  if (!user || user.masterHash !== hashMaster(masterPassword)) return res.status(401).json({ error: 'Unauthorized' });

  const encryptedPassword = encryptAES(password, masterPassword);
  const updated = updateVaultEntry(userId, entryId, { site, username, encryptedPassword });
  if (!updated) return res.status(404).json({ error: 'Entry not found' });
  auditChain.addBlock({ event: 'UPDATE_PASSWORD', detail: `Updated entry for ${site}`, userId });
  res.json({ message: 'Updated', entry: { ...updated, encryptedPassword: undefined } });
});

router.delete('/vault/:userId/:entryId', (req, res) => {
  const { masterPassword } = req.body;
  const { userId, entryId } = req.params;
  const user = findUserById(userId);
  if (!user || user.masterHash !== hashMaster(masterPassword)) return res.status(401).json({ error: 'Unauthorized' });

  const deleted = deleteVaultEntry(userId, entryId);
  if (!deleted) return res.status(404).json({ error: 'Entry not found' });
  auditChain.addBlock({ event: 'DELETE_PASSWORD', detail: `Deleted entry ${entryId}`, userId });
  res.json({ message: 'Deleted' });
});

// --- Export with digital signature ---
router.post('/export', (req, res) => {
  const { userId, masterPassword } = req.body;
  const user = findUserById(userId);
  if (!user || user.masterHash !== hashMaster(masterPassword)) return res.status(401).json({ error: 'Unauthorized' });

  const entries = getVaultEntries(userId).map(e => ({
    site: e.site,
    username: e.username,
    password: decryptAES(e.encryptedPassword, masterPassword)
  }));
  const privateKey = decryptAES(user.rsaPrivateKeyEncrypted, masterPassword);
  const signature = signData(entries, privateKey);
  const isValid = verifySignature(entries, signature, user.rsaPublicKey);

  auditChain.addBlock({ event: 'EXPORT', detail: 'Passwords exported with digital signature', userId });
  res.json({ data: entries, signature, publicKey: user.rsaPublicKey, verified: isValid });
});

// --- RSA Recovery ---
router.post('/recover', (req, res) => {
  const { userId, masterPassword } = req.body;
  const user = findUserById(userId);
  if (!user || user.masterHash !== hashMaster(masterPassword)) return res.status(401).json({ error: 'Unauthorized' });

  const privateKey = decryptAES(user.rsaPrivateKeyEncrypted, masterPassword);
  // Re-encrypt master hash with RSA public key as a recovery token
  const recoveryToken = encryptWithRSA(user.masterHash, user.rsaPublicKey);
  auditChain.addBlock({ event: 'RECOVERY_INITIATED', detail: 'RSA recovery token generated', userId });
  res.json({ recoveryToken, message: 'Decrypt this token with your RSA private key to verify identity' });
});

// --- Audit Log ---
router.get('/audit/:userId', (req, res) => {
  const { masterPassword } = req.query;
  const { userId } = req.params;
  const user = findUserById(userId);
  if (!user || user.masterHash !== hashMaster(masterPassword)) return res.status(401).json({ error: 'Unauthorized' });

  const logs = auditChain.getLogs(userId);
  const isValid = auditChain.isChainValid();
  res.json({ logs, chainIntegrity: isValid });
});

module.exports = router;
