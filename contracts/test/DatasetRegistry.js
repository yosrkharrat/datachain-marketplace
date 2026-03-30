const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("DatasetRegistry", function () {
  async function deployFixture() {
    const [owner, other] = await ethers.getSigners();
    const Factory = await ethers.getContractFactory("DatasetRegistry");
    const registry = await Factory.deploy();
    await registry.waitForDeployment();

    return { registry, owner, other };
  }

  describe("registerDataset", function () {
    it("registers a dataset and emits DatasetRegistered", async function () {
      const { registry, owner } = await deployFixture();

      const ipfsHash = "QmHash1";
      const title = "Dataset A";
      const description = "Sample dataset";
      const priceWei = ethers.parseEther("0.01");

      await expect(
        registry.registerDataset(ipfsHash, title, description, priceWei)
      )
        .to.emit(registry, "DatasetRegistered")
        .withArgs(1n, owner.address, ipfsHash, title, priceWei);

      expect(await registry.totalDatasets()).to.equal(1n);
    });

    it("reverts when ipfs hash is empty", async function () {
      const { registry } = await deployFixture();

      await expect(
        registry.registerDataset("", "Title", "Desc", 1)
      ).to.be.revertedWith("IPFS hash required");
    });

    it("reverts when title is empty", async function () {
      const { registry } = await deployFixture();

      await expect(
        registry.registerDataset("QmHash2", "", "Desc", 1)
      ).to.be.revertedWith("Title required");
    });
  });

  describe("getDataset", function () {
    it("returns all dataset fields by id", async function () {
      const { registry, owner } = await deployFixture();

      const ipfsHash = "QmHash3";
      const title = "Dataset B";
      const description = "Another dataset";
      const priceWei = 12345n;

      await registry.registerDataset(ipfsHash, title, description, priceWei);

      const dataset = await registry.getDataset(1);

      expect(dataset.id).to.equal(1n);
      expect(dataset.ipfsHash).to.equal(ipfsHash);
      expect(dataset.title).to.equal(title);
      expect(dataset.description).to.equal(description);
      expect(dataset.priceWei).to.equal(priceWei);
      expect(dataset.owner).to.equal(owner.address);
    });

    it("reverts for non-existent id", async function () {
      const { registry } = await deployFixture();
      await expect(registry.getDataset(1)).to.be.revertedWith(
        "Dataset does not exist"
      );
    });
  });

  describe("getAllDatasets", function () {
    it("returns all registered datasets in order", async function () {
      const { registry, owner, other } = await deployFixture();

      await registry.registerDataset("QmOne", "Title 1", "Desc 1", 11n);
      await registry
        .connect(other)
        .registerDataset("QmTwo", "Title 2", "Desc 2", 22n);

      const datasets = await registry.getAllDatasets();

      expect(datasets.length).to.equal(2);

      expect(datasets[0].id).to.equal(1n);
      expect(datasets[0].ipfsHash).to.equal("QmOne");
      expect(datasets[0].title).to.equal("Title 1");
      expect(datasets[0].description).to.equal("Desc 1");
      expect(datasets[0].priceWei).to.equal(11n);
      expect(datasets[0].owner).to.equal(owner.address);

      expect(datasets[1].id).to.equal(2n);
      expect(datasets[1].ipfsHash).to.equal("QmTwo");
      expect(datasets[1].title).to.equal("Title 2");
      expect(datasets[1].description).to.equal("Desc 2");
      expect(datasets[1].priceWei).to.equal(22n);
      expect(datasets[1].owner).to.equal(other.address);
    });
  });
});
