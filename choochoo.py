import urllib
import json
import logging
import urllib2
import re

from protorpc import messages, remote
from google.appengine.ext import endpoints
from lxml import html

from choo_utils import sottrai, sottostringa


__author__ = 'stefano'

logging.getLogger().setLevel(logging.DEBUG)


class Stazione(messages.Message):
    stazione = messages.StringField(1)


class Treno(messages.Message):
    numero = messages.StringField(1)
    da = messages.StringField(2)
    per = messages.StringField(3)
    orario = messages.StringField(4)
    previsto = messages.StringField(5)
    reale = messages.StringField(6)
    ritardo = messages.StringField(7)


class Treni(messages.Message):
    treni = messages.MessageField(Treno, 1, repeated=True)


@endpoints.api(name='choochoo', version='v1')
class ChooChooApi(remote.Service):
    @endpoints.method(Stazione, Treni,
                      name='ritardo', http_method="POST")
    def ritardo_stazione(self, request):
        data = {}
        logging.debug("stazione %s", request.stazione)
        stazione = request.stazione
        reale = request.stazione
        if "|" in request.stazione:
            reale = stazione.split("|")[1]
            stazione = stazione.split("|")[0]
        if stazione.startswith("S0"):
            data = {"codiceStazione": stazione, 'lang': 'IT'}
        else:
            data = {'stazione': stazione, 'lang': 'IT'}

        url = "http://mobile.viaggiatreno.it/vt_pax_internet/mobile/stazione"
        post_data_encoded = urllib.urlencode(data)
        request = urllib2.Request(url, post_data_encoded)
        f = urllib2.urlopen(request)
        risposta = f.read()
        tree = html.document_fromstring(risposta)
        risultati = []
        bloccorisultati = tree.find_class("bloccorisultato")
        logging.debug("%s", len(bloccorisultati))
        if len(bloccorisultati) == 0:
            selects = tree.findall(".//select")
            if len(selects) > 0:
                for select in selects:
                    # errors = form._errors.setdefault("stazione", ErrorList())
                    options = select.findall(".//option")
                    stazioni = []
                    for option in options:
                        stazione = {}
                        stazione['reale'] = unicode(option.text)
                        stazione['codice'] = unicode(option.get("value"))
                        stazioni.append(stazione)
                    raise endpoints.BadRequestException(json.dumps(stazioni))

            else:
                raise endpoints.NotFoundException()
        else:
            # treni is hasmap
            treni = {}
            for bloccorisultato in bloccorisultati:
                # get the train id
                treno_h2 = bloccorisultato.find(".//h2")
                numero = treno_h2.text
                # if exist retives it, otherwise create a new one
                if numero in treni:
                    treno = treni[numero]
                else:
                    treno = {}
                    treno['numero'] = treno_h2.text
                    # remaining page
                    treni[numero] = treno

                # remove special char (i guess)
                bloccotreno = bloccorisultato.find_class("bloccotreno")[0].text_content().translate(None,
                                                                                                    "\n\r\t")
                bloccotreno = re.sub(' +', ' ', bloccotreno)
                # phrases to remove
                frasi = [('Delle ore', 'orario'), ('Binario Previsto:', 'previsto'), ('Binario Reale:', 'reale')]
                treno['per'] = reale.upper()
                treno['da'] = reale.upper()
                # get from
                if "Per " in bloccotreno:
                    treno['per'] = bloccotreno[len("Per "):bloccotreno.index(frasi[0][0])]
                    bloccotreno = sottrai(bloccotreno, "Per ")
                #    get to
                else:
                    treno['da'] = bloccotreno[len("Da "):bloccotreno.index(frasi[0][0])]
                    bloccotreno = sottrai(bloccotreno, "Da ")
                # remove the phrases
                for i in range(0, len(frasi)):
                    # get the info: orario (expected), previsto, reale
                    if (i + 1) < len(frasi):
                        treno[frasi[i][1]] = sottostringa(bloccotreno, frasi[i][0], (frasi[i + 1][0]))
                    else:
                        # get the delay
                        realeandritardo = sottostringa(bloccotreno, frasi[i][0])
                        if "in orario" in realeandritardo:
                            treno['reale'] = realeandritardo[:realeandritardo.index("in orario")]
                            treno['ritardo'] = "in orario"
                        elif "ritardo" in realeandritardo:
                            treno['reale'] = realeandritardo[:realeandritardo.index("ritardo")]
                            treno['ritardo'] = "ritardo %s" % (
                                realeandritardo[realeandritardo.index("ritardo") + len("ritardo"):])
                    # remove the data.
                    bloccotreno = sottrai(bloccotreno, frasi[i][0])
            treni_t = sorted(treni.values(), key=lambda k: k['orario'])
            # now create the trains
            treni = []
            for treno in treni_t:
                logging.debug(treno)
                treni.append(Treno(numero=treno['numero'].strip(), da=treno['da'].strip(), per=treno['per'].strip(), orario=treno['orario'].strip(),
                                   previsto=treno['previsto'].strip(), reale=treno['reale'].strip(), ritardo=treno['ritardo'].strip()))
            return Treni(treni=treni)


APPLICATION = endpoints.api_server([ChooChooApi])
