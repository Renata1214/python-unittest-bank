import pytest
from bank_account.bank_account import BankAccount

# --- Fixtures ---
@pytest.fixture
def start_account():
    return BankAccount(100)

@pytest.fixture
def target_account():
    return BankAccount(50)

# --- __init__ ---
def test_init_default_zero():
    acc = BankAccount()
    assert acc.balance == 0

def test_init_negative_balance():
    with pytest.raises(ValueError, match="Initial balance cannot be negative"):
        BankAccount(-10)

# --- deposit ---
def test_deposit_positive(start_account):
    start_account.deposit(50)
    assert start_account.balance == 150

@pytest.mark.parametrize("amount", [0, -20])
def test_deposit_invalid_amounts(start_account, amount):
    with pytest.raises(ValueError, match="Deposit amount must be positive"):
        start_account.deposit(amount)
    assert start_account.balance == 100  # unchanged

# --- withdraw ---
def test_withdraw_success(start_account):
    start_account.withdraw(40)
    assert start_account.balance == 60

@pytest.mark.parametrize("amount", [0, -5])
def test_withdraw_invalid_amounts(start_account, amount):
    with pytest.raises(ValueError, match="Withdraw amount must be positive"):
        start_account.withdraw(amount)
    assert start_account.balance == 100

def test_withdraw_insufficient_funds(start_account):
    with pytest.raises(ValueError, match="Insufficient funds"):
        start_account.withdraw(200)
    assert start_account.balance == 100

# --- transfer_to ---
def test_transfer_success(start_account, target_account):
    start_account.transfer_to(target_account, 30)
    assert start_account.balance == 70
    assert target_account.balance == 80

def test_transfer_invalid_target(start_account):
    with pytest.raises(ValueError, match="Target must be a BankAccount"):
        start_account.transfer_to("not-an-account", 10)
    assert start_account.balance == 100

def test_transfer_insufficient_funds(start_account, target_account):
    with pytest.raises(ValueError, match="Insufficient funds"):
        start_account.transfer_to(target_account, 500)
    assert start_account.balance == 100
    assert target_account.balance == 50

