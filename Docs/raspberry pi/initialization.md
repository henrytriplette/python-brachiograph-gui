sudo pigpiod
cd Brachiograph
source venv/bin/activate
python3
from brachiograph import BrachioGraph
bg = BrachioGraph(inner_arm=8, outer_arm=8)

-12 -2
2 12

bg = BrachioGraph(inner_arm=8, outer_arm=8, bounds=(-8, 12, 4, 2))


-8, 12, 4, 2