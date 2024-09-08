import random
import os
import math
from aqt import mw
from aqt.qt import *
from anki.cards import Card
from aqt.stats import DeckStats
from aqt.gui_hooks import stats_dialog_will_show

class TilemapWindow(QMainWindow):
    def __init__(self, cards):
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

        # Calculate grid size based on the number of cards
        grid_size = self.calculate_grid_size(len(cards))

        # Create a grid of labels, one for each card
        self.create_grid(grid_size, cards)

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

    def calculate_grid_size(self, num_cards):
        """Calculate the grid size for the given number of cards."""
        rows = math.ceil(math.sqrt(num_cards))
        cols = rows if rows * (rows - 1) < num_cards else rows - 1
        return (rows, cols)

    def create_grid(self, grid_size, cards):
        """Create a grid of images based on the card data."""
        rows, cols = grid_size
        card_counter = 0

        for row in range(rows):
            for col in range(cols):
                if card_counter < len(cards):
                    card_data = cards[card_counter]
                    image_path = self.get_image_for_card(card_data)
                    if image_path:
                        label = QLabel()
                        pixmap = QPixmap(image_path)
                        label.setPixmap(pixmap)
                        label.setFixedSize(pixmap.size())
                        label.setScaledContents(True)
                        self.grid_layout.addWidget(label, row, col)
                    card_counter += 1

    def get_image_for_card(self, card_data):
        """Determine the image to display based on the card's interval and due status."""
        card, is_due, ivl = card_data

        if card.reps == 0:
            # Card has not been encountered yet, return an empty tile (e.g., empty.png)
            return None  # Replace with path to an empty tile image if needed

        if is_due:
            # Select a random stump based on the interval
            size = self.get_size_for_interval(ivl, is_stump=True)
            return self.select_random_image('stump', size)
        else:
            # Select a random tree based on the interval
            size = self.get_size_for_interval(ivl, is_stump=False)
            return self.select_random_image('tree', size)

    def get_size_for_interval(self, ivl, is_stump):
        """Map the card's interval to a corresponding tree or stump size."""
        interval_mapping = {
            1: 300,
            3: 350,
            8: 400,
            15: 450,
            30: 500
        }
        stump_sizes = [200, 250, 300, 350, 400]

        # Find the closest matching interval
        size_list = stump_sizes if is_stump else list(interval_mapping.values())
        return min(size_list, key=lambda x: abs(ivl - x))

    def select_random_image(self, tree_type, size):
        """Randomly select a tree or stump image based on size."""
        assets_folder = os.path.join(os.path.dirname(__file__), 'assets')
        file_prefix = f"{tree_type}_{size}_"
        matching_images = [f for f in os.listdir(assets_folder) if f.startswith(file_prefix)]

        if not matching_images:
            return None

        # Randomly select one of the matching images
        selected_image = random.choice(matching_images)
        return os.path.join(assets_folder, selected_image)

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
                size = widget.pixmap().size() * self.zoom_factor
                widget.setFixedSize(size)

def create_tilemap_window(cards):
    window = TilemapWindow(cards)
    window.resize(600, 600)  # Set an initial window size
    window.show()

    # Keep a reference to the window to prevent garbage collection
    mw.tilemap_window = window

# Function to run for the current deck
def generate_forest() -> None:
    print("Generating forest")
    col = mw.col  # Get the collection object
    current_deck_id = mw.col.decks.current()['id']
    print("Deck ID:", current_deck_id)
    cards_in_deck = mw.col.find_cards(f"did:{current_deck_id}")

    print(f"Collection contains {len(cards_in_deck)} cards")

    card_data = []
    for card_id in cards_in_deck:
        card = col.get_card(card_id)  # Get the Card object
        is_due = card.queue == 2 and card.due <= col.sched.today
        card_data.append((card, is_due, card.ivl))

    # Call to create the tilemap window and display one tree per card
    create_tilemap_window(card_data)

# Add a button to the top of the stats view
def on_stats_will_show(stats: DeckStats) -> None:
    # Create a button and add it to the stats view
    button = QPushButton("Generate Forest")
    button.clicked.connect(generate_forest)

    # Insert the button into the stats view
    stats.form.verticalLayout.insertWidget(0, button)  # Insert the button at the top (index 0)

# Hook the stats screen to add the button
stats_dialog_will_show.append(on_stats_will_show)
