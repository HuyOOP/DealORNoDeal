import getpass

password = getpass.getpass("Enter your password: ")

score = 0

if len(password) >= 8:
    score += 1

if any(char.isdigit() for char in password):
    score += 1

if any(char.isupper() for char in password):
    score += 1

if any(char.islower() for char in password):
    score += 1

if any(char in "!@#$%^&*()-_=+[{]}\|;:'\",<.>/?`~" for char in password):
    score += 1

levels = {
    0: "Very Weak",
    1: "Weak",
    2: "Moderate",
    3: "Strong",
    4: "Very Strong",
    5: "Excellent"
}

print(f"Password strength: {levels.get(score, 'Unknown')}")
