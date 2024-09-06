import os
from cryptography import x509
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend
import datetime
from cryptography.x509 import ReasonFlags
import yaml
from path import Path

# Define the directory containing the certificates to revoke
cert_extensions = {"pem", "crt", "cer", "ca"}
reasons = {
    "affiliation_changed": ReasonFlags.affiliation_changed,
    "ca_compromise": ReasonFlags.ca_compromise,
    "certificate_hold": ReasonFlags.certificate_hold,
    "cessation_of_operation": ReasonFlags.cessation_of_operation,
    "key_compromise": ReasonFlags.key_compromise,
    "privilege_withdrawn": ReasonFlags.privilege_withdrawn,
    "superseded": ReasonFlags.superseded,
}


def now(delta: int = 0) -> datetime.datetime:
    return datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=delta)


def get_serial(path: str) -> int:
    if path.endswith("txt"):
        with open(path, "r", encoding="utf-8") as f:
            serial = f.readline().strip()
            try:
                serial = int(serial)
            except ValueError:
                serial = int(serial, 16)
            return serial
    else:
        with open(path, "rb") as cert_file:
            serial = x509.load_pem_x509_certificate(
                cert_file.read(), backend=default_backend()
            ).serial_number
        return serial


def invoke(cert_directory: str | Path) -> bytes:
    # generate single CRL with given directory
    if isinstance(cert_directory, str):
        cert_directory = Path(cert_directory)

    if (cert_directory + "as_is.crl").is_file():
        return (cert_directory + "as_is.crl").read_binary()

    config = yaml.safe_load((cert_directory + "config.yml").read())
    issuer_private_key = serialization.load_pem_private_key(
        (cert_directory + config["ca"]["key"]).read_binary(), password=None
    )

    issuer_certificate = x509.load_pem_x509_certificate(
        (cert_directory + config["ca"]["cert"]).read_binary()
    )

    # Create a CRL
    builder = x509.CertificateRevocationListBuilder()
    builder = builder.issuer_name(issuer_certificate.subject)
    builder = builder.last_update(now())
    builder = builder.next_update(now(delta=config["ttl"]))
    builder = builder.add_extension(
        x509.CRLNumber(int(now().timestamp())), critical=False
    )
    # Iterate over all certificate files in the directory
    for reason in cert_directory.list():  # data/example/*
        if reason.name() not in reasons:
            continue

        for filename in filter(
            lambda i: not i.name().startswith("example"),
            (cert_directory + reason).list(),
        ):  # data/example/*/*
            revoked_cert = (
                x509.RevokedCertificateBuilder()
                .serial_number(get_serial(str(filename)))
                .revocation_date(now())
                .add_extension(
                    x509.CRLReason(reasons.get(reason.name(), ReasonFlags.unspecified)),
                    critical=False,
                )
                .build()
            )

            builder = builder.add_revoked_certificate(revoked_cert)

    crl = builder.sign(private_key=issuer_private_key, algorithm=hashes.SHA256())  # type: ignore

    return crl.public_bytes(serialization.Encoding.DER)
