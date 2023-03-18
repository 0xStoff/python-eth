import { HardhatUserConfig } from "hardhat/config";
import "@nomicfoundation/hardhat-toolbox";
require('dotenv').config();

const config: HardhatUserConfig = {
  solidity: "0.8.18",
  networks: {
    goerli: {
      url: process.env.INFURA_URL,
          accounts: [
           process.env.MM_PRIVATE_KEY,
      ],
      gas: 8000000,
      gasPrice: 20000000000,
    },
  },
};

export default config;
