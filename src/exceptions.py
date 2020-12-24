class MaxUniqueNameAttempts(Exception):
    def __init__(self, attempts, *args) -> None:
        super().__init__(f"Exceeded {attempts} attempts to find a unique name", *args)
