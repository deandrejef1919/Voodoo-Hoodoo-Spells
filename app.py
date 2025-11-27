import sqlite3
import textwrap
from datetime import datetime
from typing import List, Dict

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Voodoo & Hoodoo Spells",
    page_icon="🕯️",
    layout="wide",
)

# =========================
# THEME & STYLES (Times New Roman, bigger, shield buttons)
# =========================

APP_CSS = """
<style>
body, .stApp {
    background-color: #080808;
    color: #f3eee5;
    font-family: "Times New Roman", Times, serif;
    font-size: 16px;
    line-height: 1.7;
}

.block-container {
    padding-top: 1.5rem;
    max-width: 1100px;
}

/* Header */
.vh-header {
    text-align:center;
    padding: 0.75rem 0 0.25rem 0;
}
.vh-logo {
    font-size: 3.6rem;
}
.vh-title {
    font-size: 2.3rem;
    font-weight: 800;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #f44336;
    text-shadow:
        0 0 10px rgba(244,67,54,0.9),
        0 0 16px rgba(0,0,0,0.9);
}
.vh-subtitle {
    font-size: 1rem;
    opacity: 0.95;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: radial-gradient(circle at top, #2f0202 0%, #080808 55%, #000000 100%);
}
.sidebar-logo {
    text-align:center;
    font-size: 1rem;
    font-weight: 700;
    margin: 0.75rem 0 1.2rem 0;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    padding: 0.6rem 0.4rem;
    border-radius: 14px;
    background: radial-gradient(circle at 30% 0%, #3b0000 0%, #080808 55%, #000 100%);
    border: 1px solid rgba(244,67,54,0.7);
    box-shadow:
        0 0 10px rgba(244,67,54,0.6),
        0 0 18px rgba(0,0,0,0.9),
        inset 0 0 6px rgba(0,0,0,0.7);
}

/* Cards */
.vh-card {
    border-radius: 16px;
    border: 1px solid rgba(244,67,54,0.75);
    padding: 1.2rem 1.45rem;
    margin-bottom: 1.1rem;
    background: radial-gradient(circle at top, #191313 0%, #090808 55%, #010101 100%);
    box-shadow:
        0 0 12px rgba(244,67,54,0.45),
        0 0 26px rgba(0,0,0,0.98);
}
.vh-card h3 {
    margin-top: 0;
}

/* Typography tweaks */
.vh-card p,
p, li {
    font-size: 16px;
    line-height: 1.7;
}
h2, h3, h4 {
    font-family: "Times New Roman", Times, serif;
}

/* Shield glow animation */
@keyframes shieldGlow {
    0% {
        box-shadow:
            0 0 10px rgba(244,67,54,0.9),
            0 0 18px rgba(76,175,80,0.7),
            0 0 0 rgba(0,0,0,0.8);
    }
    100% {
        box-shadow:
            0 0 18px rgba(244,67,54,1.0),
            0 0 28px rgba(76,175,80,0.9),
            0 0 12px rgba(0,0,0,0.9);
    }
}

/* Buttons styled like glowing Zulu shields with spear motif */
div.stButton > button {
    border-radius: 999px / 70px;  /* tall oval like a shield */
    border-width: 2px;
    border-style: solid;
    border-color: #1b5e20;
    padding: 0.45rem 1.9rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.09em;
    font-family: "Times New Roman", Times, serif;
    font-size: 15px;

    background-image:
        linear-gradient(135deg, #f44336 0%, #000000 40%, #1b5e20 100%),
        radial-gradient(circle at 12% 0%, rgba(255,255,255,0.25) 0%, transparent 60%);
    background-blend-mode: overlay;

    color: #fff7ec;
    animation: shieldGlow 2.4s ease-in-out infinite alternate;
    transform: translateY(0);
}
div.stButton > button::before {
    content: "🛡️";
    margin-right: 0.35rem;
    text-shadow:
        0 0 6px rgba(244,67,54,0.9),
        0 0 10px rgba(0,0,0,0.7);
}
div.stButton > button:hover {
    border-color: #f44336;
    transform: translateY(-2px);
}

/* Footer */
.vh-footer {
    text-align:center;
    font-size: 0.9rem;
    color: #c0bbb2;
    margin-top: 2.8rem;
    padding-top: 0.9rem;
    border-top: 1px solid rgba(76,175,80,0.7);
    opacity: 0.95;
}

/* Accent pill */
.vh-pill {
    display:inline-block;
    padding: 0.18rem 0.6rem;
    border-radius: 999px;
    font-size: 0.78rem;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    border: 1px solid rgba(76,175,80,0.9);
    color: #e0f2f1;
}
</style>
"""
st.markdown(APP_CSS, unsafe_allow_html=True)


# =========================
# Helpers
# =========================

def safe_rerun():
    if hasattr(st, "rerun"):
        st.rerun()
    elif hasattr(st, "experimental_rerun"):
        st.experimental_rerun()


DB_PATH = "voodoo_hoodoo_spells.db"


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS spirits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            tradition TEXT,
            type TEXT,
            domains TEXT,
            colors TEXT,
            symbols TEXT,
            description TEXT
        )
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS workings_templates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT,
            tradition_flavor TEXT,
            intention TEXT,
            symbolism TEXT,
            script TEXT,
            ethical_note TEXT
        )
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS journal_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            title TEXT,
            tradition_context TEXT,
            intention TEXT,
            details TEXT,
            dreams_signs TEXT,
            feelings_before TEXT,
            feelings_after TEXT,
            notes TEXT
        )
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS resources (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            res_type TEXT,
            tradition_focus TEXT,
            level TEXT,
            link TEXT,
            notes TEXT
        )
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS suppliers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            shop_type TEXT,
            tradition_focus TEXT,
            owned_by_diaspora INTEGER DEFAULT 0,
            country TEXT,
            region TEXT,
            url TEXT,
            ships_to TEXT,
            notes TEXT
        )
        """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS supply_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT,
            tradition_usage TEXT,
            shop_id INTEGER,
            working_category TEXT,
            notes TEXT,
            FOREIGN KEY (shop_id) REFERENCES suppliers (id)
        )
        """
    )

    conn.commit()

    cur.execute("SELECT COUNT(*) FROM spirits")
    if cur.fetchone()[0] == 0:
        seed_spirits(cur)

    cur.execute("SELECT COUNT(*) FROM workings_templates")
    if cur.fetchone()[0] == 0:
        seed_workings(cur)

    cur.execute("SELECT COUNT(*) FROM resources")
    if cur.fetchone()[0] == 0:
        seed_resources(cur)

    conn.commit()
    conn.close()


# =========================
# Seed data
# =========================

def seed_spirits(cur):
    spirits_data = [
        # West African Vodun
        (
            "Nana Buluku",
            "Fon / West African Vodun",
            "Primordial Creator",
            "creation, cosmic order, origin",
            "white, deep blue, night-sky tones",
            "cosmic egg, night sky, stars",
            "Nana Buluku is honored in some West African Vodun lineages as a primordial creator figure. "
            "In many tellings, Nana Buluku precedes or gives birth to twin forces such as Mawu and Lisa. "
            "Different houses describe this being with different genders or as beyond gender, which reminds us that "
            "divine origin cannot be locked into one narrow image. Beginning your path with Nana Buluku centers the deep "
            "African root beneath later Vodou, Voodoo, and Hoodoo expressions."
        ),
        (
            "Mawu-Lisa",
            "Fon / West African Vodun",
            "Divine Twin Principle",
            "balance, moon and sun, coolness and heat",
            "white, gold, silver",
            "sun and moon together",
            "Mawu-Lisa is a twin divinity concept in some Vodun traditions. Mawu is often associated with the coolness of the moon, "
            "night, and rest; Lisa with the heat of the sun, day, and work. Together they embody a living balance: softness and strength, "
            "darkness and light, stillness and motion. They show that harmony comes from relationship, not from one-sided power."
        ),

        # Haitian Vodou lwa
        (
            "Papa Legba",
            "Haitian Vodou – Lwa",
            "Gatekeeper at the Crossroads",
            "thresholds, messages, beginnings, communication",
            "red, black, sometimes yellow",
            "crossroads, cane, keys, old man at the gate",
            "Papa Legba is one of the most widely known lwa (often spelled 'loa' in older sources). He stands at the crossroads, opening "
            "and closing the way between humans and the spirit world. In many houses he is greeted first, because without the key, the "
            "door does not open. He can embody the wisdom of age, the humor of a trickster, and the responsibility of carrying messages. "
            "Every lineage has its own songs, offerings, and ways of serving him; this profile is for orientation only, not instruction."
        ),
        (
            "Damballa",
            "Haitian Vodou – Lwa",
            "Serpent Creator Spirit",
            "purity, blessing, creation, rivers",
            "white, pale blue, silver",
            "serpent, water, sky arch",
            "Damballa is often envisioned as a great serpent that arches across sky and earth. His presence is linked with purity, blessing, "
            "and the quiet power of creation. In many houses, Damballa is approached softly: cool water, white cloth, silence or gentle song. "
            "Children and new beginnings are often associated with his blessings."
        ),
        (
            "Ayida Wedo",
            "Haitian Vodou – Lwa",
            "Rainbow Serpent",
            "rainbow, harmony, balance, union of forces",
            "rainbow colors, white, blue",
            "rainbow serpent, arch of light",
            "Ayida Wedo is sometimes paired with Damballa as the rainbow serpent, streaming color and movement through creation. "
            "She can symbolize harmony between forces that appear opposite: rain and sun, earth and sky, body and spirit."
        ),
        (
            "Marassa (Divine Twins)",
            "Haitian Vodou – Lwa",
            "Sacred Twins",
            "mystery, balance, paradox, children",
            "white, pastel colors (varies)",
            "twins, paired symbols, double offerings",
            "The Marassa are divine twins – and in some teachings, more-than-two – representing mystery and paradox. They are closely connected with children "
            "and with the sacredness of the child-mind. They remind people that spirit is not always either/or; it can be both/and."
        ),
        (
            "Ezili Freda",
            "Haitian Vodou – Lwa",
            "Lwa of Refined Love & Desire",
            "romantic love, elegance, beauty, longing",
            "pink, white, light blue, gold",
            "hearts, perfumes, fine cloth, mirrors",
            "Ezili Freda is associated with romance, luxury, delicate feelings, and the ache of longing. She loves beauty, fine things, and heartfelt emotion. "
            "But her path also teaches that fantasies often clash with reality; the tears of Freda remind devotees that idealized love can wound when it meets human limitation."
        ),
        (
            "Ezili Dantò",
            "Haitian Vodou – Lwa",
            "Protective Mother & Warrior",
            "mothers, fierce protection, justice, the marginalized",
            "red, blue, sometimes dark colors",
            "icon of Black Madonna, scars, knives, heart",
            "Ezili Dantò is a fierce, scarred mother who fights for children, working people, and those pushed to the edges of society. "
            "She is associated with rage against injustice and with the toughness required to survive violence and poverty. "
            "Her energy is nurturing, but not soft: she holds a knife as well as a child."
        ),
        (
            "Ogou (Ogou Feray and related)",
            "Haitian Vodou – Lwa",
            "Warrior & Iron Lwa",
            "iron, war, work, tools, discipline, struggle",
            "red, blue, metallic tones",
            "iron tools, machetes, flags",
            "The family of Ogou lwa is linked with iron, tools, soldiers, blacksmiths, and the fire of struggle. Ogou energy can feel like sharp focus, discipline, "
            "and a willingness to fight for integrity. In the Haitian Revolution, warrior lwa like Ogou are remembered in songs and stories about resistance."
        ),
        (
            "Baron Samedi",
            "Haitian Vodou – Lwa",
            "Lwa of the Cemetery & Crossing",
            "ancestors, death, boundary between worlds, irreverent humor",
            "black, purple, white, sometimes top-hat imagery",
            "top hat, cane, sunglasses, cross, cemetery symbols",
            "Baron Samedi stands at the gate of the cemetery. He watches over the dead and the moment of crossing between life and death. "
            "He is famous for raw humor, sexual jokes, and a style that shocks the polite. Underneath the theatrics, he reminds people that death is certain, "
            "so they should truly live and not waste their time on earth."
        ),
        (
            "Gede (Family of Spirits)",
            "Haitian Vodou – Lwa",
            "Spirits of the Dead & Raw Truth",
            "ancestors, sex and death, laughter, healing through honesty",
            "black, purple, white",
            "sunglasses, skulls, cigarettes, hot peppers",
            "The Gede are a wild, loving family of spirits connected with the dead and with the truths we are afraid to say. "
            "They use laughter, obscenity, and shock to break denial and bring healing where secrets have rotted. "
            "Their season in Haiti around All Saints / All Souls is full of vivid altars, dance, and graveyard visits."
        ),
        (
            "Loko",
            "Haitian Vodou – Lwa",
            "Lwa of Trees & Priesthood",
            "sacred trees, initiation, order in ritual",
            "green, white",
            "staff, trees, leaves",
            "Loko is linked with sacred trees, the stability of priesthood, and the structure of ritual life. In some houses he is understood as a guardian of how things are properly done: "
            "the rules, the boundaries, the lines that keep a temple coherent over generations."
        ),
        (
            "Ayizan",
            "Haitian Vodou – Lwa",
            "Market & Initiation Lwa",
            "markets, initiation, sacred veiling, thresholds",
            "white, gold",
            "palm fronds, veils, marketplaces",
            "Ayizan is connected with marketplaces, trade, and the veiling of sacred mysteries. She protects initiatory knowledge and the process of 'going behind the veil' "
            "for those who are truly called and properly prepared."
        ),

        # Ancestors
        (
            "Ancestors",
            "Many Traditions",
            "Collective Dead / Ancestors",
            "memory, guidance, protection, lineage",
            "white, candlelight colors",
            "glass of water, photos, names",
            "Ancestor veneration is central to many African and Diaspora traditions. The ancestors are the beloved dead of our bloodlines and of our chosen spiritual families. "
            "Many people keep a glass of water, a candle, and photos or names to honor them, tell their stories, and ask for guidance. "
            "This app encourages respectful remembrance and healing for the lineage, not attempts to control the dead."
        ),
    ]
    cur.executemany(
        """
        INSERT INTO spirits (name, tradition, type, domains, colors, symbols, description)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        spirits_data,
    )


def seed_workings(cur):
    workings = [
        (
            "Cleansing Bath Template",
            "Cleansing",
            "Hoodoo / General Diaspora",
            "Gently cleanse heavy or stagnant energy and invite calm and clarity back into your body and mind.",
            "Water is used as a symbol of renewal and flow. Salt is often used as a purifier. Safe kitchen herbs like rosemary, basil, or chamomile can be used symbolically as helpers for clarity and peace. "
            "In many Diaspora traditions, baths are prayers in motion: as water runs off the skin, the old stories and burdens are invited to run off too.",
            "As this water touches me, I release what is heavy and no longer needed. May I be clean in mind, heart, and path. May what is truly mine remain, and what is not for me gently fall away.",
            "Do not use unknown herbs internally or on sensitive skin. This template is symbolic and should not replace medical or mental-health care. "
            "It is intended for gentle cleansing of the self, not for blaming others or sending harm."
        ),
        (
            "Protection Candle Template",
            "Protection",
            "Hoodoo / Vodou-inspired",
            "Create a sense of spiritual protection and safety around yourself or your space while keeping your ethics clean.",
            "Candles can be treated as a small standing light of protection. A circle drawn around the candle or imagined in the mind can represent a boundary. "
            "White candles are often used as all-purpose lights when specific colors are not available. In many traditions, protection work is paired with common sense: locking doors, choosing good company, and saying no.",
            "Let this flame stand as a small guardian for me and those I love. May harm be turned away, and may what is safe, honest, and good be welcomed. I ask for protection that does not require anyone else to be hurt.",
            "This working is focused on protective boundaries and safety. It is not meant as a weapon. Fire is dangerous in the physical world, so never leave candles unattended or near flammable items."
        ),
        (
            "Road Opening / Opportunity Template",
            "Road Opening",
            "Vodou-inspired / Crossroads Symbolism",
            "Ask for supportive openings in work, study, relationships, or housing while you also take practical steps.",
            "Crossroads and keys are often used to symbolize decisions and opportunities. In many traditions, crossroads spirits are petitioned to open good roads. "
            "In this template we focus on asking for right opportunities while you commit to real-world effort: applications, trainings, conversations, and wise risks.",
            "May good roads open before me in the area of my life I am working on now. May paths that are truly mine become clearer, and paths that would harm me close gently. "
            "Guide my steps so that I meet honest chances and do my part with courage.",
            "This template is meant to work together with concrete actions: applying for jobs, practicing skills, having honest conversations. It is not a guarantee of specific outcomes and is not meant to override anyone else's free will."
        ),
        (
            "Prosperity & Work Blessing Template",
            "Prosperity",
            "Hoodoo / General",
            "Bless your honest work, study, and planning around money, inviting stability, wise choices, and fair exchange.",
            "Green, gold, seeds, and coins are common prosperity symbols. In Hoodoo and related traditions, money-drawing work is often paired with very practical steps: budgeting, saving, debt repair, and skill-building. "
            "The focus is on fair, honest prosperity rather than quick schemes.",
            "Bless the work of my hands and the plans I build. May opportunities to earn honestly and fairly come into my life. "
            "May I use what I receive with wisdom, care, and generosity, and remember that money is a tool, not my master.",
            "This template does not promise riches. It supports steady effort, learning, and wiser choices. Do not use it to excuse risky financial behavior or to avoid asking for real-world help from advisors when needed."
        ),
        (
            "Self-Love & Confidence Working",
            "Self-Love",
            "Diaspora / General",
            "Nurture a kinder relationship with yourself and strengthen your sense of worth, especially if old messages tried to crush you.",
            "Mirrors, gentle colors, and sweet scents are often used to represent self-love. Many Diaspora traditions emphasize that each person carries ancestors and spirit with them; "
            "to hate yourself is to insult those who walked before you. Self-love work is therefore not vanity but a way of honoring the life you were given.",
            "I release the story that I am unworthy of love and respect. Little by little, may I see myself with clearer, kinder eyes. "
            "May I walk with more confidence in who I truly am, while staying humble and open to growth.",
            "This working is about inner kindness, not arrogance. It may be helpful alongside therapy, self-help work, or support groups. "
            "If self-hatred or despair feels overwhelming, please seek professional support."
        ),
        (
            "Ancestor Connection Time",
            "Ancestor",
            "Vodun / Vodou / Hoodoo",
            "Set aside quiet time to remember and honor your ancestors or beloved dead and to notice how their stories live in you.",
            "A glass of water, a candle, and photos or written names are common elements of ancestor remembrance. In many cultures, the dead are honored with food, song, and stories. "
            "This template focuses on thanks, listening, and healing, not on controlling or forcing the dead to act.",
            "To the ancestors who walked before me, known and unknown, I thank you for the life that reaches me through you. "
            "May I live in a way that honors your strength and wisdom. Where there was harm or trauma, may healing move through the lineage.",
            "Ancestor work can bring up grief and complex family history. Go gently, and seek support if difficult memories arise. "
            "This template is for remembrance and gratitude, not for summoning or commanding spirits."
        ),
        (
            "Clarity & Signs Journal Prompt",
            "Clarity",
            "General / Introspective",
            "Create a space to notice patterns, dreams, and subtle signs over time without falling into fear or obsession.",
            "Many spiritual paths pay attention to repeating symbols, dreams, or feelings as possible messages. Journaling helps organize these impressions and keeps your feet on the ground. "
            "You can review your notes later and see what was meaningful and what was just noise.",
            "Over the coming days, may I notice what repeats or stands out, without forcing a meaning. May I be guided toward clarity step by step, and may I check my insights against common sense and wise counsel.",
            "This template encourages reflection, not obsession. If you feel overwhelmed or frightened by signs or dreams, you may want to talk with a trusted person or professional rather than interpret everything alone."
        ),
    ]

    cur.executemany(
        """
        INSERT INTO workings_templates
        (name, category, tradition_flavor, intention, symbolism, script, ethical_note)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        workings,
    )


def seed_resources(cur):
    resources = [
        (
            "Introductory Reading on West African Vodun",
            "Book",
            "West African Vodun",
            "Intro",
            "",
            "Look for works by scholars or initiates writing about Vodun in Benin, Togo, and Ghana. Collections like museum catalogues and ethnographies that center local voices "
            "can help you see actual shrines and practice instead of horror clichés."
        ),
        (
            "Documentaries on Haitian Vodou (Practitioner-Focused)",
            "Documentary",
            "Haitian Vodou",
            "Intro",
            "",
            "Seek out documentaries where Houngans, Mambos, and community members speak for themselves, rather than films that turn Vodou into a monster story. "
            "Look for work focusing on theology, history, music, and everyday life."
        ),
        (
            "Books by African American Rootworkers",
            "Book",
            "Hoodoo / Rootwork",
            "Intro",
            "",
            "Classic and modern texts written by Black practitioners of Hoodoo/rootwork tend to be more grounded and less sensational than generic 'voodoo spell' books. "
            "They also situate the practice inside Black history, migration, and resistance."
        ),
        (
            "Local Botanicas & Curio Shops",
            "Practice",
            "Mixed",
            "Intro",
            "",
            "Visiting real botanicas, herb shops, and curio stores (respectfully) teaches you a lot about what people actually use: oils, baths, candles, colognes, roots, and church supplies. "
            "Support Black and Diaspora-owned shops when you can."
        ),
    ]
    cur.executemany(
        """
        INSERT INTO resources
        (title, res_type, tradition_focus, level, link, notes)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        resources,
    )


# =========================
# DB helpers
# =========================

def fetch_spirits() -> List[sqlite3.Row]:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM spirits ORDER BY tradition, name")
    rows = cur.fetchall()
    conn.close()
    return rows


def fetch_workings() -> List[sqlite3.Row]:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM workings_templates ORDER BY category, name")
    rows = cur.fetchall()
    conn.close()
    return rows


def fetch_resources() -> List[sqlite3.Row]:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM resources ORDER BY tradition_focus, title")
    rows = cur.fetchall()
    conn.close()
    return rows


def insert_journal_entry(
    title: str,
    tradition_context: str,
    intention: str,
    details: str,
    dreams_signs: str,
    feelings_before: str,
    feelings_after: str,
    notes: str,
):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO journal_entries
        (date, title, tradition_context, intention, details, dreams_signs,
         feelings_before, feelings_after, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            datetime.now().strftime("%Y-%m-%d"),
            title,
            tradition_context,
            intention,
            details,
            dreams_signs,
            feelings_before,
            feelings_after,
            notes,
        ),
    )
    conn.commit()

