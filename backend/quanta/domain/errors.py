"""Framework-independent errors raised by deterministic business rules."""


class DomainError(Exception):
    def __init__(self, detail: str, *, conflict: bool = False):
        super().__init__(detail)
        self.detail = detail
        self.conflict = conflict
