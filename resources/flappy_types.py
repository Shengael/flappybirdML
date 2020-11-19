from typing import NewType, Tuple, Dict, List

Coordinate = NewType('Coordinate', Tuple[int, int])
States = NewType('State', Dict[Coordinate, str])

Goal = NewType('Goal', Dict[str, int])
Goals = NewType('Goals', List[Goal])
