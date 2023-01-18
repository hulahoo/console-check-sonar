"""Services for tag app"""

from console_api.tag.models import Tag


def get_new_tag_id() -> int:
    """Return id for new tag"""

    if Tag.objects.count() == 0:
        tag_id = 1
    else:
        tag_id = Tag.objects.order_by("id").last().id + 1

    return tag_id
