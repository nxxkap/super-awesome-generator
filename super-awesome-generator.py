import hmac
import secrets

SECRET_KEY = b"this code is clean as fuck"

WORD = "fuckin"
CHARS = "0123456789abcdefghijklmnopqrstuvwxyz"
RANDOM_LEN = 3
CHECK_LEN = 3


def is_mixed(code):
    return any(c.isdigit() for c in code) and any(c.isalpha() for c in code)


def _check_part(random_part):
    message = f"{WORD}:{random_part}".encode()
    n = int.from_bytes(hmac.digest(SECRET_KEY, message, "sha256"), "big")
    check = ""
    for _ in range(CHECK_LEN):
        n, r = divmod(n, len(CHARS))
        check += CHARS[r]
    return check


def encode():
    while True:
        random_part = "".join(secrets.choice(CHARS) for _ in range(RANDOM_LEN))
        code = random_part + _check_part(random_part)
        if is_mixed(code):
            return code


def decode(code):
    code = code.strip().lower()
    if len(code) != RANDOM_LEN + CHECK_LEN or not set(code) <= set(CHARS) or not is_mixed(code):
        return None
    random_part, check = code[:RANDOM_LEN], code[RANDOM_LEN:]
    return WORD if hmac.compare_digest(check, _check_part(random_part)) else None


if __name__ == "__main__":
    print("REAL")
    for _ in range(5):
        code = encode()
        print(f"  {WORD} → {code} → {decode(code)}")

    print("FAKE")
    for fake in ["a1b2c3", "x9y8z7", "7k3m2p"]:
        print(f"  {fake} → {decode(fake) or 'fake'}")
