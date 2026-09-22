class InvalidAgeError(Exception):
    pass

def set_age( age: int ) -> None:
    if age < 0:
        raise InvalidAgeError(f"Age cannot be negative. {age}")

set_age(35)
try:
    print("Invalid age: ", set_age(-5))
except InvalidAgeError as e:
    print(f"Caught it: {e}")

## Version2 

class InvalidAgeError_ad(Exception):
    def __init__(self, age: int) -> None:
        self.age = age
        super().__init__(f"age cannot be negative: {age}")
def set_age_ad(age: int) -> None:
    if age < 0:
        raise InvalidAgeError_ad(age)
set_age_ad(25)
try:
    set_age_ad(-5)
except InvalidAgeError_ad as e:
    print(f"Caught it: {e}")
    print(f"the bad value was: {e.age}")
### Version3
class ValidationError(Exception): pass

class InvalidAgeError_ad2(ValidationError):
    def __init__(self, age: int) -> None:
        self.age = age
        super().__init__(f"age cannot be neagtive. {age}")
def set_age_ad2(age: int) -> None:
    if age < 0:
        raise InvalidAgeError_ad2(age)

try:
    set_age_ad2(-5)
except ValidationError as e:
    print(f"Validation failed. {e}")
#Version4

from dataclasses import dataclass, field

class validationerror_ad2(Exception): pass 

@dataclass
class InvalidAgeError_ad3(ValidationError):
    age: int
    message: str = field(init=False)

    def __post_init__(self) -> None:
        self.message = f"age cannot be negative: {self.age}"
        super().__init__(self.message)
def set_age_ad3(age: int) -> None:

    if age < 0:
        raise InvalidAgeError_ad3(age)

try:
    set_age_ad3(-5)
except InvalidAgeError_ad3 as e:
    print(f"Caught it: {e.message}")
    print(f"As a dict-like repr: {e!r}")

# Failure handling — three different errors, three different reactions

class OutOfStockError(Exception):
    pass
class paymentDeclinedError(Exception):
    pass
class InvalidAddressError(Exception):
    pass

def process_order(problem_type):
    if problem_type == "stock":
        raise OutOfStockError("item is out of stock ")
    if problem_type == "payment":
        raise paymentDeclinedError("payment was declined")
    if problem_type == "address":
        raise InvalidAddressError("shipping address is invalid")

for problem_type in ["stock", "payment", "address"]:
    try:
        process_order(problem_type=problem_type)
    except OutOfStockError as e:
        print("Will retry later, telling the warehouse " + str(e))
    except paymentDeclinedError as e:
        print("Asking for a different payment method: " + str(e))
    except InvalidAddressError as e:
        print("Asking the customer to fix thier address: " + str(e))