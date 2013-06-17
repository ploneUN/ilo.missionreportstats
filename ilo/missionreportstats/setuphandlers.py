from collective.grok import gs
from ilo.missionreportstats import MessageFactory as _

@gs.importstep(
    name=u'ilo.missionreportstats', 
    title=_('ilo.missionreportstats import handler'),
    description=_(''))
def setupVarious(context):
    if context.readDataFile('ilo.missionreportstats.marker.txt') is None:
        return
    portal = context.getSite()

    # do anything here
