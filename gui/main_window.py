
import tkinter as tk
from tkinter import messagebox


class MainWindow:
    """Main graphical interface for Matwana."""

    def __init__(self, player, database, player_id):
        self.player = player
        self.database = database
        self.player_id = player_id

        self.root = tk.Tk()

        self.root.title("Matwana")
        self.root.geometry("1000x650")
        self.root.minsize(900, 600)

        self.setup_window()
        self.create_header()
        self.create_dashboard()
        self.create_menu()

    # ==========================================
    # WINDOW SETUP
    # ==========================================

    def setup_window(self):
        """Configure the main application window."""

        self.root.configure(
            bg="#111827"
        )

    # ==========================================
    # HEADER
    # ==========================================

    def create_header(self):
        """Create the application header."""

        header = tk.Frame(
            self.root,
            bg="#1f2937",
            height=80
        )

        header.pack(
            fill="x"
        )

        header.pack_propagate(False)

        title = tk.Label(
            header,
            text="MATWANA",
            font=("Arial", 26, "bold"),
            fg="#facc15",
            bg="#1f2937"
        )

        title.pack(
            side="left",
            padx=30
        )

        subtitle = tk.Label(
            header,
            text="Matatu Driver Simulator",
            font=("Arial", 11),
            fg="#d1d5db",
            bg="#1f2937"
        )

        subtitle.pack(
            side="left",
            padx=5
        )

    # ==========================================
    # DASHBOARD
    # ==========================================

    def create_dashboard(self):
        """Create the player dashboard."""

        dashboard = tk.Frame(
            self.root,
            bg="#111827"
        )

        dashboard.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=25
        )

        welcome = tk.Label(
            dashboard,
            text=f"Welcome, {self.player.name}",
            font=("Arial", 22, "bold"),
            fg="white",
            bg="#111827"
        )

        welcome.pack(
            anchor="w",
            pady=(0, 20)
        )

        stats_frame = tk.Frame(
            dashboard,
            bg="#111827"
        )

        stats_frame.pack(
            fill="x"
        )

        self.create_stat_card(
            stats_frame,
            "LEVEL",
            str(self.player.level),
            0
        )

        self.create_stat_card(
            stats_frame,
            "MONEY",
            f"KSh {self.player.money:,}",
            1
        )

        self.create_stat_card(
            stats_frame,
            "REPUTATION",
            str(self.player.reputation),
            2
        )

        xp_current, xp_required = (
            self.player.get_xp_progress()
        )

        self.create_stat_card(
            stats_frame,
            "EXPERIENCE",
            f"{xp_current}/{xp_required}",
            3
        )

    def create_stat_card(
        self,
        parent,
        title,
        value,
        column
    ):
        """Create a single dashboard statistic card."""

        card = tk.Frame(
            parent,
            bg="#1f2937",
            padx=20,
            pady=18
        )

        card.grid(
            row=0,
            column=column,
            padx=8,
            sticky="nsew"
        )

        parent.grid_columnconfigure(
            column,
            weight=1
        )

        title_label = tk.Label(
            card,
            text=title,
            font=("Arial", 10, "bold"),
            fg="#9ca3af",
            bg="#1f2937"
        )

        title_label.pack(
            anchor="w"
        )

        value_label = tk.Label(
            card,
            text=value,
            font=("Arial", 20, "bold"),
            fg="#facc15",
            bg="#1f2937"
        )

        value_label.pack(
            anchor="w",
            pady=(8, 0)
        )

    # ==========================================
    # MENU
    # ==========================================

    def create_menu(self):
        """Create the main game menu."""

        menu_frame = tk.Frame(
            self.root,
            bg="#111827"
        )

        menu_frame.pack(
            fill="x",
            padx=30,
            pady=(0, 30)
        )

        buttons = [
            ("START TRIP", self.start_trip),
            ("MY MATATUS", self.open_matatus),
            ("ACHIEVEMENTS", self.open_achievements),
            ("TRIP HISTORY", self.open_history),
            ("EXIT", self.exit_game)
        ]

        for text, command in buttons:
            button = tk.Button(
                menu_frame,
                text=text,
                command=command,
                font=("Arial", 11, "bold"),
                fg="white",
                bg="#374151",
                activebackground="#4b5563",
                activeforeground="white",
                relief="flat",
                padx=20,
                pady=12,
                cursor="hand2"
            )

            button.pack(
                fill="x",
                pady=5
            )

    # ==========================================
    # MENU ACTIONS
    # ==========================================

    def start_trip(self):
        """Open the trip screen."""

        messagebox.showinfo(
            "Start Trip",
            "Trip interface coming next!"
        )

    def open_matatus(self):
        """Open the matatu management screen."""

        messagebox.showinfo(
            "My Matatus",
            "Matatu management coming next!"
        )

    def open_achievements(self):
        """Open the achievements screen."""

        messagebox.showinfo(
            "Achievements",
            "Achievements interface coming next!"
        )

    def open_history(self):
        """Open the trip history screen."""

        messagebox.showinfo(
            "Trip History",
            "Trip history interface coming next!"
        )

    def exit_game(self):
        """Close the application."""

        self.root.destroy()

    # ==========================================
    # RUN
    # ==========================================

    def run(self):
        """Start the GUI event loop."""

        self.root.mainloop()
