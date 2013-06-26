from five import grok
from ilo.missionreportstats.content.mission_report_statistics import (
    IMissionReportStatistics
)
from ilo.missionreportstats.interfaces import IStatsCache

from zope.lifecycleevent import IObjectModifiedEvent

@grok.subscribe(IMissionReportStatistics, IObjectModifiedEvent)
def refresh_cache_on_save(obj, event):
    IStatsCache(obj).update()
