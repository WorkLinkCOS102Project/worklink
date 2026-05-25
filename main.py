"""WorkLink v2 — revamped Tkinter UI with PostgreSQL backend."""
from __future__ import annotations
import re, webbrowser, tkinter as tk
from tkinter import messagebox, ttk

import worklink.db as db
db.init_pool()
db.initialise_schema()

from worklink.styles import *
from worklink.widgets import *
from worklink.data_manager import *

# ── Root ──────────────────────────────────────────────────────────────────────
root = tk.Tk()
root.title("WorkLink")
root.geometry("960x640")
root.config(bg=BG)
root.resizable(True, True)
root.minsize(860, 580)

session = {"id": None, "name": None, "role": None, "skills": None}

def clear():
    for w in root.winfo_children(): w.destroy()

def do_logout():
    session.update(id=None, name=None, role=None, skills=None)
    show_landing()

# ── LANDING ───────────────────────────────────────────────────────────────────
def show_landing():
    clear()
    root.geometry("520x560")

    tk.Label(root, text="WorkLink", font=("Helvetica",32,"bold"), bg=BG, fg=ACCENT).pack(pady=(SP7,SP2))
    tk.Label(root, text="Your next opportunity is one click away.", font=FB, bg=BG, fg=MUTED).pack(pady=(0,SP6))

    for label, role in [("Continue as Employer", "Employer"), ("Continue as Job Seeker", "Employee")]:
        tk.Button(root, text=label, **BTN_P, width=28, height=2,
                  command=lambda r=role: show_auth(r)).pack(pady=SP2)

    divider(root).pack(fill="x", padx=SP6, pady=SP4)
    tk.Button(root, text="Exit", **BTN_D, width=14, command=root.destroy).pack(pady=SP2)

# ── MULTI-SKILL SELECTOR WIDGET ───────────────────────────────────────────────
class MultiSkillSelector(tk.Frame):
    """
    Scrollable list of tk.Checkbutton widgets — one per skill.
    Filter entry narrows the visible checkboxes; checked state is preserved
    across filter changes via a permanent dict of BooleanVars.
    """

    VISIBLE_ROWS = 7   # height of the scrollable area in checkbox rows (~28 px each)

    def __init__(self, parent, label_text="Skills", **kw):
        super().__init__(parent, bg=BG, **kw)

        tk.Label(self, text=label_text, font=FK, bg=BG, fg=MUTED).pack(
            anchor="w", pady=(SP3, SP1)
        )

        # Filter entry
        self._filter_var = tk.StringVar()
        self._filter_var.trace_add("write", self._rebuild)
        fe = tk.Entry(self, textvariable=self._filter_var, width=32, **ENT)
        fe.pack(anchor="w", ipady=4, pady=(0, SP1))
        tk.Label(self, text="🔍 Type to filter", font=FM, bg=BG, fg=MUTED).pack(anchor="w")

        # One BooleanVar per skill — lives for the whole lifetime of the widget
        self._vars: dict[str, tk.BooleanVar] = {
            skill: tk.BooleanVar(value=False) for skill in SKILL_POOL
        }

        # Scrollable container
        box_h = self.VISIBLE_ROWS * 28          # pixels
        outer = tk.Frame(self, bg=BORDER, padx=1, pady=1)
        outer.pack(anchor="w", pady=SP1)

        self._canvas = tk.Canvas(
            outer, bg=SURFACE2, highlightthickness=0,
            width=320, height=box_h,
        )
        self._sb = tk.Scrollbar(outer, orient="vertical", command=self._canvas.yview)
        self._canvas.configure(yscrollcommand=self._sb.set)
        self._canvas.pack(side="left")
        self._sb.pack(side="right", fill="y")

        # Inner frame that holds the checkbuttons
        self._inner = tk.Frame(self._canvas, bg=SURFACE2)
        self._win_id = self._canvas.create_window((0, 0), window=self._inner, anchor="nw")
        self._inner.bind(
            "<Configure>",
            lambda e: self._canvas.configure(scrollregion=self._canvas.bbox("all")),
        )
        # Mouse-wheel scrolling
        self._canvas.bind("<Enter>", self._bind_wheel)
        self._canvas.bind("<Leave>", self._unbind_wheel)

        # Count label
        self._count_lbl = tk.Label(self, text="0 skills selected", font=FM, bg=BG, fg=ACCENT)
        self._count_lbl.pack(anchor="w")

        self._rebuild()

    # ── wheel scroll helpers ───────────────────────────────────────────────
    def _bind_wheel(self, _e=None):
        self._canvas.bind_all("<MouseWheel>",   self._on_wheel)
        self._canvas.bind_all("<Button-4>",     self._on_wheel)
        self._canvas.bind_all("<Button-5>",     self._on_wheel)

    def _unbind_wheel(self, _e=None):
        self._canvas.unbind_all("<MouseWheel>")
        self._canvas.unbind_all("<Button-4>")
        self._canvas.unbind_all("<Button-5>")

    def _on_wheel(self, event):
        if event.num == 4:
            self._canvas.yview_scroll(-1, "units")
        elif event.num == 5:
            self._canvas.yview_scroll(1, "units")
        else:
            self._canvas.yview_scroll(int(-event.delta / 120), "units")

    # ── rebuild checkbuttons to match filter ──────────────────────────────
    def _rebuild(self, *_):
        for w in self._inner.winfo_children():
            w.destroy()

        q = self._filter_var.get().lower()
        visible = [s for s in SKILL_POOL if q in s.lower()]

        for skill in visible:
            var = self._vars[skill]
            cb = tk.Checkbutton(
                self._inner,
                text=skill,
                variable=var,
                command=self._update_count,
                bg=SURFACE2,
                fg=TEXT,
                selectcolor=ACCENT,        # box fill when checked
                activebackground=SURFACE2,
                activeforeground=TEXT,
                font=FB,
                anchor="w",
                relief="flat",
                bd=0,
                highlightthickness=0,
                cursor="hand2",
            )
            cb.pack(fill="x", padx=SP2, pady=1)

        # Reset scroll to top when filter changes
        self._canvas.yview_moveto(0)
        self._update_count()

    def _update_count(self):
        n = sum(1 for v in self._vars.values() if v.get())
        self._count_lbl.config(text=f"{n} skill{'s' if n != 1 else ''} selected")

    # ── public API ────────────────────────────────────────────────────────
    def get(self) -> str:
        """Return a comma-separated string of all checked skills."""
        return ", ".join(skill for skill in SKILL_POOL if self._vars[skill].get())

    def get_set(self) -> set[str]:
        return {skill for skill in SKILL_POOL if self._vars[skill].get()}


# ── AUTH (Login + Register in one screen) ─────────────────────────────────────
def show_auth(role, tab="login"):
    clear()
    root.geometry("520x640")

    hdr = tk.Frame(root, bg=SURFACE, pady=SP3)
    hdr.pack(fill="x")
    tk.Label(hdr, text="WorkLink", font=FS, bg=SURFACE, fg=ACCENT).pack(side="left", padx=SP4)
    tk.Button(hdr, text="← Back", **BTN_S, command=show_landing).pack(side="right", padx=SP4)

    role_label = "Employer" if role == "Employer" else "Job Seeker"
    tk.Label(root, text=f"{role_label} Portal", font=FT, bg=BG, fg=TEXT).pack(pady=(SP4,0))

    tab_frame = tk.Frame(root, bg=BG)
    tab_frame.pack(pady=SP3)

    def make_tab(t, label):
        def select(): show_auth(role, t)
        tk.Button(tab_frame, text=label, font=FK,
                  bg=ACCENT if tab == t else SURFACE2,
                  fg=WHITE if tab == t else MUTED,
                  relief="flat", bd=0, padx=SP4, pady=SP2,
                  cursor="hand2", command=select).pack(side="left", padx=2)

    make_tab("login", "Sign In")
    make_tab("register", "Create Account")

    body = tk.Frame(root, bg=BG)
    body.pack(fill="both", expand=True, padx=SP6)

    if tab == "login":
        _login_form(body, role)
    else:
        _register_form(body, role)


def _login_form(parent, role):
    em = form_field(parent, "Email Address")
    pw = form_field(parent, "Password", show="*")

    msg = tk.Label(parent, text="", font=FM, bg=BG, fg=ERROR)
    msg.pack(anchor="w", pady=SP1)

    def attempt():
        e, p = em.get().strip(), pw.get().strip()
        if not e or not p: msg.config(text="Please fill in all fields."); return
        profile = validate_login(e, p)
        if not profile: msg.config(text="Incorrect email or password."); return
        if profile["role"] != role:
            msg.config(text=f"This account is registered as {profile['role']}."); return
        session.update(**profile)
        show_dashboard()

    tk.Button(parent, text="Sign In", **BTN_P, width=24, command=attempt).pack(pady=SP4)


def _register_form(parent, role):
    # Wrap in a scrollable canvas so the skill list doesn't overflow
    canvas = tk.Canvas(parent, bg=BG, highlightthickness=0)
    sb = tk.Scrollbar(parent, orient="vertical", command=canvas.yview)
    inner = tk.Frame(canvas, bg=BG)
    inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=inner, anchor="nw", width=430)
    canvas.configure(yscrollcommand=sb.set)
    canvas.pack(side="left", fill="both", expand=True)
    sb.pack(side="right", fill="y")

    name_lbl = "Company Name" if role == "Employer" else "Full Name"
    nm = form_field(inner, name_lbl)
    em = form_field(inner, "Email Address")
    pw = form_field(inner, "Password (min 6 chars)", show="*")

    skill_lbl = "Industry / Fields (select all that apply)" if role == "Employer" else "Your Skills (select all that apply)"
    selector = MultiSkillSelector(inner, label_text=skill_lbl)
    selector.pack(anchor="w", pady=(0, SP1))

    msg = tk.Label(inner, text="", font=FM, bg=BG, fg=ERROR)
    msg.pack(anchor="w", pady=SP1)

    def attempt():
        n, e, p = nm.get().strip(), em.get().strip(), pw.get().strip()
        skills_str = selector.get()
        if not n or not e or not p:
            msg.config(text="Please fill in all fields."); return
        if not skills_str:
            msg.config(text="Please select at least one skill."); return
        if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", e):
            msg.config(text="Invalid email address."); return
        if len(p) < 6:
            msg.config(text="Password must be at least 6 characters."); return
        if len(n) > 50:
            msg.config(text="Name must be 50 characters or fewer."); return
        # Truncate skills to fit DB column (100 chars)
        if len(skills_str) > 97:
            skills_str = skills_str[:97] + "..."
        result = save_user(n, e, p, role, skills_str)
        if result == "LOCKED": msg.config(text="Database error. Try again."); return
        if not result: msg.config(text="Email already registered."); return
        messagebox.showinfo("Account Created", "Welcome to WorkLink! Please sign in.")
        show_auth(role, "login")

    tk.Button(inner, text="Create Account", **BTN_P, width=24, command=attempt).pack(pady=SP4)


# ── MAIN SHELL (sidebar + content area) ───────────────────────────────────────
content_frame: tk.Frame | None = None

def show_dashboard():
    clear()
    root.geometry("960x680")

    sidebar = tk.Frame(root, bg=SURFACE, width=210)
    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)

    tk.Label(sidebar, text="WorkLink", font=FS, bg=SURFACE, fg=ACCENT).pack(pady=(SP4,SP2), padx=SP4, anchor="w")
    divider(sidebar).pack(fill="x", padx=SP3)

    av = avatar(sidebar, session["name"])
    av.pack(pady=(SP3,SP1), padx=SP4, anchor="w")
    tk.Label(sidebar, text=session["name"], font=FK, bg=SURFACE, fg=TEXT,
             wraplength=170, anchor="w").pack(padx=SP4, anchor="w")
    role_color = ACCENT if session["role"] == "Employer" else SUCCESS
    tk.Label(sidebar, text=session["role"], font=FM, bg=SURFACE, fg=role_color).pack(padx=SP4, anchor="w", pady=(0,SP3))
    divider(sidebar).pack(fill="x", padx=SP3)

    global content_frame
    content_frame = tk.Frame(root, bg=BG)
    content_frame.pack(side="left", fill="both", expand=True)

    if session["role"] == "Employer":
        nav_items = [
            ("🏠", "Dashboard",   show_employer_home),
            ("➕", "Post a Job",  show_post_job),
            ("📋", "My Listings", show_my_jobs),
        ]
    else:
        nav_items = [
            ("🏠", "Dashboard",       show_employee_home),
            ("🔍", "Browse Jobs",     show_browse_jobs),
            ("📄", "My Applications", show_my_applications),
            ("🎓", "Learn Skills",    show_learn_skills),
        ]

    active_holder = [None]

    def nav_click(cmd, btn_frame, all_btns):
        for b in all_btns: b.config(bg=SURFACE)
        btn_frame.config(bg=SURFACE2)
        active_holder[0] = btn_frame
        cmd()

    all_btn_frames = []
    for icon, label, cmd in nav_items:
        f = sidebar_btn(sidebar, icon, label, lambda c=cmd: None)
        all_btn_frames.append(f)

    # Re-wire with real click logic after all frames exist
    for widget in sidebar.winfo_children():
        if isinstance(widget, tk.Frame) and widget not in (sidebar,):
            pass  # handled below

    # Simpler approach: rebuild sidebar buttons with nav_click
    for widget in sidebar.winfo_children():
        if isinstance(widget, tk.Frame):
            widget.destroy()

    all_btn_frames = []
    for icon, label, cmd in nav_items:
        bg = SURFACE
        f = tk.Frame(sidebar, bg=bg, cursor="hand2")
        f.pack(fill="x", pady=1)
        inner = tk.Frame(f, bg=bg, padx=SP3, pady=SP2)
        inner.pack(fill="x")
        tk.Label(inner, text=icon, font=("Helvetica",14), bg=bg, fg=ACCENT).pack(side="left")
        tk.Label(inner, text=f"  {label}", font=FK, bg=bg, fg=MUTED).pack(side="left")
        all_btn_frames.append(f)
        for w in (f, inner, *inner.winfo_children()):
            w.bind("<Button-1>", lambda e, c=cmd, bf=f: nav_click(c, bf, all_btn_frames))

    # Bottom: logout
    spacer = tk.Frame(sidebar, bg=SURFACE)
    spacer.pack(fill="both", expand=True)
    divider(sidebar).pack(fill="x", padx=SP3)
    tk.Button(sidebar, text="Log Out", **BTN_S, command=do_logout).pack(pady=SP3, padx=SP4, anchor="w")

    # Load first nav item by default
    nav_click(nav_items[0][2], all_btn_frames[0], all_btn_frames)


def content() -> tk.Frame:
    global content_frame
    for w in content_frame.winfo_children(): w.destroy()
    return content_frame


# ── EMPLOYER: HOME ─────────────────────────────────────────────────────────────
def show_employer_home():
    p = content()
    tk.Label(p, text=f"Welcome, {session['name'].split()[0]} 👋",
             font=FT, bg=BG, fg=TEXT).pack(anchor="w", padx=SP5, pady=(SP5,SP1))
    tk.Label(p, text="Manage your job listings and applicants.", font=FB, bg=BG, fg=MUTED).pack(anchor="w", padx=SP5)

    stats = get_stats(session["id"], "Employer")
    row = tk.Frame(p, bg=BG); row.pack(fill="x", padx=SP5, pady=SP4)
    for label, val, col in [("Jobs Posted", stats["jobs"], ACCENT),
                              ("Total Applicants", stats["applicants"], SUCCESS)]:
        sc = stat_card(row, label, str(val), col)
        sc.pack(side="left", padx=(0,SP3), ipadx=SP5, ipady=SP3)

    divider(p).pack(fill="x", padx=SP5, pady=SP3)
    tk.Label(p, text="Recent Listings", font=FS, bg=BG, fg=TEXT).pack(anchor="w", padx=SP5, pady=(0,SP2))
    scroll_f = scrollable(p, width=680)
    for job in get_employer_jobs(session["id"])[:3]:
        _employer_job_card(scroll_f, job)


# ── EMPLOYER: POST JOB ─────────────────────────────────────────────────────────
def show_post_job():
    p = content()
    tk.Label(p, text="Post a New Job", font=FT, bg=BG, fg=TEXT).pack(anchor="w", padx=SP5, pady=(SP5,SP1))
    divider(p).pack(fill="x", padx=SP5, pady=SP2)

    canvas = tk.Canvas(p, bg=BG, highlightthickness=0)
    sb = tk.Scrollbar(p, orient="vertical", command=canvas.yview)
    inner = tk.Frame(canvas, bg=BG)
    inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0,0), window=inner, anchor="nw", width=680)
    canvas.configure(yscrollcommand=sb.set)
    canvas.pack(side="left", fill="both", expand=True, padx=SP5)
    sb.pack(side="right", fill="y")

    ti = form_field(inner, "Job Title")

    tk.Label(inner, text="Job Description", font=FK, bg=BG, fg=MUTED).pack(anchor="w", pady=(SP3,SP1))
    desc_box = tk.Text(inner, width=55, height=6, **ENT)
    desc_box.pack(anchor="w", ipady=4)

    # Multi-skill selector for job required skills
    skill_sel = MultiSkillSelector(inner, label_text="Required Skills (select all that apply)")
    skill_sel.pack(anchor="w")

    tk.Label(inner, text="Experience Level", font=FK, bg=BG, fg=MUTED).pack(anchor="w", pady=(SP3,SP1))
    ev = tk.StringVar(value="Entry Level")
    exp_opts = ["Entry Level", "Mid Level", "Senior", "Lead / Manager"]
    om = ttk.OptionMenu(inner, ev, exp_opts[0], *exp_opts)
    om.pack(anchor="w")

    msg = tk.Label(inner, text="", font=FM, bg=BG, fg=ERROR)
    msg.pack(anchor="w", pady=SP1)

    def attempt():
        t = ti.get().strip()
        d = desc_box.get("1.0", "end").strip()
        s = skill_sel.get()
        e = ev.get()
        if not t or not d:
            msg.config(text="Please fill in all fields."); return
        if not s:
            msg.config(text="Please select at least one required skill."); return
        if len(t) > 60:
            msg.config(text="Title must be 60 characters or fewer."); return
        if len(s) > 97:
            s = s[:97] + "..."
        result = save_job(session["id"], t, d, s, e)
        if result == "LOCKED": msg.config(text="Database error. Try again."); return
        messagebox.showinfo("Job Posted!", f'"{t}" is now live.')
        show_my_jobs()

    tk.Button(inner, text="Publish Job", **BTN_P, width=20, command=attempt).pack(pady=SP4)


# ── EMPLOYER: MY JOBS ─────────────────────────────────────────────────────────
def show_my_jobs():
    p = content()
    tk.Label(p, text="My Listings", font=FT, bg=BG, fg=TEXT).pack(anchor="w", padx=SP5, pady=(SP5,SP1))
    jobs = get_employer_jobs(session["id"])
    tk.Label(p, text=f"{len(jobs)} job(s) posted", font=FB, bg=BG, fg=MUTED).pack(anchor="w", padx=SP5)
    divider(p).pack(fill="x", padx=SP5, pady=SP3)
    scroll_f = scrollable(p, width=700)
    if not jobs:
        tk.Label(scroll_f, text="No listings yet.", font=FB, bg=BG, fg=MUTED).pack(pady=SP5, padx=SP5)
        return
    for job in jobs:
        _employer_job_card(scroll_f, job, full=True)


def _employer_job_card(parent, job, full=False):
    c = card(parent)
    c.pack(fill="x", padx=SP4, pady=SP2)
    inner = tk.Frame(c, bg=SURFACE, padx=SP4, pady=SP3)
    inner.pack(fill="x")

    tr = tk.Frame(inner, bg=SURFACE); tr.pack(fill="x")
    tk.Label(tr, text=job["title"], font=FS, bg=SURFACE, fg=TEXT).pack(side="left")
    badge(tr, job["experience"], ACCENT_DARK).pack(side="right")

    mr = tk.Frame(inner, bg=SURFACE); mr.pack(fill="x", pady=SP1)
    tk.Label(mr, text=f"🎯 {job['skills']}", font=FM, bg=SURFACE, fg=MUTED).pack(side="left")

    if full:
        desc = job["description"]
        tk.Label(inner, text=desc[:160]+("..." if len(desc)>160 else ""),
                 font=FB, bg=SURFACE, fg=MUTED, wraplength=580, justify="left").pack(anchor="w", pady=(SP1,SP2))
        tk.Button(inner, text="View Applicants →", **BTN_P,
                  command=lambda jid=job["id"], jt=job["title"]: show_applicants(jid, jt)).pack(anchor="e")


# ── EMPLOYER: APPLICANTS ───────────────────────────────────────────────────────
def show_applicants(job_id, job_title):
    p = content()
    tk.Label(p, text=f"Applicants: {job_title}", font=FT, bg=BG, fg=TEXT,
             wraplength=680).pack(anchor="w", padx=SP5, pady=(SP5,SP1))

    candidates = get_job_applicants(job_id)
    tk.Label(p, text=f"{len(candidates)} applicant(s)", font=FB, bg=BG, fg=MUTED).pack(anchor="w", padx=SP5)
    tk.Button(p, text="← Back to Listings", **BTN_S, command=show_my_jobs).pack(anchor="w", padx=SP5, pady=SP2)
    divider(p).pack(fill="x", padx=SP5, pady=SP2)

    scroll_f = scrollable(p, width=700)
    if not candidates:
        tk.Label(scroll_f, text="No applicants yet.", font=FB, bg=BG, fg=MUTED).pack(pady=SP5, padx=SP5)
        return
    for cand in candidates:
        c = card(scroll_f); c.pack(fill="x", padx=SP4, pady=SP2)
        inner = tk.Frame(c, bg=SURFACE, padx=SP4, pady=SP3); inner.pack(fill="x")
        row = tk.Frame(inner, bg=SURFACE); row.pack(fill="x")
        av = avatar(row, cand["name"], size=40); av.pack(side="left", padx=(0,SP3))
        info = tk.Frame(row, bg=SURFACE); info.pack(side="left")
        tk.Label(info, text=cand["name"], font=FS, bg=SURFACE, fg=TEXT).pack(anchor="w")
        tk.Label(info, text=cand["email"], font=FM, bg=SURFACE, fg=MUTED).pack(anchor="w")
        badge(row, cand["skills"][:40], ACCENT_DARK).pack(side="right", pady=SP1)


# ── EMPLOYEE: HOME ─────────────────────────────────────────────────────────────
def show_employee_home():
    p = content()
    tk.Label(p, text=f"Welcome back, {session['name'].split()[0]} 👋",
             font=FT, bg=BG, fg=TEXT).pack(anchor="w", padx=SP5, pady=(SP5,SP1))
    tk.Label(p, text="Track your job search progress.", font=FB, bg=BG, fg=MUTED).pack(anchor="w", padx=SP5)

    stats = get_stats(session["id"], "Employee")
    row = tk.Frame(p, bg=BG); row.pack(fill="x", padx=SP5, pady=SP4)
    for label, val, col in [("Jobs Available", stats["available"], ACCENT),
                              ("Applications Sent", stats["applied"], SUCCESS)]:
        sc = stat_card(row, label, str(val), col)
        sc.pack(side="left", padx=(0,SP3), ipadx=SP5, ipady=SP3)

    divider(p).pack(fill="x", padx=SP5, pady=SP3)
    tk.Label(p, text="Latest Opportunities", font=FS, bg=BG, fg=TEXT).pack(anchor="w", padx=SP5, pady=(0,SP2))

    apps = get_applications(session["id"])
    applied_ids = {str(a["job_id"]) for a in apps}
    scroll_f = scrollable(p, width=680)
    jobs = get_jobs()[:4]
    if not jobs:
        tk.Label(scroll_f, text="No jobs available yet.", font=FB, bg=BG, fg=MUTED).pack(pady=SP5, padx=SP5)
    for job in jobs:
        _job_card(scroll_f, job, applied_ids)


# ── EMPLOYEE: BROWSE ───────────────────────────────────────────────────────────
def show_browse_jobs():
    p = content()
    tk.Label(p, text="Browse Jobs", font=FT, bg=BG, fg=TEXT).pack(anchor="w", padx=SP5, pady=(SP5,SP1))

    sf = tk.Frame(p, bg=BG); sf.pack(fill="x", padx=SP5, pady=SP2)
    sv = tk.StringVar()
    se = tk.Entry(sf, textvariable=sv, width=40, **ENT)
    se.pack(side="left", ipady=6, padx=(0,SP2))
    tk.Label(sf, text="🔍", font=FB, bg=BG, fg=MUTED).pack(side="left")

    divider(p).pack(fill="x", padx=SP5, pady=SP2)

    apps = get_applications(session["id"])
    applied_ids = {str(a["job_id"]) for a in apps}

    list_frame = tk.Frame(p, bg=BG); list_frame.pack(fill="both", expand=True)
    scroll_f = [scrollable(list_frame, width=700)]

    def refresh(query=""):
        for w in list_frame.winfo_children(): w.destroy()
        sf2 = scrollable(list_frame, width=700)
        scroll_f[0] = sf2
        jobs = get_jobs()
        if query:
            q = query.lower()
            jobs = [j for j in jobs if q in j["title"].lower() or q in j["skills"].lower()]
        apps2 = get_applications(session["id"])
        aid2 = {str(a["job_id"]) for a in apps2}
        tk.Label(sf2, text=f"{len(jobs)} result(s)", font=FM, bg=BG, fg=MUTED).pack(anchor="w", padx=SP4, pady=SP1)
        if not jobs:
            tk.Label(sf2, text="No jobs match your search.", font=FB, bg=BG, fg=MUTED).pack(pady=SP5, padx=SP5)
        for job in jobs:
            _job_card(sf2, job, aid2, on_apply=lambda: refresh(sv.get()))

    sv.trace_add("write", lambda *_: refresh(sv.get()))
    refresh()


def _job_card(parent, job, applied_ids, on_apply=None):
    already = str(job["id"]) in applied_ids
    c = card(parent); c.pack(fill="x", padx=SP4, pady=SP2)
    inner = tk.Frame(c, bg=SURFACE, padx=SP4, pady=SP3); inner.pack(fill="x")

    tr = tk.Frame(inner, bg=SURFACE); tr.pack(fill="x")
    tk.Label(tr, text=job["title"], font=FS, bg=SURFACE, fg=TEXT).pack(side="left")
    badge(tr, job["experience"], ACCENT_DARK).pack(side="right")

    mr = tk.Frame(inner, bg=SURFACE); mr.pack(fill="x", pady=SP1)
    tk.Label(mr, text=f"🎯 {job['skills']}", font=FM, bg=SURFACE, fg=MUTED).pack(side="left")

    desc = job["description"]
    tk.Label(inner, text=desc[:160]+("..." if len(desc)>160 else ""),
             font=FB, bg=SURFACE, fg=MUTED, wraplength=580, justify="left").pack(anchor="w", pady=(SP1,SP2))

    ar = tk.Frame(inner, bg=SURFACE); ar.pack(fill="x")
    if already:
        tk.Label(ar, text="✓ Applied", font=FBT, bg=SURFACE, fg=SUCCESS).pack(side="right")
    else:
        def apply_now(jid=job["id"]):
            res = save_application(jid, session["id"])
            if res == "LOCKED": messagebox.showerror("Error", "Database error. Try again."); return
            if not res: messagebox.showwarning("Already Applied", "You already applied for this role."); return
            messagebox.showinfo("Applied!", "Your application was submitted. Good luck!")
            if on_apply: on_apply()
            else: show_employee_home()
        tk.Button(ar, text="Apply Now", **BTN_P, command=apply_now).pack(side="right")


# ── EMPLOYEE: MY APPLICATIONS ─────────────────────────────────────────────────
def show_my_applications():
    p = content()
    apps = get_applications(session["id"])
    tk.Label(p, text="My Applications", font=FT, bg=BG, fg=TEXT).pack(anchor="w", padx=SP5, pady=(SP5,SP1))
    tk.Label(p, text=f"{len(apps)} application(s) submitted", font=FB, bg=BG, fg=MUTED).pack(anchor="w", padx=SP5)
    divider(p).pack(fill="x", padx=SP5, pady=SP3)

    if not apps:
        tk.Label(p, text="You haven't applied to any jobs yet.\nBrowse available roles to get started!",
                 font=FB, bg=BG, fg=MUTED, justify="center").pack(pady=SP7)
        return

    scroll_f = scrollable(p, width=700)
    for i, app in enumerate(apps, 1):
        c = card(scroll_f); c.pack(fill="x", padx=SP4, pady=SP2)
        inner = tk.Frame(c, bg=SURFACE, padx=SP4, pady=SP3); inner.pack(fill="x")
        tr = tk.Frame(inner, bg=SURFACE); tr.pack(fill="x")
        tk.Label(tr, text=f"{i}. {app['title']}", font=FS, bg=SURFACE, fg=TEXT).pack(side="left")
        badge(tr, "Applied", SUCCESS).pack(side="right")
        tk.Label(inner, text=f"🎯 {app['skills']}  ·  📊 {app['experience']}",
                 font=FM, bg=SURFACE, fg=MUTED).pack(anchor="w", pady=SP1)


# ── EMPLOYEE: LEARN SKILLS ────────────────────────────────────────────────────
def show_learn_skills():
    p = content()
    tk.Label(p, text="Learn Skills", font=FT, bg=BG, fg=TEXT).pack(anchor="w", padx=SP5, pady=(SP5,SP1))
    tk.Label(p, text="Discover free and paid resources to build in-demand skills.",
             font=FB, bg=BG, fg=MUTED).pack(anchor="w", padx=SP5)

    # Filter bar
    filter_frame = tk.Frame(p, bg=BG)
    filter_frame.pack(fill="x", padx=SP5, pady=SP3)

    fv = tk.StringVar()
    fe = tk.Entry(filter_frame, textvariable=fv, width=36, **ENT)
    fe.pack(side="left", ipady=6, padx=(0, SP2))
    tk.Label(filter_frame, text="🔍 Filter skills", font=FM, bg=BG, fg=MUTED).pack(side="left")

    divider(p).pack(fill="x", padx=SP5, pady=(0, SP2))

    list_frame = tk.Frame(p, bg=BG)
    list_frame.pack(fill="both", expand=True)

    def render(query=""):
        for w in list_frame.winfo_children(): w.destroy()
        scroll_f = scrollable(list_frame, width=700)

        skills_to_show = [
            (sk, res) for sk, res in SKILL_RESOURCES.items()
            if query.lower() in sk.lower()
        ]

        if not skills_to_show:
            tk.Label(scroll_f, text="No matching skills found.", font=FB, bg=BG, fg=MUTED).pack(pady=SP5)
            return

        for skill_name, resources in skills_to_show:
            _skill_resource_card(scroll_f, skill_name, resources)

    def _skill_resource_card(parent, skill_name, resources):
        c = card(parent)
        c.pack(fill="x", padx=SP4, pady=SP2)
        inner = tk.Frame(c, bg=SURFACE, padx=SP4, pady=SP3)
        inner.pack(fill="x")

        # Title row with skill name
        title_row = tk.Frame(inner, bg=SURFACE)
        title_row.pack(fill="x")
        tk.Label(title_row, text=skill_name, font=FS, bg=SURFACE, fg=ACCENT).pack(side="left")

        # FREE resources
        free_lbl_row = tk.Frame(inner, bg=SURFACE)
        free_lbl_row.pack(fill="x", pady=(SP2, SP1))
        tk.Label(free_lbl_row, text="🆓  Free Resources", font=FK, bg=SURFACE, fg=SUCCESS).pack(side="left")

        for name, url in resources.get("free", []):
            _resource_link_row(inner, name, url, SUCCESS)

        # PAID resources
        paid_lbl_row = tk.Frame(inner, bg=SURFACE)
        paid_lbl_row.pack(fill="x", pady=(SP2, SP1))
        tk.Label(paid_lbl_row, text="💳  Paid Resources", font=FK, bg=SURFACE, fg=WARNING).pack(side="left")

        for name, url in resources.get("paid", []):
            _resource_link_row(inner, name, url, WARNING)

    def _resource_link_row(parent, name, url, color):
        row = tk.Frame(parent, bg=SURFACE)
        row.pack(fill="x", pady=1, padx=(SP3, 0))
        lbl = tk.Label(row, text=f"→ {name}", font=FM, bg=SURFACE, fg=color,
                       cursor="hand2", anchor="w")
        lbl.pack(side="left")
        lbl.bind("<Button-1>", lambda e, u=url: webbrowser.open(u))
        lbl.bind("<Enter>", lambda e: lbl.config(fg=TEXT))
        lbl.bind("<Leave>", lambda e: lbl.config(fg=color))

    fv.trace_add("write", lambda *_: render(fv.get()))
    render()


# ── Launch ────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    show_landing()
    root.mainloop()
