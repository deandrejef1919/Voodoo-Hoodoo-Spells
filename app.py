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
# HELPERS
# =========================

def media_image(key: str, caption: str = "", width=None):
    """
    Load image from st.secrets[key].
    - If value starts with 'images/', treat as local file path.
    - If value starts with 'http', treat as remote URL.
    """
    url = st.secrets.get(key, "")
    if not url:
        st.info(f"[{key}] image not configured.")
        return

    # Local file path
    if url.startswith("images/") or url.startswith("./images/"):
        try:
            st.image(url, caption=caption or None, use_column_width=(width is None), width=width)
        except Exception as e:
            st.error(f"[{key}] local image error: {e}")
        return

    # Remote URL
    if url.startswith("http://") or url.startswith("https://"):
        try:
            st.image(url, caption=caption or None, use_column_width=(width is None), width=width)
        except Exception as e:
            st.error(f"[{key}] remote image error: {e}")
        return

    # Fallback
    st.warning(f"[{key}] value does not look like a path or URL: {url}")


def media_video(key: str):
    """
    Load video from st.secrets[key].
    Works for YouTube URLs, mp4 URLs, etc.
    """
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
# =========================
# LWA / LOA GALLERY DATA
# =========================

LOA_GALLERY_DATA = [
    {
        "name": "Papa Legba",
        "image_key": "LWA_PAPA_LEGBA_URL",
        "description": (
            "Papa Legba is the gatekeeper of the Vodou spiritual realm, standing at the crossroads. "
            "He is the wise elder who facilitates communication between the human and spirit worlds."
        ),
    },
    {
        "name": "Baron Samedi",
        "image_key": "LWA_BARON_SAMEDI_URL",
        "description": (
            "Baron Samedi is the Vodou spirit associated with death and the future. "
            "His unique appearance and playful yet unsettling demeanor mark him as guardian of the deceased "
            "and master of the transformations between life and death."
        ),
    },
    {
        "name": "Ogoun Badagri",
        "image_key": "LWA_OGOUN_BADAGRI_URL",
        "description": (
            "Ogoun Badagri is a powerful warrior spirit of strength and valor. "
            "With a fierce presence, he wields weapons that symbolize leadership, warfare, and metalcraft."
        ),
    },
    {
        "name": "Erzule Dantor",
        "image_key": "LWA_ERZULE_DANTOR_URL",
        "description": (
            "Erzule Dantor is a fierce protector of women and children in Vodou. "
            "She embodies strength, resilience, and the fire that guards family and independence."
        ),
    },
    {
        "name": "Dambala Wedo",
        "image_key": "LWA_DAMBALA_WEDO_URL",
        "description": (
            "Dambala Wedo, often shown as twin serpents and a rainbow, embodies the sacred link between "
            "heaven and earth. This lwa carries the essence of balance, harmony, and sacred life-force."
        ),
    },
    {
        "name": "Bossou",
        "image_key": "LWA_BOSSOU_URL",
        "description": (
            "Bossou is a spirit of strength, stability, and endurance, often linked to a bull. "
            "He symbolizes resilience and grounded energy."
        ),
    },
    {
        "name": "Ti Jan Dantò",
        "image_key": "LWA_TI_JAN_DANTO_URL",
        "description": (
            "Ti Jan Dantò represents youth, passion, vitality, and determination. "
            "He expresses the bold courage needed to pursue one’s goals and desires."
        ),
    },
    {
        "name": "Maman Brigitte",
        "image_key": "LWA_MAMAN_BRIGITTE_URL",
        "description": (
            "Maman Brigitte is linked to graveyards, life, and death. "
            "With striking presence, she is a powerful yet compassionate guardian of the deceased."
        ),
    },
    {
        "name": "Kouzen Azaka",
        "image_key": "LWA_KOUZEN_AZAKA_URL",
        "description": (
            "Kouzen Azaka represents agriculture, rural life, and dedication. "
            "He honors hard work, productivity, and prosperity earned through steady effort."
        ),
    },
    {
        "name": "Marasa Dosou",
        "image_key": "LWA_MARASA_DOSOU_URL",
        "description": (
            "Marasa Dosou belongs to the divine twins in Vodou, symbolizing balance and harmony between opposites. "
            "They stand between spiritual and physical worlds, holding both at once."
        ),
    },
    {
        "name": "Kalfu",
        "image_key": "LWA_KALFU_URL",
        "description": (
            "Kalfu is a spirit of the night, crossroads, and transformation. "
            "His commanding presence at dark crossroads reflects his role in navigating chaos and transitions."
        ),
    },
    {
        "name": "Damballa",
        "image_key": "LWA_DAMBALLA_URL",
        "description": (
            "Damballa is a serpent spirit of wisdom, purity, and creation. "
            "A serene, majestic lwa whose presence carries the breath of life and deep mystery."
        ),
    },
    {
        "name": "Simbi",
        "image_key": "LWA_SIMBI_URL",
        "description": (
            "Simbi is a spirit of water, magic, and communication, often linked with rivers and streams. "
            "He embodies spiritual insight, adaptability, and fluid paths of knowledge."
        ),
    },
    {
        "name": "Klemezine",
        "image_key": "LWA_KLEMEZINE_URL",
        "description": (
            "Klemezine is a protective spirit, radiating a tranquil yet formidable aura. "
            "He embodies the essence of spiritual safeguarding and boundary-keeping."
        ),
    },
    {
        "name": "Ayizan Velekete",
        "image_key": "LWA_AYIZAN_VELEKETE_URL",
        "description": (
            "Ayizan Velekete is linked to initiation and markets, representing prosperity, spiritual authority, "
            "and personal growth. Her nurturing energy guides those seeking higher paths."
        ),
    },
    {
        "name": "Gran Bwa",
        "image_key": "LWA_GRAN_BWA_URL",
        "description": (
            "Gran Bwa is the spirit of the forest, nature, and deep wisdom. "
            "As guardian of the wilderness, he protects its beauty and guides those who seek to understand it."
        ),
    },
    {
        "name": "Hogou Ferraille",
        "image_key": "LWA_HOGOU_FERRAILLE_URL",
        "description": (
            "Hogou Ferraille is a warrior expression of Ogoun, linked to protection, leadership, and strength in battle. "
            "Armored and resolute, he stands as a fierce protector."
        ),
    },
    {
        "name": "Erzulie Freda",
        "image_key": "LWA_ERZULIE_FREDA_URL",
        "description": (
            "Erzulie Freda embodies love, beauty, and luxury. "
            "She moves in matters of the heart, femininity, and refined desire."
        ),
    },
    {
        "name": "Brav Gede",
        "image_key": "LWA_BRAV_GEDE_URL",
        "description": (
            "Brav Gede is a Gede spirit of life and death, fertility, and humor. "
            "Playful and sharp, he holds the duality of joy and mortality together."
        ),
    },
]

def page_lwa():
    render_header()
    st.subheader("Lwa / Loas – Spirits of Haitian Vodou")

    st.markdown(
        """
        In Haitian Vodou, the spirits are called <strong>lwa</strong> (older English spelling: “loas”).
        They are distinct beings with their own histories, symbols, rhythms, and ways of being served.
        This page offers visual and short-text orientation to some well-known lwa.
        """
    )

    # Papa Legba
    with st.expander("Papa Legba – Gatekeeper at the Crossroads", expanded=True):
        st.markdown(
            """
            Papa Legba stands at the spiritual crossroads and opens the way between humans and the other lwa.
            Without the gatekeeper, no other lwa can easily be approached. In some houses he appears as an
            old man with cane and pipe; in others, differently. The core idea is access, language, and doorways.
            """
        )
        media_image("PAPA_LEGBA_IMAGE_URL", "Papa Legba – gatekeeper imagery")
        # Optional: veve / symbol for Papa Legba
        media_image("PAPA_LEGBA_VEVE_URL", "Veve of Papa Legba (symbol at the crossroads)")
        st.markdown("**Video**")
        media_video("PAPA_LEGBA_VIDEO_URL")

    # Damballa
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

    # Ezili
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

    # Ogou
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

    # Baron Samedi / Gede
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

    # --- OPTIONAL: existing image you already have at the end ---
    st.markdown("---")
    st.markdown("### Lwa Visual – Additional Illustration")
    # If you already have a single image here, keep this line:
    media_image("LOA_SYMBOL_MAP_URL", "Lwa symbols / map (if configured)")

    # --- NEW: full Lwa / Loa gallery using your 16 images ---
    st.markdown("### Lwa / Loa Veve & Icon Gallery")

    gallery_keys = [
        ("LWA_GALLERY_1_URL",  "Lwa image 1"),
        ("LWA_GALLERY_2_URL",  "Lwa image 2"),
        ("LWA_GALLERY_3_URL",  "Lwa image 3"),
        ("LWA_GALLERY_4_URL",  "Lwa image 4"),
        ("LWA_GALLERY_5_URL",  "Lwa image 5"),
        ("LWA_GALLERY_6_URL",  "Lwa image 6"),
        ("LWA_GALLERY_7_URL",  "Lwa image 7"),
        ("LWA_GALLERY_8_URL",  "Lwa image 8"),
        ("LWA_GALLERY_9_URL",  "Lwa image 9"),
        ("LWA_GALLERY_10_URL", "Lwa image 10"),
        ("LWA_GALLERY_11_URL", "Lwa image 11"),
        ("LWA_GALLERY_12_URL", "Lwa image 12"),
        ("LWA_GALLERY_13_URL", "Lwa image 13"),
        ("LWA_GALLERY_14_URL", "Lwa image 14"),
        ("LWA_GALLERY_15_URL", "Lwa image 15"),
        ("LWA_GALLERY_16_URL", "Lwa image 16"),
        ("LWA_GALLERY_17_URL", "Lwa image 17"),
        ("LWA_GALLERY_18_URL", "Lwa image 18"),
        ("LWA_GALLERY_19_URL", "Lwa image 19"),
    ]

    cols = st.columns(4)  # 4 images per row

    for idx, (key, label) in enumerate(gallery_keys):
        col = cols[idx % 4]
        with col:
            if st.secrets.get(key, ""):
                media_image(key, caption=label)
            # If key not set, we quietly skip it

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
        st.markdown("**Video about Marie Laveau")
        media_video("MARIE_LAVEAU_VIDEO_URL")

    with col2:
        st.markdown("### New Orleans spiritual landscape")
        media_image("NEW_ORLEANS_ALTAR_IMAGE_URL", "New Orleans Voodoo / Vodou altar")
        media_image("NEW_ORLEANS_STREET_PROCESSION_IMAGE_URL", "Procession in New Orleans streets")
        media_image("NEW_ORLEANS_CEMETERY_IMAGE_URL", "New Orleans cemetery")
        st.markdown("**New Orleans & Voodoo video")
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


def page_gallery():
    render_header()
    st.subheader("Media Gallery – All Linked Images & Videos")

    st.markdown(
        """
        
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

    # Logged in
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
            "Media Gallery",
            "Disclaimers",
            "Admin",
        ]
        choice = st.radio("Navigate", pages, index=pages.index(st.session_state["page"]))
        st.session_state["page"] = choice

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


