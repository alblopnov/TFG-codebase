import secrets

# Generar una clave secreta de 32 bytes en formato hexadecimal
secret_key = secrets.token_hex(32)
jwt_secret_key = secrets.token_hex(32)

print("SECRET_KEY =", secret_key)
print("JWT_SECRET_KEY =", jwt_secret_key)
