class Data:
    def __init__(self, ui):
        # Reference to the UI manager to update visuals
        self.ui = ui
        # Private attributes for coins and health
        self._coins = 0
        self._health = 3
        # Initialize the hearts display in the UI
        self.ui.create_hearts(self._health)
        # Track unlocked levels and the current level index
        self.unlocked_level = 0
        self.current_level = 0

    @property
    def coins(self):
        # Getter for coins value
        return self._coins

    @coins.setter
    def coins(self, value):
        # Setter for coins value
        self._coins = value
        # Update the coins display in the UI
        self.ui.show_coins(self.coins)

    @property
    def health(self):
        # Getter for health value
        return self._health

    @health.setter
    def health(self, value):
        # Setter for health value
        self._health = value
        # Update the hearts display in the UI
        self.ui.create_hearts(value)
