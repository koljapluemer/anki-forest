# Import the necessary objects
from aqt import mw
from aqt.utils import qconnect
from aqt.qt import *
from anki.cards import Card
from aqt.stats import DeckStats

from aqt.gui_hooks import stats_dialog_will_show

# Function to run for the current deck
def generate_forest() -> None:
    print("generating forest")
    col = mw.col  # Get the collection object
    # card_ids = col.find_cards("")

    current_deck_id = mw.col.decks.current()['id']
    print("id:", current_deck_id)
    cards_in_deck = mw.col.find_cards(f"did:{current_deck_id}")

    # Function to check if a card is due
    def is_card_due(_card: Card) -> bool:
        return _card.queue == 2 and _card.due <= col.sched.today

    print(f"collections contains {len(cards_in_deck)} cards")

    # Iterate over the card IDs and get learning stats
    for card_id in cards_in_deck:
        # print("card:", card_id)
        card = col.get_card(card_id)  # Get the Card object

        due_status = is_card_due(card)
        interval = card.ivl  # Interval (days until next review)
        reps = card.reps  # Number of repetitions
        ease = card.factor / 1000  # Ease factor

        if False:
            print(f"Card ID: {card_id}")
            print(f"Due: {due_status}")
            print(f"Interval: {interval} days")
            print(f"Repetitions: {reps}")
            print(f"Ease: {ease}")
            print("----------")


# Add a button to the top of the stats view
def on_stats_will_show(stats: DeckStats) -> None:
    # Create a button and add it to the stats view
    button = QPushButton("Run Test")
    button.clicked.connect(generate_forest)

    # Insert the button into the stats view
    stats.form.verticalLayout.insertWidget(0, button)  # Insert the button at the top (index 0)

# Hook the stats screen to add the button
stats_dialog_will_show.append(on_stats_will_show)
