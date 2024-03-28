from enum import Enum


class RunStatus(Enum):
    COMPLETED = 'completed'
    QUEUED = 'queued'
    IN_PROGRESS = 'in_progress'
    CANCELLING = 'cancelling'
    CANCELLED = 'cancelled'
