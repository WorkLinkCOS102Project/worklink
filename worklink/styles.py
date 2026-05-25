# WorkLink Design System v2 — Unified Purple Accent

BG          = "#0F1117"
SURFACE     = "#1A1D27"
SURFACE2    = "#222639"
BORDER      = "#2E3248"
ACCENT      = "#7C6FF7"        # purple primary
ACCENT_DARK = "#5A54C4"        # purple pressed / badge bg
TEXT        = "#F0F2FF"
MUTED       = "#8B8FA8"
SUCCESS     = "#22C55E"
ERROR       = "#EF4444"
WARNING     = "#F59E0B"
WHITE       = "#FFFFFF"

# ── Aliases used by job_browsing.py ──────────────────────────────────────────
BACKGROUND_COLOR = BG
CARD_COLOR       = SURFACE
TEXT_COLOR       = TEXT
PRIMARY_COLOR    = ACCENT
MUTED_TEXT       = MUTED
BORDER_COLOR     = BORDER
SUCCESS_COLOR    = SUCCESS

# ── Fonts ─────────────────────────────────────────────────────────────────────
FT  = ("Helvetica", 20, "bold")   # page titles
FS  = ("Helvetica", 13, "bold")   # section / card titles
FB  = ("Helvetica", 11, "normal") # body
FK  = ("Helvetica", 10, "bold")   # labels / keys
FM  = ("Helvetica",  9, "normal") # meta / small
FBT = ("Helvetica", 11, "bold")   # button text

# Aliases used by job_browsing.py
FONT_TITLE    = FT
FONT_SUBTITLE = FS
FONT_BODY     = FB
FONT_LABEL    = FK
FONT_SMALL    = FM
FONT_BUTTON   = FBT

# ── Spacing ───────────────────────────────────────────────────────────────────
SP1=4;  SP2=8;  SP3=12; SP4=16; SP5=24; SP6=32; SP7=48

# Aliases used by job_browsing.py
SP_XS  = SP1
SP_SM  = SP2
SP_MD  = SP3
SP_LG  = SP4
SP_XL  = SP5
SP_2XL = SP6
SP_3XL = SP7

# ── Button style dicts ────────────────────────────────────────────────────────
BTN_P = {
    "bg": ACCENT, "fg": WHITE, "font": FBT, "relief": "flat",
    "activebackground": ACCENT_DARK, "activeforeground": WHITE,
    "padx": SP4, "pady": SP2, "cursor": "hand2", "bd": 0,
}
BTN_S = {
    "bg": SURFACE2, "fg": TEXT, "font": FBT, "relief": "flat",
    "activebackground": BORDER, "activeforeground": TEXT,
    "padx": SP4, "pady": SP2, "cursor": "hand2", "bd": 0,
}
BTN_D = {
    "bg": ERROR, "fg": WHITE, "font": FBT, "relief": "flat",
    "activebackground": "#DC2626", "activeforeground": WHITE,
    "padx": SP4, "pady": SP2, "cursor": "hand2", "bd": 0,
}
ENT = {
    "font": FB, "bg": SURFACE2, "fg": TEXT,
    "insertbackground": TEXT, "relief": "flat", "bd": 0,
    "highlightthickness": 1, "highlightcolor": ACCENT,
    "highlightbackground": BORDER,
}

# Alias used by job_browsing.py
BTN_PRIMARY = BTN_P

# ── Skill pool ────────────────────────────────────────────────────────────────
SKILL_POOL = [
    "Python","Java","C++","JavaScript","HTML/CSS","SQL","Data Analysis",
    "Machine Learning","Project Management","UI/UX Design","Graphic Design",
    "Technical Writing","Customer Service","Digital Marketing","SEO Optimization",
    "Financial Accounting","Data Entry","Excel / Spreadsheets","Public Speaking",
    "Sales & Negotiation","Cloud Computing (AWS/Azure)","Cybersecurity",
    "DevOps","Mobile App Development","Agile Methodologies","Content Strategy",
    "Foreign Languages","Video Editing","Human Resources","Network Administration",
]

# ── Skill learning resources (free + paid) ───────────────────────────────────
SKILL_RESOURCES = {
    "Python": {
        "free":  [("Python.org Official Tutorial",  "https://docs.python.org/3/tutorial/"),
                  ("freeCodeCamp Python Course",     "https://www.freecodecamp.org/learn/scientific-computing-with-python/"),
                  ("CS50P – Harvard (edX)",          "https://cs50.harvard.edu/python/")],
        "paid":  [("Python Bootcamp – Udemy",        "https://www.udemy.com/course/complete-python-bootcamp/"),
                  ("Python Path – Codecademy Pro",   "https://www.codecademy.com/learn/learn-python-3")],
    },
    "Java": {
        "free":  [("MOOC.fi Java Programming",       "https://java-programming.mooc.fi/"),
                  ("Oracle Java Tutorials",           "https://docs.oracle.com/javase/tutorial/"),
                  ("freeCodeCamp Java Full Course",   "https://www.freecodecamp.org/news/learn-java-free-java-courses-for-beginners/")],
        "paid":  [("Java Masterclass – Udemy",        "https://www.udemy.com/course/java-the-complete-java-developer-course/"),
                  ("Java Path – Codecademy Pro",      "https://www.codecademy.com/learn/learn-java")],
    },
    "C++": {
        "free":  [("learncpp.com",                   "https://www.learncpp.com/"),
                  ("Sololearn C++",                   "https://www.sololearn.com/learn/courses/c-plus-plus-introduction"),
                  ("freeCodeCamp C++ Course",         "https://www.freecodecamp.org/news/learn-c-with-free-31-hour-course/")],
        "paid":  [("Beginning C++ – Udemy",           "https://www.udemy.com/course/beginning-c-plus-plus-programming/"),
                  ("C++ Nanodegree – Udacity",        "https://www.udacity.com/course/c-plus-plus-nanodegree--nd213")],
    },
    "JavaScript": {
        "free":  [("The Odin Project",               "https://www.theodinproject.com/paths/full-stack-javascript"),
                  ("javascript.info",                 "https://javascript.info/"),
                  ("freeCodeCamp JS Cert",            "https://www.freecodecamp.org/learn/javascript-algorithms-and-data-structures/")],
        "paid":  [("JavaScript – Zero to Expert (Udemy)", "https://www.udemy.com/course/the-complete-javascript-course/"),
                  ("JS Path – Codecademy Pro",        "https://www.codecademy.com/learn/introduction-to-javascript")],
    },
    "HTML/CSS": {
        "free":  [("MDN Web Docs",                   "https://developer.mozilla.org/en-US/docs/Learn"),
                  ("freeCodeCamp Responsive Web Design", "https://www.freecodecamp.org/learn/2022/responsive-web-design/"),
                  ("The Odin Project – Foundations",  "https://www.theodinproject.com/paths/foundations")],
        "paid":  [("Web Design Bootcamp – Udemy",    "https://www.udemy.com/course/the-web-developer-bootcamp/"),
                  ("HTML & CSS – Codecademy Pro",    "https://www.codecademy.com/catalog/language/html-css")],
    },
    "SQL": {
        "free":  [("SQLZoo",                          "https://sqlzoo.net/"),
                  ("Mode SQL Tutorial",               "https://mode.com/sql-tutorial/"),
                  ("Khan Academy SQL",                "https://www.khanacademy.org/computing/computer-programming/sql")],
        "paid":  [("The Complete SQL Bootcamp – Udemy", "https://www.udemy.com/course/the-complete-sql-bootcamp/"),
                  ("SQL Path – Codecademy Pro",      "https://www.codecademy.com/learn/learn-sql")],
    },
    "Data Analysis": {
        "free":  [("Google Data Analytics (Coursera Audit)", "https://www.coursera.org/professional-certificates/google-data-analytics"),
                  ("Kaggle Learn",                   "https://www.kaggle.com/learn"),
                  ("freeCodeCamp Data Analysis",     "https://www.freecodecamp.org/learn/data-analysis-with-python/")],
        "paid":  [("Data Analyst Bootcamp – Udemy", "https://www.udemy.com/course/the-data-analyst-bootcamp/"),
                  ("Data Analyst Path – Dataquest",  "https://www.dataquest.io/path/data-analyst/")],
    },
    "Machine Learning": {
        "free":  [("fast.ai Practical Deep Learning", "https://course.fast.ai/"),
                  ("Google ML Crash Course",          "https://developers.google.com/machine-learning/crash-course"),
                  ("Andrew Ng ML (Coursera Audit)",   "https://www.coursera.org/specializations/machine-learning-introduction")],
        "paid":  [("ML A-Z – Udemy",                 "https://www.udemy.com/course/machinelearning/"),
                  ("ML Engineer Path – Dataquest",   "https://www.dataquest.io/path/machine-learning-engineer/")],
    },
    "Project Management": {
        "free":  [("Google PM Cert (Coursera Audit)", "https://www.coursera.org/professional-certificates/google-project-management"),
                  ("PMI Free Resources",              "https://www.pmi.org/learning/library"),
                  ("Alison PM Diploma",               "https://alison.com/course/diploma-in-project-management")],
        "paid":  [("PMP Exam Prep – Udemy",           "https://www.udemy.com/course/pmp-pmbok6-7/"),
                  ("Agile PM – LinkedIn Learning",   "https://www.linkedin.com/learning/topics/project-management")],
    },
    "UI/UX Design": {
        "free":  [("Google UX Design (Coursera Audit)", "https://www.coursera.org/professional-certificates/google-ux-design"),
                  ("Nielsen Norman Group Articles",   "https://www.nngroup.com/articles/"),
                  ("Figma Learn",                     "https://help.figma.com/hc/en-us/categories/360002051613")],
        "paid":  [("UI/UX Bootcamp – Udemy",          "https://www.udemy.com/course/user-experience-design-fundamentals/"),
                  ("UX Design – Interaction Design Foundation", "https://www.interaction-design.org/courses")],
    },
    "Graphic Design": {
        "free":  [("Canva Design School",             "https://www.canva.com/designschool/"),
                  ("Adobe Express Tutorials",         "https://www.adobe.com/express/learn/tutorials"),
                  ("freeCodeCamp Design Course",      "https://www.freecodecamp.org/news/tag/graphic-design/")],
        "paid":  [("Graphic Design Masterclass – Udemy", "https://www.udemy.com/course/graphic-design-masterclass-everything-you-need-to-know/"),
                  ("Adobe CC – LinkedIn Learning",   "https://www.linkedin.com/learning/topics/graphic-design")],
    },
    "Technical Writing": {
        "free":  [("Google Technical Writing Courses", "https://developers.google.com/tech-writing"),
                  ("Write the Docs Community",        "https://www.writethedocs.org/"),
                  ("Coursera Technical Writing (Audit)", "https://www.coursera.org/learn/technical-writing")],
        "paid":  [("Technical Writing – Udemy",      "https://www.udemy.com/course/technical-writing-and-editing/"),
                  ("Professional Writing – edX",     "https://www.edx.org/learn/writing")],
    },
    "Customer Service": {
        "free":  [("HubSpot Customer Service Cert",  "https://academy.hubspot.com/courses/customer-service-training"),
                  ("Alison Customer Service",        "https://alison.com/courses/customer-service"),
                  ("LinkedIn Learning Free Trial",   "https://www.linkedin.com/learning/topics/customer-service")],
        "paid":  [("Customer Service – Udemy",       "https://www.udemy.com/topic/customer-service/"),
                  ("Salesforce Service Cloud Cert",  "https://trailhead.salesforce.com/en/credentials/servicecloudconsultant")],
    },
    "Digital Marketing": {
        "free":  [("Google Digital Marketing Cert",  "https://grow.google/certificates/digital-marketing-ecommerce/"),
                  ("HubSpot Marketing Cert",         "https://academy.hubspot.com/courses/digital-marketing"),
                  ("Meta Blueprint",                 "https://www.facebook.com/business/learn")],
        "paid":  [("Digital Marketing Bootcamp – Udemy", "https://www.udemy.com/course/learn-digital-marketing-course/"),
                  ("Digital Marketing – Coursera",  "https://www.coursera.org/specializations/digital-marketing")],
    },
    "SEO Optimization": {
        "free":  [("Moz Beginner's Guide to SEO",    "https://moz.com/beginners-guide-to-seo"),
                  ("Google Search Central Docs",     "https://developers.google.com/search/docs"),
                  ("Ahrefs SEO Course",               "https://ahrefs.com/academy/seo-training-course")],
        "paid":  [("SEO 2024 Complete Guide – Udemy", "https://www.udemy.com/course/seo-training/"),
                  ("Semrush Academy",                 "https://www.semrush.com/academy/")],
    },
    "Financial Accounting": {
        "free":  [("Khan Academy Finance",           "https://www.khanacademy.org/economics-finance-domain/core-finance"),
                  ("Coursera Accounting (Audit)",    "https://www.coursera.org/learn/accounting-fundamentals"),
                  ("edX Intro to Accounting",        "https://www.edx.org/learn/accounting")],
        "paid":  [("Accounting Bootcamp – Udemy",   "https://www.udemy.com/course/accounting-bootcamp/"),
                  ("CPA Exam Prep – Becker",         "https://www.becker.com/cpa-review")],
    },
    "Data Entry": {
        "free":  [("Alison Data Entry Course",       "https://alison.com/course/data-entry-and-ms-office"),
                  ("Excel Basics – GCFGlobal",       "https://edu.gcfglobal.org/en/excel2016/"),
                  ("Typing.com",                     "https://www.typing.com/")],
        "paid":  [("Data Entry Masterclass – Udemy", "https://www.udemy.com/topic/data-entry/"),
                  ("Excel for Beginners – LinkedIn Learning", "https://www.linkedin.com/learning/topics/excel")],
    },
    "Excel / Spreadsheets": {
        "free":  [("Microsoft Excel Training",       "https://support.microsoft.com/en-us/office/excel-video-training-9bc05390-e94c-46af-a5b3-d7c22f6990bb"),
                  ("GCFGlobal Excel",                "https://edu.gcfglobal.org/en/excel2016/"),
                  ("freeCodeCamp Excel Course",      "https://www.freecodecamp.org/news/learn-microsoft-excel/")],
        "paid":  [("Excel Mastery – Udemy",          "https://www.udemy.com/course/microsoft-excel-2013-from-beginner-to-advanced-and-beyond/"),
                  ("Excel – LinkedIn Learning",     "https://www.linkedin.com/learning/topics/excel")],
    },
    "Public Speaking": {
        "free":  [("Toastmasters Resources",         "https://www.toastmasters.org/resources"),
                  ("TED Masterclass Free Sample",    "https://www.ted.com/masterclass"),
                  ("Coursera Public Speaking (Audit)", "https://www.coursera.org/learn/public-speaking")],
        "paid":  [("Public Speaking – Udemy",        "https://www.udemy.com/topic/public-speaking/"),
                  ("Presentation Skills – LinkedIn Learning", "https://www.linkedin.com/learning/topics/presentations")],
    },
    "Sales & Negotiation": {
        "free":  [("HubSpot Sales Cert",             "https://academy.hubspot.com/courses/sales-enablement"),
                  ("Yale Negotiation (Coursera Audit)", "https://www.coursera.org/learn/negotiation"),
                  ("Alison Sales Management",        "https://alison.com/courses/sales")],
        "paid":  [("Sales Training – Udemy",         "https://www.udemy.com/topic/sales/"),
                  ("Salesforce Trailhead",            "https://trailhead.salesforce.com/")],
    },
    "Cloud Computing (AWS/Azure)": {
        "free":  [("AWS Skill Builder (Free Tier)",  "https://skillbuilder.aws/"),
                  ("Microsoft Learn – Azure",        "https://learn.microsoft.com/en-us/training/azure/"),
                  ("freeCodeCamp Cloud Cert Prep",   "https://www.freecodecamp.org/news/tag/cloud-computing/")],
        "paid":  [("AWS Certified Solutions Arch – Udemy", "https://www.udemy.com/course/aws-certified-solutions-architect-associate-saa-c03/"),
                  ("AZ-900 Azure Fundamentals – Udemy", "https://www.udemy.com/course/az900-azure/")],
    },
    "Cybersecurity": {
        "free":  [("Google Cybersecurity Cert (Coursera Audit)", "https://www.coursera.org/professional-certificates/google-cybersecurity"),
                  ("TryHackMe Free Rooms",           "https://tryhackme.com/"),
                  ("Cybrary Free Courses",            "https://www.cybrary.it/catalog/free/")],
        "paid":  [("CompTIA Security+ Prep – Udemy", "https://www.udemy.com/course/securityplus/"),
                  ("CISSP Prep – LinkedIn Learning", "https://www.linkedin.com/learning/topics/cybersecurity")],
    },
    "DevOps": {
        "free":  [("KodeKloud Free Labs",             "https://kodekloud.com/courses/"),
                  ("Linux Foundation Free Courses",  "https://training.linuxfoundation.org/resources/free-courses/"),
                  ("freeCodeCamp DevOps Handbook",   "https://www.freecodecamp.org/news/tag/devops/")],
        "paid":  [("DevOps Bootcamp – Udemy",        "https://www.udemy.com/course/learn-devops-ci-cd-with-jenkins-using-pipelines-and-docker/"),
                  ("Kubernetes – Linux Foundation",  "https://training.linuxfoundation.org/certification/certified-kubernetes-administrator-cka/")],
    },
    "Mobile App Development": {
        "free":  [("Flutter Docs & Codelabs",        "https://docs.flutter.dev/get-started/codelab"),
                  ("Android Developers Training",    "https://developer.android.com/courses"),
                  ("Apple SwiftUI Tutorials",        "https://developer.apple.com/tutorials/swiftui")],
        "paid":  [("iOS & Swift Bootcamp – Udemy",   "https://www.udemy.com/course/ios-13-app-development-bootcamp/"),
                  ("Flutter & Dart – Udemy",         "https://www.udemy.com/course/flutter-bootcamp-with-dart/")],
    },
    "Agile Methodologies": {
        "free":  [("Scrum.org Free Resources",       "https://www.scrum.org/resources"),
                  ("Atlassian Agile Coach",           "https://www.atlassian.com/agile"),
                  ("Coursera Agile (Audit)",          "https://www.coursera.org/learn/agile-development")],
        "paid":  [("PMI-ACP Prep – Udemy",            "https://www.udemy.com/topic/agile/"),
                  ("SAFe Agile Training",             "https://scaledagile.com/training/")],
    },
    "Content Strategy": {
        "free":  [("HubSpot Content Marketing Cert", "https://academy.hubspot.com/courses/content-marketing"),
                  ("Copyblogger Free Resources",     "https://copyblogger.com/"),
                  ("Content Marketing Inst. Blog",   "https://contentmarketinginstitute.com/blog/")],
        "paid":  [("Content Strategy – Udemy",       "https://www.udemy.com/topic/content-strategy/"),
                  ("Content Marketing – Coursera",   "https://www.coursera.org/specializations/content-marketing")],
    },
    "Foreign Languages": {
        "free":  [("Duolingo",                       "https://www.duolingo.com/"),
                  ("BBC Languages",                  "https://www.bbc.co.uk/languages/"),
                  ("LanguageTransfer",               "https://www.languagetransfer.org/")],
        "paid":  [("Babbel",                         "https://www.babbel.com/"),
                  ("Rosetta Stone",                  "https://www.rosettastone.com/")],
    },
    "Video Editing": {
        "free":  [("DaVinci Resolve Tutorials – Blackmagic", "https://www.blackmagicdesign.com/products/davinciresolve/training"),
                  ("freeCodeCamp Video Editing",     "https://www.freecodecamp.org/news/learn-video-editing/"),
                  ("YouTube Creator Academy",        "https://creatoracademy.youtube.com/")],
        "paid":  [("Video Editing Masterclass – Udemy", "https://www.udemy.com/topic/video-editing/"),
                  ("Premiere Pro – LinkedIn Learning", "https://www.linkedin.com/learning/topics/premiere-pro")],
    },
    "Human Resources": {
        "free":  [("SHRM Free Resources",            "https://www.shrm.org/resourcesandtools/"),
                  ("Alison HR Management",           "https://alison.com/courses/human-resources"),
                  ("Coursera HR (Audit)",            "https://www.coursera.org/specializations/human-resource-management")],
        "paid":  [("HR Management – Udemy",          "https://www.udemy.com/topic/human-resources/"),
                  ("SHRM-CP Exam Prep",              "https://www.shrm.org/certification/")],
    },
    "Network Administration": {
        "free":  [("Cisco NetAcad Free Courses",     "https://www.netacad.com/courses/networking"),
                  ("Professor Messer CompTIA N+",    "https://www.professormesser.com/network-plus/n10-008/n10-008-video/n10-008-training-course/"),
                  ("freeCodeCamp Networking",        "https://www.freecodecamp.org/news/tag/networking/")],
        "paid":  [("CompTIA Network+ – Udemy",       "https://www.udemy.com/course/comptia-network-n10-007-the-total-course/"),
                  ("CCNA Prep – Cisco",              "https://www.cisco.com/c/en/us/training-events/training-certifications/certifications/associate/ccna.html")],
    },
}
