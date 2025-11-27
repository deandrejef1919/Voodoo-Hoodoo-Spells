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

/* Slightly narrower content for readability */
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

/* Typography tweaks for readability */
.vh-card p,
p, li {
    font-size: 16px;
    line-height: 1.8;
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

/* Spear icon */
div.stButton > button::before {
    content: "⚔️";
    margin-right: 0.35rem;
    text-shadow:
        0 0 6px rgba(244,67,54,0.9),
        0 0 10px rgba(0,0,0,0.7);
}

/* Hover: stronger glow, tiny lift */
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

    # Spirits table
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

    # Workings templates
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

    # Journal
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

    # Study resources
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

    # Suppliers (shops)
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

    # Supply items
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

    # Seed if empty
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
# Seed data – deep descriptions
# =========================

def seed_spirits(cur):
    """
    Seed spirits including West African Vodun beings, Haitian Vodou lwa, and ancestors.
    This is educational only – no ritual instructions.
    """
    spirits_data = [
        # West African Vodun beings
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

        # Haitian Vodou lwa (Loas)
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
            "Children and new beginnings are often associated with his blessings. Here we honor those themes without exposing house-specific ritual secrets."
        ),
        (
            "Ayida Wedo",
            "Haitian Vodou – Lwa",
            "Rainbow Serpent",
            "rainbow, harmony, balance, union of forces",
            "rainbow colors, white, blue",
            "rainbow serpent, arch of light",
            "Ayida Wedo is sometimes paired with Damballa as the rainbow serpent, streaming color and movement through creation. "
            "She can symbolize harmony between forces that appear opposite: rain and sun, earth and sky, body and spirit. Many practitioners experience her "
            "as a principle of beauty, order, and relational balance."
        ),
        (
            "Marassa (Divine Twins)",
            "Haitian Vodou – Lwa",
            "Sacred Twins",
            "mystery, balance, paradox, children",
            "white, pastel colors (varies)",
            "twins, paired symbols, double offerings",
            "The Marassa are divine twins – and in some teachings, more-than-two – representing mystery and paradox. They are often served with paired offerings, "
            "reminding people that spirit can appear as both one and many at the same time. They are closely connected with children and with the sacredness of the child-mind."
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

        # Ancestors (general)
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
            "Look for works by scholars or initiates writing about Vodun in Benin, Togo, and Ghana. Collections like the Soul of Africa museum's Vodun material can help you see actual shrines and objects instead of horror clichés."
        ),
        (
            "Documentaries on Haitian Vodou (Practitioner-Focused)",
            "Documentary",
            "Haitian Vodou",
            "Intro",
            "",
            "Seek out documentaries where Houngans, Mambos, and community members speak for themselves, rather than films that turn Vodou into a monster story. Look for work focusing on theology, history, and everyday practice."
        ),
        (
            "Books by African American Rootworkers",
            "Book",
            "Hoodoo / Rootwork",
            "Intro",
            "",
            "Classic and modern texts written by Black practitioners of Hoodoo/rootwork tend to be more grounded and less sensational than generic 'voodoo spell' books. They also situate the practice inside Black history."
        ),
        (
            "Local Botanicas & Curio Shops",
            "Practice",
            "Mixed",
            "Intro",
            "",
            "Visiting real botanicas, herb shops, and curio stores (respectfully) teaches you a lot about what people actually use: oils, baths, candles, colognes, roots, and church supplies. Support Black and Diaspora-owned shops when you can."
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
# DB fetch/insert helpers
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
    conn.close()


def fetch_journal_entries() -> pd.DataFrame:
    conn = get_conn()
    df = pd.read_sql_query(
        "SELECT * FROM journal_entries ORDER BY date DESC, id DESC", conn
    )
    conn.close()
    return df


def insert_supplier(
    name: str,
    shop_type: str,
    tradition_focus: str,
    owned_by_diaspora: bool,
    country: str,
    region: str,
    url: str,
    ships_to: str,
    notes: str,
):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO suppliers
        (name, shop_type, tradition_focus, owned_by_diaspora,
         country, region, url, ships_to, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            name,
            shop_type,
            tradition_focus,
            1 if owned_by_diaspora else 0,
            country,
            region,
            url,
            ships_to,
            notes,
        ),
    )
    conn.commit()
    conn.close()


def fetch_suppliers() -> List[sqlite3.Row]:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM suppliers ORDER BY name")
    rows = cur.fetchall()
    conn.close()
    return rows


def insert_supply_item(
    name: str,
    category: str,
    tradition_usage: str,
    shop_id: int,
    working_category: str,
    notes: str,
):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO supply_items
        (name, category, tradition_usage, shop_id, working_category, notes)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (name, category, tradition_usage, shop_id, working_category, notes),
    )
    conn.commit()
    conn.close()


def fetch_supply_items() -> pd.DataFrame:
    conn = get_conn()
    df = pd.read_sql_query(
        """
        SELECT
            i.id,
            i.name,
            i.category,
            i.tradition_usage,
            i.working_category,
            i.notes,
            s.name AS shop_name,
            s.country AS shop_country
        FROM supply_items i
        LEFT JOIN suppliers s ON i.shop_id = s.id
        ORDER BY i.name
        """,
        conn,
    )
    conn.close()
    return df


# =========================
# UI helpers
# =========================

def render_header():
    st.markdown(
        """
        <div class="vh-header">
            <div class="vh-logo">🕯️</div>
            <div class="vh-title">VOODOO & HOODOO SPELLS</div>
            <div class="vh-subtitle">
                A respectful path through Vodun, Vodou, Voodoo, Hoodoo, lwa and ancestors.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("---")


def render_footer():
    st.markdown(
        """
        <div class="vh-footer">
            This app is for educational and reflective purposes only and does not replace clergy,
            mental-health care, or professional advice. Walk gently, and use it to support healing,
            protection, justice, and growth — never harm.
        </div>
        """,
        unsafe_allow_html=True,
    )


# =========================
# Pages
# =========================

def page_nana_buluku():
    render_header()
    col1, col2 = st.columns([1.4, 1])

    with col1:
        st.markdown(
            """
            <div class="vh-card">
                <h3>Beginning with Nana Buluku – Root Before Branch</h3>
                <p>
                    In some West African Vodun lineages, <strong>Nana Buluku</strong> is honored as a primordial
                    creator figure – the dark, deep, original presence from which other forces of creation emerge.
                    Depending on the house, Nana Buluku may be spoken of as mother, as beyond gender, or in ways that
                    cannot be mapped to European ideas of “god” at all. This reminds us that we are stepping into
                    a spiritual universe with its own language and logic.
                </p>
                <p>
                    By starting your app with Nana Buluku, you are making a clear statement:
                    this path does not begin in Hollywood horror. It begins in <strong>Africa</strong>, with
                    a cosmology that survived kidnapping, ships, sugar plantations, and centuries of disrespect.
                </p>
                <p>
                    From this root, different branches grow:
                </p>
                <ul>
                    <li><strong>West African Vodun</strong> in Benin, Togo, Ghana and beyond.</li>
                    <li><strong>Haitian Vodou</strong>, braided with Catholic and Indigenous elements, forged in revolution.</li>
                    <li><strong>Louisiana Voodoo</strong>, carrying Creole history and figures like Marie Laveau.</li>
                    <li><strong>Hoodoo / Rootwork</strong> in the US South, focused on survival, justice, and everyday life.</li>
                </ul>
                <p>
                    <span class="vh-pill">intention</span>
                    This app is a companion for your study and practice, not a replacement for elders, temples,
                    or churches. It leans toward <em>cleansing, protection, uncrossing, justice, prosperity, self-healing,
                    and ancestor remembrance</em>. Harmful work is discussed only as history, not as how-to.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        nana_img_url = st.secrets.get("NANA_BULUKU_IMAGE_URL", "")
        nana_vid_url = st.secrets.get("NANA_BULUKU_VIDEO_URL", "")
        if nana_img_url or nana_vid_url:
            with st.expander("Nana Buluku – Visuals (configure in secrets.toml)"):
                if nana_img_url:
                    st.image(nana_img_url, caption="Nana Buluku inspired art / shrine", use_column_width=True)
                if nana_vid_url:
                    st.video(nana_vid_url)
        else:
            st.info(
                "Tip: add NANA_BULUKU_IMAGE_URL and NANA_BULUKU_VIDEO_URL to your Streamlit secrets "
                "to show authentic art or video here and make this opening feel alive."
            )

    with col2:
        st.markdown(
            """
            <div class="vh-card">
                <h3>Opening Intention for Your Work</h3>
                <p>
                    You can adapt the words below as a quiet opening whenever you start a session with this app:
                </p>
                <blockquote>
                    May I remember the ancestors and nations whose blood, language, and music carried these ways. <br/>
                    May I step carefully, with respect and humility, not hunger and ego. <br/>
                    May any work I do be aligned with healing, protection, just truth, and growth — never harm. <br/>
                    May I be kept from fantasy and delusion, and brought closer to what is real and helpful.
                </blockquote>
                <p>
                    When you are ready, choose where to go next in your path:
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("")
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("📜 Origins & History"):
                st.session_state["vh_page"] = "Origins & History"
                safe_rerun()
        with col_b:
            if st.button("📓 Journal & Signs"):
                st.session_state["vh_page"] = "Journal & Signs"
                safe_rerun()

    render_footer()


def page_history():
    render_header()
    st.subheader("Origins & History – From Vodun to Vodou, Voodoo & Hoodoo")

    # --- WEST AFRICAN VODUN ---
    st.markdown(
        """
        ### West African Vodun / Vodún – The Root in the Soil

        West African Vodun is not one single, frozen religion. It is a **family of living traditions**
        practiced among Fon, Ewe, and related peoples in what is now Benin, Togo, Ghana, and parts of Nigeria.
        These traditions developed long before colonization, and they are still alive today in shrines, villages,
        cities, and diasporic communities.

        At the heart of Vodun is a layered spiritual universe. Many lineages recognize:

        - **A creator or high god** – such as Nana Buluku or the twin principle Mawu-Lisa – not always
          approached directly every day, but understood as the deep source of existence.  
        - A rich community of **spirits (vodun)** – forces connected to the sea, rivers, thunder, earth,
          forests, iron, fertility, healing, justice, and more. Each has its own songs, taboos, offerings,
          drum rhythms, and way of moving through the world.  
        - The **ancestors** – family dead, community heroes, and clan founders who continue to watch,
          advise, and sometimes correct the living. The line between “living” and “ancestors” is a door,
          not a wall.

        Ritual life in Vodun includes drumming, call-and-response singing, dance, divination, spirit possession,
        herbal medicine, masks, carved figures, and shrines built for particular vodun. Different villages and
        families may serve the same spirit in very different ways: one town might know a thunder spirit as fierce
        and hot, while another house emphasizes its protective side. There is no single book that defines Vodun.
        It is carried in **elders, drums, bodies, and community memory**.

        Divination is a central pillar. Systems such as **Fa** (or Afa), cowrie-shell casting, and other
        methods are used to read the pattern of a situation, diagnose spiritual causes of illness or misfortune,
        and ask which vodun are speaking. A good diviner does not just predict; they interpret, advise, and help
        a person find the equilibrium between their destiny and their choices.

        Vodun is also deeply tied to **place**. Sacred groves, rivers, crossroads, old trees, and family
        compounds are not just scenery – they are living locations where spirits dwell and where offerings,
        festivals, and healing work happen. Many shrines are simple and earth-based, not “grand temples,” which
        is why outsiders miss them: a clay pot under a tree, a stone, a post, or a mound can be a doorway
        between worlds.

        When enslavers tore people from the Bight of Benin and surrounding coasts, they could not fully tear out
        Vodun. The prayers, songs, drum patterns, and spiritual logic of Vodun travelled in people’s bodies and
        memories into the Caribbean and the Americas. From these roots grew:
        **Haitian Vodou, Louisiana Voodoo, Cuban and Brazilian traditions, and African American Hoodoo**.
        Each branch looks different, but the root in the soil is still West African.
        """
    )

    # --- HAITIAN VODOU & 1791 ---
    st.markdown(
        """
        ### Haitian Vodou – 1791, Revolution, and the Lwa

        On the island now known as Haiti and the Dominican Republic, Africans from many nations were forced
        together in the French colony of Saint-Domingue. They brought Vodun, Yoruba and Kongo traditions,
        Mande and Igbo spirits, and more. Under the pressure of slavery, they braided these with Catholic
        imagery and Indigenous Caribbean influences. Out of that braiding emerged **Haitian Vodou**.

        In 1791, a powerful Vodou ceremony remembered at **Bois Caïman** is said to have helped ignite the
        uprising that began the Haitian Revolution. Over the next twelve years, enslaved and free Black
        Haitians fought France, then armies from other European powers. With leadership from figures like
        Toussaint Louverture and Dessalines, they defeated a world empire and founded the first Black republic
        of the modern era.

        In Haitian memory, this was not just a political war. It was also a spiritual war, walked by the
        **lwa** – spirits of war, justice, healing, and liberation. Drums, songs, possession, and oath-making
        gave people courage to rise against plantation owners and soldiers. To this day, Haitian Vodou carries
        that history of resistance inside its prayers and feasts.
        """
    )

    haitian_img = st.secrets.get("HAITI_VODOU_IMAGE_URL", "")
    haitian_vid = st.secrets.get("HAITI_VODOU_VIDEO_URL", "")
    if haitian_img or haitian_vid:
        with st.expander("Haitian Vodou – Visuals (configure in secrets.toml)"):
            if haitian_img:
                st.image(
                    haitian_img,
                    caption="Haitian Vodou altar / ceremony (respectful image)",
                    use_column_width=True,
                )
            if haitian_vid:
                st.video(haitian_vid)

    # --- NEW ORLEANS / MARIE LAVEAU ---
    st.markdown(
        """
        ### New Orleans & Louisiana Voodoo – Marie Laveau, Voodoo Queen

        In Louisiana, especially New Orleans, African, French, Spanish, Native American, and Caribbean
        influences met in a Creole city of markets, music, and strict race laws. Out of that mix arose
        **Louisiana Voodoo**, a regional spiritual practice that used Catholic saints, drums, rootwork,
        river water, and graveyard dirt.

        At the center of many stories stands **Marie Catherine Laveau** (1801–1881), often called the
        “Voodoo Queen of New Orleans.” She was a Creole woman, a hairdresser, an herbalist, and a
        spiritual worker. Wealthy white women came to her for help with love, inheritance, court cases,
        and social power. She listened to gossip in her salon, worked with servants and free people of
        color, and combined insight with spiritual work to advise her clients.

        Under her name and influence, New Orleans Voodoo involved:

        - **Gris-gris** bags (charm bags) for protection, love, luck, and court cases.  
        - Use of **Catholic saints and psalms** side by side with African-rooted methods.  
        - Public ceremonies at places like **Congo Square**, where drumming, dance, and possession met
          after church on Sundays.

        Over time, tourism and racism turned “Voodoo” into a spooky brand, but the real tradition is a
        Creole healing and power practice rooted in the survival of Black and Creole communities.
        """
    )

    nola_img = st.secrets.get("NEW_ORLEANS_IMAGE_URL", "")
    nola_vid = st.secrets.get("NEW_ORLEANS_VIDEO_URL", "")
    if nola_img or nola_vid:
        with st.expander("New Orleans Voodoo – Visuals (configure in secrets.toml)"):
            if nola_img:
                st.image(
                    nola_img,
                    caption="New Orleans Voodoo altar / Marie Laveau related imagery",
                    use_column_width=True,
                )
            if nola_vid:
                st.video(nola_vid)

    # --- HOODOO / ROOTWORK ---
    st.markdown(
        """
        ### Hoodoo / Rootwork / Conjure – Folk Magic of Black America

        Hoodoo, rootwork, or conjure is an African American folk magic system that arose primarily in the
        US South. It weaves together:

        - African understandings of roots, crossroads, ancestors, and spirit,  
        - Native American plant knowledge and land connection,  
        - European folk practices such as using psalms, talismans, and spiritual baths.

        Rootworkers historically helped people with:

        - protection from enemies and racist violence,  
        - love, reconciliation, and fertility,  
        - luck in business, gambling, and court cases,  
        - uncrossing and healing from spiritual attacks.

        Many rootworkers are deeply Christian and treat the Bible (especially the Psalms) as a powerful
        spiritual tool. Hoodoo has always been about **survival and justice** under oppressive systems,
        not about stage tricks. This app leans into that stream: protective, cleansing, and healing work,
        not cursing or domination.
        """
    )

    st.markdown(
        """
        ### Keeping Distinctions Clear

        - **Vodun / Vodun religions** – West African traditions with temples, priesthoods, and lineages.  
        - **Haitian Vodou** – Afro-Creole religion of Haiti, with lwa, temples, and complex theology.  
        - **Louisiana Voodoo** – regional Creole spiritual practice shaped by New Orleans history and figures like Marie Laveau.  
        - **Hoodoo / Rootwork** – African American folk-magic system focused on practical life problems, not a formal religion.

        Knowing the difference is part of respect.
        """
    )

    render_footer()


def page_spirits():
    render_header()
    st.subheader("Spirits, Lwa (Loas) & Ancestors – Deep Profiles")

    st.markdown(
        """
        In Haitian Vodou and related traditions, the spirits are often called **lwa** (older English
        sometimes writes “loas”). They are not vague energies but distinct beings with their own histories,
        styles, and preferences. Different houses know them differently, and serious service to them
        belongs inside those lineages.

        Think of this page as a **map to the names and themes**, not a secret manual. It helps you keep
        track of who is who as you read and watch more authentic sources.
        """
    )

    spirits = fetch_spirits()
    if not spirits:
        st.info("No spirit profiles found in the database.")
        render_footer()
        return

    by_tradition: Dict[str, List[sqlite3.Row]] = {}
    for s in spirits:
        by_tradition.setdefault(s["tradition"], []).append(s)

    for tradition, rows in by_tradition.items():
        st.markdown(f"### {tradition}")
        for s in rows:
            with st.expander(s["name"]):
                st.write(f"**Type:** {s['type']}")
                if s["domains"]:
                    st.write(f"**Domains:** {s['domains']}")
                if s["colors"]:
                    st.write(f"**Associated colors:** {s['colors']}")
                if s["symbols"]:
                    st.write(f"**Symbols:** {s['symbols']}")
                st.markdown("---")
                st.write(s["description"])

    render_footer()


def page_hoodoo_basics():
    render_header()
    st.subheader("Hoodoo / Rootwork Basics – Everyday Power")

    st.markdown(
        """
        Hoodoo is sometimes called **rootwork** or **conjure**. It is not the same as Haitian Vodou or
        Louisiana Voodoo, although it shares history with them. Hoodoo is the everyday spiritual technology
        of African American people, especially in the South, dealing with:
        """
    )
    st.markdown(
        """
        - staying safe in dangerous conditions,  
        - keeping a roof over your head,  
        - protecting your children,  
        - winning court cases and surviving the police,  
        - drawing love, healing, and luck into broken lives.
        """
    )

    st.markdown(
        """
        ### Typical Tools in Hoodoo

        - **Roots & Herbs**: High John, angelica, gravel root, devil’s shoe strings, and many others.  
        - **Minerals & Curios**: lodestones, coins, nails, railroad spikes, keys, dirt from specific places.  
        - **Candles**: fixed with oils, herbs, and prayers for a specific purpose.  
        - **Mojo Bags / Hands**: small charm bundles carried or worn for ongoing work.  
        - **Bible & Psalms**: read or recited as direct spiritual force.  
        - **Lamps, Baths, and Floor Washes**: used to clean, protect, and draw in certain conditions.
        """
    )

    st.markdown(
        """
        ### Harmful vs. Helpful Work

        Historically, some workers took jobs for revenge, coercion, or cursing. A full teaching of Hoodoo
        must admit this shadow. But you are choosing to build an app that aligns with **helpful** forms:

        - Uncrossing and cleansing,  
        - Protection and warding,  
        - Justice framed as truth and accountability,  
        - Money drawing tied to honest work,  
        - Love and reconciliation guided by consent.

        The Workings section in this app reflects that choice: it gives you templates that protect, clean,
        and empower without stepping into domination or harm.
        """
    )

    render_footer()


def page_workings():
    render_header()
    st.subheader("Workings & Ritual Templates – Non-Harmful Only")

    st.markdown(
        """
        This section gives you **detailed templates** that you can adapt to your own situation.
        Each one has:

        - a clear intention,  
        - symbolism (why these tools?),  
        - example words or prayers,  
        - and an ethical note.

        Use them as frameworks, not as rigid scripts. Your own words and conscience matter.
        """
    )

    workings = fetch_workings()
    if not workings:
        st.info("No workings templates found in the database.")
        render_footer()
        return

    categories = sorted({w["category"] for w in workings})
    cat_choice = st.selectbox("Choose a category", categories)
    options = [w for w in workings if w["category"] == cat_choice]

    names = [w["name"] for w in options]
    tmpl_name = st.selectbox("Choose a template", names)
    tmpl = next(w for w in options if w["name"] == tmpl_name)

    st.markdown("### Template Overview")
    col1, col2 = st.columns([1.4, 1])
    with col1:
        st.write(f"**Name:** {tmpl['name']}")
        st.write(f"**Category:** {tmpl['category']}")
        st.write(f"**Tradition flavor:** {tmpl['tradition_flavor']}")
        st.markdown("**Intention:**")
        st.write(tmpl["intention"])

        st.markdown("**Symbolism (why these elements):**")
        st.write(tmpl["symbolism"])

    with col2:
        st.markdown("**Example words / prayer:**")
        st.text_area(
            "Script example (read or adapt in your own words):",
            value=textwrap.fill(tmpl["script"], width=70),
            height=200,
        )
        st.markdown("**Ethical note:**")
        st.info(tmpl["ethical_note"])

    st.markdown("---")
    st.markdown("### Your Version of This Working")

    st.markdown(
        "Use this form to plan or record your own version of the working. You can store it into your journal."
    )

    with st.form("working_journal_form"):
        title = st.text_input("Title for this working in your journal")
        tradition_context = st.selectbox(
            "Tradition context",
            [
                "West African Vodun",
                "Haitian Vodou",
                "Louisiana Voodoo",
                "Hoodoo / Rootwork",
                "Ancestor Work",
                "Mixed / Unsure",
            ],
        )
        your_intention = st.text_area(
            "In your own words, what is your intention?",
            height=90,
        )
        details = st.text_area(
            "What did you (or will you) actually do? (tools, timing, location, actions)",
            height=130,
        )
        dreams_signs = st.text_area(
            "Any dreams, signs, or patterns you noticed before/after?",
            height=90,
        )
        feelings_before = st.text_area(
            "How did you feel before the working?",
            height=70,
        )
        feelings_after = st.text_area(
            "How did you feel after (or how do you hope to feel)?",
            height=70,
        )
        notes = st.text_area(
            "Any additional notes or reflections?",
            height=90,
        )

        submitted = st.form_submit_button("💾 Save to Journal")
        if submitted:
            if not title.strip():
                st.error("Please give this working a title for your journal.")
            else:
                combined_intention = f"{tmpl['name']} – {your_intention}".strip()
                insert_journal_entry(
                    title=title.strip(),
                    tradition_context=tradition_context,
                    intention=combined_intention,
                    details=details.strip(),
                    dreams_signs=dreams_signs.strip(),
                    feelings_before=feelings_before.strip(),
                    feelings_after=feelings_after.strip(),
                    notes=notes.strip(),
                )
                st.success("Saved to your journal.")

    st.markdown("---")
    st.markdown("### Supplies From Your List (Optional)")

    df_items = fetch_supply_items()
    if df_items.empty:
        st.info(
            "You have not added any supplies yet. Use the 'Supplies & Shops' tab to create your own list of herbs, candles, and other tools."
        )
    else:
        df_filtered = df_items.copy()
        df_filtered = df_filtered[
            df_filtered["working_category"].fillna("") == tmpl["category"]
        ]
        if df_filtered.empty:
            st.write(
                "You have no saved supplies tagged for this category yet. "
                "You can still perform a simple version of this working with basic items like clean water, a plain candle, or spoken words."
            )
        else:
            st.write(
                "These are supplies you have tagged for this category. You can choose to include some of them in your version of the working."
            )
            st.dataframe(
                df_filtered[
                    [
                        "name",
                        "category",
                        "tradition_usage",
                        "shop_name",
                        "shop_country",
                        "notes",
                    ]
                ]
            )

    render_footer()


def page_journal():
    render_header()
    st.subheader("Journal & Signs – Your Ongoing Path")

    st.markdown(
        """
        This page is where your path becomes **your** path. Over months and years, this journal
        can show you:

        - which workings actually helped,  
        - which dreams or signs kept repeating,  
        - how your feelings changed over time,  
        - and what teachers, books, or spirits keep returning to your life.
        """
    )

    with st.expander("✏️ Add a quick journal entry"):
        with st.form("free_journal_form"):
            title = st.text_input("Title")
            tradition_context = st.selectbox(
                "Tradition context",
                [
                    "West African Vodun",
                    "Haitian Vodou",
                    "Louisiana Voodoo",
                    "Hoodoo / Rootwork",
                    "Ancestor Work",
                    "Mixed / Unsure",
                    "Just feelings / life",
                ],
            )
            intention = st.text_area(
                "What were you focusing on, studying, or feeling?",
                height=80,
            )
            details = st.text_area(
                "What happened? (rituals, prayers, conversations, study, life events)",
                height=120,
            )
            dreams_signs = st.text_area(
                "Any dreams or signs you want to note?",
                height=80,
            )
            feelings_before = st.text_area(
                "Feelings before",
                height=70,
            )
            feelings_after = st.text_area(
                "Feelings after",
                height=70,
            )
            notes = st.text_area(
                "Other notes",
                height=80,
            )

            saved = st.form_submit_button("💾 Save entry")
            if saved:
                if not title.strip():
                    st.error("Please give this entry a title.")
                else:
                    insert_journal_entry(
                        title=title.strip(),
                        tradition_context=tradition_context,
                        intention=intention.strip(),
                        details=details.strip(),
                        dreams_signs=dreams_signs.strip(),
                        feelings_before=feelings_before.strip(),
                        feelings_after=feelings_after.strip(),
                        notes=notes.strip(),
                    )
                    st.success("Journal entry saved.")

    st.markdown("---")
    st.markdown("### Recent Entries")

    df = fetch_journal_entries()
    if df.empty:
        st.info("No journal entries yet.")
        render_footer()
        return

    view_mode = st.radio(
        "View as",
        ["Table", "Cards"],
        horizontal=True,
    )

    if view_mode == "Table":
        st.dataframe(
            df[
                [
                    "date",
                    "title",
                    "tradition_context",
                    "intention",
                    "details",
                    "dreams_signs",
                    "feelings_before",
                    "feelings_after",
                    "notes",
                ]
            ]
        )
    else:
        for _, row in df.iterrows():
            with st.expander(f"{row['date']} – {row['title']}"):
                st.write(f"**Tradition context:** {row['tradition_context']}")
                if row["intention"]:
                    st.markdown("**Intention / focus:**")
                    st.write(row["intention"])
                if row["details"]:
                    st.markdown("**What happened:**")
                    st.write(row["details"])
                if row["dreams_signs"]:
                    st.markdown("**Dreams / signs:**")
                    st.write(row["dreams_signs"])
                if row["feelings_before"]:
                    st.markdown("**Feelings before:**")
                    st.write(row["feelings_before"])
                if row["feelings_after"]:
                    st.markdown("**Feelings after:**")
                    st.write(row["feelings_after"])
                if row["notes"]:
                    st.markdown("**Other notes:**")
                    st.write(row["notes"])

    render_footer()


def page_resources():
    render_header()
    st.subheader("Study Path & Resources – Building Real Knowledge")

    st.markdown(
        """
        Use this page as a **long-term syllabus** for yourself. Add books, documentaries, teachers,
        temples, and classes you discover. Over time, you will see which directions your path keeps pointing.
        """
    )

    with st.expander("➕ Add a resource to your list"):
        with st.form("resource_form"):
            title = st.text_input("Title")
            res_type = st.selectbox(
                "Type",
                ["Book", "Documentary", "Podcast", "Article", "Teacher / Elder", "Practice", "Other"],
            )
            tradition_focus = st.selectbox(
                "Main tradition focus",
                [
                    "West African Vodun",
                    "Haitian Vodou",
                    "Louisiana Voodoo",
                    "Hoodoo / Rootwork",
                    "Ancestor Work",
                    "Mixed / Comparative",
                    "Other / Unsure",
                ],
            )
            level = st.selectbox(
                "Level",
                ["Intro", "Intermediate", "Advanced", "All levels"],
            )
            link = st.text_input("Link (optional, website or store URL)")
            notes = st.text_area(
                "Why this resource matters / what you want to learn from it",
                height=80,
            )

            added = st.form_submit_button("Save resource")
            if added:
                if not title.strip():
                    st.error("Please provide at least a title.")
                else:
                    conn = get_conn()
                    cur = conn.cursor()
                    cur.execute(
                        """
                        INSERT INTO resources
                        (title, res_type, tradition_focus, level, link, notes)
                        VALUES (?, ?, ?, ?, ?, ?)
                        """,
                        (
                            title.strip(),
                            res_type,
                            tradition_focus,
                            level,
                            link.strip(),
                            notes.strip(),
                        ),
                    )
                    conn.commit()
                    conn.close()
                    st.success("Resource saved.")

    st.markdown("---")
    st.markdown("### Your Resources")

    res = fetch_resources()
    if not res:
        st.info("No resources saved yet.")
        render_footer()
        return

    df = pd.DataFrame(res)
    focus_filter = st.selectbox(
        "Filter by tradition focus",
        ["All"] + sorted(df["tradition_focus"].unique().tolist()),
    )
    if focus_filter != "All":
        df = df[df["tradition_focus"] == focus_filter]

    for _, row in df.iterrows():
        with st.expander(f"{row['title']} – {row['res_type']} ({row['tradition_focus']})"):
            if row["level"]:
                st.write(f"**Level:** {row['level']}")
            if row["link"]:
                st.write(f"**Link:** {row['link']}")
            if row["notes"]:
                st.markdown("**Notes:**")
                st.write(row["notes"])

    render_footer()


def page_supplies():
    render_header()
    st.subheader("Supplies & Shops – Botanicas, Curios, Tools")

    st.markdown(
        """
        This page helps you track where your ritual tools come from: candles, oils, herbs, roots, colognes,
        statuary, and curios. Over time you can build relationships with trustworthy shops instead of buying
        random items that don’t feel right.
        """
    )

    col1, col2 = st.columns(2)

    # --- Shops ---
    with col1:
        st.markdown("### Your Shops / Suppliers")

        with st.form("supplier_form"):
            name = st.text_input("Shop name")
            shop_type = st.selectbox(
                "Type",
                [
                    "Botanica",
                    "Hoodoo / Conjure Curio Shop",
                    "Occult / Metaphysical Shop",
                    "Herbalist / Farmers Market",
                    "Online Marketplace Seller",
                    "Other",
                ],
            )
            tradition_focus = st.text_input(
                "Tradition focus (e.g., Hoodoo, Vodou, Santería, Mixed)",
            )
            owned_by_diaspora = st.checkbox(
                "Owned by African / Caribbean / Afro-descendant person (to your knowledge)"
            )
            country = st.text_input("Country")
            region = st.text_input("City / Region")
            url = st.text_input("Website / URL (optional)")
            ships_to = st.text_input("Ships to (e.g., US only, Worldwide)")
            notes = st.text_area("Notes (what they carry, how they treat customers)", height=70)

            add_shop = st.form_submit_button("Save shop")
            if add_shop:
                if not name.strip():
                    st.error("Please provide a shop name.")
                else:
                    insert_supplier(
                        name=name.strip(),
                        shop_type=shop_type,
                        tradition_focus=tradition_focus.strip(),
                        owned_by_diaspora=owned_by_diaspora,
                        country=country.strip(),
                        region=region.strip(),
                        url=url.strip(),
                        ships_to=ships_to.strip(),
                        notes=notes.strip(),
                    )
                    st.success("Shop saved.")

        suppliers = fetch_suppliers()
        if not suppliers:
            st.info("No shops saved yet.")
        else:
            st.markdown("#### Saved shops")
            for s in suppliers:
                owned_label = "Yes" if s["owned_by_diaspora"] else "Not marked"
                with st.expander(f"{s['name']} – {s['shop_type']} ({s['country'] or ''})"):
                    st.write(f"**Tradition focus:** {s['tradition_focus'] or 'n/a'}")
                    st.write(f"**Owned by Diaspora (as you marked):** {owned_label}")
                    if s["region"]:
                        st.write(f"**City / Region:** {s['region']}")
                    if s["url"]:
                        st.write(f"**Website:** {s['url']}")
                    if s["ships_to"]:
                        st.write(f"**Ships to:** {s['ships_to']}")
                    if s["notes"]:
                        st.markdown("**Notes:**")
                        st.write(s["notes"])

    # --- Supplies ---
    with col2:
        st.markdown("### Your Supplies / Items")

        suppliers = fetch_suppliers()
        supplier_options = ["(none / various)"] + [s["name"] for s in suppliers]
        supplier_ids = [None] + [s["id"] for s in suppliers]

        with st.form("supply_form"):
            item_name = st.text_input("Item name (e.g., white 7-day candle, Florida Water)")
            category = st.selectbox(
                "Category",
                ["Candle", "Oil / Cologne", "Herb / Root", "Mineral / Stone", "Curio / Charm", "Other"],
            )
            tradition_usage = st.text_area(
                "How you understand or use this item in tradition (short description)",
                height=70,
            )
            shop_choice = st.selectbox("Usually purchased from", supplier_options)
            working_category = st.selectbox(
                "Tag for which kind of working",
                [
                    "",
                    "Cleansing",
                    "Protection",
                    "Road Opening",
                    "Prosperity",
                    "Self-Love",
                    "Ancestor",
                    "Clarity",
                ],
            )
            item_notes = st.text_area("Notes (quality, cautions, etc.)", height=60)

            add_item = st.form_submit_button("Save item")
            if add_item:
                if not item_name.strip():
                    st.error("Please provide an item name.")
                else:
                    idx = supplier_options.index(shop_choice)
                    shop_id = supplier_ids[idx]
                    insert_supply_item(
                        name=item_name.strip(),
                        category=category,
                        tradition_usage=tradition_usage.strip(),
                        shop_id=shop_id if shop_id is not None else None,
                        working_category=working_category.strip(),
                        notes=item_notes.strip(),
                    )
                    st.success("Item saved.")

        df_items = fetch_supply_items()
        st.markdown("#### Saved supplies")
        if df_items.empty:
            st.info("No supplies saved yet.")
        else:
            filter_cat = st.selectbox(
                "Filter by working category",
                ["All"] + sorted(
                    [c for c in df_items["working_category"].dropna().unique().tolist() if c]
                ),
            )
            df_display = df_items.copy()
            if filter_cat != "All":
                df_display = df_display[df_display["working_category"] == filter_cat]

            st.dataframe(
                df_display[
                    [
                        "name",
                        "category",
                        "tradition_usage",
                        "working_category",
                        "shop_name",
                        "shop_country",
                        "notes",
                    ]
                ]
            )

    render_footer()


def page_disclaimer():
    render_header()
    st.subheader("Disclaimers, Ethics & Safety")

    st.markdown(
        """
        ### Respect for Living Traditions

        Vodun, Vodou, Voodoo, and Hoodoo are **living traditions** carried by real communities:
        Black, African, Creole, Caribbean, and others. They are not costumes or horror props. This app is
        a bridge toward more respectful understanding, not a replacement for teachers or temples.
        """
    )

    st.markdown(
        """
        ### What This App Does

        - Offers **deep educational summaries** of history and key spirits.  
        - Gives you **non-harmful ritual templates** centered on cleansing, protection, justice,
          prosperity, self-love, ancestor work, and clarity.  
        - Provides a **journal** so you can track your own path.  
        - Helps you organize **resources, shops, and supplies** in a conscious way.
        """
    )

    st.markdown(
        """
        ### What This App Does Not Do

        - It does **not** teach curses, domination, or coercive work.  
        - It does **not** give initiatory secrets of any house, temple, or lineage.  
        - It does **not** replace:
            - Houngans, Mambos, priestesses, priests, or rootworkers,  
            - therapists, counselors, or psychiatrists,  
            - medical doctors,  
            - lawyers or financial professionals.
        """
    )

    st.markdown(
        """
        ### Mental & Physical Health

        If you are in crisis, feeling unsafe, or struggling with severe mental or physical health issues,
        please seek help from qualified professionals or local emergency services. Spiritual practices can
        support healing, but they are not a substitute for proper care.
        """
    )

    st.markdown(
        """
        ### Your Responsibility

        By using this app, you agree to:

        - Approach these traditions with respect and humility.  
        - Use any workings or templates only for non-harmful purposes.  
        - Take responsibility for the consequences of your actions in the physical world.  
        - Accept that real learning takes time, relationships, and listening.
        """
    )

    render_footer()


def page_admin():
    render_header()
    st.subheader("🛡️ Admin – Voodoo & Hoodoo Spells Control Panel")

    st.markdown(
        """
        This page is for the creator/admin only. Buttons here use the same glowing shield-and-spear style as
        the rest of the app, because even your backend deserves protection and power.
        """
    )

    if "is_admin" not in st.session_state:
        st.session_state["is_admin"] = False

    if not st.session_state["is_admin"]:
        st.markdown("### Admin Login")

        with st.form("admin_login_form"):
            username = st.text_input("Admin username")
            password = st.text_input("Admin password", type="password")
            login = st.form_submit_button("🛡️⚔️ Log In")

        if login:
            admin_user = st.secrets.get("ADMIN_USER", "admin")
            admin_pass = st.secrets.get("ADMIN_PASS", "rootworker")
            if username == admin_user and password == admin_pass:
                st.session_state["is_admin"] = True
                st.success("Admin access granted.")
                safe_rerun()
            else:
                st.error("Invalid admin credentials.")
    else:
        st.success("You are logged in as admin.")
        if st.button("🚪 Log Out of Admin"):
            st.session_state["is_admin"] = False
            safe_rerun()

        conn = get_conn()
        cur = conn.cursor()

        cur.execute("SELECT COUNT(*) FROM spirits")
        spirits_count = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM workings_templates")
        workings_count = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM journal_entries")
        journal_count = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM resources")
        resources_count = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM suppliers")
        suppliers_count = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM supply_items")
        items_count = cur.fetchone()[0]
        conn.close()

        st.markdown("### Data Snapshot")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Spirits", spirits_count)
            st.metric("Workings", workings_count)
        with col2:
            st.metric("Journal entries", journal_count)
            st.metric("Resources", resources_count)
        with col3:
            st.metric("Shops", suppliers_count)
            st.metric("Supply items", items_count)

        st.markdown("---")
        st.markdown("### Admin Notes")
        st.info(
            "You can extend this admin page later with data export, bulk edits, or content seeding tools. "
            "Right now it serves as a shielded dashboard – only accessible with your admin credentials."
        )

    render_footer()


# =========================
# Main router
# =========================

def main():
    init_db()

    if "vh_page" not in st.session_state:
        st.session_state["vh_page"] = "Nana Buluku"

    with st.sidebar:
        st.markdown(
            '<div class="sidebar-logo">VOODOO &amp; HOODOO SPELLS</div>',
            unsafe_allow_html=True,
        )
        st.markdown("**Navigate**")
        pages = [
            "Nana Buluku",
            "Origins & History",
            "Spirits & Ancestors",
            "Hoodoo Basics",
            "Workings & Templates",
            "Journal & Signs",
            "Study & Resources",
            "Supplies & Shops",
            "Disclaimers & Ethics",
            "Admin",
        ]
        page = st.radio(
            "",
            pages,
            index=pages.index(st.session_state.get("vh_page", "Nana Buluku")),
        )
        st.session_state["vh_page"] = page

    if page == "Nana Buluku":
        page_nana_buluku()
    elif page == "Origins & History":
        page_history()
    elif page == "Spirits & Ancestors":
        page_spirits()
    elif page == "Hoodoo Basics":
        page_hoodoo_basics()
    elif page == "Workings & Templates":
        page_workings()
    elif page == "Journal & Signs":
        page_journal()
    elif page == "Study & Resources":
        page_resources()
    elif page == "Supplies & Shops":
        page_supplies()
    elif page == "Disclaimers & Ethics":
        page_disclaimer()
    elif page == "Admin":
        page_admin()
    else:
        page_nana_buluku()


if __name__ == "__main__":
    main()


