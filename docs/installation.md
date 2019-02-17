# Installing "Electron as a GUI for NuCypher Apps"

This software requires the installation of dependencies from Ethereum, Electron, and NuCypher.


## Ethereum Geth / Swarm

Please take a look at Swarm's documetation on [ReadTheDocs](https://swarm-guide.readthedocs.io/en/latest/installation.html).

Download Geth from [https://geth.ethereum.org/downloads/](https://geth.ethereum.org/downloads/);

Download Swarm from [https://swarm-gateways.net/bzz:/theswarm.eth/downloads/](https://swarm-gateways.net/bzz:/theswarm.eth/downloads/)

For now, you will be required to run swarm and geth outside of Electron. Eventually this will be moved within Electron. This prototype assumes a Swarm v0.3.10 binary is located in the root directory.


### Set up the Ethereum encrypted key:

This step may not be necessary if you have a demo key ready. You will be asked for a password to protect your new Ethereum private key.

```
./geth --keystore "/your/keystore/directory..." account new
```

### Test-run Swarm:

```
./swarm --keystore "/your/keystore/directory..." --bzzaccount "0x000..."
```

## Electron

### Set up the environment:

```

export npm_config_target=1.7.6
export npm_config_runtime=electron
export npm_config_disturl=https://atom.io/download/electron
export npm_config_build_from_source=true

npm config ls
```

### Install Node v8.15.0, Electron v1.7.6, and Dependencies:

```
nvm install v8.15.0
nvm use v8.15.0
npm install
```

### Rebuild electron

This is to fix a [known node module version conflict](https://stackoverflow.com/questions/42616008/node-module-version-conflict-when-installing-modules-for-electron) relating to Electron installs.

```
npm install --save-dev electron-rebuild
./node_modules/.bin/electron-rebuild
```

## NuCypher / pyUmbral

### Install zerorpc

Works best with python v3.6.

```
pip3.6 install zerorpc
```

### Install other dependencies:

```
cd nucypher
pip3.6 install -r requirements.txt
```

Note: This was for os x installation; pypiwin32 may be needed on windows.


### Test-run the Electron app:

```
./node_modules/.bin/electron .
```





