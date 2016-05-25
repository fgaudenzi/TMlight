from xml.dom.minidom import parse
import xml.dom.minidom

class ProbeParse:
    def parseTestCase(self,tc):
        print "parsing"
        DOMTree = xml.dom.minidom.parseString(tc)
        collection = DOMTree.documentElement
        request_probe=collection.getAttribute("probe_driver")
        print request_probe
        return request_probe
