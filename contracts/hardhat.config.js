require("@nomicfoundation/hardhat-toolbox");
const path = require("path");
require("dotenv").config({ path: path.resolve(__dirname, "../.env"), quiet: true });

const privateKey = (process.env.PRIVATE_KEY || "").trim();
const normalizedPrivateKey = privateKey.startsWith("0x") ? privateKey : `0x${privateKey}`;
const isValidPrivateKey = /^0x[0-9a-fA-F]{64}$/.test(normalizedPrivateKey);

/** @type import('hardhat/config').HardhatUserConfig */
module.exports = {
  solidity: "0.8.24",
  networks: {
    sepolia: {
      url: process.env.SEPOLIA_RPC_URL || "",
      accounts: isValidPrivateKey ? [normalizedPrivateKey] : [],
    },
  },
  etherscan: {
    apiKey: process.env.ETHERSCAN_API_KEY || "",
  },
};
