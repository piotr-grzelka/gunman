from src.barrel_finder.models import portals, Portal


def get_portal(key):
    domain = portals[key][0]

    try:
        model = Portal.objects.get(url=domain)
    except Portal.DoesNotExist:
        model = Portal(name=portals[key][1], url=domain)
        model.save()

    return model