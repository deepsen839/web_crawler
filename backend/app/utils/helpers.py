import re
from urllib.parse import urlparse

import tldextract
import validators


def is_valid_url(value: str) -> bool:
    """
    Check whether a string is a valid URL.
    """
    return validators.url(value)


def normalize_url(url: str) -> str:
    """
    Normalize a URL by ensuring it has a scheme
    and removing any trailing slash.
    """
    url = url.strip()

    if not url.startswith(("http://", "https://")):
        url = f"https://{url}"

    return url.rstrip("/")


def get_domain(url: str) -> str:
    """
    Returns the registered domain.

    Example:
    https://www.microsoft.com/about
    -> microsoft.com
    """
    extracted = tldextract.extract(url)

    return f"{extracted.domain}.{extracted.suffix}"


def get_company_name_from_url(url: str) -> str:
    """
    Guess company name from URL.

    https://stripe.com -> Stripe
    https://www.microsoft.com -> Microsoft
    """
    extracted = tldextract.extract(url)

    return extracted.domain.replace("-", " ").title()


def clean_text(text: str) -> str:
    """
    Remove unnecessary whitespace.
    """

    text = re.sub(r"\s+", " ", text)

    return text.strip()


def unique_list(items: list[str]) -> list[str]:
    """
    Remove duplicates while preserving order.
    """

    seen = set()
    output = []

    for item in items:

        key = item.lower().strip()

        if key in seen:
            continue

        seen.add(key)
        output.append(item.strip())

    return output


def truncate_text(text: str, max_length: int = 12000) -> str:
    """
    Truncate text before sending it to the LLM.
    """

    if len(text) <= max_length:
        return text

    return text[:max_length]


def extract_emails(text: str) -> list[str]:
    """
    Extract email addresses from text.
    """

    pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"

    return re.findall(pattern, text)


def extract_phone_numbers(text: str) -> list[str]:
    """
    Extract phone numbers from text.
    """

    pattern = r"\+?\d[\d\s().-]{7,}\d"

    return re.findall(pattern, text)


def is_same_domain(url1: str, url2: str) -> bool:
    """
    Check whether two URLs belong to the same domain.
    """

    return get_domain(url1) == get_domain(url2)


def remove_fragment(url: str) -> str:
    """
    Remove #fragment from URL.
    """

    parsed = urlparse(url)

    return parsed._replace(fragment="").geturl()