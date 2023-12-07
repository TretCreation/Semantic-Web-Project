from SPARQLWrapper import SPARQLWrapper, JSON, N3


class Repository:

    def __init__(self):
        self.sparql = SPARQLWrapper('https://dbpedia.org/sparql')

    def get_countries(self) -> list:
        query = '''
            SELECT DISTINCT ?name
            WHERE { 
                ?country rdf:type dbo:Country ;
                        dbo:humanDevelopmentIndex ?index ;
                        dbp:commonName ?name .

            }
            ORDER BY DESC(?index)
            LIMIT 100
        '''
        self.sparql.setQuery(query)
        self.sparql.setReturnFormat(JSON)
        query_res = self.sparql.query().convert()

        return [x['name']['value'] for x in query_res['results']['bindings']]

    def get_cities(self, country_name: str) -> list:
        query = '''
            SELECT ?name
            WHERE {
             {
                SELECT DISTINCT ?country
                WHERE { 
                    ?country rdf:type dbo:Country ;
                    dbp:commonName "!_!"@en .
                }
             }
        
            ?city rdf:type dbo:City ;
                dbo:country ?country ;
                dbp:name ?name .
             # FILTER ( ?c IN (?country, ?x ) )
            }
        
            #ORDER BY DESC(?popul)
            LIMIT 100
        '''

        formatted_query = query.replace('!_!', country_name, 1)
        self.sparql.setQuery(formatted_query)
        self.sparql.setReturnFormat(JSON)
        query_res = self.sparql.query().convert()

        return [x['name']['value'] for x in query_res['results']['bindings']]

    def get_universities_by_city(self, city: str) -> list:
        query = '''
            SELECT ?name
            WHERE { 
            {
                SELECT DISTINCT ?city
                WHERE { 
                    ?city rdf:type dbo:City ;
                        dbp:name "!_!"@en .
                }
            }
            ?uni rdf:type dbo:University ;
                dbp:city ?city ;
                dbp:name ?name .
            }
            LIMIT 100
        '''

        formatted_query = query.replace('!_!', city, 1)
        self.sparql.setQuery(formatted_query)
        self.sparql.setReturnFormat(JSON)
        query_res = self.sparql.query().convert()

        return [x['name']['value'] for x in query_res['results']['bindings']]

    def get_university_by_name(self, uni_name: str) -> dict | None:
        query = '''
            SELECT ?city ?students ?desc ?logo ?site
            WHERE { 
                ?uni rdf:type dbo:University  ;
                    dbp:name "!_!"@en ;
                    dbo:city ?city ;
                    dbo:abstract ?desc ;
                    dbo:thumbnail ?logo .
        
                filter (lang(?desc) = "en")
                OPTIONAL { ?uni dbp:students ?students . } 
                OPTIONAL { ?uni dbp:website ?site . }
            }
        '''
        formatted_query = query.replace('!_!', uni_name, 1)
        self.sparql.setQuery(formatted_query)
        self.sparql.setReturnFormat(JSON)
        query_res = self.sparql.query().convert()

        res = query_res['results']['bindings']
        if len(res) > 0:
            res = res[0]
            city = res['city']['value']
            if city.startswith('http'):
                index = city.rfind('/') + 1
                city = city[index:]
            uni = {
                'name': uni_name,
                'city': city,
                'logo': res['logo']['value'],
            }
            if students := res.get('students'):
                uni['students'] = students['value']
            if site := res.get('site'):
                uni['site'] = site['value']

            return uni
