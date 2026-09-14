import assert from "node:assert/strict";
import test from "node:test";
import {LocalChain, wallet, payment, verifyPayment, merkleRoot, merkleProof, verifyProof, hash, blockHash} from "./native-chain.mjs";
function setup() { const a = wallet(), b = wallet(); return {a, b, chain: new LocalChain(a.address)}; }
function rejectedWithoutStateChange(chain, block, pattern) {
  const before = chain.snapshot();
  assert.throws(() => chain.append(block), pattern);
  assert.deepEqual(chain.snapshot(), before);
}
test("SHA-256 standard vector and signature tampering", () => {
  assert.equal(hash("abc"), "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad");
  const {a, b} = setup(), tx = payment(a, b.address, 20, 0);
  assert.equal(verifyPayment(tx), true);
  assert.equal(verifyPayment({...tx, amount: 21}), false);
  assert.equal(verifyPayment({...tx, from: b.address}), false);
  assert.equal(verifyPayment(payment(a, b.address, 20, 0, "wrong-chain")), false);
  for (const amount of [-1, 0, .5, Number.MAX_SAFE_INTEGER + 1]) assert.equal(verifyPayment(payment(a, b.address, amount, 0)), false);
});
test("Merkle inclusion with odd count, ordered siblings, and changed data", () => {
  const {a, b} = setup();
  const txs = [0, 1, 2, 3, 4].map((i) => payment(a, b.address, i + 1, i));
  for (let i = 0; i < txs.length; i++) {
    const proof = merkleProof(txs, i);
    assert.equal(verifyProof(txs[i], proof, merkleRoot(txs)), true);
    assert.equal(verifyProof({...txs[i], amount: 999}, proof, merkleRoot(txs)), false);
  }
  assert.notEqual(merkleRoot(txs), merkleRoot(txs.toReversed()));
});
test("Native coin transfer, sequential nonce, and independently replayed chain", () => {
  const {a, b, chain} = setup();
  chain.append(chain.mine([payment(a, b.address, 100, 0)], a.address));
  assert.equal(chain.snapshot().balances[a.address], 910);
  assert.equal(chain.snapshot().balances[b.address], 100);
  assert.equal(chain.snapshot().supply, 1010);
  chain.append(chain.mine([payment(b, a.address, 25, 0)], a.address));
  assert.equal(chain.snapshot().balances[a.address], 945);
  assert.equal(chain.snapshot().balances[b.address], 75);
  const replay = new LocalChain(a.address);
  for (const block of chain.blocks()) replay.append(block);
  assert.deepEqual(replay.snapshot(), chain.snapshot());
});
test("Replay, insufficient funds, and late block failures are atomic", () => {
  const {a, b, chain} = setup();
  const tx = payment(a, b.address, 100, 0);
  chain.append(chain.mine([tx], a.address));
  rejectedWithoutStateChange(chain, chain.mine([tx], a.address), /nonce/);
  rejectedWithoutStateChange(chain, chain.mine([payment(b, a.address, 101, 0)], a.address), /balance/);
  rejectedWithoutStateChange(chain, chain.mine([payment(a, b.address, 50, 1), payment(a, b.address, 1000, 2)], a.address), /balance/);
  rejectedWithoutStateChange(chain, chain.mine([payment(a, b.address, 1, 3)], a.address), /nonce/);
});
test("Header, proof of work, transaction commitment, and reward cannot be forged", () => {
  const {a, b, chain} = setup();
  const block = chain.mine([payment(a, b.address, 10, 0)], a.address);
  for (const alteration of [{parent: "f".repeat(64)}, {reward: 100}, {height: 2}, {network: "other"}, {merkleRoot: "0".repeat(64)}]) {
    rejectedWithoutStateChange(chain, {...block, ...alteration}, /header|commitment/);
  }
  const badWork = structuredClone(block);
  do { badWork.nonce++; badWork.hash = blockHash(badWork); } while (badWork.hash.startsWith("000"));
  rejectedWithoutStateChange(chain, badWork, /header|commitment/);
  const changed = structuredClone(block); changed.transactions[0].amount = 11;
  rejectedWithoutStateChange(chain, changed, /header|commitment/);
  const invalidSigned = {...payment(a, b.address, 10, 0), signature: "0".repeat(128)};
  rejectedWithoutStateChange(chain, chain.mine([invalidSigned], a.address), /signature/);
});
test("Supply cap, self transfers, and snapshot isolation", () => {
  const {a, chain} = setup();
  chain.append(chain.mine([payment(a, a.address, 1000, 0)], a.address));
  assert.equal(chain.snapshot().balances[a.address], 1010);
  for (let i = 0; i < 12; i++) chain.append(chain.mine([], a.address));
  assert.equal(chain.snapshot().supply, 1100);
  const snapshot = chain.snapshot(); snapshot.balances[a.address] = 0;
  const blocks = chain.blocks(); blocks[0].reward = 900;
  assert.equal(chain.snapshot().balances[a.address], 1100);
  assert.equal(chain.blocks()[0].reward, 10);
});
