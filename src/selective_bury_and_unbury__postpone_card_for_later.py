# -*- coding: utf-8 -*-

"""
Copyright/author: ijgnd
                  Ankitects Pty Ltd and contributors

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""


from anki.hooks import addHook
from anki.lang import _
from aqt.reviewer import Reviewer
from aqt.utils import tooltip
from aqt import mw
from aqt.qt import *


def load_config(conf):
    global config
    config=conf
load_config(mw.addonManager.getConfig(__name__))
mw.addonManager.setConfigUpdatedAction(__name__,load_config) 


def bury_and_mark_for_limited_unburying():
    if hasattr(mw.reviewer,"later_ids"):
        mw.reviewer.later_ids.append(mw.reviewer.card.id)
    else:
        mw.reviewer.later_ids = [mw.reviewer.card.id,]
    #the rest is the contents of reviewer.py - onBuryCard(self):
    mw.checkpoint(_("Bury"))
    mw.col.sched.buryCards([mw.reviewer.card.id])
    mw.reset()
    tooltip(_("later not now."))


def addShortcuts21(shortcuts):
    shortcuts.append((config['later_shortcut'], bury_and_mark_for_limited_unburying))
addHook("reviewStateShortcuts", addShortcuts21)




def limited_unbury():
    """
    Anki has only a function to unbury all buried cards. This should be a quick
    and verifiable add-on. Dealing with the database directly would be more
    complicated. Workaround: get a list of all buried cards, unbury all, rebury
    those that are not in my list later_ids. This has been tested with about 50
    buried cards and I didn't notice any delays. This add-on is not tested in
    extreme situations like thousands of buried cards (that you might have if
    you use sibling burying and add 100 notes of a note type that has 50
    cards...)
    """
    allburied = [int(x) for x in mw.col.findCards("is:buried")]
    to_rebury = []
    for i in allburied:
        if not i in mw.reviewer.later_ids:
            to_rebury.append(i)
    del mw.reviewer.later_ids
    mw.col.sched.unburyCards()
    mw.col.sched.buryCards(to_rebury)
    mw.reset()
    tooltip('Unburied the cards that were set as "later not now".')


def try_limited_unbury():
    if hasattr(mw.reviewer,"later_ids"):
        limited_unbury()
    else:
        tooltip('No cards have been postponed so far that could be unburied.')

action = QAction(mw)
action.setText("limited unbury")
action.setShortcut(QKeySequence(config["limited_unbury_shortcut"]))
mw.form.menuTools.addAction(action)
action.triggered.connect(try_limited_unbury)
