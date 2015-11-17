s = {"query": {
    "filtered": {
        "filter": {
            "bool": {
                "must": [
                    {
                        "range": {
                            "@timestamp": {
                                "from": 1446815625950,
                                "to": 1446819225950
                            }
                        }
                    },
                    {
                        "terms": {
                            "SubService": [
                                "HotelSearchDomestic"
                            ]
                        }
                    },
                    {
                        "terms": {
                            "ServiceCode": [
                                "17100101"
                            ]
                        }
                    }
                ],
                "must_not": [
                    {
                        "terms": {
                            "ServiceType": [
                                "MobileSerivce"
                            ]
                        }
                    }
                ]
            }
        }
    }}}
import json

import requests

data = {"request_body": json.dumps(s), "access_token": "8d5b2495fd24f7e5e4c913515d5204c3"}
print json.dumps(data)
r = requests.post("http://osg.ops.ctripcorp.com/api/10900/mobile-hwsvcvisitlog-2015.11.06/_search?search_type=count",
                  data=json.dumps(data))
print r.content
s1 = {
    "query": {
        "filtered": {
            "filter": {
                "bool": {
                    "must": [
                        {
                            "range": {
                                "@timestamp": {
                                    "from": 1446815625950,
                                    "to": 1446819225950
                                }
                            }
                        },
                        {
                            "terms": {
                                "SubService": [
                                    "HotelSearchDomestic"
                                ]
                            }
                        },
                        {
                            "terms": {
                                "ServiceCode": [
                                    "17100101"
                                ]
                            }
                        }
                    ],
                    "must_not": [
                        {
                            "terms": {
                                "ServiceType": [
                                    "MobileSerivce"
                                ]
                            }
                        }
                    ]
                }
            }
        }
    },
    "aggs": {
        "Interval_avg": {
            "avg": {
                "field": "Interval"
            }
        }
    }
}
data = {"request_body": json.dumps(s1), "access_token": "8d5b2495fd24f7e5e4c913515d5204c3"}
print json.dumps(data)
r = requests.post("http://osg.ops.ctripcorp.com/api/10900/mobile-hwsvcvisitlog-2015.11.06/_search?search_type=count",
                  data=json.dumps(data))
print r.content

print "----------------------------------------------"

s = {"query": {
    "filtered": {
        "filter": {
            "bool": {
                "must": [
                    {
                        "range": {
                            "@timestamp": {
                                "from": 1446815625950,
                                "to": 1446819225950
                            }
                        }
                    },
                    {
                        "terms": {
                            "SubService": [
                                "HotelSearchDomestic"
                            ]
                        }
                    },
                    {
                        "terms": {
                            "ServiceCode": [
                                "15100202"
                            ]
                        }
                    }
                ],
                "must_not": [
                    {
                        "terms": {
                            "ServiceType": [
                                "MobileSerivce"
                            ]
                        }
                    }
                ]
            }
        }
    }}}
import json, requests

data = {"request_body": json.dumps(s), "access_token": "8d5b2495fd24f7e5e4c913515d5204c3"}
print json.dumps(data)
r = requests.post("http://osg.ops.ctripcorp.com/api/10900/mobile-hwsvcvisitlog-2015.11.06/_search?search_type=count",
                  data=json.dumps(data))
print r.content
s1 = {
    "query": {
        "filtered": {
            "filter": {
                "bool": {
                    "must": [
                        {
                            "range": {
                                "@timestamp": {
                                    "from": 1446815625950,
                                    "to": 1446819225950
                                }
                            }
                        },
                        {
                            "terms": {
                                "SubService": [
                                    "HotelSearchDomestic"
                                ]
                            }
                        },
                        {
                            "terms": {
                                "ServiceCode": [
                                    "15100202"
                                ]
                            }
                        }
                    ],
                    "must_not": [
                        {
                            "terms": {
                                "ServiceType": [
                                    "MobileSerivce"
                                ]
                            }
                        }
                    ]
                }
            }
        }
    },
    "aggs": {
        "Interval_avg": {
            "avg": {
                "field": "Interval"
            }
        }
    }
}
data = {"request_body": json.dumps(s1), "access_token": "8d5b2495fd24f7e5e4c913515d5204c3"}
print json.dumps(data)
r = requests.post("http://osg.ops.ctripcorp.com/api/10900/mobile-hwsvcvisitlog-2015.11.06/_search?search_type=count",
                  data=json.dumps(data))
print r.content

print "----------------------------------------------"

s = {"query": {
    "filtered": {
        "filter": {
            "bool": {
                "must": [
                    {
                        "range": {
                            "@timestamp": {
                                "from": 1446815625950,
                                "to": 1446819225950
                            }
                        }
                    },
                    {
                        "terms": {
                            "SubService": [
                                "HotelSearchOversea"
                            ]
                        }
                    },
                    {
                        "terms": {
                            "ServiceCode": [
                                "15100102"
                            ]
                        }
                    }
                ],
                "must_not": [
                    {
                        "terms": {
                            "ServiceType": [
                                "MobileSerivce"
                            ]
                        }
                    }
                ]
            }
        }
    }}}
import json, requests

data = {"request_body": json.dumps(s), "access_token": "8d5b2495fd24f7e5e4c913515d5204c3"}
print json.dumps(data)
r = requests.post("http://osg.ops.ctripcorp.com/api/10900/mobile-hwsvcvisitlog-2015.11.06/_search?search_type=count",
                  data=json.dumps(data))
print r.content
s1 = {
    "query": {
        "filtered": {
            "filter": {
                "bool": {
                    "must": [
                        {
                            "range": {
                                "@timestamp": {
                                    "from": 1446815625950,
                                    "to": 1446819225950
                                }
                            }
                        },
                        {
                            "terms": {
                                "SubService": [
                                    "HotelSearchOversea"
                                ]
                            }
                        },
                        {
                            "terms": {
                                "ServiceCode": [
                                    "15100102"
                                ]
                            }
                        }
                    ],
                    "must_not": [
                        {
                            "terms": {
                                "ServiceType": [
                                    "MobileSerivce"
                                ]
                            }
                        }
                    ]
                }
            }
        }
    },
    "aggs": {
        "Interval_avg": {
            "avg": {
                "field": "Interval"
            }
        }
    }
}
data = {"request_body": json.dumps(s1), "access_token": "8d5b2495fd24f7e5e4c913515d5204c3"}
print json.dumps(data)
r = requests.post("http://osg.ops.ctripcorp.com/api/10900/mobile-hwsvcvisitlog-2015.11.06/_search?search_type=count",
                  data=json.dumps(data))
print r.content

print "----------------------------------------------"

s = {"query": {
    "filtered": {
        "filter": {
            "bool": {
                "must": [
                    {
                        "range": {
                            "@timestamp": {
                                "from": 1446815625950,
                                "to": 1446819225950
                            }
                        }
                    },
                    {
                        "terms": {
                            "SubService": [
                                "HotelSearchOversea"
                            ]
                        }
                    },
                    {
                        "terms": {
                            "ServiceCode": [
                                "15100202"
                            ]
                        }
                    }
                ],
                "must_not": [
                    {
                        "terms": {
                            "ServiceType": [
                                "MobileSerivce"
                            ]
                        }
                    }
                ]
            }
        }
    }}}
import json, requests

data = {"request_body": json.dumps(s), "access_token": "8d5b2495fd24f7e5e4c913515d5204c3"}
print json.dumps(data)
r = requests.post("http://osg.ops.ctripcorp.com/api/10900/mobile-hwsvcvisitlog-2015.11.06/_search?search_type=count",
                  data=json.dumps(data))
print r.content
s1 = {
    "query": {
        "filtered": {
            "filter": {
                "bool": {
                    "must": [
                        {
                            "range": {
                                "@timestamp": {
                                    "from": 1446815625950,
                                    "to": 1446819225950
                                }
                            }
                        },
                        {
                            "terms": {
                                "SubService": [
                                    "HotelSearchOversea"
                                ]
                            }
                        },
                        {
                            "terms": {
                                "ServiceCode": [
                                    "15100202"
                                ]
                            }
                        }
                    ],
                    "must_not": [
                        {
                            "terms": {
                                "ServiceType": [
                                    "MobileSerivce"
                                ]
                            }
                        }
                    ]
                }
            }
        }
    },
    "aggs": {
        "Interval_avg": {
            "avg": {
                "field": "Interval"
            }
        }
    }
}
data = {"request_body": json.dumps(s1), "access_token": "8d5b2495fd24f7e5e4c913515d5204c3"}
print json.dumps(data)
r = requests.post("http://osg.ops.ctripcorp.com/api/10900/mobile-hwsvcvisitlog-2015.11.06/_search?search_type=count",
                  data=json.dumps(data))
print r.content
