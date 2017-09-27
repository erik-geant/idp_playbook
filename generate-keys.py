import binascii
import os
import subprocess
import tempfile

_CERT_OPTIONS = {
    "C": "NL",
    "ST": "N-H",
    "L": "Amsterdam",
    "O": "GÉANT",
    "OU": "perfsonar",
    "CN": "test",
    "days": "3650",
    "key_size": "2048"
}

_SERVER_CERT_CONFIG_FORMAT = '''[ req ]
    distinguished_name     = req_distinguished_name
    x509_extensions        = cert_extensions
    prompt = no

[ req_distinguished_name ]
    C  = {C}
    ST = {ST}
    L  = {L}
    O  = {O}
    OU = {OU}
    CN = {CN}

[ cert_extensions ]
    subjectKeyIdentifier=hash
    authorityKeyIdentifier=keyid:always,issuer:always
'''

_CA_CERT_CONFIG_FORMAT = '''[ req ]
    distinguished_name     = req_distinguished_name
    x509_extensions        = cert_extensions
    prompt = no

[ req_distinguished_name ]
    C  = {C}
    ST = {ST}
    L  = {L}
    O  = {O}
    OU = {OU}
    CN = {CN}

[ cert_extensions ]
    basicConstraints=critical,CA:TRUE
    keyUsage=critical,keyCertSign,cRLSign
    subjectKeyIdentifier=hash
    authorityKeyIdentifier=keyid:always,issuer:always
'''




def create_key_and_cert(
    key_filename, cert_filename, ca=None, custom_options=None):
    # ca should be a dict with keys "keyfile" & "certfile"

    # make sure output directories exist
    # if directory can't be created, just allow system
    # exceptions to be raised (same will happen later
    # if a file with dirname exist when we try to write)
    for fn in (key_filename, cert_filename):
        dirname = os.path.dirname(fn)
        if not os.path.exists(dirname):
            os.makedirs(dirname)

    cert_options = {}
    cert_options.update(_CERT_OPTIONS)
    if custom_options is not None:
        cert_options.update(custom_options)

    # create the key
    args = [
        "openssl", "genrsa",
        "-out", key_filename,
        str(cert_options["key_size"])
    ]
    subprocess.check_call(args)

    if ca:
        # create a signing request of the new key by ca
        with tempfile.NamedTemporaryFile(mode="w+") as request:

            with tempfile.NamedTemporaryFile(mode="w+") as cert_conf:
                cert_conf.write(_SERVER_CERT_CONFIG_FORMAT.format(**cert_options))
                cert_conf.flush()

                args = [
                    "openssl", "req",
                    "-new",
                    "-key", key_filename,
                    "-out", request.name,
                    "-config", cert_conf.name
                ]
                subprocess.check_call(args)
                
                # sign the request
                os.urandom(20)
                serial = binascii.b2a_hex(os.urandom(20))
                args = [
                    "openssl", "x509",
                    "-req",
                    "-in", request.name,
                    "-CA", ca["certfile"],
                    "-CAkey", ca["keyfile"],
                    "-set_serial",
                        "0x" + binascii.b2a_hex(os.urandom(20)).decode("utf-8"),
                    "-sha256",
                    "-extfile", cert_conf.name,
                    "-extensions", "cert_extensions",
                    "-days", cert_options["days"],
                    "-out", cert_filename
                ]
                cmdline = " ".join(args)
                subprocess.check_call(args)

    else:

        with tempfile.NamedTemporaryFile(mode="w+") as cert_conf:
 
            cert_conf.write(_CA_CERT_CONFIG_FORMAT.format(**cert_options))
            cert_conf.flush()

            # create a self-signed cert
            args = [
                "openssl", "req",
                "-sha256",
                "-new",
                "-x509",
                "-days", cert_options["days"],
                "-key", key_filename,
                "-config", cert_conf.name,
                "-out", cert_filename
            ]
            subprocess.check_call(args)


def create_ssh_key(filename, hostname):

    # make sure output directory exists
    # if directory can't be created, just allow system
    # exception to be raised
    dirname = os.path.dirname(filename)
    if not os.path.exists(dirname):
        os.makedirs(dirname)

    args = [
        "ssh-keygen",
        "-C", "root@" + hostname,
        "-f", filename,
        "-q",
        "-N", ""
    ]
    subprocess.check_call(args)

if __name__ == "__main__":

    HOSTNAME = "10.11.12.99"

    ca = {
        "keyfile": "files/https/ca_root.key",
        "certfile": "files/https/ca_root.crt"
    }

    create_key_and_cert(
        ca["keyfile"],
        ca["certfile"],
        custom_options={"OU": "perfsonar", "CN": "root"})
  
    create_key_and_cert(
        "files/saml/idp.key",
        "files/saml/idp.crt",
        ca=ca,
        custom_options={"OU": "idp", "CN": HOSTNAME})

    create_ssh_key("files/ssh/idp_rsa", "idp")

    create_key_and_cert(
        "files/https/idp.key",
        "files/https/idp.crt",
        ca=ca,
        custom_options={"OU": "idp-https", "CN": HOSTNAME})
