from typing import NewType, Dict, List

Goal = NewType('Goal', Dict[str, int])
Goals = NewType('Goals', List[Goal])
