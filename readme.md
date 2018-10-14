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
