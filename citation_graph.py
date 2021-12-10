"""Read the citations from a csv file and construct the graph of those citations."""
import pickle
from os.path import exists
from typing import Tuple, Dict
import networkx as nx
import nltk
import pandas as pd
from french_lefff_lemmatizer.french_lefff_lemmatizer import FrenchLefffLemmatizer
from tqdm import tqdm

MAX_CITATION_LENGTH = 100


def pos2pos(pos: str) -> str:
    """
    Take a pos in NLTK format, and return the pos in LEFFF format.
    :param pos: pos in NLTK format.
    :return: pos : pos in LEFFF format.
    """
    if pos in {'NN', 'NNS', 'NNP', 'NNPS'}:
        return 'n'
    elif pos in {'VB', 'VBN', 'VBP', 'VBZ'}:
        return 'v'


def get_subgraph() -> Tuple[nx.DiGraph, Dict]:
    """
    Read the citations from a csv file and construct the graph of those citations.
    :return: a graph
    """
    lemmatizer = FrenchLefffLemmatizer()

    # si le fichier pickle existe, le charger
    if exists('citations_extrem.pickle'):
        with open('citations_extrem.pickle', 'rb') as f:
            citations_extrem = pickle.load(f)
    else:  # sinon :
        # lire les citations
        data = pd.read_csv('citations.csv')

        # enlever toutes les citations formattées comme des définitions
        data = data[~data['citation'].str.match(r'^[^ ]* :.*')]

        citations = data['citation'].to_list()
        auteurs = data['auteur'].to_list()

        # garder seulement citations de moins de `MAX_CITATION_LENGTH` caractères
        citations = [(citation, auteur) for citation, auteur in zip(citations, auteurs) if
                     len(citation) <= MAX_CITATION_LENGTH]

        # charger les stopwords
        with open('stopwords-fr.txt', 'r') as f:
            stop_words = set(f.read().splitlines())

        # phrase => token (découper les mots)
        print('Tokenisation...')
        citations_tokens = [nltk.word_tokenize(phrase) for phrase, _ in tqdm(citations)]
        citations_tokens = [[w for w in tokens if not w.lower() in stop_words] for tokens in citations_tokens]

        print('POS tagging...')
        citations_pos = [nltk.pos_tag(tokens) for tokens in tqdm(citations_tokens)]

        # spacy non concluant pour cette tâche
        # nlp = spacy.load('fr_core_news_sm')
        # citations_docs = [nlp(phrase) for phrase in tqdm(citations)]
        # for ent in doc:
        #     print(ent, ent.pos_)

        # * trouver premier et dernier mots "importants" de chaque phrase *
        # l'heuristique est que les mots importants sont des noms ou des verbes
        candidate_pos = {'NN', 'NNS', 'NNP', 'NNPS', 'VB', 'VBN', 'VBP', 'VBZ'}

        citations_extrem = []  # citations que l'on trouve aux extrémités des phrases (début et fin)
        for citation_pos, (citation, auteur) in tqdm(zip(citations_pos, citations)):
            premier_mot = dernier_mot = pos_premier = pos_dernier = None
            for mot, pos in citation_pos:  # parcourir la citation jusqu'à trouver un "premier mot important" valide
                if pos in candidate_pos:
                    premier_mot = mot
                    pos_premier = pos
                    break
            for mot, pos in reversed(citation_pos):  # parcourir la citation à l'envers jusqu'à trouver un "dernier mot"
                if pos in candidate_pos:
                    dernier_mot = mot
                    pos_dernier = pos
                    break
            if premier_mot is not None and dernier_mot is not None:  # sinon la citation est abandonnée
                # lemmatization (trouver le radical)
                # https://github.com/ClaudeCoulombe/FrenchLefffLemmatizer
                lemme_premier = lemmatizer.lemmatize(premier_mot, pos2pos(pos_premier))
                lemme_dernier = lemmatizer.lemmatize(dernier_mot, pos2pos(pos_dernier))

                citations_extrem.append((citation, auteur, lemme_premier, lemme_dernier))

        with open('citations_extrem.pickle', 'wb') as f:  # stocker le résultat de ce filtrage assez chronophage
            pickle.dump(citations_extrem, f, protocol=pickle.HIGHEST_PROTOCOL)

    # phrases avec mots en commun : création des dictionnaires de recherches
    lemmes_premier = dict()
    auteurs = dict()
    citations = []
    for citation, auteur, premier, dernier in citations_extrem:  # construction des dictionnaires de recherche
        citations.append((citation, dict(same=premier == dernier)))  # `same` attribute checks whether premier=dernier
        auteurs[citation] = auteur
        if premier in lemmes_premier:
            lemmes_premier[premier].append(citation)
        else:
            lemmes_premier[premier] = [citation]

    # formuler ça comme un probleme de graphe
    G = nx.DiGraph()  # graphe orienté
    G.add_nodes_from(citations)

    # ajouter au graphe les relations "est_suivi_par" (càd qu'une phrase peut être suivie par une autre dans une démo)
    for citation, _, _, dernier in citations_extrem:
        if dernier in lemmes_premier:
            # ajouter les relations
            cibles = lemmes_premier[dernier]
            G.add_edges_from([(citation, cible) for cible in cibles if citation != cible])

    # remove self loops (none after pre-processing correctly)
    # G.remove_edges_from(selfloop_edges(G))

    sg = G.edge_subgraph(G.edges()).copy()  # ne garder que les noeuds engagés dans au moins une relation (une arête)

    # from networkx import info
    # print(info(G))  # DiGraph with 3799 nodes and 28693 edges

    return sg, auteurs
