"""Code pour afficher une démo."""
import random
import pyperclip

# * connecteurs logiques à utiliser *
connecteurs_logiques = ["Et,", "De plus,", "En outre,", "Car", "Parce que", "En effet,", "Puisque", "Comme", "Donc",
                        "Aussi,", "Attendu que", "Vu que", "Etant donné que", "Par suite de", "Du fait que",
                        "Dans la mesure où", "Quoique", "Bien que", "Alors que", "Même si", "Certes,", "Bien sûr",
                        "Évidemment,", "Il est vrai que", "Toutefois,", "Sans doute", "Entre autre,",
                        "En particulier,", "Ensuite,", "De plus,", "Après,", "D’ailleurs,", "En fait,", "Mais,",
                        "Cependant,", "Or,", "En revanche,", "Pourtant,", "Par contre,", "Néanmoins,", "Au contraire,",
                        "D’un autre côté,", "Toutefois,", "Simplement,", "Néanmoins,", "Pourtant,", "Alors", "Ainsi,",
                        "Par conséquent,", "D’où", "En conséquence,", "Conséquemment,", "Par suite,", "C’est pourquoi",
                        "De surcroît,"]
intro_conn_log = ["Tout d’abord,", "En premier lieu,", "Premièrement,"]  # en introduction
concl_conn_log = ["Conclusion :", "En conclusion,", "Pour conclure,", "En guise de conclusion,", "En somme,", "Bref,",
                  "Ainsi,", "Donc", "En résumé,", "En un mot,", "Par conséquent,", "Finalement,", "Enfin,",
                  "En définitive,"]  # en conclusion


def first_lower(s: str) -> str:
    """
    Lowercase first letter in string.
    :param s: string to process
    :return: processed string
    """
    if s == "":
        return s
    return s[0].lower() + s[1:]


def print_demo(steps_l, auteurs) -> None:
    """
    Pretty-print a demo (and put it in clipboard).
    :param steps_l: steps of the demo.
    :param auteurs: dict of the authors.
    """
    print('******** Nouvelle démo ********')
    pretty_print(steps_l, auteurs)
    print('*******************************')


def pretty_print(steps_l, auteurs) -> None:
    """
    Pretty-print a demo (and put it in clipboard).
    :param steps_l: steps of the demo.
    :param auteurs: dict of the authors.
    """
    to_print = ''
    to_print += random.choice(intro_conn_log) + ' '
    to_print += first_lower(f'{steps_l[0]} ({auteurs[steps_l[0]]}) ')
    for s in steps_l[1:-1]:
        to_print += random.choice(connecteurs_logiques) + ' '
        to_print += first_lower(f'{s} ({auteurs[s]}) ')
    to_print += random.choice(concl_conn_log) + ' '
    to_print += first_lower(f'{steps_l[-1]} ({auteurs[steps_l[-1]]})')
    print(to_print)
    pyperclip.copy(to_print)  # copier la citation dans le presse-papier
