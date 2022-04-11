from typing import Dict
from django import template
from lac.models import AccessSiteCollection

register = template.Library()

@register.simple_tag
def ait_collection_name(id: str, lang_code):
    coll_names = (AccessSiteCollection.objects
        .filter(ait_collection_map__icontains=id)
        .values("display_name_en", "display_name_fr")
        .first()
    )
    return coll_names.get(f"display_name_{lang_code}", id) if coll_names else id

@register.simple_tag
def format_ait_date(date):
    return f"{date[:4]}-{date[4:6]}-{date[6:8]}" if len(date) > 8 else date

@register.simple_tag
def ait_all_crawls_url(item: Dict):
    return f"https://bac-lac.wayback.archive-it.org/query?type=urlquery&url={item['link']}"

@register.simple_tag
def ait_this_crawl_url(item: Dict):
    return f"https://bac-lac.wayback.archive-it.org/{item['date']}/{item['link']}"

@register.simple_tag
def ait_select_collection(id: int, param: str):
    if param.isnumeric() and id == int(param):
        return " selected" 

@register.simple_tag
def ait_display_name(collection: AccessSiteCollection, lang: str):
    return getattr(collection, f"display_name_{lang}", "display_name_en")
