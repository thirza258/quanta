// Original educational account ledger. No peers, persistent storage, fork choice, or real currency.
import { createHash, createPublicKey, generateKeyPairSync, sign, verify } from "node:crypto";
import { pathToFileURL } from "node:url";

export const NETWORK = "quanta-cedar-local-v1";
const REWARD = 10;
const CAP = 1100;
const GENESIS_SUPPLY = 1000;
const PREFIX = "000"; // 12 leading zero bits: deliberately trivial proof of work.
const integer = (x, min = 0) => Number.isSafeInteger(x) && x >= min;
export const hash = (bytes) => createHash("sha256").update(bytes).digest("hex");
const bytes = (value) => Buffer.from(JSON.stringify(value), "utf8");
const publicBytes = (key) => key.export({type: "spki", format: "der"}).toString("hex");
export function wallet() {
  const pair = generateKeyPairSync("ed25519");
  return {privateKey: pair.privateKey, publicKey: publicBytes(pair.publicKey), address: hash(pair.publicKey.export({type: "spki", format: "der"}))};
}
const addressValid = (value) => typeof value === "string" && /^[0-9a-f]{64}$/.test(value);
function transactionBytes(tx) {
  // A fixed ordered tuple is the protocol encoding; arbitrary object key order is irrelevant.
  return bytes(["cedar-payment-v1", tx.network, tx.from, tx.to, tx.amount, tx.nonce, tx.publicKey]);
}
export function payment(sender, to, amount, nonce, network = NETWORK) {
  const tx = {network, from: sender.address, to, amount, nonce, publicKey: sender.publicKey};
  return {...tx, signature: sign(null, transactionBytes(tx), sender.privateKey).toString("hex")};
}
export function verifyPayment(tx) {
  try {
    if (!tx || tx.network !== NETWORK || !addressValid(tx.from) || !addressValid(tx.to)
      || !integer(tx.amount, 1) || !integer(tx.nonce) || typeof tx.publicKey !== "string"
      || !/^[0-9a-f]{88}$/.test(tx.publicKey) || !/^[0-9a-f]{128}$/.test(tx.signature)) return false;
    const encoded = Buffer.from(tx.publicKey, "hex");
    const key = createPublicKey({key: encoded, type: "spki", format: "der"});
    return key.asymmetricKeyType === "ed25519" && publicBytes(key) === tx.publicKey
      && hash(encoded) === tx.from && verify(null, transactionBytes(tx), key, Buffer.from(tx.signature, "hex"));
  } catch { return false; }
}
function leaf(tx) { return hash(Buffer.concat([Buffer.from([0]), transactionBytes(tx), Buffer.from(tx.signature, "hex")])); }
function branch(left, right) { return hash(Buffer.concat([Buffer.from([1]), Buffer.from(left, "hex"), Buffer.from(right, "hex")])); }
export function merkleRoot(transactions) {
  if (!transactions.length) return hash(Buffer.from([2]));
  let level = transactions.map(leaf);
  while (level.length > 1) {
    const next = [];
    for (let i = 0; i < level.length; i += 2) next.push(branch(level[i], level[i + 1] ?? level[i]));
    level = next;
  }
  return level[0];
}
export function merkleProof(transactions, index) {
  if (!integer(index) || index >= transactions.length) throw new Error("Invalid leaf index");
  let level = transactions.map(leaf), cursor = index;
  const siblings = [];
  while (level.length > 1) {
    const sibling = cursor % 2 ? cursor - 1 : cursor + 1;
    siblings.push({hash: level[sibling] ?? level[cursor], left: cursor % 2 === 1});
    const next = [];
    for (let i = 0; i < level.length; i += 2) next.push(branch(level[i], level[i + 1] ?? level[i]));
    level = next; cursor = Math.floor(cursor / 2);
  }
  return siblings;
}
export function verifyProof(tx, proof, root) {
  try {
    let value = leaf(tx);
    for (const sibling of proof) {
      if (!addressValid(sibling.hash) || typeof sibling.left !== "boolean") return false;
      value = sibling.left ? branch(sibling.hash, value) : branch(value, sibling.hash);
    }
    return value === root;
  } catch { return false; }
}
export function blockHash(block) {
  return hash(bytes(["cedar-block-v1", block.network, block.height, block.parent,
    block.merkleRoot, block.transactions.length, block.miner, block.reward, block.nonce]));
}
export class LocalChain {
  #balances; #nonces = new Map(); #blocks = []; #supply = GENESIS_SUPPLY; #tip;
  constructor(genesisAddress) {
    if (!addressValid(genesisAddress)) throw new Error("Invalid genesis recipient");
    this.#balances = new Map([[genesisAddress, GENESIS_SUPPLY]]);
    this.#tip = hash(bytes(["cedar-genesis-v1", NETWORK, genesisAddress, GENESIS_SUPPLY, CAP, REWARD, PREFIX]));
  }
  snapshot() {
    return {height: this.#blocks.length, tip: this.#tip, supply: this.#supply,
      balances: Object.fromEntries(this.#balances), nonces: Object.fromEntries(this.#nonces)};
  }
  blocks() { return structuredClone(this.#blocks); }
  mine(transactions, miner) {
    if (!Array.isArray(transactions) || transactions.length > 100 || !addressValid(miner)) throw new Error("Invalid block input");
    // Mining does not accept the block. append independently validates all economic rules.
    const block = {network: NETWORK, height: this.#blocks.length + 1, parent: this.#tip,
      transactions: structuredClone(transactions), merkleRoot: merkleRoot(transactions), miner,
      reward: Math.min(REWARD, CAP - this.#supply), nonce: 0};
    while (!blockHash(block).startsWith(PREFIX)) {
      block.nonce++;
      if (block.nonce > 2_000_000) throw new Error("Toy mining work limit exceeded");
    }
    block.hash = blockHash(block);
    return block;
  }
  append(block) {
    if (!block || block.network !== NETWORK || block.height !== this.#blocks.length + 1
      || block.parent !== this.#tip || !Array.isArray(block.transactions) || block.transactions.length > 100
      || !addressValid(block.miner) || !integer(block.nonce) || !addressValid(block.hash)
      || block.reward !== Math.min(REWARD, CAP - this.#supply)
      || block.hash !== blockHash(block) || !block.hash.startsWith(PREFIX)
      || block.merkleRoot !== merkleRoot(block.transactions)) throw new Error("Invalid block header or commitment");
    const balances = new Map(this.#balances), nonces = new Map(this.#nonces);
    for (const tx of block.transactions) {
      if (!verifyPayment(tx)) throw new Error("Invalid signature or transaction domain");
      if (tx.nonce !== (nonces.get(tx.from) ?? 0)) throw new Error("Invalid account nonce");
      const available = balances.get(tx.from) ?? 0;
      if (available < tx.amount) throw new Error("Insufficient balance");
      balances.set(tx.from, available - tx.amount);
      balances.set(tx.to, (balances.get(tx.to) ?? 0) + tx.amount);
      nonces.set(tx.from, tx.nonce + 1);
    }
    // Reward becomes spendable only after the block's transactions have validated.
    balances.set(block.miner, (balances.get(block.miner) ?? 0) + block.reward);
    const supply = this.#supply + block.reward;
    if (supply > CAP || [...balances.values()].some((v) => !integer(v))
      || [...balances.values()].reduce((a, b) => a + b, 0) !== supply) throw new Error("Supply invariant failed");
    this.#balances = balances; this.#nonces = nonces; this.#supply = supply;
    this.#blocks.push(structuredClone(block)); this.#tip = block.hash;
    return this.snapshot();
  }
}
if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  const alice = wallet(), bob = wallet(), chain = new LocalChain(alice.address);
  const tx = payment(alice, bob.address, 100, 0);
  const block = chain.mine([tx], alice.address);
  chain.append(block);
  console.log(JSON.stringify({scope: "local educational chain; no public network", network: NETWORK,
    signatureValid: verifyPayment(tx), proofValid: verifyProof(tx, merkleProof([tx], 0), block.merkleRoot),
    aliceBalance: chain.snapshot().balances[alice.address], bobBalance: chain.snapshot().balances[bob.address],
    supply: chain.snapshot().supply, height: 1, blockHash: block.hash}, null, 2));
}
