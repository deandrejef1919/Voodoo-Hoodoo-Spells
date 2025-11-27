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
# THEME & STYLES (RED / BLACK / GREEN)
# =========================

APP_CSS = """
<style>
body, .stApp {
    background-color: #050404;
    color: #f7f7f7;
    font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}
.block-container { padding-top: 1.5rem; }

/* Header */
.vh-header {
    text-align:center;
    padding: 0.75rem 0 0.25rem 0;
}
.vh-logo {
    font-size: 3.4rem;
}
.vh-title {
    font-size: 2rem;
    font-weight: 800;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #e53935;
    text-shadow:
        0 0 8px rgba(229,57,53,0.9),
        0 0 16px rgba(0,0,0,0.9);
}
.vh-subtitle {
    font-size: 0.95rem;
    opacity: 0.9;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: radial-gradient(circle at top, #2b0000 0%, #050404 55%, #000000 100%);
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
    background: radial-gradient(circle at 30% 0%, #3b0000 0%, #050404 55%, #000 100%);
    border: 1px solid rgba(229,57,53,0.7);
    box-shadow:
        0 0 10px rgba(229,57,53,0.6),
        0 0 18px rgba(0,0,0,0.9),
        inset 0 0 6px rgba(0,0,0,0.7);
}

/* Cards */
.vh-card {
    border-radius: 14px;
    border: 1px solid rgba(229,57,53,0.75);
    padding: 1.1rem 1.35rem;
    margin-bottom: 0.9rem;
    background: radial-gradient(circle at top, #151111 0%, #050404 55%, #000000 100%);
    box-shadow:
        0 0 10px rgba(229,57,53,0.4),
        0 0 22px rgba(0,0,0,0.95);
}
.vh-card h3 {
    margin-top: 0;
}

/* Buttons styled like Zulu shields */
div.stButton > button {
    border-radius: 999px;
    border-width: 2px;
    border-style: solid;
    border-color: #1b5e20;
    padding: 0.4rem 1.6rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    background: radial-gradient(circle at 30% 15%, #e53935 0%, #1b5e20 40%, #000000 85%);
    color: #fbe9e7;
    box-shadow:
        0 0 10px rgba(229,57,53,0.9),
        0 0 18px rgba(27,94,32,0.9);
}
div.stButton > button:hover {
    box-shadow:
        0 0 16px rgba(229,57,53,1.0),
        0 0 26px rgba(27,94,32,1.0);
    transform: translateY(-1px);
    border-color: #e53935;
}

/* Footer */
.vh-footer {
    text-align:center;
    font-size: 0.8rem;
    color: #b0b0b0;
    margin-top: 2.8rem;
    padding-top: 0.75rem;
    border-top: 1px solid rgba(76,175,80,0.7);
    opacity: 0.9;
}

/* Accents */
.vh-pill {
    display:inline-block;
    padding: 0.15rem 0.5rem;
    border-radius: 999px;
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    border: 1px solid rgba(76,175,80,0.8);
    color: #c8e6c9;
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
# Seed data
# =========================

def seed_spirits(cur):
    spirits_data = [
        (
            "Nana Buluku",
            "Fon / West African Vodun",
            "Primordial Creator",
            "creation, cosmic order, origin",
            "white, deep blue, night-sky tones",
            "cosmic egg, night sky, stars",
            "Nana Buluku is honored in some West African Vodun lineages as a primordial creator figure. In many tellings, Nana Buluku precedes or gives birth to twin forces such as Mawu and Lisa. Different lineages describe this being with different genders or as beyond gender. This app begins with Nana Buluku to honor the deep West African root beneath later Vodou, Voodoo, and Hoodoo."
        ),
        (
            "Mawu-Lisa",
            "Fon / West African Vodun",
            "Divine Twin Principle",
            "balance, moon and sun, coolness and heat",
            "white, gold, silver",
            "sun and moon together",
            "Mawu-Lisa is a twin divinity concept in some Vodun traditions, sometimes understood as complementary principles like moon/sun or cool/heat. This reflects balance and the idea that creation holds multiple forces in relationship."
        ),
        (
            "Legba",
            "Haitian Vodou / Related Gatekeeper Spirits",
            "Gatekeeper / Messenger",
            "crossroads, communication, access, new beginnings",
            "red, black, sometimes yellow",
            "crossroads, cane, keys",
            "Legba (or related spirits in other traditions) is often honored as a gatekeeper at the spiritual crossroads. Many lineages say that one should greet the gatekeeper before asking for help from other spirits. This entry is educational only and does not include specific ritual instructions."
        ),
        (
            "Ancestors",
            "Many traditions",
            "Collective Dead / Ancestors",
            "memory, guidance, protection, lineage",
            "white, candlelight colors",
            "glass of water, photos, names",
            "Ancestor veneration is central to many African and Diaspora traditions. The ancestors are the beloved dead of our bloodlines and of our chosen spiritual families. Many people keep a glass of water, a candle, and photos or names to honor them. This app encourages respectful remembrance, not attempts to control the dead."
        ),
        (
            "Damballa",
            "Haitian Vodou",
            "Serpent Creator Spirit",
            "purity, blessing, creation, rivers",
            "white, pale blue, silver",
            "serpent, water, sky arch",
            "Damballa in Haitian Vodou is often associated with serpents, purity, and creative forces. Many depictions show a serpent bridging earth and sky. Here we include a brief educational mention only."
        ),
        (
            "Ezili (Erzulie) – General",
            "Haitian Vodou",
            "Lwa Family (Love, Protection)",
            "love, care, protection, passion, justice",
            "pink, red, blue (varies by aspect)",
            "heart, veils, tears",
            "The Ezili family of spirits in Haitian Vodou includes multiple aspects related to love, protection, and fierce justice in defense of children and the vulnerable. Different houses relate to these lwa in their own ways."
        ),
        (
            "Ogou / Ogun-type Figure",
            "Haitian Vodou / Yoruba-influenced traditions",
            "Warrior / Iron / Work",
            "tools, iron, strength, clearing obstacles",
            "red, dark blue, metallic colors",
            "iron tools, machete, anvil",
            "Ogou-like spirits represent iron, tools, and the fire of work and struggle. They are associated with courage, discipline, and the ability to cut through obstacles."
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
            "Gently cleanse heavy or stagnant energy and invite calm.",
            "Water is used as a symbol of renewal and flow. Salt is often used as a purifier. Safe herbs like rosemary or basil can be used symbolically as helpers for clarity and freshness. The focus is on release, not on attacking any person.",
            "As this water touches me, I release what is heavy and no longer needed. May I be clean in mind, heart, and path. May what is truly mine remain, and what is not for me gently fall away.",
            "Do not use unknown herbs internally or on sensitive skin. This template is symbolic and should not replace medical or mental-health care. It is intended for gentle cleansing of the self, not for blaming others or sending harm."
        ),
        (
            "Protection Candle Template",
            "Protection",
            "Hoodoo / Vodou-inspired",
            "Create a sense of spiritual protection and safety around yourself or your space.",
            "Candles can be treated as a small standing light of protection. A circle drawn around the candle or imagined in the mind can represent a boundary. White candles are often used as all-purpose lights when specific colors are not available.",
            "Let this flame stand as a small guardian for me and those I love. May harm be turned away, and may what is safe, honest, and good be welcomed. I ask for protection that does not require anyone else to be hurt.",
            "This working is focused on protective boundaries and safety. It is not meant as a weapon. Fire is dangerous in the physical world, so never leave candles unattended or near flammable items."
        ),
        (
            "Road Opening / Opportunity Template",
            "Road Opening",
            "Vodou-inspired / Crossroads Symbolism",
            "Ask for supportive openings in work, study, or other life paths while you also take practical steps.",
            "Crossroads and keys are often used to symbolize decisions and opportunities. In many traditions, crossroads spirits are petitioned to open good roads. In this app, we focus on asking for right opportunities while you commit to real-world effort.",
            "May good roads open before me in the area of my life I am working on now. May paths that are truly mine become clearer, and paths that would harm me close gently. Guide my steps so that I meet honest chances and do my part with courage.",
            "This template is meant to work together with concrete actions: applying for jobs, practicing skills, having honest conversations. It is not a guarantee of specific outcomes and is not meant to override anyone else's free will."
        ),
        (
            "Prosperity & Work Blessing Template",
            "Prosperity",
            "Hoodoo / General",
            "Bless your honest work, study, and planning around money, inviting stability and wise choices.",
            "Green, gold, seeds, and coins are common prosperity symbols. In Hoodoo and related traditions, money-drawing work is often paired with very practical steps like budgeting, studying, or job searching. The focus is on fair, honest prosperity.",
            "Bless the work of my hands and the plans I build. May opportunities to earn honestly and fairly come into my life. May I use what I receive with wisdom, care, and generosity, and remember that money is a tool, not my master.",
            "This template does not promise riches. It supports steady effort, learning, and wiser choices. Do not use it to excuse risky financial behavior or to avoid asking for real-world help from advisors when needed."
        ),
        (
            "Self-Love & Confidence Working",
            "Self-Love",
            "Diaspora / General",
            "Nurture a kinder relationship with yourself and strengthen your sense of worth.",
            "Mirrors, gentle colors, and sweet scents are often used to represent self-love. Many traditions emphasize the importance of speaking kindly to oneself and honoring the body and spirit as worthy of care.",
            "I release the story that I am unworthy of love and respect. Little by little, may I see myself with clearer, kinder eyes. May I walk with more confidence in who I truly am, while staying humble and open to growth.",
            "This working is about inner kindness, not arrogance. It may be helpful alongside therapy, self-help work, or support groups. If self-hatred or despair feels overwhelming, please seek professional support."
        ),
        (
            "Ancestor Connection Time",
            "Ancestor",
            "Vodun / Vodou / Hoodoo",
            "Set aside quiet time to remember and honor your ancestors or beloved dead.",
            "A glass of water, a candle, and photos or written names are common elements of ancestor remembrance. In many cultures, the dead are honored with food, song, and stories. This template focuses on thanks and connection, not on controlling the dead.",
            "To the ancestors who walked before me, known and unknown, I thank you for the life that reaches me through you. May I live in a way that honors your strength and wisdom. Where there was harm or trauma, may healing move through the lineage.",
            "Ancestor work can bring up grief and complex family history. Go gently, and seek support if difficult memories arise. This template is for remembrance and gratitude, not for summoning or commanding spirits."
        ),
        (
            "Clarity & Signs Journal Prompt",
            "Clarity",
            "General / Introspective",
            "Create a space to notice patterns, dreams, and subtle signs over time.",
            "Many spiritual paths pay attention to repeating symbols, dreams, or feelings as possible messages. Journaling helps organize these impressions without jumping to fear or fantasy.",
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
            "Look for works by scholars who specialize in West African religions or by initiates writing about their own traditions. Avoid sensationalized or overly exoticized material that treats Vodun as horror."
        ),
        (
            "Documentaries on Haitian Vodou (Practitioner-Focused)",
            "Documentary",
            "Haitian Vodou",
            "Intro",
            "",
            "Seek out documentaries that interview real Houngans, Mambos, and community members, rather than horror films. Look for material produced with Haitian voices centered."
        ),
        (
            "Books by African American Rootworkers",
            "Book",
            "Hoodoo / Rootwork",
            "Intro",
            "",
            "Many classic and modern texts on Hoodoo are written by Black practitioners from the US South. These can offer more grounded perspectives than generic spellbooks."
        ),
        (
            "Local Botanicas & Curio Shops",
            "Practice",
            "Mixed",
            "Intro",
            "",
            "Spending time respectfully in local botanicas, herb shops, and curio stores can teach you a lot about real-world practice. Support Black and Diaspora-owned businesses where possible."
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
                A respectful guide to Vodun, Vodou, Voodoo, Hoodoo, and your own spiritual work.
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
            mental-health care, or professional advice. Use it to support healing, protection,
            justice, and growth — never harm.
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
                <h3>Beginning with Nana Buluku</h3>
                <p>
                    In some West African Vodun lineages, <strong>Nana Buluku</strong> is honored as a primordial
                    creator figure — an ancient source from which other forces of creation emerge. Stories differ
                    from house to house: sometimes Nana Buluku is spoken of as mother, sometimes as beyond gender,
                    sometimes as the one who births twin forces such as Mawu and Lisa.
                </p>
                <p>
                    This app begins here to honor the deep <strong>West African root</strong> beneath later
                    Haitian Vodou, Louisiana Voodoo, and African American Hoodoo. The goal is not to speak
                    for every lineage, but to offer a gentle, respectful introduction.
                </p>
                <p>
                    Use this space as a <strong>study and reflection journal</strong> — not a toy, not a horror
                    story, and not a shortcut to real initiation. Real traditions belong to living communities,
                    elders, and lineages.
                </p>
                <p>
                    <span class="vh-pill">intention</span>
                    This app focuses on non-harmful work: cleansing, protection, uncrossing, justice,
                    prosperity, and self-healing. Historical mention of more aggressive forms of work will
                    be educational only, not instructional.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Optional visual section for Nana Buluku (user can configure image/video URLs)
        nana_img_url = st.secrets.get("NANA_BULUKU_IMAGE_URL", "")
        nana_vid_url = st.secrets.get("NANA_BULUKU_VIDEO_URL", "")
        if nana_img_url or nana_vid_url:
            with st.expander("Nana Buluku – Visuals (configure in secrets)"):
                if nana_img_url:
                    st.image(nana_img_url, caption="Nana Buluku inspired art", use_column_width=True)
                if nana_vid_url:
                    st.video(nana_vid_url)
        else:
            st.info(
                "Tip: add NANA_BULUKU_IMAGE_URL and NANA_BULUKU_VIDEO_URL to your Streamlit secrets "
                "to show art or video here and make the app feel more alive."
            )

    with col2:
        st.markdown(
            """
            <div class="vh-card">
                <h3>A Short Opening</h3>
                <p>
                    You may use the words below as a quiet opening intention when you sit down with this app:
                </p>
                <blockquote>
                    May I remember the ancestors who carried these traditions through terror and survival.<br/>
                    May I approach these ways with respect, humility, and care.<br/>
                    May any work I do be aligned with healing, protection, justice, and growth — never harm.<br/>
                    May I be guided away from fantasy and toward what is true and helpful.
                </blockquote>
                <p>
                    When you are ready, choose where to go next:
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
            if st.button("📓 Open Journal"):
                st.session_state["vh_page"] = "Journal & Signs"
                safe_rerun()

    render_footer()


def page_history():
    render_header()
    st.subheader("Origins & History – Vodun, Vodou, Voodoo, Hoodoo")

    st.markdown(
        """
        ### West African Vodun / Vodún
        West African Vodun (also spelled Vodún or Vodun) refers to a family of religions practiced among
        Fon, Ewe, and related peoples in areas that are now Benin, Togo, Ghana, and parts of Nigeria.
        These traditions honor a creator or high god, a rich community of spirits, and the ancestors.
        Rituals often involve drumming, song, dance, divination, herbal medicine, and spirit possession.

        The traditions are diverse. What one community calls a particular spirit, another may know by a
        different name or attribute. There is no single book that defines Vodun; it lives in ceremony
        and community.
        """
    )

    st.markdown(
        """
        ### From Vodun to Haitian Vodou – 1791 and the Road to Revolution
        During the transatlantic slave trade, millions of Africans were taken by force to the Caribbean
        and the Americas. On the island of Kiskeya/Ayiti (later called Saint-Domingue under French rule,
        then Haiti after independence), people from many nations were enslaved together. Their spiritual
        traditions mixed with each other, with elements of Catholicism, and with Indigenous Caribbean
        influences.

        In 1791, a famous Vodou ceremony — often remembered at Bois Caïman — is said to have helped ignite
        the Haitian uprising that led into years of war against French colonial power. Over roughly twelve
        years of struggle, Haitians fought France and other European forces and ultimately created the first
        Black republic of the modern era. Haitian Vodou and the Haitian Revolution are deeply intertwined
        in memory and history.
        """
    )

    # Optional Haitian visuals
    haitian_img = st.secrets.get("HAITI_VODOU_IMAGE_URL", "")
    haitian_vid = st.secrets.get("HAITI_VODOU_VIDEO_URL", "")
    if haitian_img or haitian_vid:
        with st.expander("Haitian Vodou – Visuals (configure in secrets)"):
            if haitian_img:
                st.image(haitian_img, caption="Haitian Vodou ceremony or altar (respectful image)", use_column_width=True)
            if haitian_vid:
                st.video(haitian_vid)

    st.markdown(
        """
        ### Louisiana / New Orleans Voodoo – Marie Laveau, the Voodoo Queen
        In what is now Louisiana, African, Caribbean, Indigenous, and European traditions met under French
        and Spanish colonial rule. New Orleans became famous for its spiritual workers, and none is more
        legendary than <strong>Marie Laveau</strong>, often called the “Voodoo Queen of New Orleans.”

        Marie Laveau lived in the 19th century and was known as a powerful spiritual leader, hairdresser,
        and community figure. Stories about her mix documented history with folklore. Under her name and
        influence, New Orleans Voodoo involved <em>gris-gris</em> bags, saints and psalms, candles, roots,
        charms, and petitions for protection, love, luck, and justice.
        """
    )

    st.markdown(
        """
        ### Hoodoo / Rootwork / Conjure
        Hoodoo (also called rootwork or conjure) is an African American folk-magic system that developed
        primarily in the US South. It draws heavily on African spiritual technologies — roots, crossroads,
        ancestors, spirit negotiation — and also integrates Native American plant knowledge and European
        folk practices like using psalms and talismans.

        Hoodoo is not a formal religion with a single priesthood. Many rootworkers are Christian and use
        the Bible in their work. The focus is practical: protection, cleansing, luck, court cases, love,
        and justice. Historically, there have been both helpful and harmful forms of work. This app will
        only provide templates for helpful forms: cleansing, protection, uncrossing, justice framed as
        truth and fair resolution, prosperity, and self-healing.
        """
    )

    # Optional New Orleans visuals
    nola_img = st.secrets.get("NEW_ORLEANS_IMAGE_URL", "")
    nola_vid = st.secrets.get("NEW_ORLEANS_VIDEO_URL", "")
    if nola_img or nola_vid:
        with st.expander("New Orleans Voodoo – Visuals (configure in secrets)"):
            if nola_img:
                st.image(nola_img, caption="New Orleans Voodoo altar or historical imagery", use_column_width=True)
            if nola_vid:
                st.video(nola_vid)

    st.markdown(
        """
        ### Keeping Distinctions Clear
        - <strong>Vodun / Vodou</strong> – religions with temples, clergy, initiations, and lineages.
        - <strong>Louisiana Voodoo</strong> – regional spiritual practices rooted in African and Creole history,
          including figures like Marie Laveau.
        - <strong>Hoodoo / Rootwork</strong> – folk magic practices, often carried by Black families in the US South.
        """
    )

    render_footer()


def page_spirits():
    render_header()
    st.subheader("Spirits & Ancestors – Educational Profiles")

    st.markdown(
        """
        This page offers short, respectful descriptions of some spirits and spiritual principles mentioned
        in West African Vodun, Haitian Vodou, and related traditions. It is <strong>not</strong> a manual
        for summoning or commanding any being, and it cannot replace study with real teachers.
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
    st.subheader("Hoodoo / Rootwork Basics")

    st.markdown(
        """
        Hoodoo (also called rootwork or conjure) is an African American folk-magic system rooted in the
        experience of Black communities in the United States, especially the South. It developed out of
        African spiritual practices, contact with Native peoples, and European folk traditions.
        """
    )

    st.markdown(
        """
        ### What Hoodoo Is (and Is Not)
        - <strong>Is:</strong> practical spiritual work around protection, cleansing, luck, love, justice, and survival.
        - <strong>Is not:</strong> a single unified church or religion with one hierarchy.
        - Many rootworkers are Christian and pray with the Bible, especially the Psalms, while working with
          herbs, roots, candles, and curios.
        """
    )

    st.markdown(
        """
        ### Common Elements in Hoodoo
        - <strong>Roots & Herbs:</strong> Plants treated as living allies with specific qualities.
        - <strong>Minerals & Curios:</strong> Lodestones, coins, nails, and other items used symbolically.
        - <strong>Candles:</strong> Often dressed with oils and herbs, burned with focused prayer.
        - <strong>Mojo Bags / Hands:</strong> Small charm bundles carried on the person.
        - <strong>Crossroads Work:</strong> Symbolic and sometimes literal work done where paths meet.
        - <strong>Bible & Psalms:</strong> Spoken as prayer, incantation, or affirmation.
        """
    )

    st.markdown(
        """
        ### About Harmful Work
        Historically, some rootworkers have done work meant to harm or coerce others. A full history cannot
        ignore this. However, this app will not provide instructions for attack, revenge, domination, or
        cursing. Instead, the Workings & Ritual Templates focus on:
        - Cleansing
        - Protection
        - Uncrossing and healing from harm
        - Justice framed as truth, accountability, and fair resolution
        - Prosperity and work blessings
        - Self-love and confidence
        - Ancestor remembrance
        - Clarity and journaling
        """
    )

    render_footer()


def page_workings():
    render_header()
    st.subheader("Workings & Ritual Templates")

    st.markdown(
        """
        These templates are <strong>blueprints</strong> for non-harmful spiritual work. They focus on
        cleansing, protection, healing, justice, prosperity, self-love, ancestor remembrance, and clarity.
        They do not replace medical, legal, or mental-health care, and they are not instructions for
        harming anyone.
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
            height=180,
        )
        st.markdown("**Ethical note:**")
        st.info(tmpl["ethical_note"])

    st.markdown("---")
    st.markdown("### Your Version of This Working")

    st.markdown(
        "Fill this in to plan or record your own version of the working. You can save it into your journal."
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
            height=80,
        )
        details = st.text_area(
            "What did you (or will you) actually do? (tools, timing, location, actions)",
            height=110,
        )
        dreams_signs = st.text_area(
            "Any dreams, signs, or patterns you noticed before/after?",
            height=80,
        )
        feelings_before = st.text_area(
            "How did you feel before the working?",
            height=60,
        )
        feelings_after = st.text_area(
            "How did you feel after (or how do you hope to feel)?",
            height=60,
        )
        notes = st.text_area(
            "Any additional notes or reflections?",
            height=80,
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
                "You can still perform a simple version of this working with basic items like clean water or a plain candle."
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
    st.subheader("Journal & Signs")

    st.markdown(
        """
        This is your private logbook. Use it to record studies, rituals, dreams, and everyday moments.
        Writing things down can reveal patterns over time.
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
                height=110,
            )
            dreams_signs = st.text_area(
                "Any dreams or signs you want to note?",
                height=80,
            )
            feelings_before = st.text_area(
                "Feelings before",
                height=60,
            )
            feelings_after = st.text_area(
                "Feelings after",
                height=60,
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
    st.subheader("Study Path & Resources")

    st.markdown(
        """
        Use this page as a long-term study map. Add books, documentaries, teachers, and other resources
        you want to explore. Try to prioritize voices from within the traditions themselves.
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
        This page helps you keep track of where you obtain ritual supplies: candles, herbs, roots, oils,
        curios, and other tools. The goal is to build relationships with trustworthy shops and to be mindful
        about what you buy and from whom.
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
                owned_label = (
                    "Yes" if s["owned_by_diaspora"] else "Not marked"
                )
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
    st.subheader("Disclaimers & Ethics")

    st.markdown(
        """
        ### Respect for Living Traditions
        The practices labeled Vodun, Vodou, Voodoo, and Hoodoo come from the survival and creativity of
        African and African-descended peoples in the face of slavery, colonialism, and ongoing oppression.
        They are not costumes or horror props. This app offers only a small, respectful window into that
        complexity.
        """
    )

    st.markdown(
        """
        ### What This App Does
        - Provides <strong>educational summaries</strong> of Vodun, Vodou, Voodoo, and Hoodoo history.
        - Offers <strong>non-harmful ritual templates</strong> centered on cleansing, protection, healing,
          justice, prosperity, self-love, ancestor remembrance, and clarity.
        - Gives you a <strong>journal</strong> to track your own experiences and studies.
        - Helps you organize <strong>resources, shops, and supplies</strong> in a thoughtful way.
        """
    )

    st.markdown(
        """
        ### What This App Does Not Do
        - It does <strong>not</strong> provide instructions for curses, attacks, domination, or coercive work.
        - It does <strong>not</strong> claim to speak for any specific temple, house, lineage, or elder.
        - It does <strong>not</strong> replace:
          - priests/priestesses, Houngans, Mambos, rootworkers, or other clergy,
          - mental-health professionals,
          - medical doctors,
          - legal counsel, or financial advisors.
        """
    )

    st.markdown(
        """
        ### Mental & Physical Health
        If you are in crisis, feeling unsafe, or struggling with severe mental or physical health issues,
        please seek help from qualified professionals or local emergency services. Spiritual work can
        support healing, but it is not a substitute for appropriate care.
        """
    )

    st.markdown(
        """
        ### Your Responsibility
        By using this app, you agree to:
        - Approach these traditions with respect and humility.
        - Use any workings or templates only for non-harmful purposes.
        - Take responsibility for your actions in the physical world.
        """
    )

    render_footer()


# =========================
# Admin Page
# =========================

def page_admin():
    render_header()
    st.subheader("🛡️ Admin – Voodoo & Hoodoo Spells Control Panel")

    st.markdown(
        """
        This page is for the creator/admin only. It lets you see quick stats, and in later versions you
        can add more management tools. Buttons here are styled like glowing shields to match the app theme.
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

        # Show basic stats
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
            "In future versions you can extend this admin page with data export, bulk edits, or additional "
            "content seeding tools. For now it serves as a themed dashboard and login-protected area."
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
