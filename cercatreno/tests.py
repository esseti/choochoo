"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
import pprint
from lxml import html


s_html = """<div class='bloccorisultato'>
   <h2>REG 2261</h2>
   ciao
   <div class='bloccotreno'>
      Per <strong>BOLOGNA C.LE</strong><br/>
      Delle ore <strong>15:10</strong><br/>
      Binario
      Previsto:
      2
      <br>
      Binario
      Reale:
    <strong>2</strong>
      <br>
      <img src='../images/pallinoRit0.png'/>
      in orario
   </div>
   <a href='scheda?numeroTreno=2261&codLocOrig=S02001&tipoRicerca=stazione' > Vedi scheda</a>
</div>"""

def sottrai(da,cosa):
    return da[(da.index(cosa)+len(cosa)):]

def sottostringa(da,inizio, fine=None):
    if fine:
        return da[(da.index(inizio)+len(inizio)):da.index(fine)]
    else:
        return da[(da.index(inizio)+len(inizio)):]

class orderDic():
    d={}
    d['a']={'n':12,'a':'a'}
    d['b']={'n':1,'a':'a'}
    d['c']={'n':15,'a':'a'}
    print newlist
    # sorted_x = sorted(x.iteritems(), key=operator.itemgetter(1))


class TestHTMLParsing():
    tree = html.document_fromstring(s_html.encode('utf-8'))
    bloccorisultati = tree.find_class("bloccorisultato")

    partenze=[]
    arrivi=[]
    treni={'partenze':partenze,'arrivi':arrivi}
    for bloccorisultato in bloccorisultati:
        treno={}
        treno_h2 = bloccorisultato.find(".//h2")
        treno['numero']=treno_h2.text
        bloccotreno = bloccorisultato.find_class("bloccotreno")[0].text_content().translate(None,"\n\r ' ' ")
        frasi=['Delleore','BinarioPrevisto:','BinarioReale:']
        if "Per" in bloccotreno:
            partenze.append(treno)
            bloccotreno=sottrai(bloccotreno,"Per")
        else:
            arrivi.append(treno)
            bloccotreno=sottrai(bloccotreno,"Da")
        treno['stazione']=bloccotreno[:bloccotreno.index(frasi[0])]
        for i  in range(0,len(frasi)):
            if (i+1)<len(frasi):
                treno[frasi[i]]=sottostringa(bloccotreno,frasi[i],(frasi[i+1]))
            else:
                realeandritardo=sottostringa(bloccotreno,frasi[i])
                if "inorario" in realeandritardo:
                    treno['BinarioReale']=realeandritardo[:realeandritardo.index("inorario")]
                    treno['ritardo']="in orario"
                elif "ritardo" in realeandritardo:
                    treno['BinarioReale']=realeandritardo[:realeandritardo.index("ritardo")]
                    treno['ritardo']="ritardo %s"%(realeandritardo[realeandritardo.index("ritardo")+len("ritardo"):])
            # print ("treno[frasi[i]]=%s"%treno[frasi[i]])
            bloccotreno=sottrai(bloccotreno,frasi[i])
        pprint.pprint(treni)

if __name__ == "__main__":
    orderDic()
