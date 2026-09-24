from http_client import (
 compute_bakoff,
#  decide_wait_seconds,
#  is_transient_status,
 request_with_retry,
)
# is_transient_status: worth retrying vs. a real mistake to fix
# for code in (429, 500, 503, 404, 401):
#  print(f"is_transient_status({code}) -> {is_transient_status(code)}")
# compute_backoff_delay: no network, no time.sleep, no mocking needed
delay = compute_bakoff(3)
print(f"compute_backoff_delay(3) -> {delay}")
# decide_wait_seconds: respects Retry-After, falls back to backoff, caps a
# huge value -- same three cases the rate-limit exercise already proved
# told_to_wait = decide_wait_seconds({"Retry-After": "2"}, attempt=0)
# print(f"decide_wait_seconds, server said wait 2s -> {told_to_wait}")
# no_header = decide_wait_seconds({}, attempt=3)
# print(f"decide_wait_seconds, no header, attempt 3 -> {no_header}")
# huge_value = decide_wait_seconds({"Retry-After": "999999999"}, attempt=0)
# print(f"decide_wait_seconds, server said wait 999999999s -> {huge_value}")
# the retry loop itself: one real call, same as the timeout/retry exercise
if __name__ == "__main__":
 result = request_with_retry("GET", "https://api.github.com")
 print(f"request_with_retry(\"GET\", api.github.com) -> {result}")