import femm
import os

corrente = 2
espiras = 200

profundidade = 5
largura = 5
altura = 25
comprimento = 20

core = 'M-14'
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

# Desenhando o core
femm.mi_drawrectangle(1,0,1+comprimento,altura)
femm.mi_drawrectangle(1+largura,largura,1+comprimento-largura,altura-largura)

# Marcando o core
femm.mi_addblocklabel(2,2)
femm.mi_selectlabel(2,2)
femm.mi_setblockprop(core,0,0,"",0,0,1)
femm.mi_clearselected()

# Desenhando a bobina (duas partes)
femm.mi_drawrectangle(0,largura+1,1,altura-largura-1)
femm.mi_drawrectangle(1+largura,largura+1,2+largura,altura-largura-1)

# Definindo o circuito de alimentacao
femm.mi_addcircprop('Alimentacao',corrente,1)

# Marcando as bobinas (lado com espiras 'negativas' e 'positivas')
femm.mi_addblocklabel(0.5,altura/2)
femm.mi_selectlabel(0.5,altura/2)
femm.mi_setblockprop(cobre,0,0,'Alimentacao',0,0,-espiras)
femm.mi_clearselected()

femm.mi_addblocklabel(1.5 + largura,altura/2)
femm.mi_selectlabel(1.5 + largura,altura/2)
femm.mi_setblockprop(cobre,0,0,'Alimentacao',0,0,espiras)
femm.mi_clearselected()

# Marcando regiões com ar
femm.mi_addblocklabel(comprimento+1, altura+1)
femm.mi_addblocklabel(comprimento/2,altura/2)
femm.mi_selectlabel(comprimento+1, altura+1)
femm.mi_selectlabel(comprimento/2,altura/2)
femm.mi_setblockprop(fluido,0,0,"",0,0,1)
femm.mi_clearselected()

# Criando 'encapsulamento'
femm.mi_makeABC()

# Ajustando o zoom e salvando a simulacao
femm.mi_zoomnatural()
femm.mi_saveas("simulacao 2-2.fem")

# Calculando a solucao e mostrando ela
femm.mi_analyse("simulacao 2-2.fem")
femm.mi_loadsolution()

# Ajustando a solucao para melhor visualizacao
femm.mo_showdensityplot(1,0,5e-2,0,"bmag")

# Obtendo a indutancia da bobina
correnteCircuito, tensaoCircuito, fluxoCircuito = femm.mo_getcircuitproperties('Alimentacao')
indutancia = fluxoCircuito/corrente
print("Indutancia (uH) = ", indutancia*1e6)

# Obtendo a densidade de fluxo no core
vetorB = femm.mo_getb(1+largura/2,altura/2)
moduloB = (vetorB[0]**2+vetorB[1]**2)**0.5
print(f'Vetor da densidade de fluxo: {vetorB}')
print(f'Modulo da densidade de fluxo: B = {moduloB}')

# Obtendo a intensidade de fluxo no core
vetorH = femm.mo_geth(1+largura/2,altura/2)
moduloH = (vetorH[0]**2+vetorH[1]**2)**0.5
print(f'Vetor da intensidade de fluxo: {vetorH}')
print(f'Modulo da intensidade de fluxo: H = {moduloH}')

os.system('pause')