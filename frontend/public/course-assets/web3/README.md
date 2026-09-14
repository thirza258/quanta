# Local cryptography and coin-creation lab

This archive contains two complete educational projects: an account-based native coin chain and a fixed-supply ERC-20 token. They use local state only. There is no public RPC, network port, wallet connection, sale, or real-fund requirement.

## 1. Native coin, without installing packages

Requires Node 22 or later:

```sh
node native-chain.mjs
node --test native-chain.test.mjs
```

The lab generates ephemeral Ed25519 keys using Node crypto. It signs a payment, constructs a SHA-256 Merkle commitment, mines a deliberately small 12-bit proof of work, and validates the resulting block. It prints public evidence only; never add private keys to your report.

The first accepted block transfers 100 atomic units from Alice to Bob and rewards Alice ten. Expected balances are **910 and 100**, total supply **1,010**, height **1**. Hashes and public identifiers vary because keys are generated each run. Genesis creates 1,000 units; accepted blocks issue up to ten until the cap of 1,100. Transactions consume sequential account nonces. Rewards are available after the block's transfers validate.

Tests cover a standard hash vector, signature tampering and sender identity, wrong domains, odd-sized Merkle trees, transfers and independent replay, duplicate and future nonces, insufficient funds, atomic rejection of a late invalid transaction, forged headers/rewards/work, cap boundaries, self-transfers, and snapshot isolation.

The commitment format is original: fixed ordered tuples; domain tags; separate leaf/branch prefixes; duplicate-last odd levels; transaction count committed in the header. It is not Bitcoin or Ethereum wire compatibility. There are no peers, persistence, fee market, difficulty adjustment, fork choice, or distributed finality. This implementation demonstrates local validation, not a secure public network.

## 2. Compile and create the ERC-20 on a local EVM

```sh
npm ci --ignore-scripts
npm test
```

This installs the locked development dependencies and runs both native tests and the Solidity deployment test. On Node versions without compatible optional native bindings, Ganache may announce its JavaScript fallback; successful assertions still determine the result.

`CedarCoin.sol` creates **1,000,000 whole CEDAR tokens**, with 18 decimals, for the constructor recipient. It inherits OpenZeppelin ERC20 and exposes no owner, external mint, transfer tax, or upgrade mechanism. Token amounts use integer atomic units in the contract and BigInt/decimal-string conversion in tests.

`token-test.mjs` compiles with optimizer runs 200 and EVM target Shanghai, creates an in-process Ganache chain 31337, deploys through ethers, and checks metadata, supply, transfers/events, finite allowances, rejection state, a zero transfer, twelve conservation steps, and deployed-runtime identity. After the main transfer fixture, the recipient holds 110 tokens and the remaining finite allowance is 15. Later tiny-unit transfers deliberately change individual balances while preserving total supply.

The test prints compiler version and source/runtime SHA-256 hashes. This is a local deployment report, not an external audit or public launch. A token has been created on this local test EVM; no exchange pool or market has been created.

## Assignments and capstone

Follow Web3 lessons 6.6–6.24 and the retained economic lessons 6.1–6.5 in the course's unit order. Add one adverse test to each project, annotate the encoding and authority rules, reconcile supply, and produce the source/build/authority dossier. Test vesting, additional mint roles, bridges, or upgrades only in separately specified local extensions; those features are not in the supplied contract.

## Sources and licenses

The Quanta wrapper, native lab, tests, and guide are original. The Solidity wrapper is marked MIT; the accompanying `LICENSE` applies to the original files in this project. Dependencies retain their own licenses and notices, available in their packages; imported OpenZeppelin implementation is not authored by Quanta.

- [NIST Secure Hash Standard](https://csrc.nist.gov/pubs/fips/180-4/upd1/final)
- [RFC 8032: EdDSA](https://www.rfc-editor.org/rfc/rfc8032)
- [Node crypto](https://nodejs.org/api/crypto.html)
- [Bitcoin paper](https://bitcoin.org/bitcoin.pdf)
- [ERC-20 standard](https://eips.ethereum.org/EIPS/eip-20)
- [OpenZeppelin ERC20](https://docs.openzeppelin.com/contracts/5.x/erc20)
- [Solidity security considerations](https://docs.soliditylang.org/en/latest/security-considerations.html)
- [ethers documentation](https://docs.ethers.org/v6/)
