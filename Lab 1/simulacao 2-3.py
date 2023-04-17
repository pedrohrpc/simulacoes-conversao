import femm
import os

corrente = 2.5
espiras = 800

profundidade = 3
lg = 3.3953
largura = 2
altura = 12 + largura + lg
comprimento = 9 + largura

core = 'M-14'
coreInf = 'inf'
fluido = 'Air'
cobre = '0.5mm'

# Criando documento novo
femm.openfemm()
femm.newdocument(0)
femm.mi_probdef(0,'centimeters','planar',1e-8,profundidade)

# Definindo materiais
femm.mi_getmaterial(core)
femm.mi_getmaterial(fluido)
femm.mi_getmaterial(cobre)

'''femm.mi_addmaterial(coreInf,float('inf'),float('inf'))
femm.mi_getmaterial(coreInf)'''

# Desenhando o core
femm.mi_drawrectangle(1,0,1+comprimento,altura)
femm.mi_drawrectangle(1+largura,0+largura,1+comprimento-largura,altura-largura)

# Marcando o core
if lg>0:
    femm.mi_addblocklabel(2,altura-1)
    femm.mi_selectlabel(2,altura-1)

femm.mi_addblocklabel(2,2)
femm.mi_selectlabel(2,2)

femm.mi_setblockprop(core,0,0,"",0,0,1)
femm.mi_clearselected()

if lg>0:
    # Desenhando entreferro
    femm.mi_drawrectangle(1,altura-largura-lg,1+largura,altura-largura)
    femm.mi_drawrectangle(1+comprimento-largura,altura-largura-lg,1+comprimento,altura-largura)

    # Deletando fronteiras
    femm.mi_selectsegment(1,altura-largura-lg/2)
    femm.mi_selectsegment(1+largura,altura-largura-lg/2)
    femm.mi_selectsegment(1+comprimento-largura,altura-largura-lg/2)
    femm.mi_selectsegment(1+comprimento+largura,altura-largura-lg/2)
    femm.mi_deleteselectedsegments()
    femm.mi_clearselected()

# Desenhando a bobina (duas partes)
femm.mi_drawrectangle(0,largura+1,1,altura-largura-1-lg)
femm.mi_drawrectangle(1+largura,largura+1,2+largura,altura-largura-1-lg)

# Definindo o circuito de alimentacao
femm.mi_addcircprop('Alimentacao',corrente,1)

# Marcando as bobinas (lado com espiras 'negativas' e 'positivas')
femm.mi_addblocklabel(0.5,altura/2)
femm.mi_selectlabel(0.5,altura/2)
femm.mi_setblockprop(cobre,0,0,'Alimentacao',0,0,espiras)
femm.mi_clearselected()

femm.mi_addblocklabel(1.5+largura,altura/2)
femm.mi_selectlabel(1.5+ largura,altura/2)
femm.mi_setblockprop(cobre,0,0,'Alimentacao',0,0,-espiras)
femm.mi_clearselected()

# Marcando regiões com ar
if lg==0:
    femm.mi_addblocklabel(comprimento+2,altura+2)
    femm.mi_selectlabel(comprimento+2,altura+2)
femm.mi_addblocklabel(7,7)
femm.mi_selectlabel(7,7)
femm.mi_setblockprop(fluido,0,0,"",0,0,1)
femm.mi_clearselected()


# Criando 'encapsulamento'
femm.mi_makeABC()

# Ajustando o zoom e salvando a simulacao

femm.mi_zoomnatural()

femm.mi_saveas("simulacao 2-3.fem")

# Calculando a solucao e mostrando ela
femm.mi_analyse("simulacao 2-3.fem")
femm.mi_loadsolution()

# Ajustando a solucao para melhor visualizacao
femm.mo_showdensityplot(1,0,5e-2,0,"bmag")

# Obtendo a indutancia da bobina
correnteCircuito, tensaoCircuito, fluxoCircuito = femm.mo_getcircuitproperties('Alimentacao')
indutancia = fluxoCircuito/corrente
print("Indutancia (uH) = ", indutancia*1e6)

# Obtendo a densidade de fluxo no core
print('Medicoes do core')
vetorB = femm.mo_getb(1+largura/2,altura/2)
moduloB = (vetorB[0]**2+vetorB[1]**2)**0.5
print(f'Vetor da densidade de fluxo: {vetorB}')
print(f'Modulo da densidade de fluxo: B = {moduloB} T')

# Obtendo a intensidade de fluxo no core
vetorH = femm.mo_geth(1+largura/2,altura/2)
moduloH = (vetorH[0]**2+vetorH[1]**2)**0.5
print(f'Vetor da intensidade de campo: {vetorH}')
print(f'Modulo da intensidade de campo: H = {moduloH} h')

if lg>0:
# Obtendo a densidade de fluxo no entreferro
    print('Medicoes do entreferro')
    vetorB = femm.mo_getb(1+largura/2,altura-largura-lg/2)
    moduloB = (vetorB[0]**2+vetorB[1]**2)**0.5
    print(f'Vetor da densidade de fluxo: {vetorB}')
    print(f'Modulo da densidade de fluxo: B = {moduloB} T')

    # Obtendo a intensidade de fluxo no entreferro
    vetorH = femm.mo_geth(1+largura/2,altura-largura-lg/2)
    moduloH = (vetorH[0]**2+vetorH[1]**2)**0.5
    print(f'Vetor da intensidade de campo: {vetorH}')
    print(f'Modulo da intensidade de campo: H = {moduloH} h')


os.system('pause')