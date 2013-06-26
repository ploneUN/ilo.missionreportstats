from five import grok
from ilo.missionreportstats.content.mission_report_statistics import (
    IMissionReportStatistics
)
from ilo.missionreportstats.interfaces import IStatsCache

from zope.lifecycleevent import IObjectModifiedEvent, IObjectAddedEvent

@grok.subscribe(IMissionReportStatistics, IObjectModifiedEvent)
def refresh_cache_on_save(obj, event):
    IStatsCache(obj).update()

@grok.subscribe(IMissionReportStatistics, IObjectAddedEvent)
def refresh_cache_on_create(obj, event):
    IStatsCache(obj).update()
