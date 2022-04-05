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
