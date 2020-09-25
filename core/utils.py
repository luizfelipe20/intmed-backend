from django.contrib.auth.hashers import PBKDF2PasswordHasher

def crypt_code(password):
    generate_password = PBKDF2PasswordHasher()
    passw = generate_password.encode(password, 'seasalt2')
    return passw
