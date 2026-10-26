import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.widgets import Button as bouton
from math import *
from random import *

#clients = {'Nom du client':[(position),capacite,(disponibilite temporelle),temps de service]}
#camion = {'Nom du camion':[capacite,vitesse]}

while True:
	print('')
	choix = input("Instances aléatoires (o/n) ? : ")
	if choix == 'o' or choix == 'n':
		break
	else:
		print('Saisie incorrecte.')
if choix == 'o':
	while True:
		N = input("Nombre de clients : ")
		if N.isdigit() and int(N) > 0:
			N = int(N)
			break
		else:
			print('Saisie incorrecte.')
			print('')
	clients, camion = {'Départ':[(randint(-100,100),randint(-100,100)),0,(randint(7,9),randint(17,19)),0]}, {1:[randint(100,1000),randint(20,100)]}
	for i in range(N):
		clients[f'Client {i+1}'] = [(randint(-100,100),randint(-100,100)),randint(50,300),(randint(7,12),randint(14,19)),randint(5,30)]
else:
	clients = {'Départ':[(0,0), 0, (8,18), 0], 'Client 1':[(12, 21), 208, (15,17), 21]}
	camion = {1:[1000, 50]}
	N = len(clients)-1

def creation_chemins(sommets):
	aretes, sommets_nom = [], list(sommets)
	for i in range(len(sommets)):
		if i != len(sommets)-1:
			aretes.append((sommets_nom[i], sommets_nom[i+1]))
		else:
			aretes.append((sommets_nom[i], sommets_nom[0]))
	return aretes

def aretes_couleurs(aretes):
	aretes_couleurs, couleurs, i = [], ['grey', 'orange', 'lightblue', 'lightgreen', 'yellow', 'red', 'cyan', 'pink', 'brown', 'purple', 'black'], -1
	for a, b in aretes:
		if a == 'Départ':
			i += 1
		if i == len(couleurs):
			i = 0
		aretes_couleurs.append(couleurs[i])
	return aretes_couleurs

def client_temps_distance(position_i, position_j, transport):
	distance = sqrt((position_j[0]-position_i[0])**2 + (position_j[1]-position_i[1])**2)
	vitesse = transport[1][1]
	temps = int(distance / vitesse * 60)
	return temps

def aretes_labels(sommets, aretes, transport):
	labels = {}
	for i, j in aretes:
		labels[(i,j)] = f'{client_temps_distance(sommets[i][0], sommets[j][0], transport)}min'
	return labels

def affichage_heures(temps):
	heures_decimal = temps
	heures = int(heures_decimal)
	minutes = str(int((heures_decimal-heures)*60)) + 'min'
	if minutes == '0min':
		minutes = ''
	return f'{heures}h{minutes}'

def infos_data(sommets, transport, etats):
	somme_capacite, somme_dispo_debut, somme_dispo_fin, somme_service = 0, 0, 0, 0
	for sommet, param in sommets.items():
		if sommet != 'Départ':
			somme_capacite += param[1]
			somme_dispo_debut += param[2][0]
			somme_dispo_fin += param[2][1]
			somme_service += param[3]
	print('')
	print(f"	État {etats['numéro']} : {etats['algos'][etats['numéro']]}")
	print(f'Client - Horaires moyenne : {affichage_heures(somme_dispo_debut/N)}-{affichage_heures(somme_dispo_fin/N)}')
	print(f'Client - Capacité q moyenne : {int(somme_capacite/N)}kg')
	print(f'Client - Service moyen : {int(somme_service/N)}min')

def client_temps_total(t_d, temps_service, horaires_i, horaires_j):
	temps_distance, horaires_i, horaires_j = t_d, horaires_i*60, horaires_j*60
	if horaires_j > horaires_i + temps_distance:
		temps_distance = horaires_j - horaires_i
	return temps_distance + temps_service

def infos_cycles(etats, labels, sommets, transport):
	cycles_nbr, temps_cycles, temps_cycle = 0, [], 0
	for arete in etats['historique'][etats['numéro']]:
		temps_cycle += client_temps_total(int(labels[arete].replace("min","")), sommets[arete[0]][3], sommets[arete[0]][2][0], sommets[arete[1]][2][0])
		if arete[0] == 'Départ':
			cycles_nbr += 1
		if arete[1] == 'Départ':
			temps_cycles.append(temps_cycle)
			temps_cycle = 0
	temps = max(temps_cycles)
	if temps < 60:
		temps = str(temps) + 'min'
	else:
		temps = affichage_heures(temps/60)
	if cycles_nbr > 1:
		print(f'{cycles_nbr} camions | Q={transport[1][0]}kg | V={transport[1][1]}km/h')
	else:
		print(f'{cycles_nbr} camion | Q={transport[1][0]}kg | V={transport[1][1]}km/h')
	if N > 1:
		print(f'{temps} pour parcourir les {N} clients.')
	else:
		print(f'{temps} pour atteindre le client.')

def algo_premier(sommets, transport):
	sommets_dico, sommets = {'Départ':sommets['Départ']}, dict(sommets)
	for i in range(len(sommets)-1):
		param1 = sommets.pop(list(sommets_dico)[-1])
		sommets_temps = {}
		for sommet, param2 in sommets.items():
			temps_distance = client_temps_distance(param1[0], param2[0], transport)
			sommets_temps[sommet] = client_temps_total(temps_distance, param2[3], param1[2][0], param2[2][0])
		sommet_temps_min = min(sommets_temps, key=sommets_temps.get)
		sommets_dico[sommet_temps_min] = sommets[sommet_temps_min]
	return sommets_dico

def algo_capacite(sommets, transport):
	sommets_dico, sommets_capacite = dict(sommets), []
	while sommets_dico:
		sommets_dico = algo_premier(sommets_dico, transport)
		capacite_total = 0
		temps_total = 0
		position_i, horaires_i = sommets['Départ'][0], sommets['Départ'][2][0]
		sommets_dico_liste = list(sommets_dico)
		while sommets_dico and capacite_total <= transport[1][0] and sommets['Départ'][2][0]*60 + temps_total + client_temps_distance(sommets['Départ'][0], sommets_dico[sommets_dico_liste[0]][0], transport) <= sommets['Départ'][2][1]*60 and sommets['Départ'][2][0]*60 + temps_total <= sommets_dico[sommets_dico_liste[0]][2][1]*60:
			sommets_dico_liste = list(sommets_dico)
			capacite_total += sommets_dico[sommets_dico_liste[0]][1]
			temps_total += client_temps_total(client_temps_distance(position_i, sommets_dico[sommets_dico_liste[0]][0], transport), sommets_dico[sommets_dico_liste[0]][3], horaires_i, sommets_dico[sommets_dico_liste[0]][2][0])
			if capacite_total <= transport[1][0] and sommets['Départ'][2][0]*60 + temps_total + client_temps_distance(sommets['Départ'][0], sommets_dico[sommets_dico_liste[0]][0], transport) <= sommets['Départ'][2][1]*60 and sommets['Départ'][2][0]*60 + temps_total <= sommets_dico[sommets_dico_liste[0]][2][1]*60:
				sommets_capacite.append(sommets_dico_liste[0])
				param = sommets_dico.pop(sommets_dico_liste[0])
				position_i, horaires_i = param[0], param[2][0]
				sommets_dico_liste = list(sommets_dico)
		if sommets_dico:
			sommets_dico = {'Départ':sommets['Départ'], **sommets_dico}
	return sommets_capacite

def simulation(sommets, aretes, transport):
	graphe, sommet_labels, couleur, etats = nx.DiGraph(), {}, [], {'historique':[aretes], 'numéro':0, 'algos':['Aucun', 'Voisins proches + Horaires', 'Capacité + Horaires']}

	for sommet, param in sommets.items():
		graphe.add_node(sommet, position=param[0])

	for sommet in graphe.nodes():
		if sommet == 'Départ':
			infos = f'{sommets[sommet][2][0]}h-{sommets[sommet][2][1]}h\n'
			infos += f'Q={transport[1][0]}kg\n'
			infos += f'V={transport[1][1]}km/h'
			couleur.append('lightgreen')
		else:
			infos = f'{sommets[sommet][2][0]}h-{sommets[sommet][2][1]}h\n'
			infos += f'q={sommets[sommet][1]}kg\n'
			infos += f'service:{sommets[sommet][3]}min'
			couleur.append('skyblue')
		sommet_labels[sommet] = f"{sommet}\n{infos}"

	def update():
		etat_actuel = etats['historique'][etats['numéro']]
		aretes_labels_temps = aretes_labels(sommets, etat_actuel, transport)
		dessin.clear()
		nx.draw_networkx_nodes(graphe, position, node_size=700, node_color=couleur, ax=dessin)
		nx.draw_networkx_labels(graphe, position, labels=sommet_labels, font_size=9, ax=dessin)
		nx.draw_networkx_edges(graphe, position, edgelist=etat_actuel, width=2, edge_color=aretes_couleurs(etat_actuel), arrowstyle='->', arrowsize=20, node_size=700, ax=dessin)
		nx.draw_networkx_edge_labels(graphe, position, edge_labels=aretes_labels_temps, font_size=8, label_pos=0.3, ax=dessin)
		dessin.set_title(f"Graphe orienté et pondéré - État {etats['numéro']} : {etats['algos'][etats['numéro']]}", fontsize=14)
		dessin.axis('off')
		fenetre.canvas.draw_idle()
		infos_data(sommets, transport, etats)
		infos_cycles(etats, aretes_labels_temps, sommets, transport)

	def precedent(event):
		if etats['numéro'] > 0:
			etats['numéro'] -= 1
			update()

	def suivant(event):
		if etats['numéro'] < len(etats['algos'])-1:
			if etats['numéro'] == len(etats['historique'])-1:
				if etats['numéro'] == 0:
					new_etat = creation_chemins(algo_premier(sommets, transport))
				elif etats['numéro'] == 1:
					new_etat = creation_chemins(algo_capacite(sommets, transport))
				etats['historique'].append(new_etat)
			etats['numéro'] += 1
			update()

	fenetre, dessin = plt.subplots(figsize=(9,7))
	position = nx.get_node_attributes(graphe, 'position')
	ax_precedent = fenetre.add_axes([0.30, 0.02, 0.18, 0.06])
	ax_suivant = fenetre.add_axes([0.52, 0.02, 0.18, 0.06])
	bouton_precedent = bouton(ax_precedent, '← Précédent')
	bouton_suivant = bouton(ax_suivant, 'Suivant →')
	bouton_precedent.on_clicked(precedent)
	bouton_suivant.on_clicked(suivant)
	
	update()
	plt.show()

routes = creation_chemins(clients)
simulation(clients, routes, camion)