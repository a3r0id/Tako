
from json import load
from dateutil import parser

from datetime import datetime, timedelta
def keepRate(kept, total):
    return 100 * ( float(kept) / float(total) )


#print(keepRate(5, 50))    

with open("datasets/totalPulls.json") as f:
    tt = load(f)

now = datetime.now()
pullsBuffer = []
for x, y in zip([i[0] for i in tt], [i[1] for i in tt]):
    then = parser.parse(x)
    if now - timedelta(hours=24) <= then <= now + timedelta(hours=24):
        pullsBuffer.append([x, y])

"""print(len(pullsBuffer))
after = pullsBuffer[:10]
print(len(after))
    """
