from five import grok
from plone.directives import dexterity, form
from ilo.missionreportstats.content.mission_report_statistics import IMissionReportStatistics
from datetime import datetime
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

    def _get_cache(self, key, year=None):
        if year is None:
            return IStatsCache(self.context).get(key)
        return IStatsCache(self.context).get('years')[year].get(key) if year in IStatsCache(self.context).get('years') else IStatsCache(self.context).get(key)

    def by_offices(self, year=None):
        return self._get_cache('office', year)

    def by_themes(self, year=None):
        return self._get_cache('theme', year)

    def by_destination(self, year=None):
        return self._get_cache('mission_location', year)

    def by_creator(self, year=None):
        return self._get_cache('creator', year)

    def years(self):
        return [None] + range(2010, datetime.now().year + 1)

