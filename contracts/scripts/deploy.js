const fs = require("fs");
const path = require("path");
const hre = require("hardhat");

async function main() {
  const [deployer] = await hre.ethers.getSigners();

  if (!deployer || !deployer.provider) {
    throw new Error(
      "No deployer signer available. Set a valid PRIVATE_KEY in the root .env file and fund it with Sepolia ETH."
    );
  }

  const deployerAddress = await deployer.getAddress();
  const deployerBalance = await hre.ethers.provider.getBalance(deployerAddress);

  console.log("Deploying with account:", deployerAddress);
  console.log("Deployer balance (wei):", deployerBalance.toString());

  if (deployerBalance === 0n) {
    throw new Error(
      "Deployer has zero Sepolia ETH. Fund this wallet from a Sepolia faucet before deploying."
    );
  }

  const DatasetRegistry = await hre.ethers.getContractFactory("DatasetRegistry");
  const datasetRegistry = await DatasetRegistry.deploy();

  await datasetRegistry.waitForDeployment();

  const contractAddress = await datasetRegistry.getAddress();
  console.log("DatasetRegistry deployed to:", contractAddress);

  const artifact = await hre.artifacts.readArtifact("DatasetRegistry");
  const chain = await hre.ethers.provider.getNetwork();
  const chainName = hre.network.name;

  const output = {
    contractName: "DatasetRegistry",
    network: chainName,
    chainId: Number(chain.chainId),
    address: contractAddress,
    deployer: deployerAddress,
    abi: artifact.abi,
    deployedAt: new Date().toISOString(),
  };

  const deploymentsDir = path.resolve(__dirname, "../deployments", chainName);
  fs.mkdirSync(deploymentsDir, { recursive: true });

  const outputPath = path.join(deploymentsDir, "DatasetRegistry.json");
  fs.writeFileSync(outputPath, JSON.stringify(output, null, 2));

  console.log("Deployment metadata written to:", outputPath);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
