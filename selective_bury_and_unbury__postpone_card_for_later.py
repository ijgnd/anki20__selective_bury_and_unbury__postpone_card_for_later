# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# License AGPLv3 


"""
this add-on adds two options to Anki:

- a shortcut (configurable) during reviews: This shortcut triggers a combined
action: The current card is buried and the ID of the card is saved in a
temporary list (that's discarded when you close Anki). 
- a shortcut (configurable) that you can trigger during reviews or from the deck
overview which in effect unburies cards that are in the temporary list. 

An add-on with a similar idea named "later not now"
(https://github.com/omega3/anki-musthave-addons-by-ankitest/blob/master/_Later_not_now_button.py)
exists. But this add-on only calls reviewer.nextCard(). The card might come back
real quick.

Burying + Unburying is a simple solution. The internals of the anki scheduler
are quite complicated and I'm afraid that modifying the cards queues might lead
to (rare) errors. An add-on can't influence the scheduling on mobile anyway. So
the simple bury/unbury solution should only have the drawbacks that it doesn't
survive a restart of Anki (not relevant for me) and that it requires a shortcut
to unbury ...
"""


############## USER CONFIGURATION START ##############
later_shortcut = "z"
limited_unbury_shortcut = "Alt+z"
##############  USER CONFIGURATION END  ##############



from aqt.reviewer import Reviewer
from aqt.utils import tooltip
from aqt import mw
from aqt.qt import *





def bury_and_mark_for_limited_unburying(self):
    try:
        if self.later_ids:
            self.later_ids.append(self.card.id)
    except:
        self.later_ids = [self.card.id,]
    #the rest is the contents of reviewer.py - onBuryCard(self):
    self.mw.checkpoint(_("Bury"))
    self.mw.col.sched.buryCards([self.card.id])
    self.mw.reset()
    tooltip(_("later not now."))
Reviewer.bury_and_mark_for_limited_unburying = bury_and_mark_for_limited_unburying


# replace _keyHandler in reviewer.py to add a keybinding
def newKeyHandler(self, evt):
    key = unicode(evt.text())
    if key == later_shortcut:
        self.bury_and_mark_for_limited_unburying()
    else:
        origKeyHandler(self, evt)
origKeyHandler = Reviewer._keyHandler
Reviewer._keyHandler = newKeyHandler








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
    mw.reviewer.later_ids = []
    mw.col.sched.unburyCards()
    mw.col.sched.buryCards(to_rebury)
    tooltip('unburied the cards that were set as "later not now"')
Reviewer.limited_unbury = limited_unbury


def try_limited_unbury():
    try:
        if mw.reviewer.later_ids:
            limited_unbury()
    except:
        pass


action = QAction(mw)
action.setText("limited unbury")
action.setShortcut(QKeySequence(limited_unbury_shortcut))
mw.form.menuTools.addAction(action)
action.triggered.connect(try_limited_unbury)
