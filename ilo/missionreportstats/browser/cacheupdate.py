from five import grok
from Products.CMFCore.interfaces import ISiteRoot
from ilo.missionreportstats.interfaces import IStatsCache

class StatsCacheUpdate(grok.View):
    grok.name('missionreportstats-update')
    grok.context(ISiteRoot)

    def render(self):
        count = 0
        for i in self.context.portal_catalog(
                portal_type='ilo.missionreportstats.missionreportstatistics'
            ):
            IStatsCache(i.getObject()).update()
            count += 1

        return u'%s items updated' % count
