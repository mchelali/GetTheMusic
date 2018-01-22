# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from rdflib import Graph


# Create your views here.
def index(request):
    return render(request, 'SementicSearch/index.html')

def search(request):
    db = Graph()
    db.parse("SementicSearch/MusicOntology.owl")

    if request.method == 'GET':

        groupe = request.GET.get('groupe', '')
        album = request.GET.get('album', '')
        chansson = request.GET.get('chansson', '')
        qres=[]
        if groupe == "" and album=="" and chansson == "" :
            return JsonResponse(["Entrez qlq chose SVP"], safe=False)
        elif groupe == "" and album=="" and chansson != "" :
            #On lance une recherche pas le titre de chansson
            qres = db.query("""
                SELECT ?nomCHansson
                where {
                    ?Chansson rdf:type music:Chansson .
                    ?Chansson  music:Nom ?nomCHansson  
                        FILTER ( ?nomCHansson ='""" + chansson +"""')
                 }
                """)
        elif groupe != "" and album=="" and chansson == "" :
            # On lance une recherche par le nom du groupe
            qres = db.query("""
                 SELECT  ?chans
                 where {
                    ?chansson music:estChantePar ?artiste .
                    ?chansson music:Nom ?chans .
                    ?artiste music:Nom ?nom
                        FILTER (?nom='"""+ groupe +"""') 
                    }
                """)
        elif groupe == "" and album!="" and chansson == "":
            # On lance une recherche par le nom de l'album
            qres = db.query("""
                SELECT ?nomCHansson
                where {
                   ?Chansson music:estDans ?album .
                   ?Chansson  music:Nom ?nomCHansson .
                   ?album music:Nom ?NomAlbum
                    FILTER (?NomAlbum='"""+ album +"""')
                }
                """)
        elif groupe != "" and album != "" and chansson == "":
            qres = db.query("""  	
                    SELECT  ?nomCHansson
                    where {
                        ?Chansson music:estDans ?album .
                        ?Chansson music:Nom ?nomCHansson .

                        ?chansson music:estChantePar ?artiste .
                        ?chansson music:Nom ?nomCHansson .

                        ?album music:Nom ?NomAlbum .
                        ?artiste music:Nom ?nom .
                        
                            FILTER (?nom='""" + groupe + """' && ?NomAlbum='""" + album + """') .
                    }
                """)
        elif groupe != "" and album == "" and chansson != "":
            qres = db.query("""  	
                        SELECT  ?nomCHansson
                        where {
                            ?Chansson music:estDans ?album .
                            ?Chansson music:Nom ?nomCHansson .

                            ?chansson music:estChantePar ?artiste .
                            ?chansson music:Nom ?nomCHansson .

                            
                            ?artiste music:Nom ?nom .
                            ?Chansson  music:Nom ?nomCHansson 

                                FILTER (?nom='""" + groupe + """' && ?nomCHansson ='""" + chansson +"""') .
                        }
                    """)
        elif groupe == "" and album!="" and chansson != "":
            qres = db.query("""  	
                SELECT  ?nomCHansson
                where {
                    ?Chansson music:estDans ?album .
                    ?Chansson music:Nom ?nomCHansson .
                    
                    ?chansson music:estChantePar ?artiste .
                    ?chansson music:Nom ?nomCHansson .
                    
                    ?album music:Nom ?NomAlbum .
                    ?Chansson  music:Nom ?nomCHansson 
                        FILTER ( ?NomAlbum='"""+ album +"""' && ?nomCHansson ='""" + chansson +"""') .
                }
            """)
        elif groupe != "" and album!="" and chansson != "":
            qres = db.query("""  	
                SELECT  ?nomCHansson
                where {
                    ?Chansson music:estDans ?album .
                    ?Chansson music:Nom ?nomCHansson .
                    
                    ?chansson music:estChantePar ?artiste .
                    ?chansson music:Nom ?nomCHansson .
                    
                    ?album music:Nom ?NomAlbum .
                    ?artiste music:Nom ?nom .
                    ?Chansson  music:Nom ?nomCHansson 
                        FILTER (?nom='"""+ groupe +"""' && ?NomAlbum='"""+ album +"""' && ?nomCHansson ='""" + chansson +"""') .
                }
            """)

        resultat = []
        for row in qres:
            resultat.append(row[0])

        return JsonResponse(resultat, safe=False)