import jwcrypto.jwk as jwk

RSAkey = jwk.JWK.generate(kty='RSA', size=4096)
private_key = RSAkey.export_private()
public_key = RSAkey.export_public()
jwks = '{"keys":[' + public_key + ']}'

print("\njwks:\n" + jwks)
print("\npublic:\n" + public_key)
print("\nprivate:\n" + private_key)
