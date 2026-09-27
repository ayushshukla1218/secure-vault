// crypto.js — AES encryption, SHA-256 hashing, RSA key generation & recovery
const forge = require('node-forge');
const crypto = require('crypto');

function hashMaster(password) {
  return crypto.createHash('sha256').update(password).digest('hex');
}

function encryptAES(plaintext, masterKey) {
  const iv = forge.random.getBytesSync(16);
  const key = forge.md.sha256.create().update(masterKey).digest().bytes();
  const cipher = forge.cipher.createCipher('AES-CBC', key);
  cipher.start({ iv });
  cipher.update(forge.util.createBuffer(plaintext, 'utf8'));
  cipher.finish();
  const encrypted = forge.util.encode64(cipher.output.bytes());
  const ivB64 = forge.util.encode64(iv);
  return `${ivB64}:${encrypted}`;
}

function decryptAES(ciphertext, masterKey) {
  const [ivB64, encrypted] = ciphertext.split(':');
  const iv = forge.util.decode64(ivB64);
  const key = forge.md.sha256.create().update(masterKey).digest().bytes();
  const decipher = forge.cipher.createDecipher('AES-CBC', key);
  decipher.start({ iv: forge.util.createBuffer(iv) });
  decipher.update(forge.util.createBuffer(forge.util.decode64(encrypted)));
  decipher.finish();
  return decipher.output.toString('utf8');
}

function generateRSAKeyPair() {
  const keypair = forge.pki.rsa.generateKeyPair({ bits: 2048 });
  return {
    publicKey: forge.pki.publicKeyToPem(keypair.publicKey),
    privateKey: forge.pki.privateKeyToPem(keypair.privateKey)
  };
}

function encryptWithRSA(plaintext, publicKeyPem) {
  const publicKey = forge.pki.publicKeyFromPem(publicKeyPem);
  const encrypted = publicKey.encrypt(plaintext, 'RSA-OAEP');
  return forge.util.encode64(encrypted);
}

function decryptWithRSA(ciphertextB64, privateKeyPem) {
  const privateKey = forge.pki.privateKeyFromPem(privateKeyPem);
  const encrypted = forge.util.decode64(ciphertextB64);
  return privateKey.decrypt(encrypted, 'RSA-OAEP');
}

function signData(data, privateKeyPem) {
  const privateKey = forge.pki.privateKeyFromPem(privateKeyPem);
  const md = forge.md.sha256.create();
  md.update(JSON.stringify(data), 'utf8');
  const signature = privateKey.sign(md);
  return forge.util.encode64(signature);
}

function verifySignature(data, signatureB64, publicKeyPem) {
  try {
    const publicKey = forge.pki.publicKeyFromPem(publicKeyPem);
    const md = forge.md.sha256.create();
    md.update(JSON.stringify(data), 'utf8');
    const signature = forge.util.decode64(signatureB64);
    return publicKey.verify(md.digest().bytes(), signature);
  } catch {
    return false;
  }
}

module.exports = {
  hashMaster,
  encryptAES,
  decryptAES,
  generateRSAKeyPair,
  encryptWithRSA,
  decryptWithRSA,
  signData,
  verifySignature
};
