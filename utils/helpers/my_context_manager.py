class TestStep:
    def __init__(self, step_name):
        self.step_name = step_name

    def __enter__(self):
        print(f"[START STEP] : {self.step_name}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # ERROR SCENARIO
        # Code executed AFTER leaving block or when error was encountered.
        # exc_type holds the value of the error when it occurs, if no error is None.

        if exc_type:
            print(f"[FAILED]: {self.step_name}")
            # important: we don't return True. No return (otherwise return None)
            # means that Python will proceed with the execution

        else:
            print(f"[SUCCESS] : {self.step_name}")


if __name__ == "__main__":
    print("--- Scenario 1: Success ---")
    with TestStep("Logging into the system"):
        print("  -> Entering login credentials...")
        print("  -> Clicking enter...")

    print("\n--- Scenario 2: Error ---")
    try:
        with TestStep("Credit card payment"):
            print("  -> Entering card number...")
            raise ValueError("Insufficient funds!")
    except ValueError:
        print("-> Error caught in the main test block (as expected).")
