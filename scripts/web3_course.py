"""Original cryptography, native coin, and token engineering course."""

from applied_courses import checkpoints_for, study
from book_courses import finish

HASH = (
    "NIST · Secure Hash Standard FIPS 180-4",
    "https://csrc.nist.gov/pubs/fips/180-4/upd1/final",
)
SIGN = (
    "IETF · RFC 8032 Edwards-Curve Digital Signatures",
    "https://www.rfc-editor.org/rfc/rfc8032",
)
NODE = ("Node.js contributors · Cryptographic primitives", "https://nodejs.org/api/crypto.html")
BTC = (
    "Satoshi Nakamoto · Bitcoin: A Peer-to-Peer Electronic Cash System",
    "https://bitcoin.org/bitcoin.pdf",
)
ACCOUNT = (
    "Ethereum contributors · Accounts and keys",
    "https://ethereum.org/en/developers/docs/accounts/",
)
CONSENSUS = (
    "Ethereum contributors · Consensus mechanisms",
    "https://ethereum.org/en/developers/docs/consensus-mechanisms/",
)
TOKEN = (
    "Vogelsteller and Buterin · ERC-20 Token Standard",
    "https://eips.ethereum.org/EIPS/eip-20",
)
OZ = (
    "OpenZeppelin · ERC-20 contract implementation",
    "https://docs.openzeppelin.com/contracts/5.x/erc20",
)
SECURE = (
    "Solidity contributors · Security considerations",
    "https://docs.soliditylang.org/en/latest/security-considerations.html",
)
AMM = (
    "Uniswap contributors · Understanding liquidity-provider returns",
    "https://docs.uniswap.org/contracts/v2/concepts/advanced-topics/understanding-returns",
)
ETHERS = ("ethers contributors · JavaScript Ethereum library", "https://docs.ethers.org/v6/")


def build_web3():
    modules = []

    def add(*args):
        modules.append(study(*args))

    add(
        "6.6",
        1,
        "Bytes, encodings, and cryptographic hashes",
        "Distinguish byte representation, hashing, and encryption, and identify the exact data committed by a digest.",
        "A protocol operates on bytes. UTF-8 text, hexadecimal display, and an integer's binary encoding can represent related ideas while producing different byte sequences. A hash commits to the bytes actually supplied; it does not interpret a business meaning or normalize a document automatically. Define field ordering, lengths, encodings, and domain tags before signing or hashing structured data.\n\nA cryptographic digest is deterministic and fixed length. Preimage resistance concerns finding an input for a specified digest; collision resistance concerns finding any two different inputs with the same digest. Neither property makes hashing encryption, authenticates the sender, or establishes that an input claim is true.",
        "A toy 16-bit digest has 65,536 possible outputs. Generic collision search reaches the birthday scale around 256 samples, while a specified target requires a different search problem. These are order-of-magnitude illustrations, not security guarantees for a real truncated scheme.\n\nThe downloadable Node lab computes SHA-256 with the standard library and tests the known digest of the three UTF-8 bytes abc. Adding a newline changes the input. The guided Python worksheet below illustrates the combinatorics; actual hashing runs in the downloaded project.",
        "Write a serialization specification before building the ledger. The lab uses fixed ordered tuples and distinct payment, block, leaf, and branch domains. Reproduce the standard hash vector, compare a one-byte change, and record both input bytes and algorithm name. Do not design a new hash function for this project. A digest can demonstrate that an artifact matches a prior commitment only when the reference commitment and its provenance are also trustworthy.",
        r"N=2^b,\quad collision\ scale\approx\sqrt N",
        'import math\nprint("Toy digest space:", 2 ** 16)\nprint("Birthday scale:", math.sqrt(2 ** 16))',
        "Run the native-chain hash test. Compare UTF-8 abc and abc followed by a newline. Explain why identical human meaning need not imply identical digests.",
        "The inputs contain different bytes, so the digests differ. Hashing commits to an agreed encoding; it does not perform semantic normalization or prove authorship.",
        [
            (
                "Hashing a document provides reversible confidentiality:",
                ["No", "Yes", "Only for short documents"],
                0,
                "Hashing is not reversible encryption.",
            ),
            (
                "A commitment must specify:",
                [
                    "Only the font",
                    "Exact input bytes and encoding rules",
                    "Only the document's topic",
                ],
                1,
                "Different byte representations produce different commitments.",
            ),
            (
                "A toy 12-bit output space contains:",
                ["12 values", "144 values", "4,096 values"],
                2,
                "The output space has 2^12=4,096 possibilities.",
            ),
            (
                "A valid digest proves an underlying financial claim is true:",
                ["No; it commits to data, not its truth", "Yes", "Only when it is hexadecimal"],
                0,
                "Cryptographic integrity and factual accuracy are separate.",
            ),
        ],
        [HASH, NODE],
    )

    add(
        "6.7",
        1,
        "Merkle commitments and inclusion proofs",
        "Construct a transaction commitment and verify an ordered inclusion path without confusing inclusion with transaction validity.",
        "A Merkle tree combines leaf hashes into parent hashes until one root commits to the collection. A proof supplies sibling hashes along one path. Verification recomputes the root in the specified left/right order. The protocol must define leaf encoding, branch encoding, ordering, treatment of odd counts, and empty-tree behavior.\n\nThe local project prefixes leaves and branches with different bytes and duplicates the last node at an odd level. Its block header also commits to the transaction count, since duplicate-last constructions require care when interpreting collection length. This is an educational commitment format, not Ethereum's execution-state trie or Bitcoin's exact wire protocol.",
        "A balanced tree of eight leaves requires three sibling hashes for an inclusion path. For a five-leaf example, the lab's tests verify every path through the odd-count construction. Changing a signed transaction amount makes the original proof fail against the original root.\n\nA valid inclusion proof only establishes membership under a root. It does not show that the root belongs to a finalized canonical block, that the signer had funds, or that all other transactions are valid. Those are separate validation and consensus questions.",
        "Trace one proof by hand using symbolic leaf labels before using actual digests. Then run the downloaded odd-leaf tests and alter a transaction and a sibling direction independently. Record which commitment changed. Keep the authoritative root and its chain context with the proof; accepting an arbitrary root supplied by the same untrusted party proves little about an external ledger. Explain the difference between proving one transaction's inclusion and replaying all state transitions.",
        r"proof\ depth=\log_2 n\quad(n\text{ a power of two})",
        'import math\nprint("Sibling hashes for eight leaves:", math.log(8) / math.log(2))\nprint("Sibling hashes for sixteen leaves:", math.log(16) / math.log(2))',
        "Verify each path in the five-transaction fixture, then change one amount. Explain two additional checks needed before treating an included payment as accepted money.",
        "The changed leaf should fail against the old root. Also validate the payment and resulting balances, and establish the block's accepted chain/finality context; inclusion alone is insufficient.",
        [
            (
                "A Merkle proof alone proves the sender could afford a payment:",
                ["Yes", "No", "Only in a balanced tree"],
                1,
                "Inclusion does not establish state-transition validity.",
            ),
            (
                "Sibling ordering in a proof is:",
                ["Always irrelevant", "A display preference", "Part of the commitment convention"],
                2,
                "Left and right concatenation can yield different parents.",
            ),
            (
                "A balanced 32-leaf tree needs how many sibling hashes per path:",
                ["5", "16", "32"],
                0,
                "There are log2(32)=5 branch levels.",
            ),
            (
                "The authoritative root must be linked to:",
                [
                    "Only a screenshot",
                    "The intended ledger and accepted block context",
                    "Any root returned by the claimant",
                ],
                1,
                "A proof needs a trusted commitment context to support a ledger claim.",
            ),
        ],
        [BTC, NODE],
    )

    add(
        "6.8",
        1,
        "Public keys and digital signatures",
        "Verify signed messages with established libraries and distinguish the cryptographic schemes used by different chains.",
        "A signature lets a verifier check that a message was authorized by the holder of a corresponding private key under a specified algorithm. The private key remains secret; the public key and signature can be distributed. Verification must bind the exact intended message and application domain. A valid signature does not establish the signer's real-world identity, sufficient balance, or permission under every contract.\n\nThis lab uses Ed25519 through Node's crypto library. Ethereum externally owned accounts conventionally use secp256k1 ECDSA instead. Their key formats, signature procedures, and address derivations are different. Do not copy an address recipe between schemes or implement signing arithmetic from a short tutorial.",
        "Alice signs a local payment of 20 atomic units to Bob with nonce 0. Verification succeeds for those fields. Changing the amount to 21 invalidates the signature. Substituting Bob's address as the claimed sender also fails because the lab checks the address against the supplied public key.\n\nA signature remains cryptographically valid after its payment has been spent. The account nonce and ledger balance checks provide replay and spending rules; signature verification alone cannot replace them.",
        "Generate ephemeral keys using the platform's cryptographic generator. Keep private keys out of logs, browser bundles, and project submissions. The downloadable tests exercise valid signatures, changed amounts, sender substitution, and a wrong network domain. Submit public identifiers and test outcomes only. Explain why the project's SHA-256 hash of an encoded Ed25519 public key is a local address convention and cannot receive assets on Ethereum or Bitcoin.",
        r"Verify(pk,message,signature)\in\{true,false\}",
        'print("Signed amount:", 20)\nprint("Tampered amount:", 21)\nprint("Amount change:", 21 - 20)',
        "Run the signature tests and document the fields bound by the message. Explain why a replayed valid signature still needs ledger rejection.",
        "The signed tuple binds domain, network, sender, recipient, amount, nonce, and public key. Replaying it preserves signature validity but violates the already consumed account nonce.",
        [
            (
                "A valid payment signature alone proves sufficient funds:",
                ["No", "Yes", "Only with a long key"],
                0,
                "Authorization and ledger balance are separate checks.",
            ),
            (
                "The local Ed25519 address is interchangeable with an Ethereum account:",
                [
                    "Yes",
                    "No; the schemes and address conventions differ",
                    "Only if both are hexadecimal",
                ],
                1,
                "An encoding's appearance does not make its protocol semantics interchangeable.",
            ),
            (
                "Changing a signed amount while keeping its signature should:",
                ["Mint the difference", "Preserve authorization", "Fail signature verification"],
                2,
                "The signature binds the original message bytes.",
            ),
            (
                "Private keys in the submitted course report should be:",
                [
                    "Omitted; submit public evidence and test results",
                    "Printed in full",
                    "Embedded in screenshots",
                ],
                0,
                "Verification evidence does not require disclosing signing secrets.",
            ),
        ],
        [SIGN, ACCOUNT, NODE],
    )

    add(
        "6.9",
        1,
        "Wallets, replay domains, and transaction nonces",
        "Treat a wallet as a signing and state-coordination interface, with explicit separation between secrets, network identity, and sequence numbers.",
        "A wallet manages keys or access to a signer and helps construct transactions. Assets are represented by ledger state, not stored inside the application icon. Recovery therefore concerns the signing authority and its supported derivation or backup scheme, while account history must be read from the intended chain. Seed phrases are secrets and should never be entered into this course.\n\nA transaction nonce is an account sequence number in this model. It is distinct from the nonce searched during proof of work and from cryptographic ephemeral values inside some signature algorithms. Reusing the word does not make these mechanisms interchangeable. A network/domain identifier further prevents a locally valid message from being accepted in another protocol context.",
        "If Alice's next expected payment nonce is 3, a signed payment with nonce 2 is a replay and nonce 4 is premature under this strict sequential ledger. Exactly nonce 3 can proceed to the balance check. After an accepted payment, the next expected value is 4.\n\nTwo concurrent wallet tasks that both read nonce 3 can create conflicting intentions. A real wallet or transaction service needs coordination and reconciliation with accepted chain state. Increasing the number locally without tracking submitted outcomes can leave a gap.",
        "Draw a wallet flow from recipient review through message construction, signing, submission, pending state, and accepted-state reconciliation. The local lab has no mempool or replacement policy, so it rejects out-of-sequence payments rather than simulating those features. Test stale and future nonces, wrong domains, and recovery by replaying accepted blocks. Never infer finality from a wallet's submitted label alone. Keep signing permission distinct from unlimited token allowances granted to another contract.",
        r"nonce_{accepted}=nonce_{expected},\quad nonce_{next}=nonce_{expected}+1",
        'expected = 3\nprint("Old nonce accepted:", 2 == expected)\nprint("Current nonce accepted:", 3 == expected)\nprint("Next nonce after acceptance:", expected + 1)',
        "Design a state table for two concurrent transfers from an account expecting nonce 5. Describe how you would reconcile one accepted and one unresolved submission.",
        "Track each intent and its nonce, query accepted state, and avoid treating an unresolved request as a second accepted payment. This local ledger accepts nonce 5 once, then expects 6.",
        [
            (
                "A wallet application physically contains the on-chain coins:",
                ["Yes", "No; ledger state records balances", "Only while offline"],
                1,
                "The wallet manages access and transaction construction.",
            ),
            (
                "Proof-of-work nonce and account nonce are:",
                ["The same counter", "Both private keys", "Different protocol mechanisms"],
                2,
                "One searches a block hash; the other sequences account transactions.",
            ),
            (
                "After accepting account nonce 7, this ledger expects:",
                ["8", "7", "0"],
                0,
                "A successful payment increments the account sequence once.",
            ),
            (
                "A network identifier in the signed message helps prevent:",
                [
                    "All market losses",
                    "Cross-domain transaction replay",
                    "Every possible wallet bug",
                ],
                1,
                "The signature is bound to its intended protocol context.",
            ),
        ],
        [ACCOUNT, SIGN],
    )

    add(
        "6.10",
        2,
        "Native coins, tokens, and ledger models",
        "Choose whether an asset belongs to a base protocol or a smart contract and specify its accounting representation.",
        "A native coin is accounted for by a blockchain's own state-transition rules. A token on an existing chain is accounted for by a contract within that chain. Deploying an ERC-20 contract creates a token ledger; it does not create a new consensus network or replace the host chain's native gas asset. The course builds one example of each locally.\n\nAn account model tracks balances and sequence numbers. A UTXO model tracks unspent outputs consumed and created by transactions. Both need authorization and conservation rules, but their data structures and replay handling differ. The native lab uses accounts for clarity and does not claim to implement Bitcoin's UTXO or Ethereum's full execution model.",
        "The native project begins with 1,000 atomic units assigned in genesis. Alice sends 100 to Bob and the first block issues a 10-unit reward to Alice. Her balance becomes 910, Bob's becomes 100, and total supply is 1,010. The transfer moves existing units; the authorized reward increases supply.\n\nThe ERC-20 project instead creates one million whole CEDAR tokens in a constructor on an in-process EVM. Token balances are separate from the local native test currency used to execute the deployment.",
        "Write an asset specification covering ledger type, unit scale, initial allocation, supply changes, signing rules, and host-chain dependence. Identify the code path allowed to create new units. Compare a transfer with a mint and with a transaction fee. A name and ticker do not make two assets identical: an ERC-20 identity requires its chain and contract address, while the native lab is identified by its own genesis and network rules.",
        r"S_{next}=S_{current}+authorized\ issuance-burns",
        'print("Alice after transfer and reward:", 1000 - 100 + 10)\nprint("Bob balance:", 100)\nprint("Native supply:", 1000 + 10)',
        "Specify one native-coin design and one ERC-20 design. For each, identify who validates transfers and which code changes supply.",
        "Native validation and issuance belong to the base protocol; ERC-20 transfers and minting follow contract code enforced by the host EVM. The local examples use a capped block reward and a constructor-only token mint respectively.",
        [
            (
                "Deploying an ERC-20 automatically creates a new consensus network:",
                ["No", "Yes", "Only with a unique ticker"],
                0,
                "The token uses an existing execution and consensus environment.",
            ),
            (
                "A transfer without fees or burns normally:",
                [
                    "Increases total supply",
                    "Moves units between holders while conserving supply",
                    "Deletes the sender's identity",
                ],
                1,
                "Ownership changes without creating new units.",
            ),
            (
                "Supply 2,000 plus authorized issuance 15 becomes:",
                ["1,985", "2,000", "2,015"],
                2,
                "Issuance adds 15 units to the existing total.",
            ),
            (
                "A token's ticker alone uniquely identifies its ledger:",
                ["No; chain and contract identity matter", "Yes", "Only if it has five letters"],
                0,
                "Different contracts can reuse the same display metadata.",
            ),
        ],
        [BTC, TOKEN],
    )

    add(
        "6.11",
        2,
        "Consensus, proof of work, and finality",
        "Separate valid state transitions from agreement on chain history and understand the limits of a single-process mining demonstration.",
        "Validation asks whether a proposed block obeys protocol rules. Consensus also addresses which valid history participants accept when competing histories exist. Proof of work attaches a computational cost to candidate blocks; proof of stake uses a different validator and incentive structure. The specific fork-choice and finality rules belong to each protocol and cannot be inferred from a generic blockchain diagram.\n\nThe downloaded native chain deliberately omits peers, network delay, fork choice, difficulty adjustment, and economic security. It checks a trivial hash target and extends one current tip. This demonstrates commitment and validation mechanics but cannot establish distributed agreement or protect a public currency.",
        "The toy target requires three leading hexadecimal zero characters, equivalent to 12 zero bits. For a uniformly distributed digest, success probability per trial is 1/4,096 and expected trials are 4,096. Actual attempts vary randomly; a successful block may arrive much sooner or later.\n\nA valid proof of work cannot authorize overspending. The validator still rejects a block containing an invalid signature, nonce, reward, or balance transition, even when its hash meets the target.",
        "Run a local block and inspect its hash and header fields. Explain why changing the parent or Merkle root invalidates the old hash. Then use the supplied tests to show a valid-looking work header cannot bypass the reward rule. In a design memo, list what a multi-node system would additionally need: peer communication, chain selection, finality interpretation, synchronization, adversarial resource limits, and recovery. Do not label the successful local demonstration as a secure public network.",
        r"p=2^{-12},\quad E[trials]=1/p=4096",
        'print("Toy success probability:", 1 / (2 ** 12))\nprint("Expected hash trials:", 2 ** 12)',
        "Explain why 12-bit proof of work is suitable for a fast exercise but inadequate evidence of public-network security. Identify two omitted consensus components.",
        "Its computational cost is intentionally tiny and there are no adversarial peers. Fork choice, synchronization, distributed finality, and economic/resource assumptions are omitted.",
        [
            (
                "A valid proof of work permits an otherwise invalid spend:",
                ["Yes", "No", "Only for the miner"],
                1,
                "Consensus work does not override state-transition validity.",
            ),
            (
                "The local single-tip lab implements distributed consensus:",
                ["Yes", "Only after two blocks", "No"],
                2,
                "It has no peer network or competing-history selection.",
            ),
            (
                "A toy 8-bit zero target has expected independent trials:",
                ["256", "8", "64"],
                0,
                "Success probability is 1/256 under the uniform-hash model.",
            ),
            (
                "Finality should be interpreted using:",
                [
                    "Only a wallet animation",
                    "The particular protocol's acceptance and consensus rules",
                    "Only the number of digits in the block hash",
                ],
                1,
                "Different consensus protocols define acceptance differently.",
            ),
        ],
        [CONSENSUS, BTC],
    )

    add(
        "6.12",
        2,
        "Atomic transaction and block validation",
        "Validate signatures, nonces, commitments, and conservation before accepting any state changes from a candidate block.",
        "A validator must reject an entire invalid block without leaving partial economic effects behind. Checking a signature is only one step. The local lab verifies the network domain, next height, parent hash, transaction commitment, proof-of-work target, permitted reward, integer amounts, sender identity, sequential nonce, and available balance.\n\nIt applies transactions to copied maps. Only after every transaction and the supply invariant pass does it replace accepted state. This makes a late failure atomic. A mutable reference to accepted balances or block history would undermine that guarantee, so the lab also returns copies from its inspection methods.",
        "Alice has 910 units after the first block. A candidate second block includes a valid 50-unit payment followed by an unaffordable 1,000-unit payment. The candidate fails. Alice remains at 910, Bob remains at 100, and no second block reward is issued. Applying the first transaction permanently before checking the second would corrupt state.\n\nA self-transfer subtracts then adds to the same account and must conserve balance while consuming one nonce. The tests cover this edge case because simplistic updates can accidentally mint or destroy units.",
        "Order checks so malformed data fails clearly before expensive or stateful operations. Preserve the exact accepted snapshot before each adverse test and compare it afterward. Test duplicate payments, future nonces, a forged reward, altered transaction bytes, and mutation of returned snapshots. Replay all accepted blocks into a new instance with the same genesis and compare the resulting state. Agreement with a fresh replay is a useful accounting check, though it does not substitute for distributed consensus.",
        r"\sum_a balance_a=S,\quad invalid\ block\Rightarrow state'=state",
        'print("Balance after rejected candidate:", 910)\nprint("Supply after rejected second block:", 1010)\nprint("Self-transfer net change:", -50 + 50)',
        "Run the late-failure and snapshot-isolation tests. Explain what must remain unchanged when a candidate block's final transaction fails.",
        "Balances, nonces, supply, height, and accepted tip must remain unchanged; no reward is granted for the rejected candidate. Returned inspection objects must not mutate accepted state.",
        [
            (
                "A late invalid transaction may leave earlier candidate transfers accepted:",
                ["No, the candidate block must fail atomically", "Yes", "Only if they were signed"],
                0,
                "A block is accepted as one validated state transition in this model.",
            ),
            (
                "A self-transfer should change total supply by:",
                ["The transferred amount", "Zero", "The current balance"],
                1,
                "Moving units to the same holder does not create units.",
            ),
            (
                "Balances 910 and 100 sum to supply:",
                ["1,000", "1,100", "1,010"],
                2,
                "The balances include the accepted ten-unit reward.",
            ),
            (
                "Replaying accepted blocks from the same genesis should reproduce:",
                [
                    "The accepted balances, nonces, and supply",
                    "New arbitrary balances",
                    "Only the ticker",
                ],
                0,
                "Deterministic transition rules should reconstruct the same economic state.",
            ),
        ],
        [BTC, NODE],
    )

    add(
        "6.13",
        2,
        "Project: create a signed native-coin blockchain",
        "Run the complete native coin fixture, inspect its issuance, and demonstrate rejection of invalid economic histories.",
        "Download the coin-lab archive and run node native-chain.mjs with Node 22 or later. This component needs no installed packages. It generates ephemeral Ed25519 keys, defines genesis allocation, signs a payment, constructs a Merkle commitment, searches a small proof-of-work target, validates the block, and prints public results. It opens no network port and connects to no chain.\n\nThe native coin has integer atomic units, an initial supply of 1,000, a reward of ten per accepted block, and a cap of 1,100. The reward becomes available after the block's transactions validate. These are original teaching rules chosen for transparent arithmetic, not an economic recommendation.",
        "The default run pays 100 units from Alice to Bob and rewards Alice ten. Expected output includes signatureValid=true, proofValid=true, aliceBalance=910, bobBalance=100, supply=1010, and height=1. Public addresses and the mined hash vary because keys are freshly generated.\n\nA second payment of 25 from Bob back to Alice, with another ten-unit reward to Alice, yields balances 945 and 75 and supply 1,020. The tests reconstruct the same state through independent replay.",
        "Run node --test native-chain.test.mjs and retain its results. Add an altered-amount case, a duplicate nonce, and a block that fails after an earlier valid transaction. Record the unchanged accepted state after each rejection. Describe the omitted peer network, persistence, fee market, fork choice, and production key custody. Your deliverable is a reproducible educational coin implementation and its validation evidence, not a claim that a public cryptocurrency has launched.",
        r"S_h=1000+\min(10h,100)",
        'print("Supply at height one:", 1000 + min(10 * 1, 100))\nprint("Supply at height twelve:", 1000 + min(10 * 12, 100))\nprint("Alice after second block:", 910 + 25 + 10)',
        "Run the demo and tests, then add a second transfer. Submit the public output, supply reconciliation, and three rejected histories without including private keys.",
        "Baseline balances are 910/100, then 945/75 with the described second block. Supply is 1,010 then 1,020. Invalid signatures, replays, or unaffordable blocks must leave accepted state unchanged.",
        [
            (
                "The native lab requires funding a public wallet:",
                ["Yes", "No", "Only for mining"],
                1,
                "All issuance and transfers are local educational state.",
            ),
            (
                "A correctly reproduced run must have identical generated addresses:",
                ["Always", "Only on weekdays", "No; compare invariants and expected balances"],
                2,
                "Fresh ephemeral key generation changes public identifiers.",
            ),
            (
                "Under this cap, supply after 20 accepted blocks is:",
                ["1,100", "1,200", "1,000"],
                0,
                "Issuance stops after the extra 100 units have been created.",
            ),
            (
                "The project's strongest supported claim is:",
                [
                    "Public-network security",
                    "Correct local behavior under its tested rules",
                    "Guaranteed token demand",
                ],
                1,
                "The demonstration tests defined mechanics, not adoption or distributed security.",
            ),
        ],
        [NODE, SIGN, BTC],
    )

    add(
        "6.14",
        3,
        "EVM execution, gas, and integer token units",
        "Trace contract execution costs and represent token amounts without floating-point rounding.",
        "The EVM executes contract instructions under a gas budget. Gas measures execution work; its monetary cost depends on the transaction's effective gas price. A transaction that reverts does not preserve its attempted contract state changes, but an included failed transaction can still consume gas. An off-chain read and an on-chain state-changing transaction have different execution contexts.\n\nERC-20 balances are integers in atomic units. Decimals provide a display scale; they do not make Solidity balances floating-point values. The local contract uses 18 decimals. Its tests use JavaScript BigInt and ethers parseUnits to preserve exact amounts rather than converting large token balances through Number.",
        "A display amount 1.25 with six decimals corresponds to 1,250,000 atomic units. With 18 decimals the scale is much larger, but the rule is the same. A transaction using a stipulated 50,000 gas at an effective price of 20 gwei costs 1,000,000 gwei, or .001 native ether units. This arithmetic is a fixture, not a current fee quote.\n\nThe project's compiler explicitly targets the Shanghai EVM implemented by the local test provider. Compiler version and EVM target are separate build settings and must agree with the execution environment.",
        "Write amount conversion tests for whole, fractional, zero, and excessively precise inputs. Record compiler, optimization settings, and EVM target with deployed bytecode. Explain why an ERC-20 balance cannot pay native gas unless an additional supported mechanism explicitly provides that service. Keep estimated gas separate from actual receipt gas, and do not interpret a successful estimate as a guarantee that later execution succeeds.",
        r"atomic=display\times10^{decimals},\quad fee=gasUsed\times effectiveGasPrice",
        'print("Atomic units with six decimals:", 1.25 * 10 ** 6)\nprint("Illustrative native fee:", 50000 * 20 / 10 ** 9)',
        "Convert 2.5 tokens with eight decimals and calculate 80,000 gas at 15 gwei. Explain why production amount parsing should avoid binary floating-point.",
        "The amount is 250,000,000 atomic units and the fee is .0012 native ether units. Decimal string parsing and integer arithmetic avoid rounding large or fractional token amounts.",
        [
            (
                "Decimals change an ERC-20 balance into floating-point storage:",
                ["No", "Yes", "Only above six decimals"],
                0,
                "Balances remain integers; decimals define their display scale.",
            ),
            (
                "An included reverted transaction can still:",
                [
                    "Keep every attempted contract update",
                    "Consume gas",
                    "Create free native currency",
                ],
                1,
                "Reversion of contract changes does not imply zero execution cost.",
            ),
            (
                "Three tokens with four decimals represent:",
                ["300", "3,000", "30,000 atomic units"],
                2,
                "Multiply three by 10^4 to obtain the integer amount.",
            ),
            (
                "Compiler output should target:",
                [
                    "An EVM revision supported by the execution environment",
                    "An arbitrary newest opcode set",
                    "Only the token's ticker",
                ],
                0,
                "Unsupported instructions can make otherwise compiled code fail at execution.",
            ),
        ],
        [
            TOKEN,
            ETHERS,
            (
                "Solidity contributors · Units and global variables",
                "https://docs.soliditylang.org/en/latest/units-and-global-variables.html",
            ),
        ],
    )

    add(
        "6.15",
        3,
        "Design and implement a fixed-supply ERC-20",
        "Read the complete CedarCoin contract and identify its supply, interface, authority, and inherited behavior.",
        "The CedarCoin source imports the pinned OpenZeppelin ERC20 implementation and adds a constructor that creates one million whole tokens for a chosen recipient. The wrapper has no owner role, external mint function, transfer tax, blacklist, proxy, or upgrade entry point. That small scope makes the intended authority easy to inspect.\n\nAn ERC-20 interface standardizes balances, transfers, allowances, and events. It does not by itself promise demand, redeemability, legal rights, or a fixed supply. Those properties come from the actual contract and surrounding arrangements. Read inherited code and dependencies when reviewing an implementation, rather than treating the wrapper's short length as its complete behavior.",
        "At deployment, totalSupply is 1,000,000×10^18 atomic units and the designated recipient owns that amount. A transfer of 100 whole tokens leaves 999,900 with the original recipient and 100 with the receiver. Total supply remains one million.\n\nThe constructor calls an internal mint operation, but no public function exposes that operation afterward. The test also inspects the ABI for the absent mint and upgrade names; this supports this particular wrapper's stated design, not a universal proof about every similarly named token.",
        "Read CedarCoin.sol alongside the dependency documentation. Identify the constructor argument, display metadata, scale, supply expression, and inherited transfer methods. Compile using the locked dependency tree and record the artifact hash. Modify a copy's initial supply only after updating the specification and expected tests. Keep the teaching name and project identity clear; deploying a contract with a familiar ticker does not make it another issuer's asset.",
        r"S_0=1{,}000{,}000\times10^{18}\;atomic\ units",
        'print("Whole supply:", 1000000)\nprint("Holder after 100-token transfer:", 1000000 - 100)\nprint("Conserved whole supply:", 999900 + 100)',
        "Annotate every line of CedarCoin.sol and explain which operation creates supply. Specify the changes needed to make a different fixed initial supply in a local copy.",
        "The constructor's internal mint creates supply once. Change its amount expression, update the design manifest and initial-balance tests, recompile, and deploy a fresh local instance; the existing instance has no supply-changing entry point.",
        [
            (
                "ERC-20 compliance alone promises a fixed supply:",
                ["Yes", "No", "Only for an 18-decimal token"],
                1,
                "Supply policy depends on the implementation's reachable mint and burn behavior.",
            ),
            (
                "CedarCoin's initial issuance occurs in:",
                ["Every transfer", "A public mining loop", "Its constructor"],
                2,
                "The original wrapper creates all units at deployment.",
            ),
            (
                "A 40-token transfer from a 1,000-token holder leaves:",
                ["960 tokens", "1,040 tokens", "1,000 tokens"],
                0,
                "A normal transfer deducts the transferred amount from the sender.",
            ),
            (
                "Reviewing an inherited token requires inspecting:",
                [
                    "Only its logo",
                    "The wrapper and the dependency behavior it exposes",
                    "Only its file length",
                ],
                1,
                "Inherited methods determine much of the deployed contract's behavior.",
            ),
        ],
        [OZ, TOKEN],
    )

    add(
        "6.16",
        3,
        "Project: compile, deploy, transfer, and approve locally",
        "Execute the token test project and reconcile balances, allowances, events, and compiled runtime identity.",
        "After downloading and extracting the project, run npm ci and npm test. The token test compiles the contract with pinned solc and OpenZeppelin versions, creates an in-process Ganache EVM, deploys through ethers, and exercises the resulting contract. The process uses generated local accounts and closes its provider when finished. There is no external RPC argument or public deployment step.\n\nA transfer moves the caller's own tokens. An allowance authorizes a named spender to transfer a bounded amount from another account. Approving an allowance does not move tokens immediately. Interfaces should make spender identity and amount clear; an allowance is a meaningful authority grant even when the transaction itself transfers nothing.",
        "The fixture sends 100 tokens to a recipient, approves a spender for 25, and lets that spender transfer another ten to the recipient. The recipient then holds 110 and the remaining finite allowance is 15. Trying to transfer 16 through that allowance must fail without changing token balances or allowance.\n\nThe test also rejects overspending and a zero-address recipient, checks zero-value transfer events, executes twelve small transfers while reconciling supply, and compares deployed runtime bytes with the compiled artifact.",
        "Retain the compiler version, source hash, runtime hash, and passing output. Explain each assertion using the state before and after its transaction. Add an allowance revocation case in a local copy, then show that the spender cannot use the revoked amount. Do not submit account secrets. Passing these fixtures demonstrates the specified local behaviors; it does not establish that arbitrary extensions, bridges, or exchange integrations are correct.",
        r"allowance_{after}=allowance_{before}-authorized\ spend",
        'print("Recipient after both transfers:", 100 + 10)\nprint("Remaining finite allowance:", 25 - 10)\nprint("Does a 16-token spend fit:", 16 <= 25 - 10)',
        "Run the complete local test. Add approve(spender,0), verify the allowance is zero, and demonstrate a subsequent delegated transfer rejection.",
        "The base fixture leaves 110 tokens with the recipient and allowance 15. Revocation sets that allowance to zero; another delegated spend must reject without changing token state.",
        [
            (
                "Approving 25 tokens immediately sends 25 to the spender:",
                ["No", "Yes", "Only on a local EVM"],
                0,
                "Approval changes permission, while transferFrom performs the delegated movement.",
            ),
            (
                "The test's deployment target is:",
                ["Ethereum mainnet", "An in-process local EVM", "A public exchange"],
                1,
                "The script constructs its own provider without an external RPC endpoint.",
            ),
            (
                "Finite allowance 40 followed by a delegated spend of 12 leaves:",
                ["52", "40", "28"],
                2,
                "The authorized spend reduces this finite allowance by twelve.",
            ),
            (
                "A runtime-bytecode match supports:",
                [
                    "That this deployed local code matches the compiled artifact",
                    "Guaranteed market demand",
                    "Correctness of all future modifications",
                ],
                0,
                "Build identity is evidence about the tested artifact, not every possible economic claim.",
            ),
        ],
        [ETHERS, TOKEN, OZ],
    )

    add(
        "6.17",
        3,
        "Minting authority, burns, vesting, and upgrades",
        "Evaluate additional token powers as explicit design changes with separate invariants and review requirements.",
        "A token's economic policy is constrained by reachable code and control over that code. A mint role can expand supply, a burn function can reduce it, and an upgrade mechanism can change future behavior. A cap is only as durable as the authority able to bypass or replace its enforcement. Map every privileged action to its controller, delay, limits, and recovery procedure.\n\nThe supplied CedarCoin intentionally does not implement these extensions. This lesson asks you to design and review them on paper before adding them to a local fork. A multisignature or timelock changes the control process; it does not prove that a proposed action is sound or that signers cannot collude.",
        "Suppose a hypothetical token has supply 800,000 and an enforced cap of one million. A 150,000-unit mint fits the remaining 200,000 capacity, while a 250,000-unit mint does not. Burning 20,000 afterward reduces outstanding supply to 930,000 under that design. Whether burned units can later be reissued must be explicitly specified.\n\nA two-of-three administrator setup requires two approvals, but the independence of those three controllers matters. Three keys held by one person do not provide three independent decision makers.",
        "Create an authority matrix for mint, burn, pause, vest, upgrade, and emergency recovery. State which powers are absent in the supplied contract. For each proposed extension, write invariants and boundary tests: unauthorized caller, exact cap, one unit above cap, expired or premature release, and failed external interaction. Keep immutable-source claims separate from proxy-based systems whose implementation can change. Review source and dependency changes as part of the same artifact release.",
        r"mint\ capacity=cap-current\ supply",
        'print("Remaining mint capacity:", 1000000 - 800000)\nprint("Supply after allowed mint and burn:", 800000 + 150000 - 20000)',
        "Design a capped-mint extension without modifying the supplied contract. Identify caller authority, cap semantics after burns, and five tests required before accepting the change.",
        "The design must specify who can mint, how the cap is checked, whether burns reopen capacity, and how authority changes. Test unauthorized access, exact and excessive caps, burn semantics, and controller transition or recovery.",
        [
            (
                "The supplied CedarCoin includes a public administrator mint:",
                ["Yes", "No", "Only after approval"],
                1,
                "Its only mint is internal to construction.",
            ),
            (
                "A cap can be weakened by:",
                [
                    "Its display precision alone",
                    "The number of holders alone",
                    "Authority that can replace or bypass its enforcement",
                ],
                2,
                "The reachable control system determines the durability of a policy.",
            ),
            (
                "Cap 500 and current supply 420 leave capacity:",
                ["80", "920", "420"],
                0,
                "The remaining permitted amount is 500−420=80.",
            ),
            (
                "An added privileged operation requires:",
                [
                    "Only a new button",
                    "An explicit authority model and adverse tests",
                    "Only a renamed ticker",
                ],
                1,
                "New powers change both economic behavior and the review surface.",
            ),
        ],
        [OZ, SECURE],
    )

    add(
        "6.1",
        4,
        "Tokenomics and monetary dilution",
        "Separate unit rewards, ownership dilution, purchasing power, and the source of a token's economic demand.",
        "Tokenomics describes issuance, distribution, use, incentives, and claims on resources. A quoted staking yield can increase a holder's units while total supply also expands. That unit reward is different from a dollar return, and a dilution-adjusted ownership calculation is different from a purchasing-power forecast. Identify who pays each reward and whether it comes from fees, new issuance, or a temporary subsidy.\n\nScarcity alone does not create demand. A fixed cap specifies one supply rule, while utility, redemption rights, competition, governance, and market access influence what participants are willing to exchange for units. The local teaching coins have no promised market value or redemption service.",
        "If a holder's units rise 8% while total supply rises 6%, the ratio of the holder's supply share changes by 1.08/1.06−1, approximately 1.887%. This does not guarantee a positive currency-denominated return. A price decline of 20% would make the holder's gross value factor 1.08×.8=.864, or a 13.6% loss before costs.\n\nA reward funded by new issuance transfers relative ownership differently from a fee funded by external users. Analyze both the numerator and the system-wide denominator.",
        "Build a supply table with opening units, issuance, burns, circulating definitions, allocations, and ending units. Separate contractual rules from discretionary policy and distinguish circulating supply from total outstanding or maximum supply. In the assignment, calculate both ownership-share change and value change under an explicit price scenario. Document uncertainties in each input instead of presenting a single yield as a comprehensive investment outcome.",
        r"share\ growth=\frac{1+r_{units}}{1+g_{supply}}-1",
        'print("Dilution-adjusted unit yield:", 1.08 / 1.06 - 1)\nprint("Value return after 20% price fall:", 1.08 * 0.8 - 1)',
        "Calculate share growth for a 10% unit reward and 8% supply growth. Then calculate value return if unit price falls 15%, explaining the difference.",
        "Share growth is 1.10/1.08−1≈1.852%. Value return is 1.10×.85−1=−6.5%. Ownership dilution and currency-denominated price risk are distinct.",
        [
            (
                "An 8% unit reward with 6% supply growth changes supply share by approximately:",
                ["8%", "1.89%", "A guaranteed 2% dollar return"],
                1,
                "The ownership ratio changes by 1.08/1.06−1, independently of price.",
            ),
            (
                "A fixed maximum supply guarantees economic demand:",
                ["Yes", "Only with a short ticker", "No"],
                2,
                "Supply rules do not establish willingness to pay or redemption value.",
            ),
            (
                "A 5% unit gain and 10% price fall give value return:",
                ["−5.5%", "+5%", "−10%"],
                0,
                "1.05×.90−1=−.055 under the stated scenario.",
            ),
            (
                "A reward analysis should identify:",
                [
                    "Only its headline percentage",
                    "The funding source and supply denominator",
                    "Only the staking button",
                ],
                1,
                "Issuance-funded and fee-funded rewards have different economic implications.",
            ),
        ],
        [CONSENSUS, TOKEN],
    )

    add(
        "6.18",
        4,
        "Distribution schedules, vesting, and treasury accounting",
        "Model who can access token supply over time and distinguish scheduled availability from actual market selling.",
        "An allocation table records intended ownership, while a vesting schedule specifies when units become claimable. Circulating-supply estimates depend on a declared definition of accessible holdings, locked balances, treasury units, and contractual restrictions. A date in a presentation does not enforce a lock; identify the actual custody or contract mechanism.\n\nUnlocks can change the amount available for sale, but an unlock is not itself a market sale. Price impact depends on holder behavior, liquidity, demand, and other events. Keep the deterministic schedule calculation separate from a speculative market-response model.",
        "A hypothetical team allocation is 120,000 units, with a 12-month cliff followed by 24 equal monthly releases. Under a rule with zero release at the cliff and the first release one month later, each release is 5,000. Six completed release dates make 30,000 cumulatively claimable. A different rule that releases an accrued amount at the cliff gives a different result and must be specified.\n\nIf 20,000 have already been claimed, the remaining claimable amount is 10,000. Claimable, claimed, and sold are three different quantities.",
        "Write boundary cases for immediately before the cliff, exactly at it, the first release, a partial claim, and the final release. Define integer rounding so total released units never exceed allocation and the final residual is handled explicitly. Reconcile treasury opening balance, incoming fees or allocations, spending, and closing balance. Do not combine token-denominated treasury gains with fiat spending power without a dated valuation convention. The supplied fixed-supply token has no vesting mechanism; this schedule is a design exercise for a separate local extension.",
        r"claimable=vested\ cumulative-already\ claimed",
        'monthly = 120000 / 24\nprint("Monthly release:", monthly)\nprint("Claimable after six releases and 20,000 claimed:", 6 * monthly - 20000)',
        "Define a 90,000-unit allocation released over 18 dates after a cliff. Calculate availability after four releases and 5,000 already claimed, and state the exact cliff convention.",
        "Each release is 5,000 and remaining claimable units are 4×5,000−5,000=15,000. The design must specify whether the cliff itself releases anything and when the first release occurs.",
        [
            (
                "An unlock necessarily means the same quantity was sold:",
                ["No", "Yes", "Only for team allocations"],
                0,
                "Availability and actual trading are separate events.",
            ),
            (
                "A vesting calculation needs:",
                [
                    "Only a total allocation",
                    "Exact release boundaries and prior claims",
                    "Only a token logo",
                ],
                1,
                "Timing and previous withdrawals determine current claimable units.",
            ),
            (
                "Allocation 60,000 over 12 equal releases gives:",
                ["12,000 each", "6,000 each", "5,000 each"],
                2,
                "60,000/12=5,000 units per stipulated release.",
            ),
            (
                "Rounding rules should ensure:",
                [
                    "Cumulative release never exceeds the allocation",
                    "An unlimited final mint",
                    "Different totals for each interface",
                ],
                0,
                "Integer scheduling must conserve the defined allocation.",
            ),
        ],
        [OZ, SECURE],
    )

    add(
        "6.2",
        4,
        "AMMs & impermanent loss",
        "Calculate a constant-product swap and distinguish fee income, slippage, and divergence from holding the original assets.",
        "A constant-product market maker relates two reserves through a curve. The marginal price at a point differs from the average price paid for a finite trade. A large trade relative to reserves moves farther along the curve and creates more price impact. Fees and implementation details modify the actual transfer calculation, so declare whether a worksheet omits them.\n\nA liquidity provider owns a changing composition of pool reserves. After external prices move and arbitrage adjusts the pool, the value can differ from simply holding the original assets. The common impermanent-loss formula is a comparison under specific constant-product, balanced-deposit, no-fee assumptions; it is not a universal loss bound.",
        "With reserves x=100 and y=10,000, the no-fee product is one million. Adding ten units of x leaves y=1,000,000/110≈9,090.909, so the trader receives about 909.091 y. Average received price is 90.909 y per x, below the initial marginal ratio 100.\n\nFor a fourfold relative price move under the standard no-fee comparison, 2√4/(1+4)−1=−20%. Fee revenue could offset some divergence, while adverse conditions can introduce additional risks not included in this expression.",
        "Reproduce reserve conservation and compare several trade sizes. Separate quoted output, a minimum-output limit, actual execution, and total transaction cost. For a liquidity position, report both its absolute value change and its performance relative to holding. The local ERC-20 project does not deploy a pool; this lesson is a reserve and risk worksheet, not a claim that creating a token also creates usable market liquidity.",
        r"xy=k,\quad IL(r)=\frac{2\sqrt r}{1+r}-1",
        'import math\noutput = 10000 - 1000000 / 110\nprint("No-fee swap output:", output)\nprint("Average output price:", output / 10)\nprint("No-fee relative LP loss at r=4:", 2 * math.sqrt(4) / 5 - 1)',
        "Calculate the no-fee output for adding 20 x to reserves 100/10,000. Compare its average price with the ten-unit case and state what the formula omits.",
        "Output is 10,000−1,000,000/120≈1,666.667 and average price≈83.333. The larger trade has more impact; this fixture omits fees, gas, changing external prices, and adversarial ordering.",
        [
            (
                "A larger swap relative to reserves generally creates:",
                ["Less impact", "More price impact", "A guaranteed fixed execution price"],
                1,
                "A finite trade moves along the reserve curve.",
            ),
            (
                "Impermanent-loss comparison means:",
                [
                    "Every LP always loses dollars",
                    "Fees cannot matter",
                    "Performance relative to holding under stated assumptions",
                ],
                2,
                "The reference portfolio and fee convention define the comparison.",
            ),
            (
                "Reserves 50 and 200 have product:",
                ["10,000", "250", "4"],
                0,
                "The constant-product fixture multiplies the two reserve quantities.",
            ),
            (
                "Deploying an ERC-20 automatically creates a liquid pool:",
                ["Yes", "No; liquidity provision is a separate operation", "Only with 18 decimals"],
                1,
                "A token ledger alone contains no exchange reserves.",
            ),
        ],
        [AMM, TOKEN],
    )

    add(
        "6.3",
        4,
        "Crypto arbitrage and imperfect neutrality",
        "Reconcile the legs, funding, custody, and timing of a nominally hedged crypto position.",
        "An arbitrage description often compares two quoted prices while ignoring whether both legs can execute and remain funded. Cross-venue trading introduces settlement delay, custody, withdrawal restrictions, and asynchronous fills. A spot-versus-derivative position may offset first-order directional exposure while retaining basis, funding, liquidation, and counterparty risk.\n\nNeutrality depends on the instruments' payoff units and current sensitivities. Equal displayed quantities do not necessarily create equal dollar delta, especially with inverse contracts, options, or changing collateral value. Specify the actual instruments and sizing convention before describing a hedge as neutral.",
        "A simplified position buys one unit of spot at 100 and shorts one linear futures unit at 103. If both settle at 101 with no costs, spot gains one and the short gains two, totaling three. If combined fees and financing are 1.2, the stipulated net gain is 1.8.\n\nIf only the spot leg fills and the price falls to 95, the account has a five-unit loss and no executed futures hedge. The intended spread trade did not remove the actual directional exposure.",
        "Write a leg-by-leg ledger including cash, collateral, contract multiplier, fees, funding, and accepted fills. Stress a failed short, a collateral haircut, a delayed withdrawal, and basis widening before convergence. Avoid treating funding receipts as fixed positive income: the sign and rate can change under the stated contract. The course projects use no live exchanges, so this worksheet illustrates accounting and failure analysis rather than executing a public arbitrage strategy.",
        r"\pi=(S_T-S_0)+(F_0-F_T)-costs",
        'print("Gross converged spread:", (101 - 100) + (103 - 101))\nprint("Net after stated costs:", 3 - 1.2)\nprint("Unhedged failed-leg loss:", 95 - 100)',
        "Buy spot at 200 and short a linear future at 206, both settling at 202. Calculate gross and net profit with costs 2.5, then describe a failed-leg scenario.",
        "Gross profit is 2+4=6 and net is 3.5. If only one leg fills, account risk follows that actual exposure; reconcile and reduce it under an explicit policy.",
        [
            (
                "Delta neutrality removes approximately:",
                [
                    "All risk",
                    "First-order directional exposure under the specified hedge",
                    "Every funding cost",
                ],
                1,
                "Basis, funding, liquidity, custody, and higher-order risks can remain.",
            ),
            (
                "An unfilled hedge leg creates:",
                [
                    "Automatic offsetting inventory",
                    "Guaranteed convergence",
                    "Residual exposure in the filled leg",
                ],
                2,
                "Intent is not an executed position.",
            ),
            (
                "A converged spread of 8 with total costs 3 leaves:",
                ["5", "11", "8"],
                0,
                "Subtract all stipulated costs from the gross spread.",
            ),
            (
                "A credible hedge ledger must include:",
                [
                    "Only two ticker symbols",
                    "Contract units, collateral, costs, and actual fills",
                    "Only the best quoted spread",
                ],
                1,
                "These determine the position's realized economics.",
            ),
        ],
        [
            AMM,
            (
                "Ethereum contributors · Transaction execution",
                "https://ethereum.org/en/developers/docs/transactions/",
            ),
        ],
    )

    add(
        "6.4",
        5,
        "Transaction lifecycle, gas limits, and ordering risk",
        "Track a submitted transaction through execution and acceptance while bounding fees and swap outcomes.",
        "Submission is an intention to enter a chain's processing pipeline. A transaction can remain pending, fail, be replaced under a provider or protocol policy, or appear in a block whose acceptance later changes. Account nonces coordinate ordering; a transaction hash is an identifier, not proof that the intended state change succeeded. Inspect execution status and the accepted chain context.\n\nA swap's minimum-output bound and deadline constrain its acceptable outcome, while gas and fee settings bound different aspects of execution. A larger priority fee can influence inclusion incentives but does not guarantee immediate inclusion or a favorable transaction order. Publicly visible intentions can also expose users to adverse ordering and sandwich-style execution risk.",
        "A quote is 1,000 output units and a user permits at most 2% output shortfall, giving a minimum of 980 under this simple convention. An eventual output of 975 should fail the bound. This protects that outcome condition but does not recover every gas cost or eliminate all ordering risk.\n\nA stipulated 100,000 gas limit at a maximum effective price of 30 gwei corresponds to .003 native units of that budget calculation. Actual charged gas and price must be read from execution evidence.",
        "Build a transaction state table with intent ID, nonce, hash, submission time, receipt status, block reference, and acceptance policy. Reconcile replacements against the same account nonce and avoid recording two intended alternatives as two accepted payments. The local native lab has strict sequential acceptance and no mempool, so document that these production lifecycle concepts are beyond its implementation. In the local EVM project, distinguish rejected estimation from an included reverted transaction when interpreting a test failure.",
        r"minimumOutput=quotedOutput(1-tolerance)",
        'print("Minimum output:", 1000 * (1 - 0.02))\nprint("975 passes bound:", 975 >= 980)\nprint("Illustrative fee budget:", 100000 * 30 / 10 ** 9)',
        "For a quote of 2,500 and tolerance 1.5%, calculate minimum output. Define the evidence needed to move a transaction from submitted to accepted.",
        "Minimum output is 2,462.5 before integer rounding under a declared conservative rule. Check receipt success, resulting state, block identity, and the chosen chain-acceptance policy rather than relying only on a hash.",
        [
            (
                "A higher priority fee guarantees the next block:",
                ["Yes", "No", "Only for ERC-20 transfers"],
                1,
                "Inclusion depends on more than the offered fee.",
            ),
            (
                "A transaction hash alone proves its state change succeeded:",
                ["Always", "Only when it is long", "No"],
                2,
                "Execution status and accepted chain state require separate evidence.",
            ),
            (
                "A 500-unit quote with 3% tolerance gives minimum:",
                ["485", "497", "515"],
                0,
                "500×.97=485 under the stated convention.",
            ),
            (
                "Minimum-output and gas limits constrain:",
                [
                    "The same quantity",
                    "Different execution conditions",
                    "Guaranteed investment returns",
                ],
                1,
                "One bounds an accepted swap result; the other bounds computational execution.",
            ),
        ],
        [
            (
                "Ethereum contributors · Transaction execution",
                "https://ethereum.org/en/developers/docs/transactions/",
            ),
            SECURE,
        ],
    )

    add(
        "6.19",
        5,
        "Oracles, bridges, and contract trust boundaries",
        "Identify the external assumptions behind on-chain decisions and review calls and privileges across contract boundaries.",
        "A contract can enforce deterministic rules over its inputs while still receiving misleading inputs. An oracle introduces a mechanism for obtaining observations such as prices; a bridge introduces assumptions about another chain's state and a process for representing or releasing assets. Trace the data and authority that cross each boundary. On-chain storage does not make an external claim automatically accurate.\n\nExternal calls can transfer execution control. Checks, state updates, and interactions must be designed together, including failure behavior and reentrancy risks. The supplied CedarCoin has no oracle, bridge, or arbitrary external-call feature. Adding one changes the system being reviewed and requires its own tests and authority model.",
        "A lending rule uses collateral quantity ten and a price input of 100, producing collateral value 1,000. If the economically relevant price is actually 70, the same quantity is worth 700. Perfect integer arithmetic cannot repair the stale or manipulated input.\n\nA bridge representation of 100 units also requires a rule connecting issued claims to valid locked or burned assets elsewhere. A ledger showing 100 claims does not prove that the backing remains available or redeemable.",
        "Draw a trust-boundary diagram with source, update frequency, freshness limits, validation rules, privileged keys, and emergency behavior. Add a stale-price case, conflicting sources, failed external call, and revoked controller. Explain what the application can verify locally and which claim depends on external participants. Avoid describing a dependency as trustless merely because it exposes a smart-contract address; inspect its validation and control mechanism. Keep a rejected external observation from silently becoming a zero price or an unrestricted mint.",
        r"collateralValue=quantity\times acceptedPrice",
        'print("Value from supplied price:", 10 * 100)\nprint("Value under lower price:", 10 * 70)\nprint("Overstatement:", 1000 - 700)',
        "Specify freshness and rejection rules for a hypothetical price input. Explain how a stale observation could affect both collateral valuation and a downstream liquidation decision.",
        "The design must bound age, validate scale/source, and define abstention or emergency behavior. An overstated price can hide insufficient collateral; a falsely low price can trigger an inappropriate liquidation.",
        [
            (
                "Storing a price on-chain proves it matches economic reality:",
                ["No", "Yes", "Only if it is an integer"],
                0,
                "Input provenance and timeliness remain separate assumptions.",
            ),
            (
                "Adding a bridge to CedarCoin would:",
                [
                    "Leave the reviewed system identical",
                    "Introduce new validation and authority assumptions",
                    "Automatically guarantee backing",
                ],
                1,
                "Cross-chain representations depend on additional mechanisms.",
            ),
            (
                "Eight collateral units at an accepted price of 75 imply value:",
                ["83", "750", "600"],
                2,
                "The valuation is eight multiplied by 75.",
            ),
            (
                "A failed oracle update should follow:",
                [
                    "An explicit freshness and failure policy",
                    "An invented current price",
                    "Automatic unlimited lending",
                ],
                0,
                "Unavailable evidence must not silently become valid economic input.",
            ),
        ],
        [SECURE, CONSENSUS],
    )

    add(
        "6.5",
        5,
        "Leverage, liquidation, and crypto stress scenarios",
        "Calculate a simplified collateral health measure and challenge liquidity, pricing, and execution assumptions together.",
        "A collateral health measure compares a protocol-defined portion of collateral value with debt. The exact formula, eligible assets, thresholds, oracle conventions, and liquidation process are implementation-specific. This lesson uses a simplified ratio to make the mechanics explicit, not to state a universal rule for every lending protocol.\n\nA position can cross its liquidation threshold before a trader's preferred long-term thesis has time to recover. Price gaps, oracle delays, collateral correlation, funding changes, and liquidation execution can interact. Stress tests should recalculate the balance sheet under scenarios rather than scaling a normal-period volatility estimate and calling it complete.",
        "Collateral quantity ten at price 100 has value 1,000. With a stipulated liquidation threshold .8 and debt 600, health is 800/600≈1.333. If price falls to 70, adjusted collateral is 560 and health becomes .933. Under this fixture, a value below one makes the account potentially liquidatable.\n\nRestoring health exactly to one at the lower price would require debt no greater than 560, so repayment of 40 reaches the boundary. A practical buffer would need a separately chosen margin and feasible funds; touching the boundary is not robust protection.",
        "Stress collateral price, debt growth, threshold changes, and available liquidation liquidity separately and jointly. Record whether the response can actually execute while the system is congested. Distinguish an accounting threshold from a guarantee of immediate liquidation at a quoted price. The local token and native-coin projects do not provide lending or leverage, so this exercise teaches risk interpretation without connecting a wallet or borrowing real assets.",
        r"H=Q P\theta/D",
        'print("Initial health:", 10 * 100 * 0.8 / 600)\nprint("Stressed health:", 10 * 70 * 0.8 / 600)\nprint("Repayment to boundary:", 600 - 560)',
        "Use collateral 20, price 50, threshold .75, and debt 500. Recalculate health after price falls to 30 and identify repayment needed to reach one.",
        "Initial health is 1.5; stressed adjusted collateral is 450, health .9, and repayment 50 reaches one. This is the boundary under the stipulated rule, not a guaranteed safe buffer.",
        [
            (
                "Health below one in the stated lending fixture indicates:",
                [
                    "Guaranteed profit",
                    "Potential liquidation eligibility",
                    "A free debt cancellation",
                ],
                1,
                "Adjusted collateral no longer covers debt under that threshold rule.",
            ),
            (
                "A stress scenario should assume every rescue trade fills instantly:",
                ["Always", "Only when profitable", "No"],
                2,
                "Congestion and liquidity can constrain the response itself.",
            ),
            (
                "Adjusted collateral 720 and debt 600 give health:",
                ["1.2", ".833", "120"],
                0,
                "The ratio is 720/600=1.2.",
            ),
            (
                "A liquidation formula applies universally to all protocols:",
                [
                    "Yes",
                    "No; inspect the particular implementation",
                    "Only when debt is denominated in dollars",
                ],
                1,
                "Thresholds, eligible collateral, and execution rules vary.",
            ),
        ],
        [SECURE, AMM],
    )

    add(
        "6.20",
        5,
        "Invariants, adversarial fixtures, and reproducible builds",
        "Turn asset promises into executable properties and preserve the exact source and dependency configuration tested.",
        "A happy-path transfer demonstrates one example. An invariant states a property that should hold across an allowed family of transitions, such as conservation of fixed supply or rejection of unauthorized delegated spending. Design tests around the specification, including boundary and failure cases, rather than merely repeating source-code branches.\n\nThe project contains deterministic transaction sequences and explicit adverse fixtures. These are not a full fuzzing campaign, formal proof, or external audit. Property-based testing can generate broader sequences, but generators, state models, and coverage still need review. A passing test suite only supports the cases and properties it actually exercises.",
        "For the fixed-supply contract, the sum of balances among all three fixture accounts remains one million whole tokens after each of twelve transfers. For the native chain, supply changes only by the permitted reward and never exceeds 1,100. A rejected candidate leaves accepted balances, nonces, height, tip, and supply unchanged.\n\nThe token test compares compiled runtime with the deployed local runtime and prints source and runtime hashes. The package lock fixes dependency resolution; compiler optimization and EVM target are also part of the build identity.",
        "Create a test matrix mapping each promise to at least one positive and one adverse case. Include zero transfer, maximum affordable transfer, overspend, expired authority where implemented, altered signatures, wrong domains, duplicate nonces, and mutation attempts against returned snapshots. Add a self-designed case and explain the expected result before running it. Retain command output and exact source versions. If a new extension changes the invariant, update the specification and tests together rather than weakening an unexplained assertion.",
        r"fixed\ supply:\sum_i balance_i=S_0",
        'print("Reconciled fixed supply:", 999890 + 110 + 0)\nprint("Native capped supply:", min(1100, 1000 + 10 * 20))',
        "Add one boundary test to each project and document the specification it checks. Explain why a passing deterministic sequence is not a complete audit.",
        "Examples include an exact-balance transfer and a native reward after reaching the cap. The tests cover defined inputs and properties; they do not exhaust every interaction, environment, or future modification.",
        [
            (
                "A deterministic test suite is automatically a formal proof:",
                ["No", "Yes", "Only if it runs quickly"],
                0,
                "Finite fixtures provide evidence for tested behavior, not universal proof.",
            ),
            (
                "A reproducible build manifest includes:",
                [
                    "Only a screenshot",
                    "Source, dependency lock, compiler, and build settings",
                    "Only the token name",
                ],
                1,
                "The resulting artifact depends on all these inputs.",
            ),
            (
                "Fixed supply 500 with holders 200 and 175 leaves the third holder:",
                ["325", "75", "125"],
                2,
                "Conservation requires 500−200−175=125 units.",
            ),
            (
                "An unexplained failed invariant should lead to:",
                [
                    "Investigation of code and specification before acceptance",
                    "Deleting the assertion",
                    "Publishing the result unchanged",
                ],
                0,
                "A failed property challenges the claimed behavior.",
            ),
        ],
        [SECURE, NODE, ETHERS],
    )

    add(
        "6.21",
        6,
        "Native monetary policy and chain recovery design",
        "Specify issuance boundaries and distinguish replay recovery from selecting a competing blockchain history.",
        "A monetary policy must define initial allocation, the schedule of new issuance, rounding, caps, and any authority that can change those rules. In the native lab, genesis creates 1,000 units and each accepted block adds up to ten until supply reaches 1,100. There are no transaction fees or burns. This makes every supply change traceable to a specific accepted block.\n\nRecovery from stored accepted blocks differs from resolving a fork. Replaying one known history can reconstruct deterministic state. Choosing between competing histories requires a consensus rule and evidence that this lab deliberately does not implement. A backup of balances alone also omits the transaction history needed to independently validate those balances.",
        "At heights zero, five, ten, and eleven, the stipulated supplies are 1,000, 1,050, 1,100, and 1,100. Once the cap is reached, further accepted blocks have reward zero. The cap test mines beyond this boundary to show that the implementation stops issuance.\n\nA fresh instance initialized with the same genesis recipient can replay the accepted block sequence and reproduce balances and nonces. A different genesis produces a different initial commitment and cannot silently accept the old history as its own.",
        "Write a policy table and test the first block, last positive reward, first zero reward, and a forged excessive reward. Design a hypothetical persistence format with version, genesis identity, accepted blocks, and integrity checks, while documenting that durable storage is not supplied by the exercise. Explain how a future protocol change would affect compatibility and who would have to adopt it. Do not equate editing a local constant with changing the policy of an established public network.",
        r"reward_h=\min(10,1100-S_{h-1})",
        'for height in [0, 5, 10, 11]:\n    print("Height and supply:", height, 1000 + min(10 * height, 100))',
        "Produce the issuance boundary table and replay the accepted test history. Explain what additional design is needed to recover after receiving two competing valid tips.",
        "Supply stops at 1,100. Replay reconstructs one known history; competing tips require a specified chain-selection and finality process, peer evidence, and associated adversarial assumptions.",
        [
            (
                "Replaying one accepted history implements fork choice:",
                ["Yes", "No", "Only after ten blocks"],
                1,
                "Reconstruction and selecting among competing histories are different tasks.",
            ),
            (
                "The native reward after reaching 1,100 supply is:",
                ["10 forever", "Negative ten", "Zero"],
                2,
                "The declared cap leaves no remaining issuance capacity.",
            ),
            (
                "Supply at height seven in this lab is:",
                ["1,070", "1,700", "1,100"],
                0,
                "Seven ten-unit rewards add 70 to genesis supply.",
            ),
            (
                "A recovery artifact should identify:",
                [
                    "Only a balance screenshot",
                    "The genesis and the accepted history being replayed",
                    "Only the miner's display name",
                ],
                1,
                "The initial rules and history determine reconstructed state.",
            ),
        ],
        [BTC, CONSENSUS],
    )

    add(
        "6.22",
        6,
        "Token release artifact and authority review",
        "Prepare a reviewable local token package that connects source, build, deployment, tests, and stated powers.",
        "A release artifact should let another reviewer establish what code was built, what code executed, and what behavior was tested. Include source, dependency lock, compiler and EVM settings, constructor arguments, artifact hashes, and test results. A contract address by itself does not communicate all these facts. On a public chain, source verification and deployment identity would require additional independently checked evidence.\n\nFor the local course, the deliverable is the supplied archive plus your annotated source, local output, and an authority matrix. The token has constructor-only fixed issuance and no owner or upgrade mechanism. Describe absent powers explicitly in that matrix without claiming that every ERC-20 has the same constraints.",
        "The initial one-million-token supply remains fixed after transfers and finite delegated spending. The test records metadata, allowance reduction, rejected overspending, conservation, and a runtime-byte match. These connect the specific compiled wrapper to its local observed behavior.\n\nChanging a constructor supply, a dependency version, or compiler settings creates a new build context. Reusing an old report without rerunning the relevant checks would misrepresent which artifact was evaluated.",
        "Create a manifest that a peer can follow from a clean extraction using npm ci and npm test. Separate stable expectations such as supply and decimals from varying local account addresses. Include the external dependency's name, version, and license attribution; do not present inherited implementation as wholly original Quanta code. Record known omissions such as no public network, external integration, or independent audit. The course's source references support attribution, while the actual dependency license governs reuse of that dependency.",
        r"artifact\ identity=(source,dependencies,compiler,settings,constructor)",
        'print("Declared whole supply:", 1000000)\nprint("Supply after two ordinary transfers:", 1000000)\nprint("Required independent review fields:", 5)',
        "Prepare a local release manifest and authority matrix. Change one build input in a separate copy and explain which evidence must be regenerated.",
        "Rebuild the changed artifact, rerun affected behavior tests, and record new identities. The report must match the actual source, dependency tree, settings, and constructor used.",
        [
            (
                "An old test report automatically applies after changing dependencies:",
                ["No", "Yes", "Only if the ticker stays the same"],
                0,
                "The evaluated artifact has changed and needs corresponding evidence.",
            ),
            (
                "Inherited implementation should be attributed to:",
                [
                    "Only the course author",
                    "Its dependency authors with version and license context",
                    "No one if imported",
                ],
                1,
                "An import does not erase source authorship or reuse conditions.",
            ),
            (
                "Two transfers of a fixed-supply token change total supply by:",
                ["Two tokens", "The sum transferred", "Zero"],
                2,
                "Normal transfers conserve the defined supply.",
            ),
            (
                "The local release report establishes:",
                [
                    "Evidence for the identified local artifact",
                    "Automatic public deployment",
                    "A completed independent audit",
                ],
                0,
                "Its claims should match the environment and review actually performed.",
            ),
        ],
        [OZ, ETHERS, SECURE],
    )

    add(
        "6.23",
        6,
        "Publication readiness, disclosures, and governance boundaries",
        "Distinguish an educational implementation from a reviewed public asset proposal and prepare accurate source and authority disclosures.",
        "A working contract is one component of an asset proposal. A public proposal also needs a clear purpose, participant rights or their absence, issuance and allocation rules, controller powers, dependencies, operational responsibilities, and evidence supporting technical claims. A token's name, website, or source citation does not establish permission to reuse another project's assets or imply endorsement.\n\nThis course does not conduct a token sale or publish to a public network. Your assignment is a review packet with explicit unresolved decisions. Jurisdiction-specific obligations, permissions, and representations require appropriate current review for the actual activity and participants; a generic course checklist cannot decide them.",
        "Consider a proposal allocating 50% to community use, 20% to a treasury, 20% to contributors, and 10% to liquidity purposes. The percentages sum to 100%, but that arithmetic does not establish whether custody, vesting, distribution, or liquidity mechanisms exist. Each allocation needs a controller, timing rule, and evidence.\n\nA document saying no administrator can mint is inconsistent with code exposing an unrestricted mint role. The review must reconcile prose with reachable authority rather than accepting the more attractive description.",
        "Prepare a source and rights register for code, text, images, datasets, and names actually used. Preserve required dependency notices and label original teaching material. Add a claims table with supporting evidence, limitations, and an owner responsible for updates. Record governance changes and incident communication procedures as design requirements. A readiness decision should remain deferred when a material authority, source-rights, security, or operational question is unresolved; passing the course exam does not resolve those questions.",
        r"\sum_i allocation_i=100\%",
        'print("Allocation total:", 50 + 20 + 20 + 10)\nprint("Contributor units from one million:", 0.20 * 1000000)',
        "Draft an allocation table, authority disclosure, source/rights register, and claims-evidence table for the local teaching token. List decisions that remain before any public proposal.",
        "The packet should identify controllers and mechanisms, reconcile claims with code, preserve attribution and license context, and record unresolved review needs without claiming the local exercise is a public launch.",
        [
            (
                "A source citation automatically grants every reuse permission:",
                ["Yes", "No", "Only if shown in a footer"],
                1,
                "Attribution and applicable permission or license conditions are separate matters.",
            ),
            (
                "An allocation chart proves its vesting contracts exist:",
                ["Always", "Only with percentages", "No"],
                2,
                "A planned distribution is not evidence of implemented enforcement.",
            ),
            (
                "A 15% allocation of 200,000 units is:",
                ["30,000", "15,000", "3,000"],
                0,
                "Multiply the total by .15 to obtain the allocated units.",
            ),
            (
                "A no-mint claim should be checked against:",
                [
                    "Only marketing text",
                    "Reachable contract authority and upgrade powers",
                    "Only the token icon",
                ],
                1,
                "Actual code and control mechanisms determine whether issuance can change.",
            ),
        ],
        [TOKEN, OZ, SECURE],
    )

    add(
        "6.24",
        6,
        "Capstone: cryptography and coin-creation dossier",
        "Demonstrate both native coin and ERC-20 creation locally, explain their differences, and defend the validation evidence.",
        "Complete both projects and assemble one dossier connecting cryptographic authorization, ledger accounting, issuance policy, and implementation identity. For the native chain, include hash-vector and signature tests, a Merkle proof, accepted transfers, rejected histories, supply-cap boundaries, and independent replay. For the token, include annotated Solidity, pinned build inputs, deployment output, transfers, finite allowances, adverse tests, and runtime identity.\n\nThe two assets deliberately have different mechanisms. Native issuance belongs to the local base rules and block validation. CEDAR issuance belongs to a constructor executed by the local EVM. Neither exercise creates a public trading market or establishes economic demand.",
        "Your native baseline should reconcile 910 units for Alice, 100 for Bob, and total 1,010 after the first block. Your token baseline should show one million whole units of supply, a 110-token recipient balance after the main transfers, and remaining allowance 15 before later fixture steps.\n\nAdd one failure that preserves accepted native state and one token operation rejected for insufficient authority. Explain the expected result before execution, preserve the actual output, and investigate any mismatch rather than adjusting the expected value after the fact.",
        "Use a 100-point self-assessment: cryptographic encoding and authorization 20, native state and issuance 20, token implementation and build 20, adverse tests and reconciliation 20, and source/authority/limitations report 20. Require at least 80 plus no unresolved forged authorization, unauthorized issuance, corrupted rejected state, exposed private key, or false public-launch claim. The automatic final tests conceptual transfer; it does not inspect your local files or independently audit either implementation. Conclude with one concrete extension and the new assumptions it would introduce.",
        r"accept=(score\ge80)\land no\ critical\ failure",
        'print("Native baseline conservation:", 910 + 100)\nprint("Token remaining finite allowance:", 25 - 10)\nprint("Capstone rubric total:", 20 + 20 + 20 + 20 + 20)',
        "Submit both project outputs, annotated rules and Solidity, one new adverse test per project, reconciliations, source/rights notes, and the completed rubric.",
        "A valid dossier reproduces the declared balances and authority rules, detects its adverse cases, preserves build identity and attribution, and states the local-only scope. A high rubric score cannot override a critical validation or disclosure failure.",
        [
            (
                "The automatic concept exam independently audits the local source files:",
                ["No", "Yes", "Only if all answers are correct"],
                0,
                "Project evidence and review are separate from multiple-choice grading.",
            ),
            (
                "A capstone with unauthorized issuance should:",
                [
                    "Pass if its report is polished",
                    "Fail the mandatory acceptance condition",
                    "Ignore the extra units",
                ],
                1,
                "The supply and authority promises are fundamental invariants.",
            ),
            (
                "Five rubric categories worth 20 each total:",
                ["80", "120", "100"],
                2,
                "Five multiplied by twenty gives a hundred-point rubric.",
            ),
            (
                "The strongest completed-course claim is:",
                [
                    "Reproducible local coin and token mechanics with tested boundaries",
                    "Guaranteed public-asset security",
                    "Guaranteed investment returns",
                ],
                0,
                "The evidence supports the defined educational implementations and their explicit limits.",
            ),
        ],
        [NODE, TOKEN, SECURE],
    )

    parts = [
        (
            "Cryptography and wallet foundations",
            "Bytes, hashes, Merkle proofs, signatures, keys, and replay domains.",
        ),
        (
            "Build a native coin ledger",
            "Account state, consensus boundaries, atomic validation, and a signed local blockchain.",
        ),
        (
            "Create an ERC-20 token",
            "EVM units, fixed-supply Solidity, local deployment, transfers, allowances, and authority design.",
        ),
        (
            "Token economics and market mechanics",
            "Dilution, vesting, AMM reserves, liquidity-provider comparisons, and hedged positions.",
        ),
        (
            "Execution and adversarial validation",
            "Transaction lifecycle, external trust, liquidation scenarios, invariants, and build identity.",
        ),
        (
            "Policy, release review, and capstone",
            "Supply boundaries, recovery, artifact review, source disclosures, and both creation projects.",
        ),
    ]
    return finish(
        {
            "id": "web3",
            "number": 6,
            "title": "Web3, cryptography & coin creation",
            "description": "Build the foundations from hashes and signatures to a native coin blockchain and an ERC-20 token, then test issuance, authority, market mechanics, and operational risks.",
            "source": "Original Quanta course · cryptographic standards and primary blockchain documentation",
            "level": "Foundations → advanced",
            "icon": "crypto",
            "studyType": "applied",
            "modules": modules,
            "prerequisites": "Basic programming and arithmetic. Guided Python worksheets run in the app. Creation projects use Node 22+, JavaScript, and introductory Solidity; no wallet connection, credentials, or real funds are required.",
            "outcomes": [
                "Explain hash commitments, Merkle proofs, signatures, and replay protection.",
                "Validate a local native ledger with capped issuance and atomic state transitions.",
                "Compile, deploy, and test a fixed-supply ERC-20 on a local EVM.",
                "Reconcile token units, delegated authority, distribution, and market scenarios.",
                "Prepare reproducible project evidence with sources and explicit implementation limits.",
            ],
            "readingGuide": "Six units, 24 original lessons, 48 practice questions, five checkpoints, and a 24-question final. Each lesson includes primary references, a worked example, a guided worksheet, and an assignment with a solution. Download both complete creation projects in one archive. The final dossier is self-assessed separately from the automatic exam; all deployment and mining exercises stay local.",
            "parts": [
                {"id": str(i), "title": title, "description": description}
                for i, (title, description) in enumerate(parts, 1)
            ],
            "references": [{"title": t, "url": u} for t, u in [HASH, SIGN, BTC, TOKEN, OZ, SECURE]],
            "resources": [
                {
                    "title": "Download both coin-creation projects",
                    "url": "/course-assets/web3/coin-lab.zip",
                },
                {
                    "title": "Download the coin-creation project guide",
                    "url": "/course-assets/web3/README.md",
                },
                {
                    "title": "Download the standalone native coin lab",
                    "url": "/course-assets/web3/native-chain.mjs",
                },
                {
                    "title": "Download the CedarCoin Solidity source",
                    "url": "/course-assets/web3/CedarCoin.sol",
                },
            ],
        },
        checkpoints_for(modules, parts, 5),
    )
