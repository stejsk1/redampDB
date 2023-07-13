import time


class Authenticator:
    def __init__(
        self, username="postgres", password="redamp", max_attempts=5, cooldown_time=60
    ):
        self.username = username
        self.password = password
        self.max_attempts = max_attempts
        self.cooldown_time = cooldown_time

    def authenticate(self):
        attempts = 0

        while True:
            input_username = input("Enter your username: ")
            input_password = input("Enter your password: ")

            if input_username == self.username and input_password == self.password:
                print("Authentication successful!")
                return True

            attempts += 1

            if attempts >= self.max_attempts:
                last_attempt_time = time.time()
                cooldown_period = time.time() - last_attempt_time

                if cooldown_period < self.cooldown_time:
                    print(
                        "Too many failed attempts. Please wait for",
                        round(self.cooldown_time - cooldown_period),
                        "seconds before trying again.",
                    )
                    time.sleep(self.cooldown_time - cooldown_period)
                attempts = 0
                last_attempt_time = time.time()
            else:
                print("Authentication failed. Please try again.")
