import { ethers } from "hardhat";
import { Airdrop } from "./Airdrop.sol";

async function main() {
  const airdropTokenAddress = "0xBA62BCfcAaFc6622853cca2BE6Ac7d845BC0f2Dc";
  const AirdropFactory = await ethers.getContractFactory("Airdrop");
  const airdrop = await AirdropFactory.deploy(airdropTokenAddress);

  await airdrop.deployed();
  console.log("Airdrop contract deployed to:", airdrop.address);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
