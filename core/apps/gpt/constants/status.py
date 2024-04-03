from enum import Enum


class RunStatus(Enum):
    QUEUED = 'queued'
    IN_PROGRESS = 'in_progress'
    REQUIRES_ACTION = 'requires_action'
    CANCELLING = 'cancelling'
    CANCELLED = 'cancelled'
    FAILED = 'failed'
    COMPLETED = 'completed'
    EXPIRED = 'expired'

