from five import grok
from plone.directives import dexterity, form
from ilo.missionreportstats.content.mission_report_statistics import IMissionReportStatistics
import Missing
from zope.annotation.interfaces import IAnnotation
from persistent.dict import PersistentDict
grok.templatedir('templates')

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


class Index(dexterity.DisplayForm):
    grok.context(IMissionReportStatistics)
    grok.require('zope2.View')
    grok.template('mission_report_statistics_view')
    grok.name('view')

    anno_key = 'ilo.missionreportstats.contextcache'

    def update_cache(self):
        anno = IAnnotation(self.context)
        anno.setdefault(self.anno_key) = PersistentDict()
        cache = anno[self.anno_key]
        cache['office'] = self._top_items_by_index('office')
        cache['theme'] = self._top_items_by_index('theme')
        cache['mission_location'] = self._top_items_by_index('mission_location')

    def update(self):
        if self.request.get('force_cache_update', None):
            self.update_cache()

    def _get_cache(self, key):
        anno = IAnnotation(self.context)
        anno.setdefault(self.anno_key) = PersistentDict()
        cache = anno[self.anno_key]
        return cache.get(key, [])

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
                val = indexdata.get(self.data.val, None)

                if val == None:
                    val = getval(
                            item.getObject(),
                            self.data.val,
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

    def by_offices(self):
        return self._get_cache('office')

    def by_themes(self):
        return self._get_cache('theme')

    def by_destination(self):
        return self._get_cache('mission_location')

