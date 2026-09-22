import os 

env_vars = {}
for line in open(".env"):
    line = line.strip()
    if not line or "=" not in line: continue
    key, value = line.split("=")
    env_vars[key] = value
print(env_vars)

# Edge cases (empty vs. missing) — Solution
import os 
class MissingConfigerror(Exception):
    pass

def require_env(key: str) -> str:
    value = os.getenv("OPENAI_API_KEY")
    if value is None or value == "":
        raise MissingConfigerror("Required environment variable is missing.")
    return value

#Case 1

os.environ.pop("OPENAI_API_KEY", None)

try:
    require_env("OPENAI_API_KEY")
except MissingConfigerror as e:
    print("None Caught it: ", e)

#Case 2

os.environ.pop("OPENAI_API_KEY", "")

try:
    require_env("OPENAI_API_KEY")
except MissingConfigerror as e:
    print("Empty Caught it: ", e)