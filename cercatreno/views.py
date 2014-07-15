# Create your views here.
import logging
import re

from django.core.urlresolvers import reverse
from django.template.context import RequestContext
from lxml import html
from django.shortcuts import render, redirect, render_to_response
from django.forms.util import ErrorList

from cercatreno.forms import RitardiForm, StazioneForm, StazioneFormChoices
import requests


log = logging.getLogger(__name__)



#
#
# def percorso(request):
#     if request.method == "GET":
#         form = RitardiForm()
#     else:
#         form = RitardiForm(request.POST)
#         if form.is_valid():
#             s_partenza = form.cleaned_data['partenza']
#             s_arrivo = form.cleaned_data['arrivo']
#             data = {'partenza': s_partenza, 'arrivo': s_arrivo, 'lang': 'IT',
#                     'swArrivoTxt': '1a',
#                     'swPartenzaTxt': '1p'}
#
#             treni = requests.post("http://mobile.viaggiatreno.it/vt_pax_internet/mobile/tragitto", data=data)
#             log.debug("response is %s", treni.status_code)
#             # log.debug("%s",treni.text)
#             tree = html.document_fromstring(treni.text.encode('utf-8'))
#             risultati = []
#             bloccorisultati = tree.find_class("bloccorisultato")
#             log.debug("%s", len(bloccorisultati))
#             if len(bloccorisultati) == 0:
#                 selects = tree.findall(".//select")
#                 if len(selects) > 0:
#                     for select in selects:
#                         field = select.get('name')
#                         errors = form._errors.setdefault(field, ErrorList())
#                         options = select.findall(".//option")
#                         stazioni = []
#                         for option in options:
#                             stazione ={}
#                             stazione['name']=option.text
#                             stazione['code']=option.get("value")
#                             stazioni.append(stazione)
#                         log.debug("stazioni %s", stazioni)
#                         log.debug("create stazioenFormCHoices")
#                         form = StazioneFormChoices(stazioni=stazioni)
#
#
#                         errors.append(u"Stazione non trovata: %s" % stazioni)
#                 else:
#                     return render_to_response('noresults.html',
#                                               {'treni': [], 'partenza': s_partenza, 'arrivo': s_arrivo},
#                                               context_instance=RequestContext(request))
#             else:
#                 for bloccorisultato in bloccorisultati:
#                     risultato = {}
#                     treno = bloccorisultato.find(".//h2")
#                     risultato['treno'] = treno.text
#                     i = 0
#                     partenza = {}
#                     arrivo = {}
#                     for bloccotreno in bloccorisultato.find_class("bloccotreno"):
#
#                         trenostazione = bloccotreno.find_class("trenostazione")
#                         # if (len(trenostazione) > 0):
#                         #     if i == 0:
#                         #         partenza['stazione'] = trenostazione[0].text
#                         #     else:
#                         #         arrivo["stazione"] = trenostazione[0].text
#                         # log.debug(trenostazione[0].text)
#                         # log.debug("%s",len(trenostazione))
#                         # log.debug("%s",bloccotreno.find_class("trenostazione")[0].text_content)
#                         trenoorario = bloccotreno.find_class("trenoorario")
#                         if (len(trenoorario) > 0):
#                             if i == 0:
#                                 partenza['orario'] = trenoorario[0].text
#                             else:
#                                 arrivo["orario"] = trenoorario[0].text
#                         else:
#                             risultato['note'] = bloccotreno.text.strip()
#                             log.debug(bloccotreno.text.strip())
#                         i = i + 1
#                     risultato['partenza'] = partenza
#                     risultato['arrivo'] = arrivo
#                     risultati.append(risultato)
#                 log.debug('risultati %s', risultati)
#                 # log.debug("%s",bloccotreno.find_class("trenoorario")[0].text_content)
#                 # log.debug("res %s",risultato.text_content)
#                 return render_to_response('list.html',
#                                           {'treni': risultati, 'partenza': s_partenza, 'arrivo': s_arrivo},
#                                           context_instance=RequestContext(request))
#
#     return render(request, 'form.html', {
#         'form': form,
#     })


    # user = request.user
    # log.debug("django %s",user)
    # user = users.get_current_user()
    # log.debug("appengine %s",user)
    #
    # user = request.user
    # if user.is_anonymous():
    #     user,created = User.objects.get_or_insert(username="Anonymous")
    # greeting, created = Greeting.objects.get_or_create(author=request.user)
    # if created:
    #     log.debug("created")
    #     greeting.content="created %s"%datetime.now
    # greeting.save()
    # http = urllib3.PoolManager()
    # response = http.get('someurl')/

    # return HttpResponse("%s"%greeting.content)
    # greeting = Greeting.get_or_insert("stefano",author=user,content="ciao")


def sottrai(da, cosa):
    return da[(da.index(cosa) + len(cosa)):]


def sottostringa(da, inizio, fine=None):
    if fine:
        return da[(da.index(inizio) + len(inizio)):da.index(fine)]
    else:
        return da[(da.index(inizio) + len(inizio)):]


#questa e' quella giusta.
def stazione(request):
    if request.method == "GET" and not request.GET.get("stazione",None):
        form = StazioneForm()
    else:
        # s_stazione = request.GET.get("stazione",None)
        # log.debug("stazione %s",s_stazione)
        form = StazioneForm(request.GET)
        log.debug("is form none %s",form==None)

        # if not s_stazione:
        #     # form = StazioneForm(initial={'stazione':stazione})
        # # else:
        if form.is_valid():
            s_stazione = form.cleaned_data['stazione'].upper()
            log.debug("form valid : %s ",form.is_valid())
            # if form.is_valid():

            data={}
            if s_stazione.startswith("S0"):
                data={"codiceStazione":s_stazione,'lang': 'IT'}
            else:
                data = {'stazione': s_stazione, 'lang': 'IT'}

            treni = requests.post("http://mobile.viaggiatreno.it/vt_pax_internet/mobile/stazione", data=data)
            log.debug("response is %s", treni.status_code)
            # log.debug("%s",treni.text)
            tree = html.document_fromstring(treni.text.encode('utf-8'))
            risultati = []
            bloccorisultati = tree.find_class("bloccorisultato")
            log.debug("%s", len(bloccorisultati))
            if len(bloccorisultati) == 0:
                selects = tree.findall(".//select")
                if len(selects) > 0:
                    for select in selects:
                        # errors = form._errors.setdefault("stazione", ErrorList())
                        options = select.findall(".//option")
                        stazioni = []
                        for option in options:
                            stazione=(unicode(option.get("value")),unicode(option.text))
                            stazioni.append(stazione)
                        log.debug("stazioni %s", stazioni)
                        log.debug("create stazioenFormCHoices")
                        form = StazioneFormChoices(stazioni=stazioni)

                else:
                    return render_to_response('noresults.html',
                                              {'stazione': s_stazione},
                                              context_instance=RequestContext(request))
            else:
                treni = {}
                for bloccorisultato in bloccorisultati:

                    treno_h2 = bloccorisultato.find(".//h2")
                    numero = treno_h2.text
                    if numero in treni:
                        treno = treni[numero]
                    else:
                        treno={}
                        treno['numero'] = treno_h2.text
                        treni[numero]=treno
                    bloccotreno = bloccorisultato.find_class("bloccotreno")[0].text_content().translate(None,
                                                                                                        "\n\r\t")
                    bloccotreno = re.sub(' +', ' ', bloccotreno)
                    frasi = [('Delle ore','orario'), ('Binario Previsto:','previsto'), ('Binario Reale:','reale')]
                    if "Per " in bloccotreno:
                        treno['per']=bloccotreno[len("Per "):bloccotreno.index(frasi[0][0])]

                        bloccotreno = sottrai(bloccotreno, "Per ")
                    else:
                        treno['da']=bloccotreno[len("Da "):bloccotreno.index(frasi[0][0])]
                        bloccotreno = sottrai(bloccotreno, "Da ")

                    for i in range(0, len(frasi)):
                        if (i + 1) < len(frasi):
                            treno[frasi[i][1]] = sottostringa(bloccotreno, frasi[i][0], (frasi[i + 1][0]))
                        else:
                            realeandritardo = sottostringa(bloccotreno, frasi[i][0])
                            if "in orario" in realeandritardo:
                                treno['reale'] = realeandritardo[:realeandritardo.index("in orario")]
                                treno['ritardo'] = "in orario"
                            elif "ritardo" in realeandritardo:
                                treno['reale'] = realeandritardo[:realeandritardo.index("ritardo")]
                                treno['ritardo'] = "ritardo %s" % (
                                realeandritardo[realeandritardo.index("ritardo") + len("ritardo"):])
                            # print ("treno[frasi[i]]=%s"%treno[frasi[i]])
                        bloccotreno = sottrai(bloccotreno, frasi[i][0])
                treni_t =  sorted(treni.values(), key=lambda k: k['orario'])

                return render_to_response('list_stazione.html',
                                          {'treni': treni_t, 'stazione': s_stazione},
                                          context_instance=RequestContext(request))

    return render(request, 'form.html', {
        'form': form,
    })