import base64
import hashlib
import hmac
import secrets


class PasswordHasher:
    ALGORITHM = "pbkdf2_sha256"
    ITERATIONS = 600_000
    SALT_SIZE = 16

    def hash(self, password: str) -> str:
        salt = secrets.token_bytes(self.SALT_SIZE)
        digest = hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), salt, self.ITERATIONS
        )
        encoded_salt = base64.b64encode(salt).decode("ascii")
        encoded_digest = base64.b64encode(digest).decode("ascii")
        return (
            f"{self.ALGORITHM}${self.ITERATIONS}$"
            f"{encoded_salt}${encoded_digest}"
        )

    def verify(self, password: str, stored_hash: str) -> bool:
        try:
            algorithm, iterations, encoded_salt, encoded_digest = (
                stored_hash.split("$", 3)
            )
            if algorithm != self.ALGORITHM:
                return False

            salt = base64.b64decode(encoded_salt, validate=True)
            expected_digest = base64.b64decode(encoded_digest, validate=True)
            actual_digest = hashlib.pbkdf2_hmac(
                "sha256", password.encode("utf-8"), salt, int(iterations)
            )
        except (TypeError, ValueError):
            return False

        return hmac.compare_digest(actual_digest, expected_digest)
