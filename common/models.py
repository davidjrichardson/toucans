from dataclasses import dataclass


@dataclass
class ThreeLegStanding:
    team_name: str
    leg_1: tuple[int, int, int]
    leg_2: tuple[int, int, int]
    leg_3: tuple[int, int, int]
    champs: tuple[int, int, int]

    @property
    def is_empty(self) -> bool:
        return (
            self.leg_1 == (0, 0, 0) 
            and self.leg_2 == (0, 0, 0) 
            and self.leg_3 == (0, 0, 0) 
            and self.champs == (0, 0, 0)
        )
    
    @property
    def results(self) -> list[tuple[int, int, int]]:
        return [self.leg_1, self.leg_2, self.leg_3, self.champs]
    
    def __str__(self) -> str:
        return f"{self.team_name}: {self.leg_1}, {self.leg_2}, {self.leg_3}, {self.champs}"