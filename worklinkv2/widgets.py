"""Shared reusable widgets for WorkLink v2."""
import tkinter as tk
from tkinter import ttk
from worklink.styles import *

def avatar(parent, name, size=36):
    initials = "".join(w[0].upper() for w in name.split()[:2])
    c = tk.Canvas(parent, width=size, height=size, bg=ACCENT, highlightthickness=0)
    c.create_oval(0,0,size,size,fill=ACCENT,outline="")
    c.create_text(size//2,size//2,text=initials,fill=WHITE,font=("Helvetica",size//3,"bold"))
    return c

def badge(parent, text, color=ACCENT):
    f = tk.Frame(parent, bg=color, padx=6, pady=2)
    tk.Label(f, text=text, font=FM, bg=color, fg=WHITE).pack()
    return f

def divider(parent):
    return tk.Frame(parent, bg=BORDER, height=1)

def sidebar_btn(parent, icon, label, cmd, active=False):
    bg = SURFACE2 if active else SURFACE
    f = tk.Frame(parent, bg=bg, cursor="hand2")
    f.pack(fill="x", pady=1)
    inner = tk.Frame(f, bg=bg, padx=SP3, pady=SP2)
    inner.pack(fill="x")
    tk.Label(inner, text=icon, font=("Helvetica",14), bg=bg, fg=ACCENT if active else MUTED).pack(side="left")
    tk.Label(inner, text=f"  {label}", font=FK, bg=bg, fg=TEXT if active else MUTED).pack(side="left")
    for w in (f, inner):
        w.bind("<Button-1>", lambda e: cmd())
    return f

def card(parent, **kw):
    return tk.Frame(parent, bg=SURFACE, highlightthickness=1,
                    highlightbackground=BORDER, **kw)

def section_title(parent, text):
    tk.Label(parent, text=text, font=FS, bg=BG, fg=TEXT).pack(anchor="w", pady=(SP4,SP2))

def form_field(parent, label, show=None, width=36):
    tk.Label(parent, text=label, font=FK, bg=BG, fg=MUTED).pack(anchor="w", pady=(SP3,SP1))
    kw = {**ENT, "width": width}
    if show: kw["show"] = show
    e = tk.Entry(parent, **kw)
    e.pack(anchor="w", ipady=6)
    return e

def scrollable(parent, width=700):
    c = tk.Canvas(parent, bg=BG, highlightthickness=0)
    sb = tk.Scrollbar(parent, orient="vertical", command=c.yview,
                      bg=SURFACE, troughcolor=BG, bd=0, highlightthickness=0)
    f = tk.Frame(c, bg=BG)
    f.bind("<Configure>", lambda e: c.configure(scrollregion=c.bbox("all")))
    c.create_window((0,0), window=f, anchor="nw", width=width)
    c.configure(yscrollcommand=sb.set)
    c.pack(side="left", fill="both", expand=True)
    sb.pack(side="right", fill="y")
    return f

def stat_card(parent, label, value, color=ACCENT):
    f = card(parent)
    inner = tk.Frame(f, bg=SURFACE, padx=SP4, pady=SP3)
    inner.pack(fill="both")
    tk.Label(inner, text=value, font=("Helvetica",28,"bold"), bg=SURFACE, fg=color).pack(anchor="w")
    tk.Label(inner, text=label, font=FM, bg=SURFACE, fg=MUTED).pack(anchor="w")
    return f
