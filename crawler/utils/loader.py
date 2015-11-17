from jsonpath_rw import parse
from scrapy.loader import ItemLoader
from scrapy.utils.python import flatten


class JsonItemLoader(ItemLoader):
    def _get_xpathvalues(self, xpaths, **kw):
        self._check_selector_method()
        jsonpath_expr = parse(xpaths)
        # self.log("SELECTOR: %s" % unicode(self.selector), log.INFO)
        res_list = [match.value for match in jsonpath_expr.find(self.selector)]
        return flatten(res_list)
