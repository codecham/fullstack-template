from app.core.security import hash_password, verify_password

PASSWORD = "correct horse battery staple"


def test_hash_is_not_the_password() -> None:
    hashed = hash_password(PASSWORD)

    assert hashed != PASSWORD
    assert hashed.startswith("$argon2")


def test_same_password_gives_different_hashes() -> None:
    first = hash_password(PASSWORD)
    second = hash_password(PASSWORD)

    # A random salt is added each time, so the hashes never match
    assert first != second


def test_verify_accepts_the_right_password() -> None:
    hashed = hash_password(PASSWORD)

    assert verify_password(PASSWORD, hashed)


def test_verify_rejects_a_wrong_password() -> None:
    hashed = hash_password(PASSWORD)

    assert not verify_password("wrong password", hashed)
