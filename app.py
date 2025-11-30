import streamlit as st
import random
import datetime
from pathlib import Path

# =========================
# BASIC CONFIG
# =========================

st.set_page_config(
    page_title="Voodoo & Hoodoo Spells",
    page_icon="🕯️",
    layout="wide",
)


# =========================
# CSS THEMES (DAY & NIGHT)
# =========================

APP_CSS_DAY = """
<style>
body, .stApp {
    background-color: #050505;
    color: #f4efe6;
    font-family: "Times New Roman", Times, serif;
    font-size: 16px;
    line-height: 1.75;
}

/* Main container width & padding */
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

/* 🔥 Mojo heartbeat glow for sidebar media (separate tiles, synced timing) */
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

/* Shared heartbeat animation for header candle */
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

/* Sharper red pulse for player */
@keyframes mojo-video-pulse {
    0%   { box-shadow: 0 0 4px rgba(255, 0, 0, 0.6); }
    50%  { box-shadow: 0 0 14px rgba(255, 0, 0, 1.0); }
    100% { box-shadow: 0 0 4px rgba(255, 0, 0, 0.6); }
}

/* Golden pulse for Mojo Bag */
@keyframes mojo-bag-pulse {
    0%   { box-shadow: 0 0 4px rgba(255, 215, 0, 0.6); }
    50%  { box-shadow: 0 0 14px rgba(255, 215, 0, 1.0); }
    100% { box-shadow: 0 0 4px rgba(255, 215, 0, 0.6); }
}

/* Incense burner & smoke animation */
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

/* Zulu shield-like buttons */
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

/* Spear icon */
div.stButton > button::before {
    content: "⚔️";
    margin-right: 0.35rem;
    text-shadow:
        0 0 6px rgba(244,67,54,0.9),
        0 0 10px rgba(0,0,0,0.7);
}

/* Button hover */
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

/* Pill label */
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

# Night theme: keep structure but slightly colder / more purple
APP_CSS_NIGHT = """
<style>
body, .stApp {
    background-color: #020208;
    color: #f1e6ff;
    font-family: "Times New Roman", Times, serif;
    font-size: 16px;
    line-height: 1.75;
}
.block-container {
    max-width: 1100px;
    padding-top: 1.2rem;
}
.vh-header { text-align:center; padding: 0.75rem 0 0.25rem 0; }
.vh-logo {
    font-size: 3.4rem;
    text-shadow:
        0 0 12px rgba(156,39,176,0.95),
        0 0 20px rgba(0,0,0,1.0);
    animation: mojo-heartbeat 1.6s ease-in-out infinite;
}
.vh-title {
    font-size: 2.4rem;
    font-weight: 800;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #ce93d8;
    text-shadow:
        0 0 12px rgba(156,39,176,1.0),
        0 0 26px rgba(0,0,0,1.0);
}
.vh-subtitle { font-size: 1rem; opacity: 0.95; }

section[data-testid="stSidebar"] {
    background: radial-gradient(circle at top, #210038 0%, #04000a 55%, #000 100%);
    border-right: 1px solid rgba(103,58,183,0.8);
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
    background: radial-gradient(circle at 30% 0%, #3a005e 0%, #050010 55%, #000 100%);
    border: 1px solid rgba(156,39,176,0.8);
    box-shadow:
        0 0 10px rgba(156,39,176,0.6),
        0 0 18px rgba(0,0,0,0.9),
        inset 0 0 6px rgba(0,0,0,0.7);
}

/* reuse pulses */
.mojo-video-glow, .mojo-bag-glow { border-radius: 16px; padding: 0.45rem; }
.mojo-video-glow {
    background: radial-gradient(circle at 50% 0%, #1f0022 0, #090010 55%, #000000 100%);
    box-shadow: 0 0 4px rgba(244, 143, 177, 0.8);
    animation: mojo-video-pulse 1.6s ease-in-out infinite;
}
.mojo-bag-glow {
    background: radial-gradient(circle at 50% 0%, #1d1400 0, #090600 55%, #000 100%);
    box-shadow: 0 0 4px rgba(255, 215, 0, 0.9);
    animation: mojo-bag-pulse 1.6s ease-in-out infinite;
}
.mojo-video-container iframe { border-radius: 12px; width: 100%; height: 118px; }
.mojo-bag-container img { border-radius: 14px; display:block; margin:0 auto; }

/* incence + heartbeat reused from day */
.smoke { width: 4px; height: 60px; margin: 0 auto;
         background: linear-gradient(to top, rgba(255,255,255,0.0), rgba(209,196,233,0.6));
         border-radius: 999px; animation: smoke-rise 4.2s ease-in-out infinite; }

.vh-card {
    border-radius: 16px;
    border: 1px solid rgba(156,39,176,0.85);
    padding: 1.2rem 1.45rem;
    margin-bottom: 1.1rem;
    background: radial-gradient(circle at top, #130019 0%, #06000a 55%, #010101 100%);
    box-shadow:
        0 0 16px rgba(156,39,176,0.65),
        0 0 28px rgba(0,0,0,0.98);
}
.vh-footer {
    text-align:center;
    font-size: 0.9rem;
    color: #d1c4e9;
    margin-top: 2.8rem;
    padding-top: 0.9rem;
    border-top: 1px solid rgba(103,58,183,0.8);
    opacity: 0.95;
}

div.stButton > button {
    border-radius: 999px / 70px;
    border-width: 2px;
    border-style: solid;
    border-color: #4527a0;
    padding: 0.45rem 1.9rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.09em;
    font-family: "Times New Roman", Times, serif;
    font-size: 15px;

    background-image:
        linear-gradient(135deg, #7b1fa2 0%, #000000 40%, #283593 100%),
        radial-gradient(circle at 16% 0%, rgba(255,255,255,0.25) 0%, transparent 60%);
    background-blend-mode: overlay;
    color: #f3e5f5;
}
</style>
"""


def apply_theme():
    """Apply CSS according to theme stored in session_state."""
    theme = st.session_state.get("theme", "day")
    if theme == "night":
        st.markdown(APP_CSS_NIGHT, unsafe_allow_html=True)
    else:
        st.markdown(APP_CSS_DAY, unsafe_allow_html=True)


apply_theme()


# =========================
# LWA / LOA GALLERY DATA (19)
# (from your previous configuration)
# =========================

# NOTE: image_key MUST match keys you set in Streamlit secrets
LOA_GALLERY_DATA = [
    {
        "name": "Papa Legba",
        "image_key": "LWA_PAPA_LEGBA_URL",
        "description": "Papa Legba is the gatekeeper at the crossroads, facilitator of communication between worlds.",
        "attributes": [
            "🕯️ Offerings: tobacco, coffee, rum, sugar cane, roasted corn",
            "🔑 Domains: crossroads, guidance, language, access, destiny",
            "📅 Feast Day: June 13",
            "📆 Day of the week (trad.): Monday",
            "🎨 Colors: red, black, yellow, brown",
            "⛪ Syncretized Saint: St. Peter",
            "🐕 Sacred Animals: dogs, roosters",
            "🌿 Sacred Plants: basil, bay leaf, tobacco leaf",
            "🗝️ Symbols: cane, crutches, keys, crossroads",
            "⚠️ Caution: Must ALWAYS be invoked first — or no spirit will arrive",
            "🔥 Classification: Rada",
        ],
    },
    {
        "name": "Baron Samedi",
        "image_key": "LWA_BARON_SAMEDI_URL",
        "description": "Baron Samedi is the spirit of death, rebirth, and ancestor gateways.",
        "attributes": [
            "🕯️ Offerings: rum, cigars, grilled corn, peanuts, black coffee",
            "💀 Domains: death, resurrection, fertility, ancestor communication",
            "📅 Feast Day: November 2 (Fête des Morts)",
            "📆 Day of the week (trad.): Saturday",
            "⛪ Syncretized Saint: Saint Martin de Porres",
            "🎨 Colors: black, purple, white",
            "⚰️ Symbols: top hat, skull, cross, sunglasses",
            "🐓 Sacred Animals: black roosters",
            "🌶️ Sacred Foods: hot peppers",
            "😈 Behavior: crude humor, sexually explicit jokes",
            "🔥 Classification: Gede",
        ],
    },
    {
        "name": "Ogoun Badagri",
        "image_key": "LWA_OGOUN_BADAGRI_URL",
        "description": "Ogoun Badagri is a warrior spirit of force, metal, leadership and revolution.",
        "attributes": [
            "🕯️ Offerings: rum, raw meat, red beans, iron tools, cigars",
            "⚔️ Domains: war, metal, blood, military action, political force",
            "📅 Feast Day: July 25 (varies)",
            "📆 Day of the week (trad.): Tuesday",
            "⛪ Syncretized Saint: St. James the Greater",
            "🎨 Colors: red, blue",
            "🧲 Sacred Metals: iron, steel",
            "🐓 Sacred Animals: ram, dogs",
            "⚠️ Caution: Very strong — do not call without intent & purpose",
            "🔥 Classification: Petro / Nago",
        ],
    },
    {
        "name": "Erzule Dantor",
        "image_key": "LWA_ERZULE_DANTOR_URL",
        "description": "Erzule Dantor is the fierce protector of women, mothers, and children.",
        "attributes": [
            "🕯️ Offerings: black coffee, blue candles, rum, pork, dark chocolate",
            "🔥 Domains: protection, vengeance, motherhood, independence",
            "📆 Day of the week (trad.): Tuesday or Saturday (varies by house)",
            "⛪ Syncretized Saint: Mater Dolorosa",
            "🎨 Colors: dark blue, red, gold",
            "🐗 Sacred Animals: pigs, boars",
            "🗡️ Symbols: dagger, scratched heart",
            "⚠️ Caution: Protective but fierce — reacts to injustice",
            "🔥 Classification: Petro",
        ],
    },
    {
        "name": "Damballa Wedo",
        "image_key": "LWA_DAMBALA_WEDO_URL",
        "description": "Damballa Wedo, the twin cosmic serpents, bring harmony and celestial breath.",
        "attributes": [
            "🕯️ Offerings: white eggs, rice, cool water, flour, milk",
            "🐍 Domains: creation, purity, cosmic blessing",
            "📆 Day of the week (trad.): Thursday",
            "⛪ Syncretized Saint: St. Patrick",
            "🎨 Colors: white, silver",
            "🧊 Caution: No alcohol, no profanity, no spicy foods",
            "🐍 Symbols: snakes",
            "🌈 Sacred Element: rainbow",
            "🔥 Classification: Rada",
        ],
    },
    {
        "name": "Bossou",
        "image_key": "LWA_BOSSOU_URL",
        "description": "Bossou is a bull-spirit representing unstoppable force and endurance.",
        "attributes": [
            "🕯️ Offerings: raw meat, rum, cigars, yams",
            "🐂 Domains: strength, virility, ground power",
            "📆 Day of the week (trad.): Thursday",
            "🎨 Colors: red, black",
            "⚠️ Caution: Very intense — should be handled by experienced priests",
            "🔥 Classification: Nago / Petro",
        ],
    },
    {
        "name": "Ti Jan Dantor",
        "image_key": "LWA_TI_JAN_DANTOR_URL",
        "description": "Spirit of youthful fire, passion, and courageous energy.",
        "attributes": [
            "🕯️ Offerings: rum, red fruit, candied ginger",
            "🔥 Domains: youth, passion, fearless action",
            "📆 Day of the week (trad.): Saturday",
            "🎨 Colors: red, gold",
            "⚠️ Caution: Impulsive — must be guided with discipline",
            "🔥 Classification: Petro",
        ],
    },
    {
        "name": "Maman Brigitte",
        "image_key": "LWA_MAMAN_BRIGITTE_URL",
        "description": "Maman Brigitte guards the graves and protects the dead.",
        "attributes": [
            "🕯️ Offerings: rum with hot pepper, candles, black bread",
            "💀 Domains: graves, justice, death, past lives",
            "📆 Day of the week (trad.): Saturday",
            "⛪ Syncretized Saint: St. Brigid / Brigid of Kildare",
            "🎨 Colors: purple, black, white",
            "🐓 Sacred Animals: black hen",
            "🔥 Classification: Gede",
        ],
    },
    {
        "name": "Kouzen Azaka",
        "image_key": "LWA_KOUZEN_AZAKA_URL",
        "description": "Kouzen Azaka is the rural peasant spirit of farming, honesty, and simple living.",
        "attributes": [
            "🕯️ Offerings: sugar cane, bread, beans, corn meal, fresh fruit",
            "🌾 Domains: agriculture, rural life, diligence",
            "📆 Day of the week (trad.): Thursday",
            "⛪ Syncretized Saint: St. Isidore the Farmer",
            "🎨 Colors: denim blue, straw brown",
            "🔥 Classification: Rada",
        ],
    },
    {
        "name": "Marasa Dosou",
        "image_key": "LWA_MARASA_DOSOU_URL",
        "description": "The Marasa are sacred twins representing divine polarity — duality in unity, childlike purity, and cosmic symmetry.",
        "attributes": [
            "🕯️ Offerings: candies, milk, white cakes, coconut, popcorn",
            "👥 Domains: twins, childhood, cosmic balance, innocence",
            "📆 Day of the week (trad.): Sunday",
            "🎨 Colors: white, light blue, pink",
            "⛪ Syncretized Saints: Saints Cosmas and Damian",
            "🐓 Sacred Animals: doves",
            "🌿 Plants: coconut palm",
            "⚠️ Caution: ALWAYS feed both — never make an offering to one twin alone",
            "🔥 Classification: Rada",
        ],
    },
    {
        "name": "Kalfu",
        "image_key": "LWA_KALFU_URL",
        "description": "Kalfu rules the powerful crossroads of the night and governs the darker pathways of fate and possibility.",
        "attributes": [
            "🕯️ Offerings: dark rum, gunpowder, spicy food, black candles",
            "🌒 Domains: night magic, crossroads, destiny manipulation",
            "📆 Day of the week (trad.): Saturday (night works)",
            "🎨 Colors: black, red",
            "🗝️ Symbols: inverted crosses, shadowed crossroads",
            "⚠️ Caution: Do NOT invoke without Legba’s permission",
            "🔥 Classification: Petro",
        ],
    },
    {
        "name": "Damballa",
        "image_key": "LWA_DAMBALLA_URL",
        "description": "Damballa embodies purity, wisdom, innocence, and the breath of creation — a calm serpent of heavenly radiance.",
        "attributes": [
            "🕯️ Offerings: white eggs, filtered water, rice, coconut milk",
            "🐍 Domains: creation, peace, purity, celestial order",
            "📆 Day of the week (trad.): Thursday",
            "🎨 Colors: white, silver, pale blue",
            "⛪ Syncretized Saint: St. Patrick",
            "⚠️ Caution: No alcohol or profanity",
            "🔥 Classification: Rada",
        ],
    },
    {
        "name": "Simbi",
        "image_key": "LWA_SIMBI_URL",
        "description": "Simbi is a water and communication spirit — associated with magic, telepathy, divination, and flowing intelligence.",
        "attributes": [
            "🕯️ Offerings: rum, fresh water, anise, fish",
            "💧 Domains: water, magic, channeling, spiritual transmission",
            "📆 Day of the week (trad.): Wednesday",
            "🎨 Colors: green, blue, white",
            "🌊 Sacred Places: rivers, springs, wells",
            "🔥 Classification: Rada / Kongo",
        ],
    },
    {
        "name": "Klemezine",
        "image_key": "LWA_KLEMEZINE_URL",
        "description": "Klemezine offers psychic and spiritual protection — a firm yet gentle guardian of sacred spaces.",
        "attributes": [
            "🕯️ Offerings: white rum, silver jewelry, incense",
            "🛡️ Domains: protection, clarity, defensive magic",
            "📆 Day of the week (trad.): Wednesday",
            "🎨 Colors: white, silver, grey",
            "🌿 Plants: sage, palm leaf",
            "🔥 Classification: Rada / Kongo",
        ],
    },
    {
        "name": "Ayizan Velekete",
        "image_key": "LWA_AYIZAN_VELEKETE_URL",
        "description": "Ayizan is the matron of priesthood, commerce, and spiritual initiation — keeper of sacred lineage.",
        "attributes": [
            "🕯️ Offerings: cassava, breadfruit, palm wine, corn",
            "🌿 Domains: priesthood, social order, commerce, knowledge",
            "📆 Day of the week (trad.): Friday",
            "🎨 Colors: gold, yellow, green",
            "🌿 Sacred Plants: palm frond",
            "⛪ Syncretized Saint: St. Clare",
            "🔥 Classification: Rada",
        ],
    },
    {
        "name": "Gran Bwa",
        "image_key": "LWA_GRAN_BWA_URL",
        "description": "Gran Bwa is master of the forest, herbal mysteries, and green life — a primal nature spirit.",
        "attributes": [
            "🕯️ Offerings: tobacco, honey, herbs, fresh fruit",
            "🌳 Domains: nature, wilderness, secrets of plants",
            "📆 Day of the week (trad.): Thursday",
            "🎨 Colors: green, brown",
            "🌿 Sacred Plants: vetiver grass",
            "🔥 Classification: Kongo",
        ],
    },
    {
        "name": "Hogou Ferralle",
        "image_key": "LWA_HOGOU_FERALLE_URL",
        "description": "Hogou Ferralle is an armored aspect of Ogun — the disciplined, militant, steel-willed warforce.",
        "attributes": [
            "🕯️ Offerings: iron nails, rum, whiskey, blood sausage",
            "🛡️ Domains: warfare, iron, defense, righteous conflict",
            "📆 Day of the week (trad.): Tuesday",
            "🎨 Colors: red, metallic steel",
            "⛪ Syncretized Saint: St. George",
            "🔥 Classification: Nago / Petro",
        ],
    },
    {
        "name": "Erzulie Freda",
        "image_key": "LWA_ERZULIE_FREDA_URL",
        "description": "Erzulie Freda is the patroness of love, romance, perfume, elegance and sensual beauty.",
        "attributes": [
            "🕯️ Offerings: champagne, perfumes, sweets, pink flowers",
            "💗 Domains: romance, luxury, femininity, emotional longing",
            "📆 Day of the week (trad.): Friday",
            "🎨 Colors: pink, gold, white",
            "⛪ Syncretized Saint: Our Lady of Sorrows",
            "🔥 Classification: Rada",
        ],
    },
    {
        "name": "Brav Gede",
        "image_key": "LWA_BRAV_GEDE_URL",
        "description": "Brav Gede walks the line between life and death, using humor as spiritual medicine.",
        "attributes": [
            "🕯️ Offerings: rum, peanuts, popcorn, cigars",
            "😈 Domains: death, sexuality, laughter, truth-telling",
            "📆 Day of the week (trad.): Saturday",
            "🎨 Colors: black, purple, white",
            "💀 Symbols: skull, cross of the cemetery",
            "🔥 Classification: Gede",
        ],
    },
]


# =========================
# CURATED SUPPLY SHOPS
# =========================

HOODOO_SUPPLY_SHOPS = [
    {
        "name": "SHOPPE BLACK",
        "url": "https://shoppeblack.us/black-owned-hoodoo-shops/",
        "tagline": "Your gateway to the global Black business ecosystem",
        "description": (
            "A platform that highlights and supports Black-owned businesses worldwide. "
            "This link gathers Black-owned Hoodoo and spiritual shops so your money "
            "circulates within the community."
        ),
        "location": "Online / Global",
    },
    {
        "name": "Conjure South",
        "url": "https://conjuresouth.com/",
        "tagline": "Hoodoo • Obeah • Gris-gris from Queen Co. Meadows",
        "description": (
            "Founded by Queen Co. Meadows in Mobile, Alabama. Offers traditional Hoodoo, Obeah, "
            "and gris-gris products, along with publications and educational resources rooted "
            "in lived practice."
        ),
        "location": "Mobile, Alabama (USA) + Online",
    },
    {
        "name": "Memphis Conjure",
        "url": "https://memphisconjure.com/",
        "tagline": "Master-crafted by hand • Authentic • Affordable • Delta Hoodoo",
        "description": (
            "Family-run Memphis Conjure Supply, tracing a 110-year lineage in Delta Hoodoo and "
            "over 30 years of experience. Recognized in Tony Kail’s 'Stories of Rootworkers & "
            "Hoodoo in the Mid-South'. Historically located in Memphis, Tennessee — known as "
            "“Mojo City”."
        ),
        "location": "Memphis, Tennessee (USA) + Online",
    },
    {
        "name": "The Hoodoo & Good Juju Botanica",
        "url": "https://hoodoogoodjuju.org/",
        "tagline": "Healing the homies, werking the roots",
        "description": (
            "A botanica focused on returning the authority and heritage of Hoodoo traditions "
            "to the Black community. Offers organic roots, herbs, and spiritual medicines."
        ),
        "location": "Online (Black-centered)",
    },
    {
        "name": "Hoodoo Hussy Conjure Enterprises",
        "url": "https://hoodoohussy.squarespace.com/",
        "tagline": "Spiritual care via plant medicine & tradition",
        "description": (
            "Provides spiritual care rooted in African and African American traditional practices. "
            "Carries condition oils, cleansing sprays, incense, spiritual bath teas, and more."
        ),
        "location": "Online",
    },
    {
        "name": "BLK + GRN",
        "url": "https://blkgrn.com/",
        "tagline": "All-natural marketplace curated by Black artisans",
        "description": (
            "A marketplace featuring all-natural products from over 60 Black artisans, including "
            "wellness, self-care, and some spiritually aligned items."
        ),
        "location": "Online",
    },
    {
        "name": "Sacred Botanica",
        "url": "https://www.sacredbotanicabk.com/",
        "tagline": "Incense, candles, crystals & spiritual advisement",
        "description": (
            "Offers incense, candles, crystals, and spiritual advisements via Zoom, including tarot "
            "and astrology readings. Brooklyn-based with an online presence."
        ),
        "location": "Brooklyn, New York (USA) + Online",
    },
]


# =========================
# SUPPLICATION / OFFERING DATA (SAFE)
#  (shortened here, but keeps your Ancestors + key lwa)
# =========================

SUPPLICATION_DATA = {
    "Ancestors": {
        "type": "Ancestors",
        "offerings": [
            "A clean glass of fresh water",
            "A white candle in a safe holder",
            "A small plate of food your people would recognize",
            "Photos or written names of your beloved dead",
        ],
        "guidelines": [
            "Keep the space clean and respectful.",
            "Speak to them as you would to elders you love, not as servants.",
            "Replace water regularly; do not leave spoiled food.",
        ],
        "sample_words": """
Beloved Ancestors, blood and spirit,
those whose names I know and those whose names I have forgotten,
I honor you.

I offer you this water, this light, and this food
in gratitude for the lives you lived,
for the paths you walked,
and for the strength that flows through me from you.

If it is right and aligned with the good order of things,
please watch over me, guide my steps,
and help me walk in dignity, courage, and wisdom.

May you be elevated, remembered, and at peace.
Ayibobo.
""",
    },
    # For brevity we keep a few key lwa examples; you can add more
    "Papa Legba": {
        "type": "Lwa",
        "offerings": [
            "Black coffee (no sugar) or coffee with a little sugar",
            "A small cup of rum (if appropriate to your house / teacher)",
            "Tobacco, candy, or roasted corn",
            "A simple candle (often white or red) at a crossroads imagery",
        ],
        "guidelines": [
            "Legba is gatekeeper: in many houses he is approached first before other lwa.",
            "Keep the tone respectful and clear; ask for open, honest roads.",
            "Never promise what you cannot sincerely offer in return.",
        ],
        "sample_words": """
Papa Legba, Atibon Legba,
keeper of the crossroads and opener of the way, I greet you with respect.

If it is pleasing to you, accept this coffee/rum and light,
and open good roads before me:
roads of right relationship, roads of honest work,
roads where my head can be clear.

Do not open doors that would destroy me.
Open instead the ways that are good for my spirit
and close the ways that would drag me backward.

Mèsi anpil, Papa Legba. Ayibobo.
""",
    },
    "Baron Samedi": {
        "type": "Lwa",
        "offerings": [
            "Purple, black, or white candle",
            "Small glass of rum (often with hot pepper)",
            "Cigars or tobacco",
            "Black coffee or grilled corn/peanuts",
        ],
        "guidelines": [
            "Baron is powerful — approach with seriousness and humor, but not mockery.",
            "Keep all work with the dead respectful.",
            "Avoid asking for harm; focus on courage, clarity, healing.",
        ],
        "sample_words": """
Baron Samedi, guardian of the grave and lord of the boundary,
I come with respect and clean intention.

If you accept my light and this drink,
stand by the gates between life and death for me and mine.
Help me face the truth without fear,
and teach me to remember that life is short and precious.

Where there is sickness of the spirit, bring clarity and laughter that heals.
Where there is despair, open a little road toward courage.

If it is not right to intervene, let me be at peace with that.
Ayibobo, Baron.
""",
    },
    "Erzulie Freda": {
        "type": "Lwa",
        "offerings": [
            "Glass of champagne or sweet liqueur",
            "Perfume or scented oil in a small dish",
            "Pink or white flowers",
            "Pastel candles",
        ],
        "guidelines": [
            "Freda is about refined love, not manipulation.",
            "Avoid asking to control another person’s will.",
            "Ask for healing of the heart, self-worth, and good partnership.",
        ],
        "sample_words": """
Erzulie Freda, lady of sweet waters and delicate perfume,
if this offering pleases you, pour beauty, self-respect and healthy love into my life.

Heal what is bruised in my heart, and teach me to love
myself without vanity and others without chains.

Keep me away from relationships that are false or degrading.
Bring me into connections that honor my soul.

Mèsi, Ezili Freda. Ayibobo.
""",
    },
}


# =========================
# HELPERS
# =========================

def media_image(secret_key: str, caption: str = "", width=None):
    """Render image from secrets; supports http URLs or local 'images/...'. """
    url = st.secrets.get(secret_key, "")
    if not url:
        st.info(f"[{secret_key}] image not configured in secrets.")
        return

    # Local file
    if url.startswith("images/") or url.startswith("./images/"):
        try:
            st.image(url, caption=caption or None,
                     use_column_width=(width is None), width=width)
        except Exception as e:
            st.error(f"[{secret_key}] local image error: {e}")
        return

    # Remote
    st.image(url, caption=caption or None,
             use_column_width=(width is None), width=width)


def media_video(secret_key: str, label: str = ""):
    """Render YouTube-style video from secrets (expects full iframe-able URL)."""
    url = st.secrets.get(secret_key, "")
    if not url:
        st.info(f"[{secret_key}] video not configured.")
        return
    st.markdown(f"**{label}**" if label else "", unsafe_allow_html=True)
    st.video(url)


def render_header():
    st.markdown(
        """
        <div class="vh-header">
            <div class="vh-logo">🕯️</div>
            <div class="vh-title">VOODOO &amp; HOODOO SPELLS</div>
            <div class="vh-subtitle">
                From West African Vodun to Haitian Vodou, New Orleans Voodoo &amp; Black American Hoodoo —
                a learning temple, not a toy.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_footer():
    st.markdown(
        """
        <div class="vh-footer">
            This app is for respectful study, ancestor-honoring, and spiritual reflection only.<br/>
            It does not substitute for elders, clergy, mental health care, or medical help.
        </div>
        """,
        unsafe_allow_html=True,
    )


def sidebar_mojo():
    with st.sidebar:
        st.markdown('<div class="sidebar-logo">VOODOO • HOODOO • ROOTS</div>', unsafe_allow_html=True)

        # Mojo Music
        mojo_url = st.secrets.get("MOJO_MUSIC_URL", "")
        st.markdown("#### Louisiana “Mojo Music”")
        if mojo_url:
            st.markdown(
                '<div class="mojo-video-glow mojo-video-container">',
                unsafe_allow_html=True,
            )
            st.video(mojo_url)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.info("Set `MOJO_MUSIC_URL` in secrets for the sidebar music.")

        # Mojo Bag image
        mojo_img_url = st.secrets.get("MOJO_BAG_IMAGE_URL", "")
        st.markdown("#### Mojo Bag")
        if mojo_img_url:
            st.markdown('<div class="mojo-bag-glow mojo-bag-container">', unsafe_allow_html=True)
            st.image(mojo_img_url, caption="Mojo Bag", use_column_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.info("Set `MOJO_BAG_IMAGE_URL` in secrets for the Mojo Bag art.")

        # Simple theme toggle in sidebar (for convenience)
        st.markdown("---")
        theme_choice = st.radio(
            "Theme",
            ["Current (Red/Green Day)", "Dark Ritual Night"],
            index=0 if st.session_state.get("theme", "day") == "day" else 1,
        )
        st.session_state["theme"] = "day" if theme_choice.startswith("Current") else "night"


# =========================
# CORE PAGES (HISTORY / LORE)
# =========================

def page_home():
    render_header()

    st.markdown(
        """
        <div class="vh-card">
        <h3>Welcome</h3>
        <p>
        This working is not a game. It is a study temple built around 
        West African Vodun, Haitian Vodou, Louisiana Voodoo and Black American Hoodoo.
        </p>
        <p>
        Everything here stays on the side of <strong>respectful, non-harmful practice</strong>:
        ancestor veneration, offerings, supplications, journaling, and divination for clarity —
        never for violence, coercion, or self-harm.
        </p>
        <p>
        Move through the pages like a pilgrimage: from West Africa to Haiti, to New Orleans, to 
        the rootwork of the American South, and finally into your own altar, journal, and path.
        </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Small incense animation on home
    st.markdown("#### Incense for the Road")
    st.markdown(
        """
        <div class="incense-container">
            <div class="incense-burner">🪔</div>
            <div class="smoke"></div>
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
        Vodun (Vodún, Vodoun) is a family of spiritual traditions practiced among Fon, Ewe and
        related peoples in present-day Benin, Togo, Ghana and Nigeria. There is no single holy book.
        Knowledge is carried by elders, drums, masks, proverbs and living community.
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)
    with col1:
        media_video("VODUN_VIDEO_URL", "Vodun documentary / overview")
    with col2:
        media_video("VODUN_VIDEO_2_URL", "Ritual & festival footage")

    st.markdown(
        """
        <div class="vh-card">
        <h3>Core Themes</h3>
        <ul>
          <li>A high creator (Nana Buluku, Mawu-Lisa, etc.) beyond direct daily worship.</li>
          <li>Many spirits / forces served in shrines, families and lineages.</li>
          <li>Ancestors tightly intertwined with the living — no hard wall between worlds.</li>
          <li>Divination, spirit possession, drumming and song as everyday technologies.</li>
        </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

    render_footer()


def page_lwa():
    render_header()
    st.subheader("Lwa / Loas – Spirits of Haitian Vodou")

    st.markdown(
        """
        In Haitian Vodou, the spirits are called <strong>lwa</strong> (older English: “loas”).
        They are not vague archetypes but distinct presences with histories, veves, songs and
        ways of being served. Below you can meet some of them visually and through their
        attributes. This is orientation, not initiation.
        """,
        unsafe_allow_html=True,
    )

    # Portrait list
    for loa in LOA_GALLERY_DATA:
        st.markdown(f"### {loa['name']}")
        col_text, col_img = st.columns([2, 3])
        with col_text:
            st.markdown(
                f"<p style='font-size: 17px; line-height: 1.6;'>{loa['description']}</p>",
                unsafe_allow_html=True,
            )
            for line in loa["attributes"]:
                st.markdown(
                    f"<p style='font-size: 15px; line-height: 1.4;'>{line}</p>",
                    unsafe_allow_html=True,
                )
        with col_img:
            media_image(loa["image_key"], caption=loa["name"], width=520)

        st.markdown("<hr/>", unsafe_allow_html=True)

    render_footer()


def page_hoodoo():
    render_header()
    st.subheader("Hoodoo / Rootwork – Black American Conjure")

    st.markdown(
        """
        Hoodoo (conjure, rootwork) is a Black American folk-magic tradition grown primarily in the
        U.S. South out of West and Central African practices braided with Native and European
        influences. It is not a religion on its own, but a toolkit often practiced alongside
        Christianity.
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="vh-card">
        <h3>Rootwork Themes</h3>
        <ul>
          <li>Mojo hands / nation sacks (like the Mojo bag glowing in your sidebar).</li>
          <li>Condition oils, spiritual baths, powders and floor washes.</li>
          <li>Work for uncrossing, justice, court cases, money-drawing, protection and love —
              always with the understanding that <em>what you do returns to you</em>.</li>
          <li>Strong link to the Psalms and biblical language (“Hoodoo in the Psalms”).</li>
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

    st.markdown(
        """
        Most African-descended traditions begin with the dead — the ones whose blood and stories
        you carry. This page gives a gentle, safe way to set up a simple ancestor glass and candle.
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Offerings")
    for item in data["offerings"]:
        st.markdown(f"- {item}")

    st.markdown("### Guidelines")
    for g in data["guidelines"]:
        st.markdown(f"- {g}")

    st.markdown("### Sample Words (Adapt, don’t recite like a robot)")
    st.code(data["sample_words"].strip())

    render_footer()


def page_supplications():
    render_header()
    st.subheader("Supplications & Offerings")

    st.markdown(
        """
        Choose a spirit from the list to see suggested offerings, safety notes and a sample
        supplication. This is <strong>orientation only</strong>; real work should be done under
        the guidance of elders and lineage.
        """,
        unsafe_allow_html=True,
    )

    loa_names = list(SUPPLICATION_DATA.keys())
    choice = st.selectbox("Choose spirit / Ancestors", loa_names, index=0)

    data = SUPPLICATION_DATA[choice]

    st.markdown(f"### {choice}")
    st.markdown("#### Offerings")
    for item in data["offerings"]:
        st.markdown(f"- {item}")

    st.markdown("#### Guidelines")
    for g in data["guidelines"]:
        st.markdown(f"- {g}")

    st.markdown("#### Suggested Words")
    st.code(data["sample_words"].strip())

    render_footer()


def page_resources():
    render_header()
    st.subheader("Supplies & Resources")

    st.markdown(
        """
        These are <strong>real-world shops and resources</strong> where you can learn more or
        obtain candles, herbs, books, and condition products. Always vet for yourself, support
        Black-owned spaces where possible, and stay away from anyone promising guaranteed results
        or quick fixes.
        """,
        unsafe_allow_html=True,
    )

    for shop in HOODOO_SUPPLY_SHOPS:
        st.markdown("----")
        st.markdown(f"### [{shop['name']}]({shop['url']})")
        st.markdown(f"*{shop['tagline']}*  \nLocation: {shop['location']}")
        st.markdown(shop["description"])

    render_footer()


# =========================
# NEW: DIVINATION, OMENS, AI SUGGESTIONS
# =========================

DIVINATION_ITEMS = {
    "Cowrie shells": [
        "Open shell: a road opening, conversation flowing.",
        "Closed shell: something withheld, more listening needed.",
        "Cluster of shells: community and ancestors close by.",
    ],
    "Bones": [
        "Bone pointing toward you: take responsibility.",
        "Bone pointing away: release control where you have none.",
        "Bone crossing another: conflict that needs honest words.",
    ],
    "Stones": [
        "Smooth white stone: clarity, truth coming to light.",
        "Dark stone: rest, retreat, gather strength.",
        "Two stones touching: partnership, alliance, reconciliation.",
    ],
}


def pick_random_divination(tool: str) -> str:
    choices = DIVINATION_ITEMS.get(tool, [])
    return random.choice(choices) if choices else ""


def random_lwa_omen() -> dict:
    """Pick a random lwa each day (seeded by date so it is stable per day)."""
    today = datetime.date.today()
    random.seed(today.toordinal())
    loa = random.choice(LOA_GALLERY_DATA)
    return loa


def ai_style_suggestion(question: str) -> str:
    """Very simple rule-based 'AI' to suggest which lwa themes might fit."""
    q = question.lower()
    picks = []

    def add(name):
        if name not in picks:
            picks.append(name)

    if any(k in q for k in ["road", "path", "blocked", "stuck", "direction", "open"]):
        add("Papa Legba")
    if any(k in q for k in ["love", "romance", "heart", "relationship", "beauty"]):
        add("Erzulie Freda")
    if any(k in q for k in ["abuse", "violence", "protect", "safety", "kids", "children"]):
        add("Erzule Dantor")
    if any(k in q for k in ["grave", "dead", "death", "ancestors", "cemetery"]):
        add("Baron Samedi")
    if any(k in q for k in ["money", "work", "job", "harvest", "farm", "crop"]):
        add("Kouzen Azaka")
    if any(k in q for k in ["war", "fight", "battle", "court", "lawsuit", "conflict"]):
        add("Ogoun Badagri")
    if any(k in q for k in ["forest", "trees", "plants", "herb", "nature"]):
        add("Gran Bwa")
    if any(k in q for k in ["child", "innocent", "twins", "playful"]):
        add("Marasa Dosou")

    if not picks:
        add("Ancestors")

    return ", ".join(picks)


def page_divination_omens():
    render_header()
    st.subheader("Divination, Omens & Spirit Guidance")

    st.markdown(
        """
        This page offers a simple, safe way to pull symbolic messages — like sitting quietly
        with a small throwing set. It does not replace full divination by a priest or reader.
        """,
        unsafe_allow_html=True,
    )

    # --- Incense animation at top of page ---
    st.markdown("#### Incense Burner")
    st.markdown(
        """
        <div class="incense-container">
            <div class="incense-burner">🪔</div>
            <div class="smoke"></div>
        </div>
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
        st.markdown(f"**Today’s lwa to meditate on:** {loa['name']}")
        st.markdown(loa["description"])
        st.markdown("**Key themes:**")
        for line in loa["attributes"][:4]:
            st.markdown(f"- {line}")
    with col2:
        media_image(loa["image_key"], caption=loa["name"], width=420)

    st.markdown("---")
    st.markdown("### 3. Spirit Suggestion Helper (local AI-style logic)")

    q = st.text_area(
        "Describe what you’re seeking help with (non-harmful only):",
        placeholder="Example: I feel blocked in work and unsure which direction to move...",
    )
    if q.strip():
        names = ai_style_suggestion(q)
        st.info(
            f"Based on what you wrote, spirits whose themes might be relevant include: **{names}**.\n\n"
            "This is not divination and not a command — just a pointer to where you might study or pray."
        )

    render_footer()


# =========================
# SPELL JOURNAL & VOICE
# =========================

def page_spell_journal_voice():
    render_header()
    st.subheader("Spell Journal & Voice Invocation")

    # --- Spell journaling (session-based) ---
    st.markdown("### Spell & Prayer Journal")

    if "journal_entries" not in st.session_state:
        st.session_state["journal_entries"] = []

    entry = st.text_area(
        "Write what you did, saw, dreamed, or promised.",
        height=180,
        placeholder="Example: Tonight I lit a white candle for my ancestors and prayed for clarity...",
    )

    col_save, col_clear = st.columns(2)
    with col_save:
        if st.button("Save Entry"):
            if entry.strip():
                st.session_state["journal_entries"].append(
                    {
                        "timestamp": datetime.datetime.now().isoformat(timespec="seconds"),
                        "text": entry.strip(),
                    }
                )
                st.success("Entry saved in this session.")
    with col_clear:
        if st.button("Clear All Saved (this session only)"):
            st.session_state["journal_entries"] = []
            st.warning("Journal cleared for this session.")

    if st.session_state["journal_entries"]:
        st.markdown("#### Entries This Session")
        for e in reversed(st.session_state["journal_entries"]):
            st.markdown(f"**{e['timestamp']}**")
            st.markdown(e["text"])
            st.markdown("---")

        # Download as text
        text_blob = "\n\n".join(
            f"{e['timestamp']}\n{e['text']}" for e in st.session_state["journal_entries"]
        )
        st.download_button(
            "Download Journal (TXT)",
            data=text_blob.encode("utf-8"),
            file_name="voodoo_hoodoo_journal.txt",
            mime="text/plain",
        )

    st.markdown("---")
    st.markdown("### Voice Invocation Mode")

    st.markdown(
        """
        There is power in speaking prayers and psalms aloud. This section is kept simple so
        it works everywhere:
        """,
        unsafe_allow_html=True,
    )

    chant_url = st.secrets.get("VOICE_CHANT_URL", "")
    if chant_url:
        st.markdown("#### Example Chant / Song")
        st.audio(chant_url)
    else:
        st.info("Set `VOICE_CHANT_URL` in secrets to embed a chant or drumming track.")

    st.markdown(
        """
        1. Choose who you are addressing (Ancestors, a lwa, or God as you understand).  
        2. Light a candle safely.  
        3. Read your supplication, journal entry, or a psalm <em>slowly and clearly</em>.  
        4. Leave space for silence after you speak.
        """,
        unsafe_allow_html=True,
    )

    render_footer()


# =========================
# PDF LIBRARY – HOODOO IN THE PSALMS
# =========================

def page_pdf_library():
    render_header()
    st.subheader("Library – Hoodoo in the Psalms")

    st.markdown(
        """
        This is a study PDF, not a promise machine. It connects particular Psalms with
        traditional conditions (healing, protection, justice, etc.).
        """,
        unsafe_allow_html=True,
    )

    pdf_path = Path("Hoodoo_in_the_Psalms.pdf")
    if pdf_path.exists():
        with pdf_path.open("rb") as f:
            pdf_bytes = f.read()
        st.download_button(
            "📖 Download “Hoodoo in the Psalms” (PDF)",
            data=pdf_bytes,
            file_name="Hoodoo_in_the_Psalms.pdf",
            mime="application/pdf",
        )
        st.info("Place this PDF on your device, read slowly, and cross-reference with your elders/teachers.")
    else:
        st.error(
            "Could not find `Hoodoo_in_the_Psalms.pdf` in the app folder. "
            "Add it next to app.py when you deploy."
        )

    render_footer()


# =========================
# ACCOUNT BLESSINGS & INITIATION LOCK
# =========================

def page_account_and_initiation():
    render_header()
    st.subheader("Account Blessings & Initiation Gate")

    # --- Private blessing form ---
    st.markdown("### Private Blessing (local only – nothing leaves this browser)")
    name = st.text_input("Your name or ritual name")
    focus = st.text_input("Main focus right now (e.g., protection, clarity, courage)")
    fav_spirit = st.text_input("Spirit you feel closest to (Ancestors, Papa Legba, etc.)")

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

If it is right with {fav_spirit or 'the spirits'}, may doors that are good
for your spirit open, and doors that would destroy you quietly close.

Ayibobo.
"""
            )

    st.markdown("---")
    st.markdown("### Initiation-Locked Notes")

    st.info(
        "This section is intentionally light. It is not real initiation, just a way to hide "
        "a deeper study note behind a passphrase you choose."
    )

    code = st.text_input("Enter initiation code", type="password")
    real_code = st.secrets.get("INITIATION_CODE", "")

    if real_code and code == real_code:
        st.success("Gate opened (for this session).")
        st.markdown(
            """
            - Keep a separate physical notebook for dreams, omens and altar experiences.  
            - Check in with your mental health and body regularly; spirits do not replace doctors.  
            - Remember that saying “no” to work you do not understand is also part of the path.
            """,
            unsafe_allow_html=True,
        )
    elif code:
        st.error("Code not recognized. Keep the mysteries safe — try again or leave it closed.")

    render_footer()


# =========================
# SETTINGS – THEME & DRUMS
# =========================

def page_settings_themes():
    render_header()
    st.subheader("Settings – Themes, Drums & Atmosphere")

    st.markdown("### Theme")
    theme_choice = st.radio(
        "Choose app theme",
        ["Current (Red/Green Day)", "Dark Ritual Night"],
        index=0 if st.session_state.get("theme", "day") == "day" else 1,
    )
    st.session_state["theme"] = "day" if theme_choice.startswith("Current") else "night"
    st.info("Theme will re-apply on the next rerun (change page or press 'R' in dev).")

    st.markdown("---")
    st.markdown("### Drum Track (for safe use only)")

    drum_url = st.secrets.get("DRUMS_AUDIO_URL", "")
    if drum_url:
        st.audio(drum_url)
        st.caption("Use this softly; do not overwork yourself or others.")
    else:
        st.info("Set `DRUMS_AUDIO_URL` in secrets to embed a drum rhythm track.")

    render_footer()


# =========================
# MAIN NAVIGATION
# =========================

def main():
    sidebar_mojo()

    pages_main = {
        "Home": page_home,
        "West African Vodun": page_vodun,
        "Lwa / Loas": page_lwa,
        "Hoodoo / Rootwork": page_hoodoo,
        "Ancestor Veneration": page_ancestors,
        "Supplications & Offerings": page_supplications,
        "Supplies & Resources": page_resources,
        "Divination & Omens": page_divination_omens,
        "Spell Journal & Voice": page_spell_journal_voice,
        "PDF Library": page_pdf_library,
        "Account & Initiation": page_account_and_initiation,
        "Settings & Themes": page_settings_themes,
    }

    with st.sidebar:
        st.markdown("---")
        choice = st.radio("Navigate", list(pages_main.keys()), index=0)

    # Re-apply theme each run in case user changed it
    apply_theme()
    pages_main[choice]()


if __name__ == "__main__":
    main()
