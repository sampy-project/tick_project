from .base import BaseTickFourPhases
from .stage_transition import ProportionBasedStageTransition
from .mortality import ProportionBasedTickMortality
from .feeding import FeedingSingleGraph
from sampy.utils.decorators import sampy_class


@sampy_class
class BasicTick(BaseTickFourPhases,
                ProportionBasedStageTransition,
                ProportionBasedTickMortality,
                FeedingSingleGraph):
    """
    First iteration of a tick for SamPy. Provides basic methods for tick population dynamics.
    This class assumes that the tick population and all the hosts share the same graph.

    IMPORTANT: Theoretically, this class provides enough tool to satisfy most modelization needs,
               but using it as it is now may require quite a lot of customization by the user.

    Note on the 31-08-2023: at the present date, there are still functionalities missing.
                            Use this class at your own risks.
    """
    def __init__(self, **kwargs):
        pass