import streamlit as st
import random
import datetime
from pathlib import Path

# ------------------------------------------------------
# BASIC CONFIG
# ------------------------------------------------------
st.set_page_config(
    page_title="Voodoo & Hoodoo Spells",
    page_icon="🕯️",
    layout="wide",
)

# ------------------------------------------------------
# CORE THEME (single red / black / green theme)
# ------------------------------------------------------
APP_CSS = """
<style>
body, .stApp {
    background-color: #050505;
    color: #f4efe6;
    font-family: "Times New Roman", Times, serif;
    font-size: 16px;
    line-height: 1.75;
}

.block-container {
    max-width: 1100px;
    padding-top: 1.2rem;
}

/* Header */
.vh-header {
    text-align:center;
    padding: 0.75rem 0 0.25rem 0;
}
.vh-logo {
    font-size: 3.4rem;
    text-shadow:
        0 0 8px rgba(244,67,54,0.9),
        0 0 14px rgba(0,0,0,1.0);
    animation: mojo-heartbeat 1.6s ease-in-out infinite;
}
.vh-title {
    font-size: 2.4rem;
    font-weight: 800;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #f44336;
    text-shadow:
        0 0 10px rgba(244,67,54,0.9),
        0 0 20px rgba(0,0,0,1.0);
}
.vh-subtitle {
    font-size: 1rem;
    opacity: 0.95;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: radial-gradient(circle at top, #310000 0%, #050505 55%, #000 100%);
    border-right: 1px solid rgba(76,175,80,0.65);
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
    background: radial-gradient(circle at 30% 0%, #3b0000 0%, #050505 55%, #000 100%);
    border: 1px solid rgba(244,67,54,0.7);
    box-shadow:
        0 0 10px rgba(244,67,54,0.6),
        0 0 18px rgba(0,0,0,0.9),
        inset 0 0 6px rgba(0,0,0,0.7);
}

/* Mojo tiles (separate pulse for each) */
.mojo-video-glow {
    border-radius: 16px;
    padding: 0.45rem;
    background: radial-gradient(circle at 50% 0%, #330000 0, #120000 55%, #000000 100%);
    box-shadow: 0 0 4px rgba(255, 0, 0, 0.7);
    animation: mojo-video-pulse 1.6s ease-in-out infinite;
}
.mojo-bag-glow {
    border-radius: 16px;
    padding: 0.45rem;
    background: radial-gradient(circle at 50% 0%, #2a1b00 0, #120b00 55%, #000000 100%);
    box-shadow: 0 0 4px rgba(255, 215, 0, 0.7);
    animation: mojo-bag-pulse 1.6s ease-in-out infinite;
}
.mojo-video-container iframe {
    border-radius: 12px;
    width: 100%;
    height: 118px;
}
.mojo-bag-container img {
    border-radius: 14px;
    display:block;
    margin:0 auto;
}

/* Heartbeat / candle animation */
@keyframes mojo-heartbeat {
    0% {
        box-shadow: 0 0 0 0 rgba(255, 0, 0, 0.0);
    }
    20% {
        box-shadow: 0 0 25px 8px rgba(255, 0, 0, 0.85);
    }
    35% {
        box-shadow: 0 0 10px 3px rgba(255, 0, 0, 0.45);
    }
    55% {
        box-shadow: 0 0 20px 6px rgba(255, 0, 0, 0.75);
    }
    100% {
        box-shadow: 0 0 0 0 rgba(255, 0, 0, 0.0);
    }
}

/* Sharper pulses */
@keyframes mojo-video-pulse {
    0%   { box-shadow: 0 0 4px rgba(255, 0, 0, 0.6); }
    50%  { box-shadow: 0 0 14px rgba(255, 0, 0, 1.0); }
    100% { box-shadow: 0 0 4px rgba(255, 0, 0, 0.6); }
}
@keyframes mojo-bag-pulse {
    0%   { box-shadow: 0 0 4px rgba(255, 215, 0, 0.6); }
    50%  { box-shadow: 0 0 14px rgba(255, 215, 0, 1.0); }
    100% { box-shadow: 0 0 4px rgba(255, 215, 0, 0.6); }
}

/* Incense smoke */
.incense-container {
    text-align: center;
    margin-top: 0.5rem;
}
.incense-burner {
    font-size: 32px;
}
.smoke {
    width: 4px;
    height: 60px;
    margin: 0 auto;
    background: linear-gradient(to top, rgba(255,255,255,0.0), rgba(255,255,255,0.45));
    border-radius: 999px;
    animation: smoke-rise 4.2s ease-in-out infinite;
}
@keyframes smoke-rise {
    0%   { opacity: 0.0; transform: translateY(20px); }
    20%  { opacity: 0.5; transform: translateY(0px); }
    80%  { opacity: 0.5; transform: translateY(-24px); }
    100% { opacity: 0.0; transform: translateY(-40px); }
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

/* Typography */
p, li {
    font-size: 16px;
    line-height: 1.8;
}
h2, h3, h4 {
    font-family: "Times New Roman", Times, serif;
}

/* Shield buttons */
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
div.stButton > button {
    border-radius: 999px / 70px;
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
        radial-gradient(circle at 16% 0%, rgba(255,255,255,0.25) 0%, transparent 60%);
    background-blend-mode: overlay;
    color: #fff7ec;
    animation: shieldGlow 2.4s ease-in-out infinite alternate;
    transform: translateY(0);
}
div.stButton > button::before {
    content: "⚔️";
    margin-right: 0.35rem;
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
</style>
"""
st.markdown(APP_CSS, unsafe_allow_html=True)

# ------------------------------------------------------
# LWA DATA (19) – same structure as last time
# ------------------------------------------------------
LOA_GALLERY_DATA = [
    # (shortened descriptions so app fits nicely – you still get all 19)
    {
        "name": "Papa Legba",
        "image_key": "LWA_PAPA_LEGBA_URL",
        "description": "Gatekeeper of the crossroads, opening and closing spiritual roads.",
        "attributes": [
            "🕯️ Coffee, tobacco, rum, candy",
            "🔑 Crossroads, communication, access",
            "📆 Monday • 🎨 Brown, red, yellow",
            "🐕 Dogs and roosters • Rada current",
        ],
    },
    {
        "name": "Baron Samedi",
        "image_key": "LWA_BARON_SAMEDI_URL",
        "description": "Gede lord of the grave, death, rebirth and sharp truth.",
        "attributes": [
            "🕯️ Rum with hot pepper, cigars, peanuts",
            "💀 Death, ancestors, fertility, gallows humor",
            "📆 Saturday • 🎨 Black, purple, white",
        ],
    },
    {
        "name": "Ogoun Badagri",
        "image_key": "LWA_OGOUN_BADAGRI_URL",
        "description": "Warrior of metal, revolution and disciplined force.",
        "attributes": [
            "🕯️ Rum, raw meat, iron tools",
            "⚔️ War, courage, politics, surgery",
            "📆 Tuesday • 🎨 Red, blue",
        ],
    },
    {
        "name": "Erzule Dantor",
        "image_key": "LWA_ERZULE_DANTOR_URL",
        "description": "Fierce protector of mothers, children and the wronged.",
        "attributes": [
            "🕯️ Black coffee, rum, pork, dark chocolate",
            "🗡️ Protection, vengeance, independence",
            "📆 Sat / Tue • 🎨 Dark blue, red, gold",
        ],
    },
    {
        "name": "Damballa Wedo",
        "image_key": "LWA_DAMBALA_WEDO_URL",
        "description": "Twin cosmic serpent of creation, purity and blessing.",
        "attributes": [
            "🕯️ White eggs, rice, milk, water",
            "🐍 Creation, peace, purity",
            "📆 Thursday • 🎨 White, silver",
        ],
    },
    {
        "name": "Bossou",
        "image_key": "LWA_BOSSOU_URL",
        "description": "Bull-like force of endurance, will and ground power.",
        "attributes": [
            "🕯️ Raw meat, rum, yams",
            "🐂 Strength, virility, stubborn power",
            "📆 Thursday • 🎨 Red, black",
        ],
    },
    {
        "name": "Ti Jan Dantor",
        "image_key": "LWA_TI_JAN_DANTOR_URL",
        "description": "Young fiery aspect of Dantor – passion and courage.",
        "attributes": [
            "🔥 Youth, daring, bold movement",
            "📆 Saturday • 🎨 Red, gold",
        ],
    },
    {
        "name": "Maman Brigitte",
        "image_key": "LWA_MAMAN_BRIGITTE_URL",
        "description": "Graveyard mistress, wife of Baron, sharp protector.",
        "attributes": [
            "🕯️ Rum with hot pepper, black bread",
            "💀 Graves, justice, honest speech",
            "📆 Saturday • 🎨 Purple, black, white",
        ],
    },
    {
        "name": "Kouzen Azaka",
        "image_key": "LWA_KOUZEN_AZAKA_URL",
        "description": "Peasant spirit of fields, farms, honest work.",
        "attributes": [
            "🌾 Sugar cane, beans, corn meal",
            "📆 Thursday • 🎨 Denim blue, straw brown",
        ],
    },
    {
        "name": "Marasa Dosou",
        "image_key": "LWA_MARASA_DOSOU_URL",
        "description": "Sacred twins – childlike purity and cosmic balance.",
        "attributes": [
            "👥 Candy, milk, white cakes",
            "📆 Sunday • 🎨 White, soft blue, pink",
        ],
    },
    {
        "name": "Kalfu",
        "image_key": "LWA_KALFU_URL",
        "description": "Night crossroads, wild chance, shadow roads.",
        "attributes": [
            "🕯️ Dark rum, spicy food, black candles",
            "🌒 Night magic, high-risk choices",
            "📆 Saturday night • 🎨 Black, red",
        ],
    },
    {
        "name": "Damballa",
        "image_key": "LWA_DAMBALLA_URL",
        "description": "Serpent of purity, silence and blessing breath.",
        "attributes": [
            "🕯️ White eggs, cool water, rice",
            "🐍 Peace, innocence, order",
            "📆 Thursday • 🎨 White, pale blue",
        ],
    },
    {
        "name": "Simbi",
        "image_key": "LWA_SIMBI_URL",
        "description": "Water, magic and communication current.",
        "attributes": [
            "💧 Rivers, streams, telepathy, divination",
            "📆 Wednesday • 🎨 Green, blue, white",
        ],
    },
    {
        "name": "Klemezine",
        "image_key": "LWA_KLEMEZINE_URL",
        "description": "Psychic and spiritual protection current.",
        "attributes": [
            "🛡️ Guarding, clarity, warding",
            "📆 Wednesday • 🎨 White, silver",
        ],
    },
    {
        "name": "Ayizan Velekete",
        "image_key": "LWA_AYIZAN_VELEKETE_URL",
        "description": "Matron of priesthood, markets and sacred order.",
        "attributes": [
            "🌿 Palm fronds, markets, initiation",
            "📆 Friday • 🎨 Yellow, gold, green",
        ],
    },
    {
        "name": "Gran Bwa",
        "image_key": "LWA_GRAN_BWA_URL",
        "description": "Forest master – herbs, wilderness and deep nature.",
        "attributes": [
            "🌳 Forests, roots, green mysteries",
            "📆 Thursday • 🎨 Green, brown",
        ],
    },
    {
        "name": "Hogou Ferralle",
        "image_key": "LWA_HOGOU_FERALLE_URL",
        "description": "Armored Ogun – disciplined war and defense.",
        "attributes": [
            "🛡️ Military, surgery, righteous fight",
            "📆 Tuesday • 🎨 Red, steel",
        ],
    },
    {
        "name": "Erzulie Freda",
        "image_key": "LWA_ERZULIE_FREDA_URL",
        "description": "Love, perfume, luxury and tender longing.",
        "attributes": [
            "💗 Champagne, perfume, sweets, flowers",
            "📆 Friday • 🎨 Pink, gold, white",
        ],
    },
    {
        "name": "Brav Gede",
        "image_key": "LWA_BRAV_GEDE_URL",
        "description": "Laughing Gede – jokes about death and truth.",
        "attributes": [
            "😈 Rum, popcorn, peanuts, cigars",
            "📆 Saturday • 🎨 Black, purple, white",
        ],
    },
]

# ------------------------------------------------------
# SUPPLICATION DATA (Ancestors + a few key lwa)
# ------------------------------------------------------
SUPPLICATION_DATA = {
    "Ancestors": {
        "offerings": [
            "Clean glass of fresh water",
            "White candle in safe holder",
            "Small plate of food your people would recognize",
            "Photos or written names of your beloved dead",
        ],
        "guidelines": [
            "Keep the altar space clean and respectful.",
            "Replace water often; do not leave spoiled food.",
            "Speak from the heart – you’re talking to real people.",
        ],
        "sample": """
Beloved Ancestors, blood and spirit,
known and unknown, I honor you.

I offer this water, this light, and this food
in gratitude for the lives you lived and the paths you walked.

If it is good and right, guide my steps,
protect my mind, and help me walk in dignity.

May you be elevated, remembered, and at peace.
Ayibobo.
""",
    },
    "Papa Legba": {
        "offerings": [
            "Coffee, rum (if appropriate), roasted corn",
            "Tobacco, candy, simple candle at a symbolic crossroads",
        ],
        "guidelines": [
            "Legba is the gatekeeper – often approached first.",
            "Be clear and honest about what you ask.",
            "Never promise what you cannot truly offer.",
        ],
        "sample": """
Papa Legba, Atibon Legba,
keeper of the crossroads, I greet you.

If this offering pleases you, open good roads before me —
roads of honest work, right relationship, and clear mind.
Close the ways that would drag me backward.

Mèsi, Papa Legba. Ayibobo.
""",
    },
    "Baron Samedi": {
        "offerings": [
            "Purple/black/white candles",
            "Rum with hot pepper, cigars, peanuts",
        ],
        "guidelines": [
            "Approach with seriousness and humor, never mockery.",
            "Do not play with the dead: keep requests within respect.",
        ],
        "sample": """
Baron Samedi, guardian of the boundary,
I come with respect and clean intention.

If you accept this drink and this light,
help me face the truth without fear,
and remember that my days are precious.

Where despair has settled, open a small road toward courage.
Ayibobo, Baron.
""",
    },
    "Erzulie Freda": {
        "offerings": [
            "Champagne or sweet liqueur",
            "Perfume, pink / white flowers, sweets",
        ],
        "guidelines": [
            "Focus on healing of the heart, not control of others.",
            "Ask for self-worth, honest love and beauty in life.",
        ],
        "sample": """
Erzulie Freda, lady of sweet waters,
if this offering pleases you,
heal what is bruised in my heart.

Teach me to love myself without vanity,
and others without chains.
Bring into my life relationships that honor my spirit.

Mèsi, Ezili Freda. Ayibobo.
""",
    },
}

# ------------------------------------------------------
# HOODOO SUPPLY SHOPS (summary)
# ------------------------------------------------------
HOODOO_SUPPLY_SHOPS = [
    {
        "name": "SHOPPE BLACK – Hoodoo Shops List",
        "url": "https://shoppeblack.us/black-owned-hoodoo-shops/",
        "desc": "Directory of Black-owned Hoodoo and spiritual shops so your money stays in the community.",
    },
    {
        "name": "Conjure South",
        "url": "https://conjuresouth.com/",
        "desc": "Queen Co. Meadows – Hoodoo, Obeah, gris-gris and writings rooted in lived practice.",
    },
    {
        "name": "Memphis Conjure",
        "url": "https://memphisconjure.com/",
        "desc": "Delta Hoodoo lineage shop from Memphis, “Mojo City”, with oils, powders and more.",
    },
    {
        "name": "The Hoodoo & Good Juju Botanica",
        "url": "https://hoodoogoodjuju.org/",
        "desc": "Botanica focused on Black community healing, roots and herbs.",
    },
    {
        "name": "Hoodoo Hussy Conjure Enterprises",
        "url": "https://hoodoohussy.squarespace.com/",
        "desc": "Condition oils, baths, incense and plant-based spiritual care.",
    },
]

# ------------------------------------------------------
# SMALL HELPERS
# ------------------------------------------------------
def media_image(key: str, caption: str = "", width=None):
    url = st.secrets.get(key, "")
    if not url:
        st.info(f"[{key}] image URL not set in secrets.")
        return
    st.image(url, caption=caption or None, use_column_width=(width is None), width=width)


def media_video(key: str, label: str = ""):
    url = st.secrets.get(key, "")
    if not url:
        st.info(f"[{key}] video URL not set in secrets.")
        return
    if label:
        st.markdown(f"**{label}**")
    st.video(url)


def render_header():
    st.markdown(
        """
        <div class="vh-header">
            <div class="vh-logo">🕯️</div>
            <div class="vh-title">VOODOO &amp; HOODOO SPELLS</div>
            <div class="vh-subtitle">
                From West African Vodun to Haitian Vodou, Louisiana Voodoo &amp; Hoodoo.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_footer():
    st.markdown(
        """
        <div class="vh-footer">
            This app is for respectful study, ancestor-honoring, and spiritual reflection only.
            It does not replace elders, clergy, therapy, or medical care.
        </div>
        """,
        unsafe_allow_html=True,
    )


def sidebar_mojo():
    with st.sidebar:
        st.markdown('<div class="sidebar-logo">VOODOO • HOODOO • ROOTS</div>', unsafe_allow_html=True)

        # Mojo music
        st.markdown("#### Louisiana “Mojo Music”")
        mojo_url = st.secrets.get("MOJO_MUSIC_URL", "")
        if mojo_url:
            st.markdown('<div class="mojo-video-glow mojo-video-container">', unsafe_allow_html=True)
            st.video(mojo_url)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.info("Set `MOJO_MUSIC_URL` in secrets for sidebar music.")

        # Mojo bag
        st.markdown("#### Mojo Bag")
        mojo_bag = st.secrets.get("MOJO_BAG_IMAGE_URL", "")
        if mojo_bag:
            st.markdown('<div class="mojo-bag-glow mojo-bag-container">', unsafe_allow_html=True)
            st.image(mojo_bag, caption="Mojo Bag", use_column_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.info("Set `MOJO_BAG_IMAGE_URL` in secrets for Mojo Bag art.")

        # Small incense
        st.markdown("---")
        st.markdown("#### Incense")
        st.markdown(
            """
            <div class="incense-container">
                <div class="incense-burner">🪔</div>
                <div class="smoke"></div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# ------------------------------------------------------
# DIVINATION & AI-STYLE HELPER
# ------------------------------------------------------
DIVINATION_ITEMS = {
    "Cowrie shells": [
        "Open shell: a road opening, conversation flowing.",
        "Closed shell: something withheld; more listening needed.",
        "Clustered shells: community and ancestors close.",
    ],
    "Bones": [
        "Bone toward you: take responsibility.",
        "Bone away from you: release what you cannot control.",
        "Crossed bones: conflict that needs honest words.",
    ],
    "Stones": [
        "Smooth white stone: clarity and truth.",
        "Dark stone: rest, retreat and recharge.",
        "Two stones touching: partnership and reconciliation.",
    ],
}


def pick_random_divination(tool: str) -> str:
    options = DIVINATION_ITEMS.get(tool, [])
    return random.choice(options) if options else ""


def random_lwa_omen():
    today = datetime.date.today()
    random.seed(today.toordinal())
    return random.choice(LOA_GALLERY_DATA)


def ai_style_suggestion(question: str) -> str:
    q = question.lower()
    picks = []

    def add(name):
        if name not in picks:
            picks.append(name)

    if any(k in q for k in ["road", "path", "blocked", "stuck", "direction"]):
        add("Papa Legba")
    if any(k in q for k in ["love", "relationship", "romance", "heart"]):
        add("Erzulie Freda")
    if any(k in q for k in ["protect", "safety", "abuse", "children"]):
        add("Erzule Dantor")
    if any(k in q for k in ["grave", "death", "dead", "cemetery", "ancestor"]):
        add("Baron Samedi")
    if any(k in q for k in ["money", "job", "work", "harvest"]):
        add("Kouzen Azaka")
    if any(k in q for k in ["war", "fight", "lawsuit", "conflict"]):
        add("Ogoun Badagri")
    if any(k in q for k in ["forest", "tree", "herb", "plants"]):
        add("Gran Bwa")
    if any(k in q for k in ["child", "children", "twins", "innocent"]):
        add("Marasa Dosou")

    if not picks:
        add("Ancestors")

    return ", ".join(picks)

# ------------------------------------------------------
# PAGES
# ------------------------------------------------------
def page_home():
    render_header()

    st.markdown(
        """
        <div class="vh-card">
        <h3>Welcome</h3>
        <p>
        This app is a living study altar: West African Vodun, Haitian Vodou, Louisiana Voodoo,
        and Black American Hoodoo. It is <strong>not</strong> a toy and not a substitute for elders.
        </p>
        <p>
        What you see here: history, imagery, safe offerings, ancestor veneration, journaling,
        divination for clarity, and links to real-world resources.
        No curses, no coercion, no self-harm work.
        </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    render_footer()


def page_vodun():
    render_header()
    st.subheader("West African Vodun – Roots in the Soil")

    st.markdown(
        """
        Vodun (Vodún, Vodoun) is a family of spiritual traditions among Fon, Ewe and related peoples
        in Benin, Togo, Ghana and Nigeria. There is no single holy book; knowledge lives in elders,
        drums, proverbs and shrines.
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)
    with col1:
        media_video("VODUN_VIDEO_URL", "Documentary / Overview")
    with col2:
        media_video("VODUN_VIDEO_2_URL", "Ritual / Festival Footage")

    render_footer()


def page_lwa():
    render_header()
    st.subheader("Lwa / Loas – Spirits of Haitian Vodou")

    st.markdown(
        """
        The lwa are distinct spirits with their own histories, veves, songs and ways of service.
        What follows is orientation only – initiation and deep work belongs in community.
        """,
        unsafe_allow_html=True,
    )

    for loa in LOA_GALLERY_DATA:
        st.markdown(f"### {loa['name']}")
        col_text, col_img = st.columns([2, 3])
        with col_text:
            st.markdown(
                f"<p style='font-size: 17px; line-height: 1.6;'>{loa['description']}</p>",
                unsafe_allow_html=True,
            )
            for line in loa["attributes"]:
                st.markdown(f"- {line}")
        with col_img:
            media_image(loa["image_key"], caption=loa["name"], width=520)
        st.markdown("---")

    render_footer()


def page_hoodoo():
    render_header()
    st.subheader("Hoodoo / Rootwork – Black American Conjure")

    st.markdown(
        """
        Hoodoo (conjure, rootwork) is a Black American folk-magic system grown from African roots,
        Native knowledge and European influences – especially in the U.S. South.
        It is often practiced alongside Christianity.
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="vh-card">
        <h3>Key Themes</h3>
        <ul>
          <li>Mojo hands / nation sacks, like the glowing Mojo Bag in your sidebar.</li>
          <li>Condition oils, powders, baths and floor washes for specific needs.</li>
          <li>Work for uncrossing, protection, justice, money-drawing and love – with the
              understanding that <em>what you do returns to you</em>.</li>
          <li>Strong connection to the Psalms and biblical language.</li>
        </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

    render_footer()


def page_ancestors():
    render_header()
    st.subheader("Ancestor Veneration")

    data = SUPPLICATION_DATA["Ancestors"]

    st.markdown("### Offerings")
    for o in data["offerings"]:
        st.markdown(f"- {o}")

    st.markdown("### Guidelines")
    for g in data["guidelines"]:
        st.markdown(f"- {g}")

    st.markdown("### Sample Words")
    st.code(data["sample"].strip())

    render_footer()


def page_supplications():
    render_header()
    st.subheader("Supplications & Offerings")

    names = list(SUPPLICATION_DATA.keys())
    choice = st.selectbox("Choose spirit / Ancestors", names, index=0)
    data = SUPPLICATION_DATA[choice]

    st.markdown(f"### {choice}")
    st.markdown("#### Offerings")
    for o in data["offerings"]:
        st.markdown(f"- {o}")

    st.markdown("#### Guidelines")
    for g in data["guidelines"]:
        st.markdown(f"- {g}")

    st.markdown("#### Suggested Words")
    st.code(data["sample"].strip())

    render_footer()


def page_divination_omens():
    render_header()
    st.subheader("Divination & Omens")

    st.markdown(
        """
        This is a gentle, symbolic divination helper. It does not replace a full reading by an
        initiated priest or reader – it is more like pulling a proverb for the day.
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### 1. Quick Throw")
    tool = st.selectbox("Choose your divination tool", list(DIVINATION_ITEMS.keys()))
    if st.button("Cast & Read"):
        msg = pick_random_divination(tool)
        st.success(msg)

    st.markdown("---")
    st.markdown("### 2. Daily Lwa Omen")

    loa = random_lwa_omen()
    col1, col2 = st.columns([2, 3])
    with col1:
        st.markdown(f"**Spirit to meditate on today:** {loa['name']}")
        st.markdown(loa["description"])
    with col2:
        media_image(loa["image_key"], caption=loa["name"], width=420)

    st.markdown("---")
    st.markdown("### 3. Spirit Suggestion Helper")

    q = st.text_area(
        "Describe what you need help with (non-harmful only):",
        placeholder="Example: I feel blocked in work and unsure which direction to move...",
    )
    if q.strip():
        suggestion = ai_style_suggestion(q)
        st.info(
            f"Based on what you wrote, spirits whose themes might be relevant include: **{suggestion}**.\n\n"
            "This is not divination, just a study pointer."
        )

    render_footer()


def page_spell_journal_voice():
    render_header()
    st.subheader("Spell Journal & Voice Invocation")

    if "journal_entries" not in st.session_state:
        st.session_state["journal_entries"] = []

    st.markdown("### Spell / Prayer Journal")
    txt = st.text_area(
        "Write what you did, saw, dreamed or prayed:",
        height=180,
        placeholder="Tonight I lit a white candle for my ancestors and prayed for clarity...",
    )
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Save Entry"):
            if txt.strip():
                st.session_state["journal_entries"].append(
                    {
                        "time": datetime.datetime.now().isoformat(timespec="seconds"),
                        "text": txt.strip(),
                    }
                )
                st.success("Entry saved (this browser session).")
    with col2:
        if st.button("Clear Journal (this session)"):
            st.session_state["journal_entries"] = []
            st.warning("Cleared.")

    if st.session_state["journal_entries"]:
        st.markdown("#### Entries This Session")
        for e in reversed(st.session_state["journal_entries"]):
            st.markdown(f"**{e['time']}**")
            st.markdown(e["text"])
            st.markdown("---")

        blob = "\n\n".join(f"{e['time']}\n{e['text']}" for e in st.session_state["journal_entries"])
        st.download_button(
            "Download Journal (TXT)",
            data=blob.encode("utf-8"),
            file_name="voodoo_hoodoo_journal.txt",
            mime="text/plain",
        )

    st.markdown("---")
    st.markdown("### Voice Invocation")

    chant_url = st.secrets.get("VOICE_CHANT_URL", "")
    if chant_url:
        st.audio(chant_url)
        st.caption("Optional chant / drum track set in `VOICE_CHANT_URL`.")
    else:
        st.info("Set `VOICE_CHANT_URL` in secrets to embed a chant or drum track.")

    st.markdown(
        """
        Speak slowly and clearly. Address Ancestors, God, or a lwa respectfully and leave silence
        after you speak so your own spirit can answer.
        """,
        unsafe_allow_html=True,
    )

    render_footer()


def page_pdf_library():
    render_header()
    st.subheader("PDF Library – Hoodoo in the Psalms")

    pdf_path = Path("Hoodoo_in_the_Psalms.pdf")
    if pdf_path.exists():
        pdf_bytes = pdf_path.read_bytes()
        st.download_button(
            "📖 Download “Hoodoo in the Psalms”",
            data=pdf_bytes,
            file_name="Hoodoo_in_the_Psalms.pdf",
            mime="application/pdf",
        )
    else:
        st.error("`Hoodoo_in_the_Psalms.pdf` not found next to app.py. Add it and redeploy.")

    render_footer()


def page_resources():
    render_header()
    st.subheader("Supplies & Resources")

    for shop in HOODOO_SUPPLY_SHOPS:
        st.markdown(f"### [{shop['name']}]({shop['url']})")
        st.markdown(shop["desc"])
        st.markdown("---")

    render_footer()


def page_account_initiation():
    render_header()
    st.subheader("Account Blessings & Initiation Notes")

    st.markdown("### Personal Blessing (local only)")
    name = st.text_input("Your name or ritual name")
    focus = st.text_input("Main focus right now (protection, clarity, courage, etc.)")
    fav = st.text_input("Spirit you feel closest to (Ancestors, Papa Legba, etc.)")

    if st.button("Generate Blessing Text"):
        if not name.strip():
            st.warning("Give at least a name so the blessing has somewhere to land.")
        else:
            st.success(
                f"""
{name}, may your steps be watched by your ancestors
and by the spirits you walk with.

May your work around **{focus or 'the path before you'}**
be guided by wisdom and protected from confusion.

If it is right with {fav or 'the spirits'},
may good doors open and destructive doors quietly close.

Ayibobo.
"""
            )

    st.markdown("---")
    st.subheader("Initiation-Locked Note")

    code = st.text_input("Enter initiation code (set INITIATION_CODE in secrets)", type="password")
    real_code = st.secrets.get("INITIATION_CODE", "")
    if real_code and code:
        if code == real_code:
            st.success("Gate opened.")
            st.markdown(
                """
                - Keep a physical notebook for dreams, omens and altar work.  
                - Monitor your mental and physical health; spirits do not replace doctors.  
                - Saying “no” to work you do not understand is also part of the path.
                """,
                unsafe_allow_html=True,
            )
        else:
            st.error("Code not recognized. Better to leave the gate closed than force it.")

    render_footer()


def page_settings():
    render_header()
    st.subheader("Settings – Drum Track & Atmosphere")

    drum = st.secrets.get("DRUMS_AUDIO_URL", "")
    if drum:
        st.audio(drum)
        st.caption("Ritual drum track from `DRUMS_AUDIO_URL` – use gently.")
    else:
        st.info("Set `DRUMS_AUDIO_URL` in secrets to embed a drum rhythm.")

    render_footer()

# ------------------------------------------------------
# MAIN
# ------------------------------------------------------
def main():
    sidebar_mojo()

    pages = {
        "Home": page_home,
        "West African Vodun": page_vodun,
        "Lwa / Loas": page_lwa,
        "Hoodoo / Rootwork": page_hoodoo,
        "Ancestor Veneration": page_ancestors,
        "Supplications & Offerings": page_supplications,
        "Divination & Omens": page_divination_omens,
        "Spell Journal & Voice": page_spell_journal_voice,
        "PDF Library": page_pdf_library,
        "Supplies & Resources": page_resources,
        "Account & Initiation": page_account_initiation,
        "Settings": page_settings,
    }

    with st.sidebar:
        st.markdown("---")
        choice = st.radio("Navigate", list(pages.keys()), index=0)

    pages[choice]()


if __name__ == "__main__":
    main()
