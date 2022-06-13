from django.contrib.auth.hashers import (BCryptSHA256PasswordHasher,PBKDF2PasswordHasher, SHA1PasswordHasher,)

class PBKDF2WrappedSHA1PasswordHasher(PBKDF2PasswordHasher):
    algorithm = 'pbkdf2_wrapped_sha1'

    def encode_sha1_hash(self, sha1_hash, salt, iterations=None):
        return super().encode(sha1_hash, salt, iterations)

    def encode(self, password, salt, iterations=None):
        _, _, sha1_hash = SHA1PasswordHasher().encode(password, salt).split('$', 2)
        return self.encode_sha1_hash(sha1_hash, salt, iterations)


class BCryptWrappedSHA256PasswordHasher(BCryptSHA256PasswordHasher):
    algorithm = 'bcrypt_sha256'

    def encode_sha256_hash(self, sha256_hash, salt, iterations=None):
        return super().encode(sha256_hash, salt, iterations)

    def encode(self, password, salt, iterations=None):
        _, _, sha1_hash = SHA1PasswordHasher().encode(password, salt).split('$', 2)
        return self.encode_sha256_hash(sha1_hash, salt, iterations)
