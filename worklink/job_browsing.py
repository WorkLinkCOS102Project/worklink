"""
job_browsing.py  –  Employee-side dashboard (Browse Jobs + My Applications).

Ported from job_browsing.ipynb.  All data access goes through data_manager;
no CSV or file I/O here.
"""

from __future__ import annotations
import tkinter as tk
from tkinter import messagebox, ttk

from worklink.styles import (
    BACKGROUND_COLOR, CARD_COLOR, TEXT_COLOR, PRIMARY_COLOR,
    MUTED_TEXT, BORDER_COLOR, SUCCESS_COLOR,
    FONT_SUBTITLE, FONT_BODY, FONT_SMALL, FONT_BUTTON, FONT_LABEL,
    BTN_PRIMARY,
    SP_XS, SP_SM, SP_MD, SP_LG, SP_XL, SP_2XL, SP_3XL,
)
from worklink.data_manager import get_jobs, save_application, get_applications


# ---------------------------------------------------------------------------
# Shared scrollable-frame helper
# ---------------------------------------------------------------------------

def _make_scrollable_frame(parent: tk.Widget) -> tuple[tk.Canvas, tk.Frame]:
    """Return (canvas, inner_frame) with a vertical scrollbar already packed."""
    canvas = tk.Canvas(parent, bg=BACKGROUND_COLOR, highlightthickness=0)
    scrollbar = tk.Scrollbar(parent, orient="vertical", command=canvas.yview)
    inner = tk.Frame(canvas, bg=BACKGROUND_COLOR)

    inner.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all")),
    )
    canvas.create_window((0, 0), window=inner, anchor="nw", width=720)
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    return canvas, inner


# ---------------------------------------------------------------------------
# EmployeeDashboard
# ---------------------------------------------------------------------------

class EmployeeDashboard(tk.Frame):
    """
    Full job-seeker interface with two tabs:
        • Browse Jobs
        • My Applications
    """

    def __init__(self, master: tk.Widget, current_user: dict) -> None:
        super().__init__(master, bg=BACKGROUND_COLOR)
        self.master = master
        self.current_user = current_user
        self._build_ui()

    # ------------------------------------------------------------------
    # Layout
    # ------------------------------------------------------------------

    def _build_ui(self) -> None:
        # Top greeting bar
        header_bar = tk.Frame(self, bg=CARD_COLOR, pady=SP_MD)
        header_bar.pack(fill="x")

        tk.Label(
            header_bar,
            text=f"Hi, {self.current_user['name']}  👋",
            font=FONT_SUBTITLE,
            bg=CARD_COLOR,
            fg=TEXT_COLOR,
        ).pack(side="left", padx=SP_XL)

        tk.Label(
            header_bar,
            text="Find your next opportunity",
            font=FONT_BODY,
            bg=CARD_COLOR,
            fg=MUTED_TEXT,
        ).pack(side="left")

        # Tabs
        style = ttk.Style()
        style.configure("TNotebook", background=BACKGROUND_COLOR, borderwidth=0)
        style.configure("TNotebook.Tab", font=FONT_BUTTON, padding=[SP_LG, SP_SM])

        self.tabs = ttk.Notebook(self)
        self.tabs.pack(fill="both", expand=True, padx=SP_LG, pady=SP_MD)

        self.explore_tab = tk.Frame(self.tabs, bg=BACKGROUND_COLOR)
        self.tabs.add(self.explore_tab, text="  Browse Jobs  ")
        self._build_explore_tab()

        self.history_tab = tk.Frame(self.tabs, bg=BACKGROUND_COLOR)
        self.tabs.add(self.history_tab, text="  My Applications  ")
        self._build_history_tab()

    # ------------------------------------------------------------------
    # Tab 1 — Browse Jobs
    # ------------------------------------------------------------------

    def _build_explore_tab(self) -> None:
        self.explore_canvas, self.scroll_frame = _make_scrollable_frame(self.explore_tab)
        self._refresh_job_listings()

    def _refresh_job_listings(self) -> None:
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        all_jobs   = get_jobs()
        my_apps    = get_applications(self.current_user["id"])
        applied_ids = {str(app["job_id"]) for app in my_apps}

        if not all_jobs:
            tk.Label(
                self.scroll_frame,
                text="No jobs available right now.\nCheck back soon!",
                font=FONT_SUBTITLE,
                bg=BACKGROUND_COLOR,
                fg=MUTED_TEXT,
                justify="center",
            ).pack(pady=SP_3XL)
            return

        for job in all_jobs:
            self._render_job_card(job, applied_ids)

    def _render_job_card(self, job: dict, applied_ids: set) -> None:
        """
        Render a single job card.
        Visual hierarchy: Title → metadata → description preview → action
        """
        j_id = str(job["id"])
        already_applied = j_id in applied_ids

        card = tk.Frame(
            self.scroll_frame,
            bg=CARD_COLOR,
            relief="flat",
            bd=0,
            highlightthickness=1,
            highlightbackground=BORDER_COLOR,
        )
        card.pack(fill="x", padx=SP_LG, pady=SP_SM)

        inner = tk.Frame(card, bg=CARD_COLOR)
        inner.pack(fill="x", padx=SP_XL, pady=SP_MD)

        # Row 1: title
        tk.Label(
            inner,
            text=job["title"],
            font=FONT_SUBTITLE,
            bg=CARD_COLOR,
            fg=PRIMARY_COLOR,
            anchor="w",
        ).pack(fill="x")

        # Row 2: metadata
        meta_row = tk.Frame(inner, bg=CARD_COLOR)
        meta_row.pack(fill="x", pady=(SP_XS, SP_SM))
        tk.Label(meta_row, text=f"🎯  {job['skills']}",    font=FONT_SMALL, bg=CARD_COLOR, fg=MUTED_TEXT).pack(side="left")
        tk.Label(meta_row, text="  ·  ",                    font=FONT_SMALL, bg=CARD_COLOR, fg=MUTED_TEXT).pack(side="left")
        tk.Label(meta_row, text=f"📊  {job['experience']}", font=FONT_SMALL, bg=CARD_COLOR, fg=MUTED_TEXT).pack(side="left")

        # Row 3: description preview
        desc    = job["description"]
        preview = desc[:140] + "..." if len(desc) > 140 else desc
        tk.Label(
            inner,
            text=preview,
            font=FONT_BODY,
            bg=CARD_COLOR,
            fg=TEXT_COLOR,
            wraplength=560,
            justify="left",
            anchor="w",
        ).pack(fill="x", pady=(0, SP_MD))

        # Row 4: action
        action_row = tk.Frame(inner, bg=CARD_COLOR)
        action_row.pack(fill="x")

        if already_applied:
            tk.Label(
                action_row,
                text="✓  Applied",
                font=FONT_BUTTON,
                bg=CARD_COLOR,
                fg=SUCCESS_COLOR,
            ).pack(side="right")
        else:
            tk.Button(
                action_row,
                text="Apply Now",
                **BTN_PRIMARY,
                command=lambda jid=j_id: self._submit_application(jid),
            ).pack(side="right")

    def _submit_application(self, job_id: str) -> None:
        status = save_application(job_id, self.current_user["id"])

        if status == "LOCKED":
            messagebox.showerror(
                "Something went wrong",
                "We could not submit your application right now. Please try again.",
            )
        elif status:
            messagebox.showinfo("Application Sent!", "Your application has been submitted. Good luck!")
            self._refresh_job_listings()
            self._refresh_history_tab()
        else:
            messagebox.showwarning("Already Applied", "You have already applied for this role.")

    # ------------------------------------------------------------------
    # Tab 2 — My Applications
    # ------------------------------------------------------------------

    def _build_history_tab(self) -> None:
        self.history_container = tk.Frame(self.history_tab, bg=BACKGROUND_COLOR)
        self.history_container.pack(fill="both", expand=True, padx=SP_LG, pady=SP_LG)
        self._refresh_history_tab()

    def _refresh_history_tab(self) -> None:
        for widget in self.history_container.winfo_children():
            widget.destroy()

        my_apps = get_applications(self.current_user["id"])

        if not my_apps:
            tk.Label(
                self.history_container,
                text="You haven't applied to any jobs yet.\nBrowse available roles in the Browse Jobs tab!",
                font=FONT_SUBTITLE,
                bg=BACKGROUND_COLOR,
                fg=MUTED_TEXT,
                justify="center",
            ).pack(pady=SP_3XL)
            return

        tk.Label(
            self.history_container,
            text=f"You have applied to {len(my_apps)} role(s)",
            font=FONT_BODY,
            bg=BACKGROUND_COLOR,
            fg=MUTED_TEXT,
        ).pack(anchor="w", pady=(0, SP_SM))

        # Treeview table — data now comes pre-joined from the DB query
        style = ttk.Style()
        style.configure(
            "Applications.Treeview",
            background=CARD_COLOR,
            foreground=TEXT_COLOR,
            rowheight=28,
            fieldbackground=CARD_COLOR,
            font=FONT_BODY,
        )
        style.configure(
            "Applications.Treeview.Heading",
            font=FONT_LABEL,
            background=BACKGROUND_COLOR,
            foreground=MUTED_TEXT,
        )

        columns = ("num", "title", "experience", "skills")
        table = ttk.Treeview(
            self.history_container,
            columns=columns,
            show="headings",
            height=15,
            style="Applications.Treeview",
        )

        table.heading("num",        text="#")
        table.heading("title",      text="Job Title")
        table.heading("experience", text="Experience Level")
        table.heading("skills",     text="Required Skill")

        table.column("num",        width=40,  anchor="center")
        table.column("title",      width=240, anchor="w")
        table.column("experience", width=150, anchor="center")
        table.column("skills",     width=200, anchor="w")

        for idx, app in enumerate(my_apps, start=1):
            table.insert(
                "", "end",
                values=(idx, app["title"], app["experience"], app["skills"]),
            )

        table.pack(fill="both", expand=True)
