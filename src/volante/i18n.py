"""Bilingual UI strings for the Volante landing page (ES default, EN toggle).

Server-rendered per request via ``?lang=`` so search engines see real content in
each language (matters for the neighborhood-SEO play).
"""

from __future__ import annotations

LANGS = ("es", "en")
DEFAULT_LANG = "es"

ZONES = ["Brickell", "Downtown", "Wynwood", "South Beach", "Coral Gables", "Coconut Grove"]

STRINGS: dict[str, dict[str, str]] = {
    "es": {
        "meta_title": "Volante — Te llevamos a ti y a tu carro a casa | Miami",
        "meta_desc": (
            "Conductor de confianza que maneja tu propio carro hasta tu casa en Miami. "
            "Sin membresía, sin mínimo, precio fijo. Bilingüe."
        ),
        "nav_how": "Cómo funciona",
        "nav_why": "Por qué Volante",
        "nav_join": "Únete a la lista",
        "switch_to": "EN",
        "hero_pre": "Te llevamos a ti",
        "hero_accent": "y a tu carro",
        "hero_post": "a casa.",
        "hero_sub": (
            "Un conductor bilingüe de confianza maneja tu propio carro hasta tu casa. "
            "Sin membresía. Sin mínimo. Precio fijo."
        ),
        "badge": "Hecho en Miami · Bilingüe",
        "form_label": "¿Dónde sales esta noche?",
        "form_contact_ph": "Tu WhatsApp o email",
        "form_zone_default": "Elige tu zona",
        "form_zone_other": "Otra",
        "form_cta": "Únete a la lista",
        "form_micro": "Te avisamos cuando lancemos en tu zona. Cero spam.",
        "success": "¡Listo! Te avisamos en cuanto lancemos en tu zona. 🚗",
        "error": "Escribe tu WhatsApp o email para unirte.",
        "pains_kicker": "El problema",
        "pains_title": "Las otras opciones te cuestan más",
        "pain1_t": "Un DUI",
        "pain1_d": "~$10,000 todo incluido en Florida, sin contar el susto.",
        "pain2_t": "La grúa",
        "pain2_d": "$516 + $30 si dejas tu carro en South Beach — más el Uber al día siguiente.",
        "pain3_t": "El surge",
        "pain3_d": "$40–$100+ una noche de fiesta… y tu carro sigue varado.",
        "how_kicker": "Así de fácil",
        "how_title": "Cómo funciona",
        "step1_t": "Pides",
        "step1_d": "Nos dices dónde estás y a dónde vas.",
        "step2_t": "Llega tu conductor",
        "step2_d": "Bilingüe y verificado, con su nombre y foto antes de llegar.",
        "step3_t": "Maneja tu carro",
        "step3_d": "Te lleva a ti y a tu carro a casa, sano y salvo.",
        "step4_t": "Llegas seguro",
        "step4_d": "Tu carro en tu casa. Sin grúa, sin viaje extra mañana.",
        "why_kicker": "La diferencia",
        "why_title": "Por qué Volante",
        "why1": "Sin membresía de $99 al mes",
        "why2": "Sin mínimo de 2 horas",
        "why3": "Bilingüe, hecho en Miami",
        "why4": "Tu carro se queda contigo",
        "cta_title": "Sé de los primeros en Miami",
        "cta_sub": "Lanzamos pronto en Brickell, Wynwood y South Beach.",
        "footer_note": (
            "Volante conecta clientes con conductores independientes. "
            "En desarrollo — aún no operativo."
        ),
        "footer_legal": "© 2026 Volante · Miami, FL",
    },
    "en": {
        "meta_title": "Volante — We drive you AND your car home | Miami",
        "meta_desc": (
            "A trusted driver drives your own car home in Miami. "
            "No membership, no minimum, flat fee. Bilingual."
        ),
        "nav_how": "How it works",
        "nav_why": "Why Volante",
        "nav_join": "Join the list",
        "switch_to": "ES",
        "hero_pre": "We drive you",
        "hero_accent": "and your car",
        "hero_post": "home.",
        "hero_sub": (
            "A trusted bilingual driver drives your own car home. "
            "No membership. No minimum. Flat fee."
        ),
        "badge": "Made in Miami · Bilingual",
        "form_label": "Where are you out tonight?",
        "form_contact_ph": "Your WhatsApp or email",
        "form_zone_default": "Choose your area",
        "form_zone_other": "Other",
        "form_cta": "Join the list",
        "form_micro": "We'll text you when we launch in your area. Zero spam.",
        "success": "You're in! We'll reach out the moment we launch near you. 🚗",
        "error": "Enter your WhatsApp or email to join.",
        "pains_kicker": "The problem",
        "pains_title": "Every other option costs you more",
        "pain1_t": "A DUI",
        "pain1_d": "~$10,000 all-in in Florida — never mind the scare.",
        "pain2_t": "The tow",
        "pain2_d": "$516 + $30 if you leave your car in South Beach — plus the Uber back tomorrow.",
        "pain3_t": "The surge",
        "pain3_d": "$40–$100+ on a party night… and your car is still stranded.",
        "how_kicker": "It's simple",
        "how_title": "How it works",
        "step1_t": "Request",
        "step1_d": "Tell us where you are and where you're headed.",
        "step2_t": "Your driver arrives",
        "step2_d": "Bilingual and vetted, with their name and photo before they show up.",
        "step3_t": "They drive your car",
        "step3_d": "They take you and your car home, safe and sound.",
        "step4_t": "Home safe",
        "step4_d": "Your car in your driveway. No tow, no extra trip tomorrow.",
        "why_kicker": "The difference",
        "why_title": "Why Volante",
        "why1": "No $99/month membership",
        "why2": "No 2-hour minimum",
        "why3": "Bilingual, made in Miami",
        "why4": "Your car stays with you",
        "cta_title": "Be among the first in Miami",
        "cta_sub": "Launching soon in Brickell, Wynwood and South Beach.",
        "footer_note": (
            "Volante connects customers with independent drivers. "
            "In development — not yet operating."
        ),
        "footer_legal": "© 2026 Volante · Miami, FL",
    },
}


def normalize_lang(lang: str | None) -> str:
    return lang if lang in LANGS else DEFAULT_LANG


def get_strings(lang: str | None) -> dict[str, str]:
    return STRINGS[normalize_lang(lang)]
