from django.shortcuts import render
from acftdata.models import Acfts


def planes_page(requsts):
    all_aircraft = Acfts.objects.order_by('type_acft')
    return render(requsts, 'planes.html', context={'data': all_aircraft})
