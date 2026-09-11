class InvalidAgeError(Exception): pass

def set_age(age: int) -> None:
    if age < 0:
        raise InvalidAgeError(" Age cannot be negative" + str(age))
try:
    print(set_age(25))
    print(set_age(-10))
except InvalidAgeError as e:
    print('Caught it: ', e)

### Intermediate Version
