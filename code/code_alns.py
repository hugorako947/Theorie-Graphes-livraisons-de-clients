import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.widgets import Button as bouton
from math import *
from random import *

#clients = {'Nom du client':[(position),capacite,(disponibilite temporelle),temps de service]}
#camion = {'Nom du camion':[capacite,vitesse]}

print('''
Tapez 'q' pour quitter.''')

choix = ''
while choix != 'q':
	print('')
	choix = input("Instances aléatoires (o/n) ? : ")
	if choix == 'o' or choix == 'n':
		break
	elif choix == 'q':
		quit()
	else:
		print('Saisie incorrecte.')
if choix == 'o':
	N = ''
	while N != 'q':
		N = input("Nombre de clients : ")
		if N.isdigit() and int(N) > 0:
			N = int(N)
			break
		elif N == 'q':
			quit()
		else:
			print('Saisie incorrecte.')
			print('')
	if N != 'q':
		clients, camion = {'Départ':[(randint(-100,100),randint(-100,100)),0,(randint(7,9),randint(17,19)),0]}, {1:[randint(100,1000),randint(20,100)]}
		for i in range(N):
			clients[f'Client {i+1}'] = [(randint(-100,100),randint(-100,100)),randint(50,300),(randint(7,12),randint(14,19)),randint(5,30)]
else:
	clients = {'Départ':[(0,0), 0, (8,18), 0],
		   'Client 1':[(20,15), 100, (8,9), 20],
		   'Client 2':[(10,0), 100, (8,18), 20],
		   'Client 3':[(0,15), 100, (8,18), 20],
		   'Client 4':[(20,0), 100, (8,18), 20]}
	camion = {1:[1000, 60]}
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
	print(f'CesiCDP - Horaires : {sommets['Départ'][2][0]}h-{sommets['Départ'][2][1]}h')
	print(f'Client - Horaires moyenne : {affichage_heures(somme_dispo_debut/N)}-{affichage_heures(somme_dispo_fin/N)}')
	print(f'Client - Capacité q moyenne : {int(somme_capacite/N)}kg')
	print(f'Client - Service moyen : {int(somme_service/N)}min')

def client_temps_total(t_d, temps_service, horaires_i, horaires_j):
	temps_distance, horaires_i, horaires_j = t_d, horaires_i*60, horaires_j*60
	if horaires_j > horaires_i + temps_distance:
		temps_distance = horaires_j - horaires_i
	return temps_distance + temps_service

def timeline_cycle(route, sommets, T, depot='Départ'):
	# Simule la tournée minute par minute -> (duree_horloge, faisable).
	t, prec, faisable = sommets[depot][2][0]*60, depot, True
	for c in route:
		arrivee = t + T[prec][c]
		debut = max(arrivee, sommets[c][2][0]*60)
		if debut + sommets[c][3] > sommets[c][2][1]*60:
			faisable = False
		t = debut + sommets[c][3]
		prec = c
	retour = t + T[prec][depot]
	if retour > sommets[depot][2][1]*60:
		faisable = False
	return retour - sommets[depot][2][0]*60, faisable

def infos_cycles(etats, labels, sommets, transport):
	T = matrice_temps(sommets, transport)
	depot_ouv, depot_ferm = sommets['Départ'][2][0], sommets['Départ'][2][1]
	cycles, cycle = [], []
	for a, b in etats['historique'][etats['numéro']]:
		if a == 'Départ':
			cycle = []
		if b != 'Départ':
			cycle.append(b)
		else:
			cycles.append(cycle)
	cycles_nbr = len(cycles)
	durees, hors_horaires = [], 0
	for cl in cycles:
		duree, faisable = timeline_cycle(cl, sommets, T)
		durees.append(duree)
		if not faisable:
			hors_horaires += 1
	temps = max(durees) if durees else 0
	temps_txt = str(temps) + 'min' if temps < 60 else affichage_heures(temps/60)
	if cycles_nbr > 1:
		print(f'{cycles_nbr} camions | Q={transport[1][0]}kg | V={transport[1][1]}km/h')
	else:
		print(f'{cycles_nbr} camion | Q={transport[1][0]}kg | V={transport[1][1]}km/h')
	if N > 1:
		print(f'{temps_txt} pour parcourir les {N} clients.')
	else:
		print(f'{temps_txt} pour atteindre le client.')
	if hors_horaires == 0:
		print(f'Tournées dans les horaires CesiCDP ({depot_ouv}h-{depot_ferm}h).')
	else:
		print(f'ATTENTION : {hors_horaires} tournée(s) hors des horaires CesiCDP ({depot_ouv}h-{depot_ferm}h).')

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
		nombre_avant = len(sommets_capacite)
		while sommets_dico and capacite_total <= transport[1][0] and sommets['Départ'][2][0]*60 + temps_total + client_temps_distance(sommets['Départ'][0], sommets_dico[sommets_dico_liste[0]][0], transport) <= sommets['Départ'][2][1]*60 and sommets['Départ'][2][0]*60 + temps_total <= sommets_dico[sommets_dico_liste[0]][2][1]*60:
			sommets_dico_liste = list(sommets_dico)
			capacite_total += sommets_dico[sommets_dico_liste[0]][1]
			temps_total += client_temps_total(client_temps_distance(position_i, sommets_dico[sommets_dico_liste[0]][0], transport), sommets_dico[sommets_dico_liste[0]][3], horaires_i, sommets_dico[sommets_dico_liste[0]][2][0])
			if capacite_total <= transport[1][0] and sommets['Départ'][2][0]*60 + temps_total + client_temps_distance(sommets['Départ'][0], sommets_dico[sommets_dico_liste[0]][0], transport) <= sommets['Départ'][2][1]*60 and sommets['Départ'][2][0]*60 + temps_total <= sommets_dico[sommets_dico_liste[0]][2][1]*60:
				sommets_capacite.append(sommets_dico_liste[0])
				param = sommets_dico.pop(sommets_dico_liste[0])
				position_i, horaires_i = param[0], param[2][0]
				sommets_dico_liste = list(sommets_dico)
		if len(sommets_capacite) - nombre_avant <= 1 and any(s != 'Départ' for s in sommets_dico):
			if sommets_capacite and sommets_capacite[-1] == 'Départ':
				sommets_capacite.pop()
			client_impossible = next(s for s in sommets_dico if s != 'Départ')
			print(f"{client_impossible} ne peut pas être servi (q={sommets_dico[client_impossible][1]}kg > Q={transport[1][0]}kg, ou fenêtre horaire inatteignable) : client ignoré.")
			del sommets_dico[client_impossible]
		if sommets_dico:
			sommets_dico = {'Départ':sommets['Départ'], **sommets_dico}
	return sommets_capacite

# ===================== ALNS =====================

# ---------------------------------------------------------------------------
# Modèle : mêmes données que le projet.
#   clients[nom] = [(x,y), q, (ouverture, fermeture), service]
#   camion[1]    = [Q, V]
# Temps de trajet (min) = int( distance_euclidienne / V * 60 ), comme dans le code.
# ---------------------------------------------------------------------------

PENALITE_CAMION = 300   # minutes "facturées" par camion utilisé : pousse à en utiliser moins


def matrice_temps(sommets, transport):
	vitesse, noms = transport[1][1], list(sommets)
	T = {i: {} for i in noms}
	for a in range(len(noms)):
		i = noms[a]
		T[i][i] = 0
		for b in range(a + 1, len(noms)):
			j = noms[b]
			(xi, yi), (xj, yj) = sommets[i][0], sommets[j][0]
			T[i][j] = T[j][i] = int(hypot(xj - xi, yj - yi) / vitesse * 60)
	return T


def evaluer_route(route, sommets, T, Q, depot='Départ'):
	"""Simule la tournée minute par minute.
	Retourne (faisable, temps_trajet, instant_retour).
	Convention (identique à algo_capacite) : le service doit être TERMINÉ avant
	la fermeture du client ; retour au dépôt avant sa fermeture ; charge <= Q."""
	if not route:
		return True, 0, sommets[depot][2][0] * 60
	charge = sum(sommets[c][1] for c in route)
	if charge > Q:
		return False, None, None
	depot_ouv, depot_ferm = sommets[depot][2][0] * 60, sommets[depot][2][1] * 60
	t, prec, temps_trajet = depot_ouv, depot, 0
	for c in route:
		temps_trajet += T[prec][c]
		arrivee = t + T[prec][c]
		ouv, ferm, service = sommets[c][2][0] * 60, sommets[c][2][1] * 60, sommets[c][3]
		debut = max(arrivee, ouv)          # on attend l'ouverture si on arrive trop tôt
		if debut + service > ferm:         # le service doit finir avant la fermeture
			return False, None, None
		t = debut + service
		prec = c
	temps_trajet += T[prec][depot]
	retour = t + T[prec][depot]
	if retour > depot_ferm:
		return False, None, None
	return True, temps_trajet, retour


def cout(routes, sommets, T, Q):
	total, nb = 0, 0
	for r in routes:
		if r:
			ok, tt, _ = evaluer_route(r, sommets, T, Q)
			if not ok:
				return inf
			total += tt
			nb += 1
	return total + PENALITE_CAMION * nb


def clients_placables(sommets, transport, T):
	"""Clients qu'un camion peut servir seuls (sinon q>Q ou fenêtre inatteignable)."""
	Q = transport[1][0]
	ok_list, ko_list = [], []
	for c in sommets:
		if c == 'Départ':
			continue
		faisable, _, _ = evaluer_route([c], sommets, T, Q)
		(ok_list if faisable else ko_list).append(c)
	return ok_list, ko_list


# ---------------------------------------------------------------------------
# Insertion : liste des positions faisables pour un client, avec leur surcoût.
# Une option = (surcout, indice_route | None, position). None => ouvrir une route.
# ---------------------------------------------------------------------------

def options_insertion(client, routes, sommets, T, Q):
	opts = []
	for ri, r in enumerate(routes):
		_, base_tt, _ = evaluer_route(r, sommets, T, Q)
		for p in range(len(r) + 1):
			ok, tt, _ = evaluer_route(r[:p] + [client] + r[p:], sommets, T, Q)
			if ok:
				opts.append((tt - base_tt, ri, p))                       # pas de camion en plus
	opts.append((T['Départ'][client] + T[client]['Départ'] + PENALITE_CAMION, None, 0))  # route neuve
	return opts


def reparation_gloutonne(routes, retires, sommets, T, Q):
	retires = list(retires)
	shuffle(retires)
	for c in retires:
		surcout, ri, p = min(options_insertion(c, routes, sommets, T, Q), key=lambda o: o[0])
		if ri is None:
			routes.append([c])
		else:
			routes[ri].insert(p, c)
	return [r for r in routes if r]


def reparation_regret(routes, retires, sommets, T, Q):
	restants = list(retires)
	while restants:
		meilleur_c, meilleure_pos, meilleur_regret, meilleur_surcout = None, None, -inf, inf
		for c in restants:
			opts = sorted(options_insertion(c, routes, sommets, T, Q), key=lambda o: o[0])
			best = opts[0]
			second = opts[1] if len(opts) > 1 else opts[0]
			regret = second[0] - best[0]                                 # regret-2
			if regret > meilleur_regret or (regret == meilleur_regret and best[0] < meilleur_surcout):
				meilleur_c, meilleure_pos, meilleur_regret, meilleur_surcout = c, best, regret, best[0]
		_, ri, p = meilleure_pos
		if ri is None:
			routes.append([meilleur_c])
		else:
			routes[ri].insert(p, meilleur_c)
		restants.remove(meilleur_c)
	return [r for r in routes if r]


# ---------------------------------------------------------------------------
# Destruction : retire k clients et les renvoie.
# ---------------------------------------------------------------------------

def _retirer(routes, cibles):
	cibles = set(cibles)
	clients = [c for r in routes for c in r if c in cibles]
	reste = [[c for c in r if c not in cibles] for r in routes]
	return [r for r in reste if r], clients


def destruction_aleatoire(routes, k, sommets, T):
	tous = [c for r in routes for c in r]
	return _retirer(routes, sample(tous, min(k, len(tous))))


def destruction_pire(routes, k, sommets, T):
	# surcoût de chaque client dans sa tournée = détour qu'il provoque
	gains = []
	for r in routes:
		chemin = ['Départ'] + r + ['Départ']
		for i in range(1, len(chemin) - 1):
			a, c, b = chemin[i - 1], chemin[i], chemin[i + 1]
			gains.append((T[a][c] + T[c][b] - T[a][b], c))
	gains.sort(reverse=True)                                              # les pires détours d'abord
	choisis, p = [], 4
	dispo = gains[:]
	while dispo and len(choisis) < k:
		idx = int(len(dispo) * (random() ** p))                          # biais vers le haut, un peu d'aléa
		choisis.append(dispo.pop(idx)[1])
	return _retirer(routes, choisis)


def destruction_shaw(routes, k, sommets, T):
	# retire des clients "proches" (distance + écart de fenêtre) d'un client germe
	tous = [c for r in routes for c in r]
	if not tous:
		return routes, []
	germe = choice(tous)
	def relation(c):
		return T[germe][c] + abs(sommets[germe][2][0] - sommets[c][2][0]) * 60
	tous.sort(key=relation)                                              # plus proche en premier
	choisis, p = [], 4
	dispo = tous[:]
	while dispo and len(choisis) < k:
		idx = int(len(dispo) * (random() ** p))
		choisis.append(dispo.pop(idx))
	return _retirer(routes, choisis)


# ---------------------------------------------------------------------------
# Solution initiale : insertion gloutonne (respecte la faisabilité stricte).
# ---------------------------------------------------------------------------

def solution_initiale(sommets, transport, T, germes):
	Q, routes = transport[1][0], []
	for c in germes:
		surcout, ri, p = min(options_insertion(c, routes, sommets, T, Q), key=lambda o: o[0])
		if ri is None:
			routes.append([c])
		else:
			routes[ri].insert(p, c)
	return [r for r in routes if r]


# ---------------------------------------------------------------------------
# Boucle ALNS : destruction + réparation adaptatives + recuit simulé.
# ---------------------------------------------------------------------------

def alns(sommets, transport, iterations=1500, graine=0, bavard=False, objectif='makespan'):
	seed(graine)
	Q = transport[1][0]
	f_cout = cout_makespan if objectif == 'makespan' else cout
	T = matrice_temps(sommets, transport)
	placables, impossibles = clients_placables(sommets, transport, T)
	for c in impossibles:
		print(f"{c} ne peut pas être servi (q>Q ou fenêtre inatteignable) : client ignoré.")

	destructions = [destruction_aleatoire, destruction_pire, destruction_shaw]
	if objectif == 'makespan':
		reparations = [reparation_makespan_gloutonne, reparation_makespan_regret]
	else:
		reparations = [reparation_gloutonne, reparation_regret]
	poids_d = [1.0] * len(destructions)
	poids_r = [1.0] * len(reparations)
	score_d = [0.0] * len(destructions)
	score_r = [0.0] * len(reparations)
	usage_d = [0] * len(destructions)
	usage_r = [0] * len(reparations)

	courante = solution_initiale(sommets, transport, T, placables)
	cout_courant = f_cout(courante, sommets, T, Q)
	meilleure, cout_meilleur = [r[:] for r in courante], cout_courant
	cout_initial = cout_courant

	# recuit : on accepte au départ une solution ~5 % plus coûteuse avec proba 0.5
	temperature = max(1.0, -0.05 * cout_initial / log(0.5))
	refroidissement = (1e-3) ** (1.0 / max(1, iterations))
	SIGMA = (33, 20, 13)                                                  # best / mieux / accepté
	nb_clients = len(placables)
	k_max = max(1, min(nb_clients // 3, 15))

	def tirer(poids):
		s = random() * sum(poids)
		cumul = 0
		for i, w in enumerate(poids):
			cumul += w
			if s <= cumul:
				return i
		return len(poids) - 1

	for it in range(1, iterations + 1):
		id_d, id_r = tirer(poids_d), tirer(poids_r)
		usage_d[id_d] += 1
		usage_r[id_r] += 1
		k = randint(1, k_max)

		partielle, retires = destructions[id_d]([r[:] for r in courante], k, sommets, T)
		candidate = reparations[id_r](partielle, retires, sommets, T, Q)
		cout_candidat = f_cout(candidate, sommets, T, Q)

		recompense = 0
		if cout_candidat < cout_meilleur:
			meilleure, cout_meilleur = [r[:] for r in candidate], cout_candidat
			courante, cout_courant = candidate, cout_candidat
			recompense = SIGMA[0]
		elif cout_candidat < cout_courant:
			courante, cout_courant = candidate, cout_candidat
			recompense = SIGMA[1]
		elif random() < exp(-(cout_candidat - cout_courant) / temperature):
			courante, cout_courant = candidate, cout_candidat
			recompense = SIGMA[2]
		score_d[id_d] += recompense
		score_r[id_r] += recompense

		temperature *= refroidissement
		if it % 100 == 0:                                                # mise à jour adaptative des poids
			rho = 0.2
			for i in range(len(poids_d)):
				if usage_d[i]:
					poids_d[i] = (1 - rho) * poids_d[i] + rho * score_d[i] / usage_d[i]
				score_d[i], usage_d[i] = 0.0, 0
			for i in range(len(poids_r)):
				if usage_r[i]:
					poids_r[i] = (1 - rho) * poids_r[i] + rho * score_r[i] / usage_r[i]
				score_r[i], usage_r[i] = 0.0, 0

	if bavard:
		print(f"ALNS : coût initial {cout_initial} -> {cout_meilleur}  (poids destruction {[round(w,2) for w in poids_d]}, réparation {[round(w,2) for w in poids_r]})")
	# conversion au format plat du projet : ['Départ', c, c, 'Départ', c, ...]
	flat = []
	for r in meilleure:
		flat.append('Départ')
		flat.extend(r)
	return flat, meilleure, cout_meilleur, cout_initial


# ---- Objectif alternatif : minimiser le makespan (la plus longue tournée) ----
def duree_route(route, sommets, T, Q, depot='Départ'):
	ok, tt, retour = evaluer_route(route, sommets, T, Q, depot)
	if not ok:
		return inf, inf
	return retour - sommets[depot][2][0] * 60, tt   # (durée horloge, temps de trajet)

def cout_makespan(routes, sommets, T, Q):
	makespan, total = 0, 0
	for r in routes:
		if r:
			d, tt = duree_route(r, sommets, T, Q)
			if d == inf:
				return inf
			makespan = max(makespan, d)
			total += tt
	return makespan + 0.001 * total        # makespan prioritaire, trajet total en départage


# ---------------------------------------------------------------------------
# Réparations orientées MAKESPAN : on place chaque client de façon à ne pas
# allonger la plus longue tournée, et on ouvre un camion seulement si ça aide.
# ---------------------------------------------------------------------------

def _duree(route, sommets, T, Q):
	ok, tt, retour = evaluer_route(route, sommets, T, Q)
	return None if not ok else retour - sommets['Départ'][2][0] * 60


def options_makespan(client, routes, sommets, T, Q, makespan_actuel):
	# clé = (makespan résultant, camion neuf ?, durée de la tournée) -> à minimiser
	opts = []
	for ri, r in enumerate(routes):
		for p in range(len(r) + 1):
			d = _duree(r[:p] + [client] + r[p:], sommets, T, Q)
			if d is not None:
				opts.append(((max(makespan_actuel, d), 0, d), ri, p))
	d = _duree([client], sommets, T, Q)
	if d is not None:
		opts.append(((max(makespan_actuel, d), 1, d), None, 0))   # ouvrir une tournée
	return opts


def reparation_makespan_gloutonne(routes, retires, sommets, T, Q):
	retires = list(retires)
	shuffle(retires)
	for c in retires:
		mk = max((_duree(r, sommets, T, Q) for r in routes), default=0)
		cle, ri, p = min(options_makespan(c, routes, sommets, T, Q, mk), key=lambda o: o[0])
		if ri is None:
			routes.append([c])
		else:
			routes[ri].insert(p, c)
	return [r for r in routes if r]


def reparation_makespan_regret(routes, retires, sommets, T, Q):
	restants = list(retires)
	while restants:
		choix = None
		for c in restants:
			mk = max((_duree(r, sommets, T, Q) for r in routes), default=0)
			opts = sorted(options_makespan(c, routes, sommets, T, Q, mk), key=lambda o: o[0])
			best, second = opts[0], (opts[1] if len(opts) > 1 else opts[0])
			regret = second[0][0] - best[0][0]
			if choix is None or regret > choix[0] or (regret == choix[0] and best[0] < choix[1]):
				choix = (regret, best[0], c, best[1], best[2])
		_, _, c, ri, p = choix
		if ri is None:
			routes.append([c])
		else:
			routes[ri].insert(p, c)
		restants.remove(c)
	return [r for r in routes if r]


def algo_alns(sommets, transport):
	flat, routes, cout_final, cout_initial = alns(sommets, transport, iterations=1200, graine=1, objectif='makespan')
	print(f"ALNS (objectif makespan) : {len(routes)} camion(s)")
	return flat


def simulation(sommets, aretes, transport):
	graphe, sommet_labels, couleur, etats = nx.DiGraph(), {}, [], {'historique':[aretes], 'numéro':0, 'algos':['Aucun', 'Voisins proches + Services', 'Capacité + Horaires', 'ALNS (makespan)']}

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
				elif etats['numéro'] == 2:
					new_etat = creation_chemins(algo_alns(sommets, transport))
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