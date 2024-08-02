# WidgetsCustomizer.py

import toga
from toga.style import Pack

class WidgetsCustomizer:
    @staticmethod
    def customize_widget(widget):
        if isinstance(widget, toga.Button):
            widget.style = Pack(
                background_color='#007bff',  # Blue background color
                color='#ffffff',  # White text color
                font_weight='bold',  # Bold font weight
                padding=10  # Padding of 10
            )
        elif isinstance(widget, toga.TextInput):
            widget.style = Pack(
                background_color='#f8f9fa',  # Light gray background color
                color='#212529',  # Dark text color
                padding=10,  # Padding of 10
            )
        elif isinstance(widget, toga.PasswordInput):
            widget.style = Pack(
                background_color='#f8f9fa',  # Light gray background color
                color='#212529',  # Dark text color
                padding=10,  # Padding of 10
                font_family='monospace'  # Use monospace font for password input
            )
        elif isinstance(widget, toga.Label):
            widget.style = Pack(
                color='#212529',  # Dark text color
                font_weight='bold',  # Bold font weight
                padding=10  # Padding of 10
            )
