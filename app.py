import streamlit as st

# =========================
# BASIC CONFIG
# =========================

st.set_page_config(
    page_title="Voodoo & Hoodoo Spells",
    page_icon="🕯️",
    layout="wide",
)

# =========================
# CSS THEME (Times New Roman, red/black/green, Zulu shield buttons)
# =========================

APP_CSS = """
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
st.markdown(APP_CSS, unsafe_allow_html=True)

# =========================
# LWA / LOA GALLERY DATA (19)
# =========================

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
        "name": "Baron Semedi",
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
# CURATED HOODOO & SPIRITUAL SUPPLY SHOPS
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
# SUPPLICATION / OFFERING DATA (SAFE, NON-HARMFUL)
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
            "Never promise what you cannot sincerely offer in return (like regular prayer or charity).",
        ],
        "sample_words": """
Papa Legba, Atibon Legba,
keeper of the crossroads and opener of the way,
I greet you with respect.

If it is pleasing to you, accept this coffee / rum and light,
and open good roads before me:
roads of right relationship,
roads of honest work,
roads where my head can be clear.

Do not open doors that would destroy me.
Open, instead, the ways that are good for my spirit
and close the ways that would drag me backward.

Mèsi anpil, Papa Legba.
Ayibobo.
""",
    },
    "Baron Samedi": {
        "type": "Lwa",
        "offerings": [
            "A candle in purple, black, or white",
            "A small glass of rum (often with hot pepper, depending on house)",
            "Cigars or tobacco (if you use them in ritual contexts)",
            "Black coffee or grilled corn/peanuts on a small plate",
        ],
        "guidelines": [
            "Baron is powerful: do not approach lightly or as a joke.",
            "Keep all work with the dead respectful; never try to disturb the dead for gossip or trivial reasons.",
            "Avoid asking for harm; stay with healing, courage, and truthful clarity.",
        ],
        "sample_words": """
Baron Samedi, guardian of the grave and lord of the boundary,
I come with respect and clean intention.

If you accept my light and this drink,
stand by the gates between life and death for me and mine.
Help me face the truth without fear,
help me honor those who have passed,
and teach me to remember that life is short and precious.

Where there is sickness of the spirit,
bring clarity and laughter that heals.
Where there is despair,
open a little road toward courage.

If it is not right to intervene, let me be at peace with that.
Ayibobo, Baron.
""",
    },
    "Maman Brigitte": {
        "type": "Lwa",
        "offerings": [
            "Rum with hot pepper (if appropriate to your house)",
            "Purple or black candles in safe holders",
            "Bread or dark bread, sometimes at a grave (if permitted, never trespassing)",
        ],
        "guidelines": [
            "Maman Brigitte loves justice and truth. Speak honestly.",
            "Keep graveyard work lawful and respectful; never steal from graves.",
            "Offer prayers for souls who are forgotten or unattended.",
        ],
        "sample_words": """
Maman Brigitte, strong lady of the graves and fire-tongued protector,
I call you with honor in my heart.

If it is your will, receive this rum and light.
Stand watch over the forgotten dead,
and over those in my bloodline who have no one else to pray for them.

Where injustice has laid its hand on me or mine,
help me find paths of righteous protection and repair,
without falling into cruelty or bitterness.

May your fire burn away lies and fear,
leaving courage and clear sight.
Ayibobo, Maman Brigitte.
""",
    },
    "Erzulie Freda": {
        "type": "Lwa",
        "offerings": [
            "A glass of champagne or sweet liqueur (if appropriate and respectful)",
            "Perfume or scented oil in a small dish",
            "Pink or white flowers",
            "Pastel candles in safe holders",
        ],
        "guidelines": [
            "Freda is about refined love, not manipulation.",
            "Avoid asking for control over another person’s will.",
            "Ask for healing of the heart, self-worth, and good partnership.",
        ],
        "sample_words": """
Erzulie Freda,
lady of sweet waters, perfume, and tender longing,
I greet you with respect.

If this offering pleases you,
pour beauty, self-respect, and healthy love into my life.
Heal what is bruised in my heart,
and teach me to love myself without vanity,
and others without chains.

Keep me away from relationships that are false, cruel, or degrading.
Bring me instead into connections that honor my soul.

If it is not the time for romance,
then let your blessing fall as peace and self-love.

Mèsi, Ezili Freda. Ayibobo.
""",
    },
    "Erzulie Dantò": {
        "type": "Lwa",
        "offerings": [
            "Black coffee, strong and sometimes unsweetened",
            "Blue or red candles, safely tended",
            "Pork dishes or dark chocolate (where culturally appropriate)",
        ],
        "guidelines": [
            "Dantò is fierce and protective. Come with honesty about pain.",
            "Focus on protection, boundaries, and courage — not revenge fantasies.",
            "Remember that justice can also mean walking away and healing.",
        ],
        "sample_words": """
Erzulie Dantò,
scarred mother, protector of women and children,
I come to you with the truth of my wounds.

If it is right for you to accept this coffee and light,
stand over me as a shield.
Cut the cords that bind me to abuse,
give me courage to say no,
and help me defend those who cannot defend themselves.

Guide my anger so it becomes a sword of justice
and not a fire that burns my own house down.

May your strength sit in my bones.
Ayibobo, Ezili Dantò.
""",
    },
    "Ogou": {
        "type": "Lwa",
        "offerings": [
            "Rum or strong liquor (if used in your house)",
            "Red candles in safe holders",
            "Iron tools placed respectfully near the altar (not random sharp clutter)",
        ],
        "guidelines": [
            "Ogou is about discipline and clear action, not chaos.",
            "Be prepared to work: Ogou can push for effort, not laziness.",
            "Ask for strategy, courage, and endurance.",
        ],
        "sample_words": """
Ogou,
warrior of iron and disciplined fire,
I salute you.

If it is pleasing to you, accept this drink, this flame, and these tools.
Sharpen my mind and my will.
Cut away laziness, confusion, and cowardice.

Teach me how to plan, how to work, and how to stand firm
without becoming cruel or reckless.

Where I must fight for my life, work, or dignity,
let me do it with clarity and honor.

Ayibobo, Ogou.
""",
    },
    "Gran Bwa": {
        "type": "Lwa",
        "offerings": [
            "Tobacco, honey, or good rum (if appropriate to your lineage)",
            "Fresh fruit",
            "Leaves or herbs gathered respectfully (never stripping plants bare)",
        ],
        "guidelines": [
            "Gran Bwa is forest depth: approach slowly and humbly.",
            "Spend time in nature, not only at the altar.",
            "Ask for help understanding which plants and paths are right for you.",
        ],
        "sample_words": """
Gran Bwa,
master of the deep woods and green mysteries,
I come to you in humility.

If this light and these offerings please you,
open my eyes to the wisdom of the living earth.
Help me respect the plants and places I enter,
and only take what I truly need.

Root me in strength and patience,
and help my spirit grow like a tree:
deep-rooted, flexible, and hard to uproot.

Ayibobo, Gran Bwa.
""",
    },
}

# =========================
# HELPERS
# =========================

def media_image(key: str, caption: str = "", width=None):
    url = st.secrets.get(key, "")
    if not url:
        st.info(f"[{key}] image not configured.")
        return

    if url.startswith("images/") or url.startswith("./images/"):
        try:
            st.image(url, caption=caption or None, use_column_width=(width is None), width=width)
        except Exception as e:
            st.error(f"[{key}] local image error: {e}")
        return

    if url.startswith("http://") or url.startswith("https://"):
        try:
            st.image(url, caption=caption or None, use_column_width=(width is None), width=width)
        except Exception as e:
            st.error(f"[{key}] remote image error: {e}")
        return

    st.warning(f"[{key}] value does not look like a path or URL: {url}")


def media_video(key: str):
    url = st.secrets.get(key, "")
    if not url:
        st.info(f"[{key}] video not configured.")
        return
    try:
        st.video(url)
    except Exception as e:
        st.error(f"[{key}] video error: {e}")


def render_header():
    st.markdown(
        """
        <div class="vh-header">
            <div class="vh-logo">🕯️</div>
            <div class="vh-title">VOODOO &amp; HOODOO SPELLS</div>
            <div class="vh-subtitle">
                Rooted in West African Vodun, Haitian Vodou, New Orleans Voodoo, Hoodoo &amp; Ancestor ways.
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
            This app is for educational and reflective purposes only. It does not teach harmful work and does not
            replace elders, clergy, doctors, or mental-health professionals. Use everything here for healing,
            protection, justice, and growth — never for harm.
        </div>
        """,
        unsafe_allow_html=True,
    )


def safe_rerun():
    if hasattr(st, "rerun"):
        st.rerun()
    elif hasattr(st, "experimental_rerun"):
        st.experimental_rerun()

# =========================
# PAGES
# =========================

def page_home():
    render_header()

    col1, col2 = st.columns([1.3, 1])
    with col1:
        st.markdown(
            """
            <div class="vh-card">
                <h3>Nana Buluku – Beginning at the Root</h3>
                <p>
                    Many West African Vodun lineages speak of a primordial presence known as
                    <strong>Nana Buluku</strong> (or Nana Buruku). In some houses this being is beyond gender;
                    in others, described as parent of other divine forces like Mawu and Lisa. By placing
                    Nana Buluku at the door of this app, we remember that the story begins in
                    <strong>Africa</strong>, not in Hollywood horror.
                </p>
                <p>
                    From this dark, deep origin flow many branches:
                </p>
                <ul>
                    <li><strong>West African Vodun</strong> among Fon, Ewe, and related peoples.</li>
                    <li><strong>Haitian Vodou</strong>, braided with Catholic and Indigenous traditions and forged in revolution.</li>
                    <li><strong>Louisiana Voodoo</strong> and the legacy of Marie Laveau in New Orleans.</li>
                    <li><strong>Hoodoo / Rootwork</strong>, the folk-magic of Black America focused on survival and justice.</li>
                </ul>
                <p>
                    <span class="vh-pill">intention</span>
                    This app does not give initiatory secrets. It offers orientation, respectful knowledge,
                    and images/videos so your understanding is rooted in real traditions, not stereotypes.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("#### Visual – Nana Buluku")
        media_image("NANA_BULUKU_IMAGE_URL", caption="Nana Buluku (Nana Buruku) – West African Vodun")
        st.markdown("#### Video – Cosmic origins")
        media_video("NANA_BULUKU_VIDEO_URL")

    with col2:
        st.markdown(
            """
            <div class="vh-card">
                <h3>Mawu-Lisa – Twin Balance</h3>
                <p>
                    In some Vodun cosmologies, <strong>Mawu-Lisa</strong> represents a twin principle:
                    moon and sun, cool and hot, night and day. Together they express a living balance that
                    is never static. By remembering them, we see that Vodun speaks a language of
                    <em>relationship and balance</em>, not simple “good vs evil”.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("#### Visual – Mawu-Lisa")
        media_image("MAWU_LISA_IMAGE_URL", caption="Mawu-Lisa – twin forces of balance")
        st.markdown("#### Video – Mawu-Lisa")
        media_video("MAWU_LISA_VIDEO_URL")

        st.markdown("---")
        st.markdown(
            """
            Use the shield buttons in the sidebar to walk through:
            - West African Vodun roots  
            - Haitian Vodou & the 1791 uprising  
            - Lwa (Loas) like Papa Legba, Damballa, Ezili, Ogou, Baron  
            - New Orleans & Marie Laveau  
            - Hoodoo / Rootwork  
            - Ancestor remembrance  
            - Supplications & Offerings  
            - Resources & Supplies  
            """
        )

    render_footer()


def page_vodun():
    render_header()
    st.subheader("West African Vodun – The Root in the Soil")

    st.markdown(
        """
        Vodun (or Vodún) is a family of living traditions from West Africa. There is no single holy book;
        the religion lives in shrines, elders, drums, diviners, and community memory. This page focuses on
        the African root that stands underneath many Diaspora paths.
        """
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Altars, Drums & Festivals")
        st.markdown("**Altar / Shrine**")
        media_image("VODUN_ALTAR_IMAGE_URL", "Vodun altar or ritual focus")
        st.markdown("**Drumming**")
        media_image("VODUN_DRUMMING_IMAGE_URL", "Drumming – heart of Vodun ritual")
        st.markdown("**Festival**")
        media_image("VODUN_FESTIVAL_IMAGE_URL", "Festival / public Vodun celebration")

    with col2:
        st.markdown("### Divination, Sacred Trees & Ancestral Art")
        st.markdown("**Divination**")
        media_image("VODUN_DIVINATION_IMAGE_URL", "Divinatory symbols and patterns")
        st.markdown("**Sacred tree / ancestral place**")
        media_image("VODUN_SACRED_TREE_IMAGE_URL", "Sacred tree / rooted place in Vodun")
        st.markdown("**Ancestral art / sculpture**")
        media_image("VODUN_ANCESTRAL_ART_IMAGE_URL", "Ancestral or ritual art in Vodun")

    st.markdown("### Video – Vodun in West Africa")
    media_video("VODUN_VIDEO_URL")

    render_footer()


def page_lwa():
    render_header()
    st.subheader("Lwa / Loas – Spirits of Haitian Vodou")

    st.markdown(
        """
        In Haitian Vodou, the spirits are called <strong>lwa</strong> (older English spelling: "loas").
        They are distinct beings with their own histories, symbols, rhythms, and ways of being served.
        This page offers visual and short-text orientation to some well-known lwa.
        """,
        unsafe_allow_html=True,
    )

    with st.expander("Papa Legba – Gatekeeper at the Crossroads", expanded=True):
        st.markdown(
            """
            Papa Legba stands at the spiritual crossroads and opens the way between humans and the other lwa.
            Without the gatekeeper, no other lwa can easily be approached. In some houses he appears as an
            old man with cane and pipe; in others, differently. The core idea is access, language, and doorways.
            """
        )
        media_image("PAPA_LEGBA_IMAGE_URL", "Papa Legba – gatekeeper imagery")
        media_image("PAPA_LEGBA_VEVE_URL", "Veve of Papa Legba (symbol at the crossroads)")
        st.markdown("**Video**")
        media_video("PAPA_LEGBA_VIDEO_URL")

    with st.expander("Damballa – Serpent Creator"):
        st.markdown(
            """
            Damballa is often envisioned as a great serpent of creation, associated with purity, blessing,
            rivers, and the quiet power of life itself. Devotees often approach him in a soft, cool, respectful way.
            """
        )
        media_image("DAMBALLA_IMAGE_URL", "Damballa – serpent creator imagery")
        media_image("DAMBALLA_VEVE_URL", "Veve of Damballa (serpent and sky)")
        st.markdown("**Video**")
        media_video("DAMBALLA_VIDEO_URL")

    with st.expander("Ezili Freda & Ezili Dantò – Hearts, Wounds & Protection"):
        st.markdown(
            """
            The Ezili family expresses different faces of love, desire, and protection.
            Ezili Freda leans toward romantic love, luxury, and refined longing; Ezili Dantò toward fierce
            maternal protection, rage against injustice, and the scars of struggle.
            """
        )
        media_image("EZILI_FREDA_IMAGE_URL", "Ezili Freda – refined love")
        media_image("EZILI_DANTO_IMAGE_URL", "Ezili Dantò – protective mother")
        media_image("EZILI_FREDA_VEVE_URL", "Veve of Ezili Freda")
        media_image("EZILI_DANTO_VEVE_URL", "Veve of Ezili Dantò")
        st.markdown("**Video**")
        media_video("EZILI_VIDEO_URL")

    with st.expander("Ogou – Iron, War & Discipline"):
        st.markdown(
            """
            Ogou (Ogoun) is a family of warrior lwa connected with iron, tools, soldiers, and hard struggle.
            Ogou energy can feel like sharp focus, courage, and disciplined fire — useful for strategy,
            work, and resistance.
            """
        )
        media_image("OGOU_IMAGE_URL", "Ogou – warrior and iron imagery")
        media_image("OGOU_VEVE_URL", "Veve of Ogou (iron, tools, war)")
        st.markdown("**Video**")
        media_video("OGOU_VIDEO_URL")

    with st.expander("Baron Samedi & the Gede – Cemeteries, Ancestors & Raw Truth"):
        st.markdown(
            """
            Baron Samedi is guardian of the cemetery gates; the Gede are a wild, loving family of spirits
            linked with the dead, sex, and raw truth. They use jokes, shock, and laughter to cut through denial
            and bring healing where secrets have festered.
            """
        )
        media_image("BARON_SAMEDI_IMAGE_URL", "Baron Samedi / Gede imagery")
        media_image("BARON_SAMEDI_VEVE_URL", "Veve of Baron Samedi / Gede")
        st.markdown("**Video**")
        media_video("BARON_SAMEDI_VIDEO_URL")

    st.markdown("---")
    st.markdown("### Lwa Visual – Additional Illustration")
    media_image("LOA_SYMBOL_MAP_URL", "Lwa symbols / map (if configured)")

    st.markdown("---")
    st.markdown("### Lwa / Loa Portraits with Descriptions")
    st.markdown(
        "Below are visual and symbolic representations of various lwa, "
        "with imagery, attributes, and a short explanation of who they are."
    )

    for loa in LOA_GALLERY_DATA:
        image_url = st.secrets.get(loa["image_key"], "")
        if not image_url:
            continue

        st.markdown(f"#### {loa['name']}")

        col_text, col_img = st.columns([2, 3])

        with col_text:
            st.markdown(
                f"<p style='font-size: 17px; line-height: 1.6; font-family: \"Times New Roman\";'>{loa['description']}</p>",
                unsafe_allow_html=True,
            )
            for line in loa.get("attributes", []):
                st.markdown(
                    f"<p style='font-size: 15px; line-height: 1.4; font-family: \"Times New Roman\";'>{line}</p>",
                    unsafe_allow_html=True,
                )

        with col_img:
            media_image(loa["image_key"], caption=loa["name"], width=600)

        st.markdown(
            "<hr style='border: 1px solid #555; margin-top: 1.2rem; margin-bottom: 1.2rem;'>",
            unsafe_allow_html=True,
        )

    render_footer()


def page_haiti_1791():
    render_header()
    st.subheader("Haiti, 1791 & the Revolution")

    st.markdown(
        """
        In 1791, an important Vodou ceremony remembered at Bois Caïman is said to have helped ignite
        the uprising that led to the Haitian Revolution. Over more than a decade, enslaved and free Black
        Haitians fought and defeated a major European empire, founding the first Black republic of the
        modern era. Vodou, drums, oaths, and lwa walked inside that struggle.
        """
    )

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Ceremony & symbolism")
        media_image(
            "HAITI_1791_VOODOO_CEREMONY_IMAGE_URL",
            "Artistic representation of 1791 Vodou ceremony",
        )
        media_image("BOIS_CAIMAN_ALTAR_IMAGE_URL", "Bois Caïman / ceremony altar imagery")

    with col2:
        st.markdown("### People, drums & possession")
        media_image("HAITI_DRUM_CIRCLE_IMAGE_URL", "Haitians dancing and drumming")
        media_image("HAITI_SPIRIT_POSSESSION_IMAGE_URL", "Spirit possession in Haitian Vodou")

    st.markdown("### Videos – Haiti history & ceremony")
    st.markdown("**History / revolution**")
    media_video("HAITI_HISTORY_VIDEO_URL")
    st.markdown("**Ceremony / Vodou practice**")
    media_video("HAITI_CEREMONY_VIDEO_URL")

    render_footer()


def page_new_orleans():
    render_header()
    st.subheader("New Orleans, Louisiana Voodoo & Marie Laveau")

    st.markdown(
        """
        New Orleans is a Creole city where African, French, Spanish, Native American, and Caribbean influences
        met. Out of that mix arose Louisiana Voodoo, a regional spiritual practice that used
        Catholic saints, herbs, roots, river water, and graveyard dirt.
        """
    )

    st.markdown(
        """
        At the center of many stories stands Marie Laveau, often called “The Voodoo Queen of
        New Orleans.” She worked as a hairdresser, herbalist, and spiritual worker, serving clients across the
        color line and navigating a harsh racial order with intelligence and power.
        """
    )

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Marie Laveau – person & legend")
        media_image("MARIE_LAVEAU_IMAGE_URL", "Marie Laveau – Voodoo Queen of New Orleans")
        media_image("MARIE_LAVEAU_TOMB_IMAGE_URL", "Tomb associated with Marie Laveau")
        st.markdown("**Video about Marie Laveau**")
        media_video("MARIE_LAVEAU_VIDEO_URL")

    with col2:
        st.markdown("### New Orleans spiritual landscape")
        media_image("NEW_ORLEANS_ALTAR_IMAGE_URL", "New Orleans Voodoo / Vodou altar")
        media_image("NEW_ORLEANS_STREET_PROCESSION_IMAGE_URL", "Procession in New Orleans streets")
        media_image("NEW_ORLEANS_CEMETERY_IMAGE_URL", "New Orleans cemetery")
        st.markdown("**New Orleans & Voodoo video**")
        media_video("NEW_ORLEANS_VOODOO_VIDEO_URL")

    render_footer()


def page_hoodoo():
    render_header()
    st.subheader("Hoodoo / Rootwork – Folk Magic of Black America")

    st.markdown(
        """
        Hoodoo (also called rootwork or conjure) is an African American folk-magic tradition rooted in the
        experience of Black people in the United States, especially in the South. It braids African spiritual
        logic, Indigenous plant knowledge, and European Bible magic into a toolkit for survival and justice.
        """
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Mojo bags, roots & herbs")
        media_image("HOODOO_MOJO_BAG_IMAGE_URL", "Mojo bag / conjure hand")
        media_image("HOODOO_ROOTS_AND_HERBS_IMAGE_URL", "Hoodoo roots and herbs")

    with col2:
        st.markdown("### Candles, graveyard work & Psalms")
        media_image("HOODOO_CANDLE_WORK_IMAGE_URL", "Candle / lamp work imagery")
        media_image("HOODOO_GRAVEYARD_WORK_IMAGE_URL", "Cemetery / graveyard work symbolism")
        media_image("HOODOO_PSAWMS_BIBLE_IMAGE_URL", "Bible & Psalms used in spiritual work")

    st.markdown("### Hoodoo teaching / documentary video")
    media_video("HOODOO_VIDEO_URL")

    render_footer()


def page_ancestors():
    render_header()
    st.subheader("Ancestor Veneration – Remembering Who Walked Before")

    st.markdown(
        """
        In many African and Diaspora traditions, the ancestors are central. They are the beloved dead of our
        bloodlines and our chosen families. Remembering them with water, candles, photos, and stories can become
        a steady spiritual practice of healing and guidance.
        """
    )

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Altars & elements")
        media_image("ANCESTOR_ALTAR_IMAGE_URL", "Ancestor altar")
        media_image("ANCESTOR_WATER_GLASS_IMAGE_URL", "Glass of water / libation offering")

    with col2:
        st.markdown("### Photos, candles & remembrance")
        media_image("ANCESTOR_PHOTO_COLLECTION_IMAGE_URL", "Photos of ancestors / elders")
        media_image("ANCESTOR_CANDLE_LIGHTING_IMAGE_URL", "Candle lighting for the dead")

    st.markdown("### Ancestor reflection / ritual video")
    media_video("ANCESTOR_VIDEO_URL")

    render_footer()


def page_supplications():
    """Supplications & Offerings (dropdown-based)."""
    render_header()
    st.subheader("Supplications & Offerings – Speaking with Respect")

    st.markdown(
        """
        This section gives **non-harmful**, respectful patterns for speaking with your Ancestors and
        selected lwa. It is **not** a replacement for initiation, house rules, or the guidance of elders.

        Use this page to:
        - Understand common *offerings* associated with each spirit.  
        - Get a feel for the *tone* of respectful supplication.  
        - Focus your work on **healing, protection, courage, clarity, and right order**, not on harm.
        """
    )

    spirit_names = list(SUPPLICATION_DATA.keys())
    choice = st.selectbox("Choose who you wish to address:", spirit_names, index=0)

    data = SUPPLICATION_DATA[choice]

    st.markdown("---")
    st.markdown(f"### {choice} – Suggested Offerings & Approach")

    col1, col2 = st.columns([1.2, 1])

    with col1:
        st.markdown("#### Offerings (general examples)")
        st.markdown(
            "<ul>" + "".join([f"<li>{o}</li>" for o in data["offerings"]]) + "</ul>",
            unsafe_allow_html=True,
        )

        st.markdown("#### Guidelines")
        st.markdown(
            "<ul>" + "".join([f"<li>{g}</li>" for g in data["guidelines"]]) + "</ul>",
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <p style="font-size: 0.9rem; opacity: 0.9;">
            <strong>Always obey</strong> the rules of your own house/temple, and the counsel of elders.
            These examples are for orientation and reflection, not a fixed ritual script.
            </p>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown("#### Sample Supplication (you can adapt this)")
        st.text_area(
            "Example words you might say quietly at your altar:",
            value=data["sample_words"].strip(),
            height=260,
        )

    st.markdown("---")
    st.markdown(
        """
        **Practical tip:**  
        Before you ask for anything, take a moment to:
        - Breathe slowly and ground yourself.  
        - Name what you’re grateful for.  
        - Be clear about what you’re asking and why.  
        - Be willing to listen in dreams, intuition, and the behavior of life over time.
        """
    )

    render_footer()


def page_resources():
    """Resources & Supplies – now including curated shop list."""
    render_header()
    st.subheader("Resources & Supplies – Study, Shops & Ethical Notes")

    st.markdown(
        """
        This section is here to help you think about:
        - **How to study** these traditions with respect.  
        - **Where to look** for supplies and tools in a grounded way.  
        - **How to move** with ethics so your practice stays aligned with healing and justice.
        """
    )

    # 1. Study
    st.markdown("### 1. Study & Books (Orientation)")
    st.markdown(
        """
        Look for books and materials that are:
        - Written by practitioners from within the culture.  
        - Recommended by temples, houses, or long-standing communities.  
        - Clear about the difference between **Vodun / Vodou / Voodoo / Hoodoo**.  

        When possible, look for:
        - Histories of <strong>Haitian Vodou</strong> that discuss the 1791 uprising.  
        - Works on <strong>Louisiana Voodoo</strong> and <strong>Marie Laveau</strong> that cite real archives.  
        - Studies of <strong>Hoodoo / Rootwork</strong> that center Black experience and survival.  
        """,
        unsafe_allow_html=True,
    )

    # 2. Curated shops
    st.markdown("---")
    st.markdown("### 2. Curated Hoodoo & Spiritual Supply Shops")
    st.markdown(
        """
        Below are some shops and platforms connected to Hoodoo, rootwork, and Black-owned spiritual
        businesses. Always read each shop’s own descriptions, policies, and lineage notes so you can decide
        what feels aligned with your practice.
        """
    )

    for shop in HOODOO_SUPPLY_SHOPS:
        st.markdown(
            f"""
            <div class="vh-card">
                <h3>{shop['name']}</h3>
                <p style="font-size: 0.95rem; font-style: italic; opacity:0.95;">
                    {shop['tagline']}
                </p>
                <p>{shop['description']}</p>
                <p style="font-size: 0.9rem; opacity:0.9;">
                    <strong>Location / Reach:</strong> {shop['location']}
                </p>
                <p>
                    <a href="{shop['url']}" target="_blank" style="color:#80cbc4; text-decoration:none;">
                        🔗 Visit {shop['name']} website
                    </a>
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # 3. Botanicas & local
    st.markdown("### 3. Botanicas & Local Supply Shops")
    st.markdown(
        """
        For candles, herbs, oils, and other physical items, beyond the list above:

        - Search locally for **“botanica”**, **“spiritual supply shop”**, or **“occult shop”** that:
            - Is frequented by Caribbean / Latinx / African-diasporic communities, or  
            - Has staff who actually know the traditions they stock.  
        - When buying online:
            - Prefer shops that are transparent about who runs them.  
            - Read policies and reviews carefully.  
            - Support Black and Afro-Caribbean owned businesses where you can.  

        Common items you might look for (always within your own house rules):
        - Glass-encased candles (white, purple, red, blue, etc.).  
        - Basic herbs: basil, bay leaf, rosemary, hyssop, etc.  
        - Florida Water or similar colognes used in cleansing and blessing.  
        - Small statues, pictures of saints (if you work in a Catholic-syncretic current).  
        """
    )

    # 4. Elders & houses
    st.markdown("### 4. Working with Elders, Priests & Houses")
    st.markdown(
        """
        Because these are **living religions and systems**, not just “spells,” the strongest path is
        relationship with real communities:

        - Haitian Vodou temples (lakou, sosyete)  
        - West African Vodun shrines and families  
        - New Orleans houses or churches that continue work in this line  
        - Experienced rootworkers and conjure folk with community reputation  

        Signs of trustworthy people:
        - They are honest about what they know and do not know.  
        - They are not trying to sell you instant power or initiation in a weekend.  
        - They encourage you to grow in maturity and responsibility, not fear.  
        """
    )

    # 5. Ethics
    st.markdown("### 5. Ethical Compass for Your Practice")
    st.markdown(
        """
        As you use this app and any other resource, ask:

        - Does this work aim at **healing, protection, justice, clarity, and right order**?  
        - Am I respecting the dead, the living, and the spirits I’m calling on?  
        - Am I crossing someone else’s will in ways that mirror abuse or control?  

        If the answer feels off, **pause**.  
        Talk to elders, pray, and re-align your intentions before moving forward.
        """
    )

    render_footer()


def page_gallery():
    render_header()
    st.subheader("Media Gallery – All Linked Images & Videos")

    st.markdown(
        """
        This page lists all image and video keys that the app knows about.
        Use it as a debugging tool to confirm which secrets are set correctly.
        """
    )

    image_keys = [
        ("NANA_BULUKU_IMAGE_URL", "Nana Buluku"),
        ("MAWU_LISA_IMAGE_URL", "Mawu-Lisa"),
        ("VODUN_ALTAR_IMAGE_URL", "Vodun Altar"),
        ("VODUN_DRUMMING_IMAGE_URL", "Vodun Drumming"),
        ("VODUN_FESTIVAL_IMAGE_URL", "Vodun Festival"),
        ("VODUN_DIVINATION_IMAGE_URL", "Vodun Divination"),
        ("VODUN_SACRED_TREE_IMAGE_URL", "Vodun Sacred Tree"),
        ("VODUN_ANCESTRAL_ART_IMAGE_URL", "Vodun Ancestral Art"),
        ("PAPA_LEGBA_IMAGE_URL", "Papa Legba"),
        ("DAMBALLA_IMAGE_URL", "Damballa"),
        ("EZILI_FREDA_IMAGE_URL", "Ezili Freda"),
        ("EZILI_DANTO_IMAGE_URL", "Ezili Dantò"),
        ("OGOU_IMAGE_URL", "Ogou"),
        ("BARON_SAMEDI_IMAGE_URL", "Baron Samedi"),
        ("HAITI_1791_VOODOO_CEREMONY_IMAGE_URL", "Haiti 1791 Ceremony"),
        ("BOIS_CAIMAN_ALTAR_IMAGE_URL", "Bois Caïman Altar"),
        ("HAITI_DRUM_CIRCLE_IMAGE_URL", "Haiti Drum Circle"),
        ("HAITI_SPIRIT_POSSESSION_IMAGE_URL", "Haiti Spirit Possession"),
        ("MARIE_LAVEAU_IMAGE_URL", "Marie Laveau"),
        ("MARIE_LAVEAU_TOMB_IMAGE_URL", "Marie Laveau Tomb"),
        ("NEW_ORLEANS_ALTAR_IMAGE_URL", "New Orleans Altar"),
        ("NEW_ORLEANS_STREET_PROCESSION_IMAGE_URL", "New Orleans Procession"),
        ("NEW_ORLEANS_CEMETERY_IMAGE_URL", "New Orleans Cemetery"),
        ("HOODOO_MOJO_BAG_IMAGE_URL", "Hoodoo Mojo Bag"),
        ("HOODOO_ROOTS_AND_HERBS_IMAGE_URL", "Hoodoo Roots & Herbs"),
        ("HOODOO_CANDLE_WORK_IMAGE_URL", "Hoodoo Candle Work"),
        ("HOODOO_GRAVEYARD_WORK_IMAGE_URL", "Hoodoo Graveyard Work"),
        ("HOODOO_PSAWMS_BIBLE_IMAGE_URL", "Hoodoo Psalms / Bible"),
        ("ANCESTOR_ALTAR_IMAGE_URL", "Ancestor Altar"),
        ("ANCESTOR_WATER_GLASS_IMAGE_URL", "Ancestor Water Glass"),
        ("ANCESTOR_PHOTO_COLLECTION_IMAGE_URL", "Ancestor Photos"),
        ("ANCESTOR_CANDLE_LIGHTING_IMAGE_URL", "Ancestor Candle Lighting"),
        ("LOA_SYMBOL_MAP_URL", "Lwa Symbol Map / Illustration"),
    ]

    video_keys = [
        ("NANA_BULUKU_VIDEO_URL", "Nana Buluku Video"),
        ("MAWU_LISA_VIDEO_URL", "Mawu-Lisa Video"),
        ("VODUN_VIDEO_URL", "Vodun Video"),
        ("PAPA_LEGBA_VIDEO_URL", "Papa Legba Video"),
        ("DAMBALLA_VIDEO_URL", "Damballa Video"),
        ("EZILI_VIDEO_URL", "Ezili Video"),
        ("OGOU_VIDEO_URL", "Ogou Video"),
        ("BARON_SAMEDI_VIDEO_URL", "Baron Samedi / Gede Video"),
        ("HAITI_HISTORY_VIDEO_URL", "Haiti History Video"),
        ("HAITI_CEREMONY_VIDEO_URL", "Haiti Ceremony Video"),
        ("NEW_ORLEANS_VOODOO_VIDEO_URL", "New Orleans Voodoo Video"),
        ("MARIE_LAVEAU_VIDEO_URL", "Marie Laveau Video"),
        ("HOODOO_VIDEO_URL", "Hoodoo Video"),
        ("ANCESTOR_VIDEO_URL", "Ancestor Video"),
    ]

    st.markdown("### Images")
    for key, label in image_keys:
        url = st.secrets.get(key, "")
        if url:
            st.markdown(f"**{label}** (`{key}`)")
            media_image(key)
        else:
            st.markdown(f"- `{key}` not set")

    st.markdown("---")
    st.markdown("### Videos")
    for key, label in video_keys:
        url = st.secrets.get(key, "")
        if url:
            st.markdown(f"**{label}** (`{key}`)")
            media_video(key)
        else:
            st.markdown(f"- `{key}` not set")

    render_footer()


def page_admin():
    render_header()
    st.subheader("🛡️ Admin – Control & Diagnostics")

    if "is_admin" not in st.session_state:
        st.session_state["is_admin"] = False

    if not st.session_state["is_admin"]:
        st.markdown("### Admin login")
        with st.form("admin_login_form"):
            username = st.text_input("Admin username")
            password = st.text_input("Admin password", type="password")
            login = st.form_submit_button("🛡️⚔️ Log In")

        if login:
            admin_user = st.secrets.get("ADMIN_USER", "")
            admin_pass = st.secrets.get("ADMIN_PASS", "")
            if username == admin_user and password == admin_pass and admin_user and admin_pass:
                st.session_state["is_admin"] = True
                st.success("Admin access granted.")
                safe_rerun()
            else:
                st.error("Invalid admin credentials or admin secrets not configured.")
        render_footer()
        return

    st.success("You are logged in as admin.")
    if st.button("🚪 Log Out"):
        st.session_state["is_admin"] = False
        safe_rerun()

    st.markdown("---")
    st.markdown("### Secrets keys overview")
    keys = list(st.secrets.keys())
    st.write("Loaded secret keys:")
    st.code("\n".join(sorted(keys)), language="text")

    st.markdown(
        """
        #### Media links check

        If some images do not show up (especially old MediaFire links), make sure:
        - The value is either:
            - a local path like `images/baron_samedi.webp`, or
            - a direct URL ending in `.jpg`, `.png`, `.gif`, `.mp4`, etc.
        """
    )

    render_footer()


def page_disclaimer():
    render_header()
    st.subheader("Disclaimers, Ethics & Safety")

    st.markdown(
        """
        - This app is for **education and personal reflection**.  
        - It does **not** teach harmful, coercive, or cursing work.  
        - It does **not** claim to replace:
            - Vodun/Vodou/Voodoo clergy or elders,  
            - rootworkers or spiritual workers,  
            - doctors, therapists, or mental-health providers,  
            - lawyers or financial professionals.
        """
    )

    st.markdown(
        """
        Approach all traditions mentioned here with **respect, humility, and patience**. Real learning requires
        time, relationship, and listening. If you feel called to deeper involvement, seek out legitimate elders,
        temples, churches, or rootworkers and support the communities that carry these paths.
        """
    )

    render_footer()

# =========================
# MAIN ROUTER
# =========================

def main():
    if "page" not in st.session_state:
        st.session_state["page"] = "Home"

    with st.sidebar:
        st.markdown(
            '<div class="sidebar-logo">VOODOO &amp; HOODOO SPELLS</div>',
            unsafe_allow_html=True,
        )
        pages = [
            "Home",
            "West African Vodun",
            "Lwa / Loas",
            "Haiti 1791 & Revolution",
            "New Orleans & Marie Laveau",
            "Hoodoo / Rootwork",
            "Ancestor Veneration",
            "Supplications & Offerings",
            "Resources & Supplies",
            "Media Gallery",
            "Disclaimers",
            "Admin",
        ]
        # Safe index
        current = st.session_state["page"]
        if current not in pages:
            current = "Home"
            st.session_state["page"] = "Home"

        choice = st.radio("Navigate", pages, index=pages.index(current))
        st.session_state["page"] = choice

        # --- Louisiana Mojo Music block ---
        st.markdown("---")
        st.markdown("### Louisiana \"Mojo Music\"")

        st.markdown(
            """
            <div class="mojo-video-glow mojo-video-container">
                <iframe
                    src="https://www.youtube.com/embed/UuA4eRCvTbo?rel=0&modestbranding=1&loop=1&playlist=UuA4eRCvTbo"
                    title="Louisiana Mojo Music"
                    frameborder="0"
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                    allowfullscreen
                ></iframe>
            </div>
            """,
            unsafe_allow_html=True,
        )

        mojo_bag_url = st.secrets.get("MOJO_BAG_IMAGE_URL", "")
        if mojo_bag_url:
            st.markdown(
                f"""
                <div class="mojo-bag-glow mojo-bag-container" style="margin-top: 0.85rem; text-align:center;">
                    <img src="{mojo_bag_url}" alt="Mojo Bag"
                         style="width:70%; max-width:140px;" />
                    <div style="margin-top:0.35rem; font-size:0.9rem; opacity:0.9; font-family:'Times New Roman';">
                        Mojo Bag
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    if choice == "Home":
        page_home()
    elif choice == "West African Vodun":
        page_vodun()
    elif choice == "Lwa / Loas":
        page_lwa()
    elif choice == "Haiti 1791 & Revolution":
        page_haiti_1791()
    elif choice == "New Orleans & Marie Laveau":
        page_new_orleans()
    elif choice == "Hoodoo / Rootwork":
        page_hoodoo()
    elif choice == "Ancestor Veneration":
        page_ancestors()
    elif choice == "Supplications & Offerings":
        page_supplications()
    elif choice == "Resources & Supplies":
        page_resources()
    elif choice == "Media Gallery":
        page_gallery()
    elif choice == "Disclaimers":
        page_disclaimer()
    elif choice == "Admin":
        page_admin()
    else:
        page_home()


if __name__ == "__main__":
    main()
