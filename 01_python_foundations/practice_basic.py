# Basic Practice

class InValidAgeError(Exception): 
    pass 

def set_age(age: int) -> None:
    if age < 0:
        raise InValidAgeError(" Age cann't be negative: " + str(age))

print(set_age(10))
try:
    print(set_age(-6))
except InValidAgeError as e:
    print("Caught it:", e)

# Intermediate Version 

class InvalidAgeError(Exception):
    """ Raised when an age value is negative."""
    pass

def set_age(age: int) -> None:
    """ Validate and age. Raises InvalidAgeError if age is negative."""

    if age >= 0:
        return
    raise InvalidAgeError(f" age cannot be negative: {age}")

set_age(25)

try:
    set_age(-5)
except InvalidAgeError as e:
    print(f"Caught it: {e}")

# Advanced Version

class InvalidAgeError(Exception):
    def __init__(self, age: int):
        self.age = age
        super().__init__(f" age cannot be negative: {age}")

def set_age(age: int) -> None:
    if age < 0:
        raise InvalidAgeError(age)

set_age(25)

try:
    set_age(-5)
except InvalidAgeError as e:
    print(f"Caught it: {e}")
    print(f"The bad value was: {e.age}")

# Advanced Version2 

class ValidationError(Exception): pass

class InvalidAgeError(ValidationError):
    def __init__(self, age: int):
        self.age = age
        super().__init__(f" Age cannot be negative: {age}")

def set_age(age: int) -> None:
    if age < 0:
        raise InvalidAgeError(age)

set_age(25)

try:
    set_age(-5)
except ValidationError as e:
    print(f"Validation failed: {e}")

# Advanced Version3

from dataclasses import dataclass, field

class ValidationError(Exception): pass

@dataclass
class InvalidAgeError(ValidationError):
    age: int
    message: str = field(init=False)

    def __post_init__(self) -> None:
        self.message = f"age cannot be negative: {self.age}"
        super().__init__(self.message)

def set_age(age: int) -> None:
    if age < 0:
        raise InvalidAgeError(age)

try:
    set_age(-5)
except InvalidAgeError as e:
    print(f"Caught it: {e.message}")
    print(f"As a dict-like repr: {e!r}")