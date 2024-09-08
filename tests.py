# import the main window object (mw) from aqt
from aqt import mw
# import the "show info" tool from utils.py
from aqt.utils import showInfo, qconnect
# import all of the Qt GUI library
from aqt.qt import *

from anki.cards import Card

# We're going to add a menu item below. First we want to create a function to
# be called when the menu item is activated.

def testFunction() -> None:
    col = mw.col
    card_ids = col.db.list("SELECT id FROM cards")

    # Function to check if a card is due
    def is_card_due(card: Card) -> bool:
        # Card is due if it's in the review queue and due <= today
        return card.queue == 2 and card.due <= col.sched.today

    # Iterate over the card IDs and get learning stats
    for card_id in card_ids:
        card = col.get_card(card_id)  # Get the Card object

        due_status = is_card_due(card)
        interval = card.ivl  # Interval (days until next review)
        reps = card.reps  # Number of repetitions
        ease = card.factor / 1000  # Ease factor
        level = card.memory_state

        if due_status:

            print(f"Card ID: {card_id}")
            print(f"Due: {due_status}")
            print(f"Interval: {interval} days")
            print(f"Repetitions: {reps}")
            print(f"Ease: {ease}")
            print(f"Level: {level}")
            print("----------")

# create a new menu item, "test"
action = QAction("test", mw)
# set it to call testFunction when it's clicked
qconnect(action.triggered, testFunction)
# and add it to the tools menu
mw.form.menuTools.addAction(action)
