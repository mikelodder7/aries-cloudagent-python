"""Validators for schema fields."""

from datetime import datetime

from base58 import alphabet
from marshmallow.exceptions import ValidationError
from marshmallow.validate import OneOf, Range, Regexp

from .util import epoch_to_str

B58 = alphabet if isinstance(alphabet, str) else alphabet.decode("ascii")


class IntEpoch(Range):
    """Validate value against (integer) epoch format."""

    EXAMPLE = int(datetime.now().timestamp())

    def __init__(self):
        """Initializer."""

        super().__init__(
            min=0,
            max=2147483647,
            error="Value {input} is not a valid integer epoch time."
        )


class IndyDID(Regexp):
    """Validate value against indy DID."""

    EXAMPLE = "WgWxqztrNooG92RXvxSTWv"

    def __init__(self):
        """Initializer."""

        super().__init__(
            rf"^[{B58}]{{21,22}}$",
            error="Value {input} is not an indy decentralized identifier (DID)."
        )


class IndyCredDefId(Regexp):
    """Validate value against indy credential definition identifier specification."""

    EXAMPLE = "WgWxqztrNooG92RXvxSTWv:3:CL:20:tag"

    def __init__(self):
        """Initializer."""

        super().__init__(
            (
                rf"([{B58}]{{21,22}})"  # issuer DID
                f":3"  # cred def id marker
                f":CL"  # sig alg
                rf":(([1-9][0-9]*)|([{B58}]{{21,22}}:2:.+:[0-9.]+))"  # schema txn / id
                f"(.+)?$"  # tag
            ),
            error="Value {input} is not an indy credential definition identifier."
        )


class IndyVersion(Regexp):
    """Validate value against indy version specification."""

    EXAMPLE = "1.0"

    def __init__(self):
        """Initializer."""

        super().__init__(
            rf"^[0-9.]+$",
            error="Value {input} is not an indy version (use only digits and '.')."
        )


class IndySchemaId(Regexp):
    """Validate value against indy schema identifier specification."""

    EXAMPLE = "WgWxqztrNooG92RXvxSTWv:2:schema_name:1.0"

    def __init__(self):
        """Initializer."""

        super().__init__(
            rf"^[{B58}]{{21,22}}:2:.+:[0-9.]+$",
            error="Value {input} is not an indy schema identifier."
        )


class IndyPredicate(OneOf):
    """Validate value against indy predicate."""

    EXAMPLE = ">="

    def __init__(self):
        """Initializer."""

        super().__init__(
            choices=["<", "<=", ">=", ">"],
            error="Value {input} must be one of {choices}."
        )


class IndyISO8601DateTime(Regexp):
    """Validate value against ISO 8601 datetime format, indy profile."""

    EXAMPLE = epoch_to_str(int(datetime.now().timestamp()))

    def __init__(self):
        """Initializer."""

        super().__init__(
            r"^(\d{4})-(\d\d)-(\d\d)[T ](\d\d):(\d\d)"
            r"(?:\:(\d\d(?:\.\d{1,6})?))?([+-]\d\d:?\d\d|Z)$",
            error="Value {input} is not a date in valid format."
        )


class Base64(Regexp):
    """Validate base64 value."""

    EXAMPLE = "ey4uLn0="

    def __init__(self):
        """Initializer."""

        super().__init__(
            r"^[a-zA-Z0-9+/]*={0,2}$",
            error="Value is not a valid base64 encoding"
        )

    def __call__(self, value):
        """Validate input value."""

        if value is None or len(value) % 4:
            raise ValidationError(self.error)

        return super().__call__(value)


class SHA256Hash(Regexp):
    """Validate (binhex-encoded) SHA256 value."""

    EXAMPLE = "617a48c7c8afe0521efdc03e5bb0ad9e655893e6b4b51f0e794d70fba132aacb"

    def __init__(self):
        """Initializer."""

        super().__init__(
            r"^[a-fA-F0-9+/]{64}$",
            error="Value is not a valid (binhex-encoded) SHA-256 hash"
        )


# Instances for marshmallow schema specification
INT_EPOCH = {
    "validate": IntEpoch(),
    "example": IntEpoch.EXAMPLE
}
INDY_DID = {
    "validate": IndyDID(),
    "example": IndyDID.EXAMPLE
}
INDY_CRED_DEF_ID = {
    "validate": IndyCredDefId(),
    "example": IndyCredDefId.EXAMPLE
}
INDY_VERSION = {
    "validate": IndyVersion(),
    "example": IndyVersion.EXAMPLE
}
INDY_SCHEMA_ID = {
    "validate": IndySchemaId(),
    "example": IndySchemaId.EXAMPLE
}
INDY_PREDICATE = {
    "validate": IndyPredicate(),
    "example": IndyPredicate.EXAMPLE
}
INDY_ISO8601_DATETIME = {
    "validate": IndyISO8601DateTime(),
    "example": IndyISO8601DateTime.EXAMPLE
}
BASE64 = {
    "validate": Base64(),
    "example": Base64.EXAMPLE
}
SHA256 = {
    "validate": SHA256Hash(),
    "example": SHA256Hash.EXAMPLE
}
