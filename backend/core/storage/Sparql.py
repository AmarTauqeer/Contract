from SPARQLWrapper import SPARQLWrapper, BASIC
import os


class SPARQL():
    def __init__(self):
        super().__init__()
        host_get = os.getenv("HOST_URI_GET")
        self.HOST_URI = host_get

    def init_sparql(self, hostname, userid, password):
        sparql = SPARQLWrapper(hostname)
        sparql.setCredentials(userid, password)
        return sparql

    def post_sparql(self, userid, password, query, type="insert"):
        host_post = os.getenv("HOST_URI_POST")
        hostname = host_post

        sparql = SPARQLWrapper(hostname)
        sparql.setHTTPAuth(BASIC)
        sparql.setCredentials(userid, password)
        sparql.setQuery(query)
        sparql.method = "POST"
        sparql.queryType = "INSERT"
        sparql.setReturnFormat('json')
        result = sparql.query()
        if str(result.response.read().decode("utf-8")) == "":
            return "Success"
        else:
            return "Fail"
