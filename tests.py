# import the main window object (mw) from aqt
from aqt import mw
# import the "show info" tool from utils.py
from aqt.utils import showInfo, qconnect
# import all of the Qt GUI library
from aqt.qt import *

# We're going to add a menu item below. First we want to create a function to
# be called when the menu item is activated.
def get_progress_of_cards() -> None:
    # for each card in the collection
    for card in mw.col.find_cards(""):
        # get the card's note
        note = card.note()
        # get the card's progress
        progress = card.ivl
        # get the card's interval
        interval = card.ivl
        # get the card's ease
        ease = card.factor
        # get the card's due date
        due = card.due
        # get the card's creation date
        # get the card's lapses
        lapses = card.lapses
        # get the card's time of last review
        last_review = card.mod
        # get the card's time of next review
        nr_of_reps = card.reps
        # get the card's number of lapses
        nr_of_lapses = card.lapses
        print(f"Progress: {progress}, Interval: {interval}, Ease: {ease}, Due: {due}, Last Review: {last_review},  Number of Reviews: {nr_of_reps}, Number of Lapses: {nr_of_lapses}")

# create a new menu item, "test"
action = QAction("test", mw)
# set it to call testFunction when it's clicked
qconnect(action.triggered, get_progress_of_cards)
# and add it to the tools menu
mw.form.menuTools.addAction(action)