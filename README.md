### simple idp configuration for test environments

This repo contains an ansible playbook for configuring a server to act as a simple IDP.  There is also a vagrant file for creating a local VM to act as the playbook target.

### setup notes

1. this repo contains a reference to an external submodule, so after cloning make sure to execute the following:

```bash
  git submodule update --init
```

2. from this folder run the command:

```bash
  python3 generate-keys.py
```

3. to create the test virtual machine, run:

```bash
  vagrant up
```

4. to provision the test vm:

```bash
  ansible-playbook -i inventory playbook.yml
```

5. to modify the authenticated user database, edit ``roles/idp/files/authsources.php`` and rerun the playbook

6. test authentication against the configured data source by loading the following url in a browser:

```bash
  http://10.11.12.99/simplesaml
```

... then select ``Authentication`` - ``Test configured authentication sources`` - ``test-users``
