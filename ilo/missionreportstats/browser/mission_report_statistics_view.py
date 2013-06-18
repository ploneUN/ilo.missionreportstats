from five import grok
from plone.directives import dexterity, form
from ilo.missionreportstats.content.mission_report_statistics import IMissionReportStatistics
from ilo.missionreportstats.interfaces import IStatsCache
import Missing
grok.templatedir('templates')

class Index(dexterity.DisplayForm):
    grok.context(IMissionReportStatistics)
    grok.require('zope2.View')
    grok.template('mission_report_statistics_view')
    grok.name('view')

    def update(self):
        if self.request.get('force_cache_update', None):
            IStatsCache(self.context).update()

    def _get_cache(self, key):
        return IStatsCache(self.context).get(key)

    def by_offices(self):
        return self._get_cache('office')

    def by_themes(self):
        return self._get_cache('theme')

    def by_destination(self):
        return self._get_cache('mission_location')

