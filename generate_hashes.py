from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
hash1 = bcrypt.generate_password_hash('password1').decode('utf-8')  # Change 'password1' to your desired plain password for john_doe
hash2 = bcrypt.generate_password_hash('password2').decode('utf-8')  # For jane_smith
print(hash1)
print(hash2)