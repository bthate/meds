# defines.py
#
#

""" constants and definitions """

__copyright__ = "Copyright 2015, Bart Thate"

import logging
import os.path
import string
import socket
import os
import re

#:
LEVELS = {'debug': logging.DEBUG,
          'info': logging.INFO,  
          'warning': logging.WARNING,
          'warn': logging.WARNING,   
          'error': logging.ERROR,    
          'critical': logging.CRITICAL
        }


#:
timere = re.compile('(\S+)\s+(\S+)\s+(\d+)\s+(\d+):(\d+):(\d+)\s+(\d+)')
bdmonths = ['Bo', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
monthint = {
            'Jan': 1,
            'Feb': 2,
            'Mar': 3,
            'Apr': 4,
            'May': 5,
            'Jun': 6,
            'Jul': 7,
            'Aug': 8,
            'Sep': 9,
            'Oct': 10,
            'Nov': 11,
            'Dec': 12 
           }

#:
port = 10102

#:
homedir = os.path.expanduser("~") 
curdir = os.getcwd()
try: hostname = socket.getfqdn()
except: hostname = "localhost" 
logdir = homedir + os.sep + "meds.logs" + os.sep

#:
datefmt = '%H:%M:%S'
format_large = "%(asctime)-8s %(message)-80s %(module)s.%(lineno)s"
format = "%(asctime)-8s %(message)-8s"

#:
leapfactor = float(6*60*60)/float(365*24*60*60)
daylist = ["Date", "path"]
dayformats = ["%Y-%m-%d %H:%M:%S", "%a, %d %m %Y %H:%M:%S", "%a, %d %m %Y %H:%M:%S %s (%s)", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d", "%d-%m-%Y"]
dayshorts =  ["%H:%M:%S", "%H:%M"]
short_day = "(%s %s %s %s:%s:%s)"

#:
dirmask = 0o700
filemask = 0o600

#:
headertxt = '''# this is an MEDS file, %s
#
# this file can be edited !!

'''

#:
basic_types= [ str, int, float, bool, None]

#:
attributes = {}
subelements = {}

attributes['message'] = ['type', 'from', 'to', 'id']
subelements['message'] = ['subject', 'body', 'error', 'thread', 'x']

attributes['presence'] = ['type', 'from', 'to', 'id']
subelements['presence'] = ['show', 'status', 'priority', 'x']

attributes['iq'] = ['type', 'from', 'to', 'id']
subelements['iq'] = ['query', 'error']

allowedchars = string.ascii_letters + string.digits + "_,-. \n" + string.punctuation
allowednamechars = string.ascii_letters + string.digits + '!.@'

#:
ERASE_LINE = '\033[2K'
BOLD='\033[1m'
GRAY='\033[99m'
RED = '\033[91m'
YELLOW = '\033[93m'
GREEN = '\033[92m'
BLUE = '\033[94m'
BLA = '\033[95m'
ENDC = '\033[0m'

#:
re_url_match  = re.compile('((?:http|https)://\S+)')

#:
reason_txt = """
Wetboek van Strafrecht:

1) Antipsychotica zijn in hun werking benadeling van de gezondheid.
2) Daarmee is toedienen van deze medicijnen misnhandeling zoals vernoemd in het wetboek van strafrecht.
3) Het doen laten verdwijnen van gevaar is het oogmerk.

Verdrag tegen foltering:

1) Een maatregel is geen straf.
2) Een ambtsbevel is geen rechtvaardiging.
3) Geen enkele omstandigheid is een rechtvaardiging.
"""
#:
gemeenten = """Amsterdam
Aa en Hunze
Aalburg
Aalsmeer
Aalten
Achtkarspelen
Alblasserdam
Albrandswaard
Alkmaar
Almelo
Almere
Alphen aan den Rijn
Alphen-Chaam
Ameland
Amersfoort
Amstelveen
Amsterdam
Apeldoorn
Appingedam
Arnhem
Assen
Asten
Baarle-Nassau
Baarn
Barendrecht
Barneveld
Bedum
Beek
Beemster
Beesel
Bellingwedde
Bergeijk
Bergen (Limburg)
Bergen (Noord-Holland)
Bergen op Zoom
Berkelland
Bernheze
Best
Beuningen
Beverwijk
Binnenmaas
Bladel
Blaricum
Bloemendaal
Bodegraven-Reeuwijk
Boekel
Bonaire
Borger-Odoorn
Borne
Borsele
Boxmeer
Boxtel
Breda
Brielle
Bronckhorst
Brummen
Brunssum
Bunnik
Bunschoten
Buren
Bussum
Capelle aan den IJssel
Castricum
Coevorden
Cranendonck
Cromstrijen
Cuijk
Culemborg
Dalfsen
Dantumadeel
De Bilt
De Friese Meren
De Marne
De Ronde Venen
De Wolden
Delft
Delfzijl
Den Haag s-Gravenhage
Den Helder
Deurne
Deventer
Diemen
Dinkelland
Doesburg
Doetinchem
Dongen
Dongeradeel
Dordrecht
Drechterland
Drimmelen
Dronten
Druten
Duiven
Echt-Susteren
Edam-Volendam
Ede
Eemnes
Eemsmond
Eersel
Eijsden-Margraten
Eindhoven
Elburg
Emmen
Enkhuizen
Enschede
Epe
Ermelo
Etten-Leur
Ferwerderadeel
Geertruidenberg
Geldermalsen
Geldrop-Mierlo
Gemert-Bakel
Gennep
Giessenlanden
Gilze en Rijen
Goeree-Overflakkee
Goes
Goirle
Gorinchem (Gorcum of Gorkum)
Gouda
Grave
Groesbeek
Groningen
Grootegast
Gulpen-Wittem
Haaksbergen
Haaren
Haarlem
Haarlemmermeer
Halderberge
Hardenberg
Harderwijk
Hardinxveld-Giessendam
Haren
Harlingen
Hattem
Heemskerk
Heemstede
Heerde
Heerenveen
Heerhugowaard
Heerlen
Heeze-Leende
Heiloo
Hellendoorn
Hellevoetsluis
Helmond
Hendrik-Ido-Ambacht
Hengelo (Overijssel)
s-Hertogenbosch (Den Bosch)
Het Bildt
Heumen
Heusden
Hillegom
Hilvarenbeek
Hilversum
Hof van Twente
Hollands Kroon
Hoogeveen
Hoogezand-Sappemeer
Hoorn
Horst aan de Maas
Houten
Huizen
Hulst
IJsselstein
Kaag en Braassem
Kampen
Kapelle
Katwijk
Kerkrade
Koggenland
Kollumerland en Nieuwkruisland
Korendijk
Krimpen aan den IJssel
Krimpenerwaard
Laarbeek
Landerd
Landgraaf
Landsmeer
Langedijk
Lansingerland
Laren
Leek
Leerdam
Leeuwarden
Leeuwarderadeel
Leiden
Leiderdorp
Leidschendam-Voorburg
Lelystad
Leudal
Leusden
Lingewaal
Lingewaard
Lisse
Littenseradeel
Lochem
Loon op Zand
Lopik
Loppersum
Losser
Maasdriel
Maasgouw
Maassluis
Maastricht
Marum
Medemblik
Meerssen
Menaldumadeel
Menterwolde
Meppel
Middelburg
Midden-Delfland
Midden-Drenthe
Mill en Sint Hubert
Moerdijk
Molenwaard
Montferland
Montfoort
Mook en Middelaar
Muiden
Naarden
Neder-Betuwe
Nederweert
Neerijnen
Nieuwegein
Nieuwkoop
Nijkerk
Nijmegen
Nissewaard
Noord-Beveland
Noordenveld
Noordoostpolder
Noordwijk
Noordwijkerhout
Nuenen, Gerwen en Nedercoreten
Nunspeet
Nuth
Oegstgeest
Oirschot
Oisterwijk
Oldambt
Oldebroek
Oldenzaal
Olst-Wijhe
Ommen
Onderbanken
Oost Gelre
Oosterhout
Ooststellingwerf
Oostzaan
Opmeer
Opsterland
Oss
Oud-Beijerland
Oude IJsselstreek
Ouder-Amstel
Oudewater
Overbetuwe
Papendrecht
Peel en Maas
Pekela
Pijnacker-Nootdorp
Purmerend
Putten
Raalte
Reimerswaal
Renkum
Renswoude
Reusel-De Mierden
Rheden
Rhenen
Ridderkerk
Rijnwaarden
Rijssen-Holten
Rijswijk
Roerdalen
Roermond
Roosendaal
Rotterdam
Rozendaal
Rucphen
Saba
Schagen
Scherpenzeel
Schiedam
Schiermonnikoog
Schijndel
Schinnen
Schouwen-Duiveland
Simpelveld
Sint Anthonis
Sint Eustatius
Sint-Michielsgestel
Sint-Oedenrode
Sittard-Geleen
Sliedrecht
Slochteren
Sluis
Smallingerland
Soest
Someren
Son en Breugel
Stadskanaal
Staphorst
Stede Broec
Steenbergen
Steenwijkerland
Stein
Stichtse Vecht
Strijen
Ten Boer
Terneuzen
Terschelling
Texel
Teylingen
Tholen
Tiel
Tietjerksteradeel
Tilburg
Tubbergen
Twenterand
Tynaarlo
Uden
Uitgeest
Uithoorn
Urk
Utrecht
Utrechtse Heuvelrug
Vaals
Valkenburg aan de Geul
Valkenswaard
Veendam
Veenendaal
Veere
Veghel
Veldhoven
Velsen
Venlo
Venray
Vianen
Vlaardingen
Vlagtwedde
Vlieland
Vlissingen
Voerendaal
Voorschoten
Voorst
Vught
Waalre
Waalwijk
Waddinxveen
Wageningen
Wassenaar
Waterland
Weert
Weesp
Werkendam
West Maas en Waal
Westerveld
Westervoort
Westland
Weststellingwerf
Westvoorne
Wierden
Wijchen
Wijdemeren
Wijk bij Duurstede
Winsum
Winterswijk
Woensdrecht
Woerden
Wormerland
Woudenberg
Woudrichem
Zaanstad
Zaltbommel
Zandvoort
Zederik
Zeevang
Zeewolde
Zeist
Zevenaar
Zoetermeer
Zoeterwoude
Zuidhorn
Zuidplas
Zundert
Zutphen
Zwartewaterland
Zwijndrecht
Zwolle""".split("\n")
