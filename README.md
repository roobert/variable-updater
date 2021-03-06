# Variable Updater

## About

Set BitBucket pipeline variables with values from Vault

## Install

```
pip install variable-updater
```

## Docker

```
make docker
```

## Requirements

* BitBucket "app password" with edit variables permission
* Vault user with permission to read keys to use as source for BitBucket variables

## Example

```
# Read bitbucket credentials from vault
export VAULT_BITBUCKET_KEY_MOUNT=secret
export VAULT_BITBUCKET_PASSWORD_KEY=app/variable-updater/bitbucket-password
export VAULT_BITBUCKET_USERNAME_KEY=app/variable-updater/bitbucket-username

# vault settings
export VAULT_USERNAME="variable-updater"
export VAULT_PASSWORD="secret_password"
export VAULT_ADDR="https://vault.example.com"

# config file contains values to read from vault and write to bitbucket..
variable-updater --config config.example.yml
```
