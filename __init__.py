# Import the necessary objects
from aqt import mw
from aqt.utils import qconnect
from aqt.qt import *
from anki.cards import Card
from aqt.stats import DeckStats

from aqt.gui_hooks import stats_dialog_will_show

import os

class TilemapWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Scrollable and Zoomable Tilemap")

        # Central widget and layout
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Create a scrollable area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        # Container for the grid
        self.grid_container = QWidget()
        self.grid_layout = QGridLayout(self.grid_container)

        # Path to the image in the project folder
        image_path = os.path.join(os.path.dirname(__file__), 'assets', 'tree.png')

        # Load the image
        self.tree_pixmap = QPixmap(image_path)

        # Create a 5x5 grid of labels with the image
        self.create_grid(5, 5)

        # Add the grid container to the scroll area
        self.scroll_area.setWidget(self.grid_container)

        # Create a layout for the central widget
        layout = QVBoxLayout(central_widget)

        # Add zoom buttons
        self.zoom_in_button = QPushButton("Zoom In")
        self.zoom_in_button.clicked.connect(self.zoom_in)
        self.zoom_out_button = QPushButton("Zoom Out")
        self.zoom_out_button.clicked.connect(self.zoom_out)

        # Add buttons to the layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.zoom_in_button)
        button_layout.addWidget(self.zoom_out_button)
        layout.addLayout(button_layout)

        # Add the scroll area below the buttons
        layout.addWidget(self.scroll_area)

        # Initialize zoom factor
        self.zoom_factor = 1.0

    def create_grid(self, rows, cols):
        for row in range(rows):
            for col in range(cols):
                label = QLabel()
                label.setPixmap(self.tree_pixmap)
                label.setFixedSize(self.tree_pixmap.size())
                label.setScaledContents(True)
                self.grid_layout.addWidget(label, row, col)

    def zoom_in(self):
        self.zoom_factor += 0.1
        self.apply_zoom()

    def zoom_out(self):
        self.zoom_factor = max(0.1, self.zoom_factor - 0.1)  # Ensure zoom factor doesn't go below 0.1
        self.apply_zoom()

    def apply_zoom(self):
        # Adjust the size of each label based on the zoom factor
        for i in range(self.grid_layout.count()):
            widget = self.grid_layout.itemAt(i).widget()
            if isinstance(widget, QLabel):
                size = self.tree_pixmap.size() * self.zoom_factor
                widget.setFixedSize(size)

def create_tilemap_window():
    window = TilemapWindow()
    window.resize(600, 600)  # Set an initial window size
    window.show()

    # Keep a reference to the window to prevent garbage collection
    mw.tilemap_window = window

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

    create_tilemap_window()


# Add a button to the top of the stats view
def on_stats_will_show(stats: DeckStats) -> None:
    # Create a button and add it to the stats view
    button = QPushButton("Run Test")
    button.clicked.connect(generate_forest)

    # Insert the button into the stats view
    stats.form.verticalLayout.insertWidget(0, button)  # Insert the button at the top (index 0)

# Hook the stats screen to add the button
stats_dialog_will_show.append(on_stats_will_show)
