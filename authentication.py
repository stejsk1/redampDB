import time


def authenticate_user(max_attempts=5, cooldown_time=60):
    username = "postgres"
    password = "redamp"
    attempts = 0

    while True:
        input_username = input("Enter your username: ")
        input_password = input("Enter your password: ")

        if input_username == username and input_password == password:
            print("Authentication successful!")
            return True

        attempts += 1

        if attempts >= max_attempts:
            last_attempt_time = time.time()
            cooldown_period = time.time() - last_attempt_time

            if cooldown_period < cooldown_time:
                print(
                    "Too many failed attempts. Please wait for",
                    round(cooldown_time - cooldown_period),
                    "seconds before trying again.",
                )
                time.sleep(cooldown_time - cooldown_period)

            attempts = 0
            last_attempt_time = time.time()

        else:
            print("Authentication failed. Please try again.")
