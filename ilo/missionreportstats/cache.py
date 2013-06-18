from ilo.missionreportstats.interfaces import IStatsCache
from ilo.missionreportstats.content.mission_report_statistics import IMissionReportStatistics
from zope.annotation.interfaces import IAnnotations
from five import grok

import Missing
from zope.annotation.interfaces import IAnnotations
from persistent.dict import PersistentDict
from operator import itemgetter
from heapq import nlargest


def mostcommon(iterable,n=None):
    """Return a sorted list of the most common to least common elements and
    their counts.  If n is specified, return only the n most common elements.
    """

    # http://code.activestate.com/recipes/347615/ (Raymond
    # Hettinger)

    bag = {}
    for elem in iterable:
        bag[elem] = bag.get(elem, 0) + 1
    if n is None:
        return sorted(bag.iteritems(), key=itemgetter(1), reverse=True)
    it = enumerate(bag.iteritems())
    nl = nlargest(n, ((cnt, i, elem) for (i, (elem, cnt)) in it))
    return [(elem,cnt) for cnt, i, elem in nl]


class StatsCache(grok.Adapter):
    grok.context(IMissionReportStatistics)
    grok.implements(IStatsCache)

    anno_key = 'ilo.missionreportstats.contextcache'

    def __init__(self, context):
        self.context = context

    def update(self):
        anno = IAnnotations(self.context)
        anno.setdefault(self.anno_key, PersistentDict())
        cache = anno[self.anno_key]
        cache['office'] = self._top_items_by_index('office')
        cache['theme'] = self._top_items_by_index('theme')
        cache['mission_location'] = self._top_items_by_index('mission_location')

    def _top_items_by_index(self, index):
        result = []
        for i in mostcommon(self._items(index)):
            result.append({'elem':i[0],'count':i[1]})
        return result

    def _items(self, attr):
        query = {
            'portal_type':  'MissionReport',
            'office': self.context.offices or []
        }

        result = []
        for item in self.context.portal_catalog(query):
            val = getattr(item, attr, None)

            if val == None or val == Missing.Value:
                indexdata = self.context.portal_catalog.getIndexDataForRID(
                        item.getRID())
                val = indexdata.get(attr, None)

            if val == None:
                val = getattr(
                        item.getObject(),
                        attr,
                        None
                        )

            if callable(val):
                val = val()

            if val:
                if type(val) == str:
                    result.append(val)

                elif iter(val):
                    for i in val:
                        result.append(i)
        return result

    def get(self, key):
        anno = IAnnotations(self.context)
        anno.setdefault(self.anno_key, PersistentDict())
        cache = anno[self.anno_key]
        return cache.get(key, [])

