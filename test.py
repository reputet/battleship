from pprint import pprint
from classes import Field, BattleField

point = Field("A", "5")
f = BattleField()
n = Field("A", "1")
foo = f.mapping["G6"]
bar = f.mapping["F1"]

for key, value in f.mapping.items():
	if key not in ("D3", "D4", "D5", "D6", "C4", "E4", "F4"):
		value.involve()

