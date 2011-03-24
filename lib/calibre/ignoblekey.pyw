#! /usr/bin/python

# ignoblekey.pyw, version 2

# To run this program install Python 2.6 from <http://www.python.org/download/>
# Save this script file as ignoblekey.pyw and double-click on it to run it.

# Revision history:
#   1 - Initial release
#   2 - Add some missing code
#   2.5 - Updating against 2.5.3.4630

"""
Retrieve B&N DesktopReader EPUB user AES key.
"""

from __future__ import with_statement

__license__ = 'GPL v3'

import sys
import os
import binascii
import glob

import logging
import time
import gettext

import Tkinter
import Tkconstants
import tkMessageBox
import traceback

BN_KEY_KEY = 'uhk00000000'
BN_APPDATA_DIR = r'Barnes & Noble\DesktopReader'
B64_ENCODED = True
KEYLEN = 20

BN_KEY_KEY = 'hk00000000'
KEYLEN = 28
BN_APPDATA_DIR = r'Barnes & Noble\*DesktopReader'
BN_CONFIG_DB_GLOB = 'ClientAPI*.db'
KEYPATH = 'bnepubkey.b64'
B64_ENCODED = False

#BN_KEY_KEY = 'hk00000001'
#KEYLEN = 16

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

class IgnobleError(Exception):
    pass

def retrieve_key(dbpath, outpath):
    # The B&N DesktopReader 'ClientAPI' file is just a sqlite3 DB.  Requiring
    # users to install sqlite3 and bindings seems like overkill for retrieving
    # one value, so we go in hot and dirty.
    with open(dbpath, 'rb') as f:
        data = f.read()
    log.info("Searching for: " + BN_KEY_KEY)
    if BN_KEY_KEY not in data:
        raise IgnobleError('B&N user key not found; unexpected DB format?')
    index = data.rindex(BN_KEY_KEY) + len(BN_KEY_KEY)
    log.info("Found key @ offset: " + str(index))

    if not B64_ENCODED:
        data = data[index:index + KEYLEN]
        keyb64 = data.encode('base64')
    else:
        index = index + 1 # This is the offset from version 2
        data = data[index:index + 2 * KEYLEN]
        for i in xrange(KEYLEN, len(data)):
            try:
                keyb64 = data[:i]
                if len(keyb64.decode('base64')) == KEYLEN:
                    break
            except binascii.Error:
                pass
        else:
            raise IgnobleError('Problem decoding key; unexpected DB format?')

    log.info("Retrieved key: " + keyb64)
    with open(outpath, 'wb') as f:
        f.write(keyb64 + '\n')
        #f.write(data)
    log.info("Key saved to %s" % (outpath))

def find_bnclientdb_path():
    appdata = os.environ['APPDATA']
    confglob = os.path.join(appdata, BN_APPDATA_DIR, BN_CONFIG_DB_GLOB)
    log.info("Searching for config at: " + confglob)
    dbpath = glob.glob(confglob)
    if len(dbpath) == 0:
        raise IgnobleError('Problem locating B&N Reader DB')
    elif len(dbpath) > 1:
        log.error("Matched " + len(dbpath) + " files")
    db = sorted(dbpath)[-1]
    log.info("Found config: " + db)
    return db

def cli_main(argv=sys.argv):
    progname = os.path.basename(argv[0])
    args = argv[1:]
    if len(args) != 2:
        log.error("USAGE: %s CLIENTDB KEYFILE" % (progname,))
        return 1
    inpath, outpath = args
    retrieve_key(inpath, outpath)
    return 0

def gui_main(argv=sys.argv):
    root = Tkinter.Tk()
    viewer = LogView(root)

    handler = LoggerToWindowHandler(viewer)
    fmt='%(asctime)s %(message)s'
    datefmt='%H:%M:%S'
    handler.setFormatter(logging.Formatter(fmt, datefmt))
    logging.getLogger().addHandler(handler)

    try:
        dbpath = find_bnclientdb_path()
        retrieve_key(dbpath, KEYPATH)
    except IgnobleError, e:
        log.error("Error: " + str(e))
    except Exception:
        log.error("Exception: " + traceback.format_exc())
        
    viewer.wait_window(viewer)
    return 0

import ScrolledText
import gettext
_ = gettext.gettext

class LogView(Tkinter.Frame):
    def __init__(self, root):
        Tkinter.Frame.__init__(self, root, border=5)
        self.text = ScrolledText.ScrolledText(root, width=120, height=20)
        self.text.pack(fill=Tkconstants.BOTH, expand=1)

        close = Tkinter.Button(root, text=_('Close'), width=10, command=self.ok, default=Tkinter.ACTIVE)
        close.pack(side=Tkinter.RIGHT)
        root.bind("<Return>", self.ok)
        root.bind("<Escape>", self.ok)

        root.title(_('Log Entries'))
        self.root = root

    def ok(self, event=None):
        self.root.withdraw()
        self.root.update_idletasks()
        self.root.destroy()

    def insert(self, msg):
        self.text.insert(Tkconstants.END, msg + "\n")
        self.text.see(Tkconstants.END)


# adapted from: http://uucode.com/texts/pylongopgui/pyguiapp.html
""" Deliver logger messages to logger window """
# $Id: LoggerToWindow.py,v 1.3 2004/04/06 03:48:14 prof Exp $

class LoggerToWindowHandler(logging.Handler):
    """ Provide a logging handler """

    def __init__(self, win):
        """ Create handler, remember threads connector """
        logging.Handler.__init__(self)
        self.win = win

    def emit(self, record):
        """ Process a log message """
        self.win.insert(self.format(record))

if __name__ == '__main__':
    if len(sys.argv) > 1:
        sys.exit(cli_main())
    sys.exit(gui_main())
