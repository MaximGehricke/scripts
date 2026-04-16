#radialMenu

RADIUS = 110      # Distance of visual buttons from center
BTN_SIZE = 64     # Visual size of the buttons
DEAD_ZONE = 20    # Minimum distance from center to trigger a selection

class InfiniteRadialMenu(QtWidgets.QWidget):
    def __init__(self):
        super(InfiniteRadialMenu, self).__init__(hou.qt.mainWindow(), QtCore.Qt.Window | QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setMouseTracking(True)
        
        # Make the widget large enough to cover common flick distances
        # and ensure it catches mouse events.
        self.setFixedSize(1000, 1000)
        self.center = self.rect().center()
        self.hovered_idx = -1
        
        self.buttons = []
        self._build_buttons()
        
        # Center the whole widget on the cursor
        self.move(QtGui.QCursor.pos() - self.center)

    def _build_buttons(self):
        num_items = len(MENU_ITEMS)
        for i, label in enumerate(MENU_ITEMS):
            btn = QtWidgets.QPushButton(label, self)
            btn.setFixedSize(BTN_SIZE, BTN_SIZE)
            
            # Standard radial placement for visual buttons
            angle = math.radians((i * 360 / num_items) - 90)
            x = self.center.x() + RADIUS * math.cos(angle) - BTN_SIZE / 2
            y = self.center.y() + RADIUS * math.sin(angle) - BTN_SIZE / 2
            
            btn.move(int(x), int(y))
            btn.setStyleSheet(self.get_style(False))
            # Clicking the button directly still works
            btn.clicked.connect(lambda chk=False, l=label: self.execute(l))
            self.buttons.append(btn)

    def get_style(self, hovered):
        bg = "#00aaff" if hovered else "#333"
        border = "#55f" if hovered else "#555"
        return f"""
            QPushButton {{
                background-color: {bg};
                color: white;
                border: 2px solid {border};
                border-radius: {BTN_SIZE // 2}px;
                font-weight: bold;
                font-size: 10px;
            }}
        """

    def get_index_at_pos(self, pos):
        offset = pos - self.center
        dist = math.sqrt(offset.x()**2 + offset.y()**2)
        
        if dist < DEAD_ZONE:
            return -1
        
        # Infinite Hitbox: Calculate angle regardless of distance
        angle = math.degrees(math.atan2(-offset.y(), offset.x()))
        if angle < 0: angle += 360
        
        # Normalize to 0 at top, clockwise
        adjusted_angle = (90 - angle + 360) % 360
        slice_size = 360 / len(MENU_ITEMS)
        
        # Calculate index based on which "pizza slice" the mouse is in
        return int((adjusted_angle + (slice_size / 2)) % 360 // slice_size)

    def mouseMoveEvent(self, event):
        new_idx = self.get_index_at_pos(event.pos())
        if new_idx != self.hovered_idx:
            # Reset old button style
            if self.hovered_idx != -1:
                self.buttons[self.hovered_idx].setStyleSheet(self.get_style(False))
            
            # Apply new hover style
            self.hovered_idx = new_idx
            if self.hovered_idx != -1:
                self.buttons[self.hovered_idx].setStyleSheet(self.get_style(True))

    def mousePressEvent(self, event):
        # Because the hitbox is infinite, any click inside the 1000px widget
        # that isn't in the dead zone will trigger the hovered action.
        if self.hovered_idx != -1:
            self.execute(MENU_ITEMS[self.hovered_idx])
        else:
            self.close()

    def execute(self, label):
        print(f"Executing: {label}")
        self.close()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()

# --- Entry Point ---
if hasattr(hou.session, 'infinite_menu'):
    try: hou.session.infinite_menu.close()
    except: pass

hou.session.infinite_menu = InfiniteRadialMenu()
hou.session.infinite_menu.show()
