# stats.py
#
#

""" statistics on suicide. """

from meds.misc import elapsed, to_time
from meds.mods.clock import Repeater
from meds.scheduler import launcher
from meds.defines import gemeenten
from meds.object import Object
from meds.cfg import cfg

import logging
import random
import time

def register(mods): mods.register("mention", mention)

def init(mods):
    for names in ["suicide", "pogingen", "incidenten", "opname", "alarm"]:
        if names not in cfg.main.init: continue
        for name in display.get(names):
            nr = cijfers.get(name, 0)
            if nr:
                repeater = Repeater(seconds(cijfers.get(name)), mention, name=name)
                launcher.launch(repeater.start)

def seconds(nrperjaar):
    if not nrperjaar: return 0
    return int((365 * 24 * 60 * 60) / nrperjaar)

def mention(event):
    global display
    name = event.rest or event.name
    delta = time.time() - starttime
    sec = seconds(cijfers.get(name, 0))
    if sec: nr = int(delta / sec)
    else: nr = 0 ;
    txt = "%s #%s" % (name.upper(), nr)
    if name in omschrijving: txt += " (%s)" % omschrijving.get(name)
    if name in cijfers: txt += " %d/jaar elke %s" % (cijfers.get(name), elapsed(seconds(cijfers.get(name))))
    if name in soort: txt += " %s" % soort.get(name)
    if name in dbc: txt += " %s" % dbc.get(name)
    txt += ", bijv. uit %s" % (random.choice(gemeenten))
    if name in tags: txt += " %s" % tags.get(name)
    txt += " (%s)" % elapsed(delta)
    event.announce(txt)

startdate = "2012-11-23 00:00:00"
starttime = to_time(startdate)
source = "http://pypi.python.org/pypi/meds"

display = Object()
display.alarm = ["politie", "hap", "keten"]
display.oordeel = ["verwijs", "uitstroom", "opname"]
display.vergiftigingen = ["vergiftigingen", "tumor"]
display.neurotoxisch = ["neurotoxisch", ]
display.suicide = ["suicide",]
display.pogingen = ["pogingen",]   
display.incidenten = ["incidenten",]
display.acuut = ["acuut",]   
display.zorgmijder = ["zorgmijder", ] 
display.opname = ["ibs", "rm", "vlm", "mvv", "vwm", "ev", "ob", "zb"]

tags = Object()
tags.opname = "#broodjepindakaas"
tags.crisis = "#triade"
tags.suicide = "#wetverplichteggz"
tags.pogingen = "#prettigweekend"
tags.incidenten = "#jammerdan"
tags.acuut = "#geenbedvoorjou"
tags.zorgmijder = "#helaas"
tags.inwoners = "#gebodenvrucht"
tags.crisis = "#gijzultdoden"
tags.alarm = "#telaat"
tags.oordeel = "#geencrisis"
tags.vergiftigingen = "#overduur"
tags.neurotoxisch = "#overdosis"
tags.schizofrenie = "#gifmedicijn"
tags.angst = "#gifmedicijn"
tags.depressie = "#gifmedicijn"
tags.meds = "#gifmedicijn"
tags.ibs = "#overlas"
tags.rm = "#benadeling"
tags.vwm = "#maatregel"
tags.mvv = "#nogeven"
tags.vlm = "#direct!!"
tags.evb = "#kieserzelfvoor"
tags.ob = "#ffkijken#"
tags.zb = "????"

cijfers = Object()
cijfers.ibs = 7964
cijfers.rm = 14902
cijfers.vwm = 6163
cijfers.mvv = 3966
cijfers.vlm = 4699
cijfers.evb = 65
cijfers.ob = 0
cijfers.zb = 9
cijfers.opnames = 22866
cijfers.crisis = 150000
cijfers.oordeel = 150000
cijfers.suicide = 1854
cijfers.pogingen = 95000
cijfers.incidenten = 51876
cijfers.acuut = 8000
cijfers.zorgmijder = 24000
cijfers.politie = 0.15 * cijfers.crisis
cijfers.hap = 0.40 * cijfers.crisis
cijfers.keten = 0.45 * cijfers.crisis
cijfers.verwijs = cijfers.crisis * 0.85 
cijfers.uitstroom = cijfers.crisis * 0.05
cijfers.opname = cijfers.crisis * 0.10
cijfers.vergiftigingen = 25262
cijfers.neurotoxisch = 0.49 * cijfers.vergiftigingen
cijfers.burenoverlast = 12000
cijfers.huisartsen = 11345
cijfers.speed = 20000
cijfers.cocaine = 50000
cijfers.alcohol = 400000
cijfers.wiet = 500000
cijfers.antipsychotica = 150000
cijfers.antidepresiva = 600000
cijfers.slaapmiddel = 1000000
cijfers.ambulant = 792000
cijfers.verslaving = 13000
cijfers.schizofrenie = 9800
cijfers.depressie = 9600
cijfers.poh = 1300000
cijfers.amitriptyline = 189137
cijfers.paroxetine = 186028
cijfers.citalopram = 154620
cijfers.oxazepam = 133608
cijfers.venlafaxine = 112000
cijfers.mirtazapine = 110742
cijfers.quetiapine = 84414
cijfers.diazepam = 72000
cijfers.sertraline = 68000
cijfers.haloperidol = 59825
cijfers.tumor = 12000
cijfers.detox = 65654
cijfers.verslaafden = 2074278
cijfers.volwassendoop = 500
cijfers.arbeidshandicap = 103000
cijfers.uitzetting = 5900
cijfers.inwoners = 16800000

dbc = Object()
dbc.middelgebondenstoornissen = 33060
dbc.somatoformestoornissen = 21841
dbc.cognitievestoornissen = 25717
dbc.angststoornissen = 54458
dbc.aanpassingsstoornissen = 43079
dbc.depressievestoornissen = 102361
dbc.eetstoornissen = 8688
dbc.restgroepdiagnose = 16996
dbc.ontbrekendeprimairediagnose = 3030
dbc.andereproblemenredenvoorzorg = 49286
dbc.schizofrenieenanderepsychotischestoornissen = 6798
dbc.bipolairestoornissen = 3569
dbc.posttraumatischestressstoornis = 24716
dbc.persoonlijkheidsstoornissen = 36574
dbc.adhd = 25951
dbc.gedrag = 1176
dbc.kindertijdoverig = 1035
dbc.autismespectrum = 9436

display = Object()
display.alarm = ["politie", "hap", "keten"]
display.oordeel = ["verwijs", "uitstroom", "opname"]
display.vergiftigingen = ["vergiftigingen", "tumor"]
display.neurotoxisch = ["neurotoxisch", ]
display.suicide = ["suicide",]
display.pogingen = ["pogingen",]
display.incidenten = ["incidenten",]
display.acuut = ["acuut",]
display.zorgmijder = ["zorgmijder", ]
display.opname = ["ibs", "rm", "vlm", "mvv", "vwm", "ev", "ob", "zb"]

omschrijving = Object()
omschrijving.ibs = "inbewaringstelling"
omschrijving.rm = "rechterlijke machtiging"
omschrijving.vlm = "voorlopige rechterlijke machtiging"
omschrijving.mvv = "machtiging voortgezet verblijf"
omschrijving.vwm = "voorwaardelijke rechterlijke machtiging"
omschrijving.mev = "machtiging eigen verzoek"
omschrijving.zb = "zelfbinding"
omschrijving.ob = "observatie"

urls = Object()
urls.IBS = "http://www.tijdschriftvoorpsychiatrie.nl/assets/articles/57-2015-4-artikel-broer.pdf"
urls.RM = "http://www.tijdschriftvoorpsychiatrie.nl/assets/articles/57-2015-4-artikel-broer.pdf"
urls.VM = "http://www.tijdschriftvoorpsychiatrie.nl/assets/articles/57-2015-4-artikel-broer.pdf"
urls.MVV = "http://www.tijdschriftvoorpsychiatrie.nl/assets/articles/57-2015-4-artikel-broer.pdf"
urls.VW = "http://www.tijdschriftvoorpsychiatrie.nl/assets/articles/57-2015-4-artikel-broer.pdf"
urls.MEV = "http://www.tijdschriftvoorpsychiatrie.nl/assets/articles/57-2015-4-artikel-broer.pdf"
urls.ZB = "http://www.tijdschriftvoorpsychiatrie.nl/assets/articles/57-2015-4-artikel-broer.pdf"
urls.OB = "http://www.tijdschriftvoorpsychiatrie.nl/assets/articles/57-2015-4-artikel-broer.pdf"
urls.opname = "http://www.tijdschriftvoorpsychiatrie.nl/issues/434/articles/8318"
urls.crisis = "http://www.rijksoverheid.nl/documenten-en-publicaties/rapporten/2015/02/11/acute-geestelijke-gezondheidszorg-knelpunten-en-verbetervoorstellen-in-de-keten.html"
urls.tuchtrecht = "http://tuchtrecht.overheid.nl/zoeken/resultaat/uitspraak/2014/ECLI_NL_TGZRAMS_2014_94?zaaknummer=2013%2F221&Pagina=1&ItemIndex=1"
urls.suicide = "http://www.cbs.nl/nl-NL/menu/themas/bevolking/publicaties/artikelen/archief/2014/2014-4204-wm.htm"
urls.pogingen = "http://www.veiligezorgiederszorg.nl/speerpunt-suicide/factsheet-trimbos-suicide.pdf"
urls.incident = "https://www.wodc.nl/onderzoeksdatabase/2337-de-effectiviteit-van-de-politiele-taakuitvoering-en-de-taken-en-verantwoordelijkheden-van-andere-partijen.aspx"
urls.zorgmijder = "http://www.gezondheidsraad.nl/sites/default/files/samenvatting_noodgedwongen_0.pdf"
urls.acuut = "http://www.gezondheidsraad.nl/sites/default/files/samenvatting_noodgedwongen_0.pdf"
urls.wvggz = "https://www.dwangindezorg.nl/de-toekomst/wetsvoorstellen/wet-verplichte-geestelijke-gezondheidszorg"
urls.politie = "http://www.rijksoverheid.nl/documenten-en-publicaties/rapporten/2015/02/11/acute-geestelijke-gezondheidszorg-knelpunten-en-verbetervoorstellen-in-de-keten.html"
urls.hap = "http://www.rijksoverheid.nl/documenten-en-publicaties/rapporten/2015/02/11/acute-geestelijke-gezondheidszorg-knelpunten-en-verbetervoorstellen-in-de-keten.html"
urls.keten = "http://www.rijksoverheid.nl/documenten-en-publicaties/rapporten/2015/02/11/acute-geestelijke-gezondheidszorg-knelpunten-en-verbetervoorstellen-in-de-keten.html"
urls.verwijs = "http://www.rijksoverheid.nl/documenten-en-publicaties/rapporten/2015/02/11/acute-geestelijke-gezondheidszorg-knelpunten-en-verbetervoorstellen-in-de-keten.html"
urls.uitstroom = "http://www.rijksoverheid.nl/documenten-en-publicaties/rapporten/2015/02/11/acute-geestelijke-gezondheidszorg-knelpunten-en-verbetervoorstellen-in-de-keten.html" 
urls.opnames = "http://www.rijksoverheid.nl/documenten-en-publicaties/rapporten/2015/02/11/acute-geestelijke-gezondheidszorg-knelpunten-en-verbetervoorstellen-in-de-keten.html"
urls.vergifitigingen = "http://www.umcutrecht.nl/getmedia/f9f152e2-8638-4ffc-a05f-fce72f5f416a/NVIC-Jaaroverzicht-2014.pdf.aspx?ext=.pdf"
urls.neurotoxisch = "http://www.umcutrecht.nl/getmedia/f9f152e2-8638-4ffc-a05f-fce72f5f416a/NVIC-Jaaroverzicht-2014.pdf.aspx?ext=.pdf"
urls.incidenten = "http://www.dsp-groep.nl/userfiles/file/Politie%20en%20verwarde%20personen%20_DSP-groep.pdf"
urls.ambulant = "https://www.zorgprismapubliek.nl/informatie-over/geestelijke-gezondheidszorg/row-3/hoeveel-pati%C3%ABnten-worden-behandeld-zonder-opname/"
urls.verslaving = "https://www.zorgprismapubliek.nl/informatie-over/geestelijke-gezondheidszorg/row-2/voor-welke-aandoening-worden-de-meeste-pati%C3%ABnten-opgenomen/"
urls.poh = "https://www.zorgprismapubliek.nl/informatie-over/geestelijke-gezondheidszorg/row-4/hoe-heeft-de-poh-ggz-zich-in-de-afgelopen-jaren-ontwikkeld/"
urls.meds = "https://www.zorgprismapubliek.nl/informatie-over/geestelijke-gezondheidszorg/row-5/welke-geneesmiddelen-worden-het-meest-voorgeschreven-in-de-ggz/"
urls.depressie = "https://www.zorgprismapubliek.nl/informatie-over/geestelijke-gezondheidszorg/row-5/welke-geneesmiddelen-worden-het-meest-voorgeschreven-in-de-ggz/"
urls.angst = "https://www.zorgprismapubliek.nl/informatie-over/geestelijke-gezondheidszorg/row-5/welke-geneesmiddelen-worden-het-meest-voorgeschreven-in-de-ggz/"
urls.schizofrenie = "https://www.zorgprismapubliek.nl/informatie-over/geestelijke-gezondheidszorg/row-5/welke-geneesmiddelen-worden-het-meest-voorgeschreven-in-de-ggz/"
urls.detox = "https://www.jellinek.nl/vraag-antwoord/hoeveel-mensen-zijn-verslaafd-en-hoeveel-zijn-er-in-behandeling/"
urls.verslaafden = "https://www.jellinek.nl/vraag-antwoord/hoeveel-mensen-zijn-verslaafd-en-hoeveel-zijn-er-in-behandeling/"
urls.volwassendoop = ""
urls.arbeidshandicap = "http://www.nationalezorggids.nl/gehandicaptenzorg/nieuws/27841-ruim-100-000-mensen-op-sociale-werkplaats.html"

soort = Object()
soort.alarm = "door patient"
soort.oordeel = "van arts"
soort.neurotoxisch = "van patient"
soort.angst = "van patient"
soort.depressie = "van patient"
soort.schizofrenie = "van patient"
soort.ibs = "door burgemeester"
soort.rm = "door rechter"
soort.vlrm = "door rechter"
soort.mvv = "door rechter"
soort.vwrm = "door rechter"
soort.ev = "door patient"
soort.ob ="door kliniek"
soort.zb = "door patient"
soort.politie = "door agent"
soort.hap = "door huisarts"
soort.keten  = "door spv/psychiater"
soort.verwijs = "door crisisdienst"
soort.uitstroom = "door eigen behandelaar"
soort.suicide = "door patient"
soort.crisis = "van patient"
soort.pogingen = "door patient"
soort.incidenten = "met patient"
soort.acuut = "met patient"
soort.meds = "door patient"
soort.amitriptyline = "door patient"
soort.paroxetine = "door patient"
soort.citalopram = "door patient"
soort.oxazepam = "door patient"
soort.venlafaxine = "door patient"
soort.mirtazapine = "door patient"
soort.quetiapine = "door patient"
soort.diazepam = "door patient"
soort.sertrali = "door patient"
soort.haloperidol = "door patient"
