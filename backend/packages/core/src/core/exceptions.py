class CoreError(Exception):
    pass


class InvalidProblemError(CoreError):
    pass


class ObjectiveCoefficientsCountMismatchError(InvalidProblemError):
    pass


class ConstraintCoefficientsCountMismatchError(InvalidProblemError):
    pass


class DuplicateVariableError(InvalidProblemError):
    pass


class NotSolvableError(CoreError):
    pass
