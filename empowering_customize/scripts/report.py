from ast import literal_eval
from urlparse import urlparse
import sys
import base64
from subprocess import call
import time
import tempfile

from erppeek import Client


url = urlparse(sys.argv[1])
report = sys.argv[2]
ids = literal_eval(sys.argv[3])
context = literal_eval(sys.argv[4])

O = Client(
    '{x.scheme}://{x.hostname}:{x.port}'.format(x=url),
    url.path.lstrip('/'),
    url.username,
    url.password
)

report_id = O.report(report, ids, {}, context)
sys.stdout.write("Waiting")
res = {'state': False}

while not res['state']:
    res = O.report_get(report_id)
    sys.stdout.write(".")
    time.sleep(0.1)
    sys.stdout.flush()

sys.stdout.write("\n")

report_file = tempfile.mktemp(prefix='oo-report-')
with open(report_file, 'w') as f:
    f.write(base64.b64decode(res['result']))
    call(['gnome-open', report_file])
