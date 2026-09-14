// Compile and deploy inside this process. No public RPC, wallet connection, or real funds.
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { createHash } from "node:crypto";
import solc from "solc";
import ganache from "ganache";
import { BrowserProvider, ContractFactory, parseUnits, ZeroAddress } from "ethers";

const source = readFileSync(new URL("./CedarCoin.sol", import.meta.url), "utf8");
const input = {
  language: "Solidity",
  sources: {"CedarCoin.sol": {content: source}},
  settings: {
    optimizer: {enabled: true, runs: 200},
    // Match the local execution VM; do not silently emit newer unsupported opcodes.
    evmVersion: "shanghai",
    outputSelection: {"*": {"*": ["abi", "evm.bytecode.object", "evm.deployedBytecode.object"]}},
  },
};
const output = JSON.parse(solc.compile(JSON.stringify(input), {import: (path) => {
  if (!path.startsWith("@openzeppelin/contracts/") || path.includes("..")) {
    return {error: "Import outside the pinned OpenZeppelin package"};
  }
  try { return {contents: readFileSync(new URL(`./node_modules/${path}`, import.meta.url), "utf8")}; }
  catch { return {error: `Missing dependency: ${path}`}; }
}}));
const errors = (output.errors ?? []).filter((error) => error.severity === "error");
assert.equal(errors.length, 0, errors.map((error) => error.formattedMessage).join("\n"));
const compiled = output.contracts["CedarCoin.sol"].CedarCoin;
const rpc = ganache.provider({logging: {quiet: true}, chain: {chainId: 31337, hardfork: "shanghai"}, wallet: {totalAccounts: 3}});
try {
  const provider = new BrowserProvider(rpc);
  const [owner, spender, recipient] = await Promise.all([0, 1, 2].map((i) => provider.getSigner(i)));
  const addresses = await Promise.all([owner, spender, recipient].map((s) => s.getAddress()));
  const coin = await new ContractFactory(compiled.abi, compiled.evm.bytecode.object, owner).deploy(addresses[0]);
  await coin.waitForDeployment();
  const unit = (value) => parseUnits(value, 18);
  const supply = unit("1000000");
  assert.equal(await coin.name(), "Cedar Learning Coin");
  assert.equal(await coin.symbol(), "CEDAR");
  assert.equal(await coin.decimals(), 18n);
  assert.equal(await coin.totalSupply(), supply);
  assert.equal(await coin.balanceOf(addresses[0]), supply);
  const transfer = await (await coin.transfer(addresses[2], unit("100"))).wait();
  assert.ok(transfer.logs.some((log) => { try { return coin.interface.parseLog(log)?.name === "Transfer"; } catch { return false; } }));
  await (await coin.approve(addresses[1], unit("25"))).wait();
  await (await coin.connect(spender).transferFrom(addresses[0], addresses[2], unit("10"))).wait();
  assert.equal(await coin.allowance(addresses[0], addresses[1]), unit("15"));
  assert.equal(await coin.balanceOf(addresses[2]), unit("110"));
  await assert.rejects(coin.connect(spender).transferFrom(addresses[0], addresses[2], unit("16")));
  await assert.rejects(coin.connect(recipient).transfer(addresses[1], unit("111")));
  await assert.rejects(coin.transfer(ZeroAddress, 1n));
  // Rejections leave token state unchanged; failed real transactions may still consume gas.
  assert.equal(await coin.balanceOf(addresses[2]), unit("110"));
  assert.equal(await coin.allowance(addresses[0], addresses[1]), unit("15"));
  const zero = await (await coin.transfer(addresses[2], 0n)).wait();
  assert.ok(zero.logs.some((log) => { try { return coin.interface.parseLog(log)?.name === "Transfer"; } catch { return false; } }));
  // Exercise a deterministic sequence of transfers and check supply conservation after every step.
  for (let i = 1; i <= 12; i++) {
    await (await coin.connect(recipient).transfer(addresses[1], BigInt(i))).wait();
    const balances = await Promise.all(addresses.map((address) => coin.balanceOf(address)));
    assert.equal(balances.reduce((a, b) => a + b, 0n), supply);
    assert.equal(await coin.totalSupply(), supply);
  }
  assert.ok(!compiled.abi.some((entry) => entry.type === "function" && ["mint", "upgradeTo", "owner"].includes(entry.name)));
  const runtime = await provider.getCode(await coin.getAddress());
  assert.equal(runtime.slice(2), compiled.evm.deployedBytecode.object);
  console.log(JSON.stringify({scope: "in-process local EVM only", chainId: 31337, compiler: solc.version(),
    sourceSha256: createHash("sha256").update(source).digest("hex"),
    runtimeSha256: createHash("sha256").update(Buffer.from(runtime.slice(2), "hex")).digest("hex"),
    decimals: 18, wholeTokenSupply: "1000000", checks: "deployment, metadata, supply, transfer/events, finite allowance, rejection state, zero transfer, 12 conservation steps, runtime match",
    passed: true}, null, 2));
} finally { await rpc.disconnect(); }
