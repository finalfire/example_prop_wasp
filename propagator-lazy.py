from itertools import groupby
from scipy import stats
import wasp

atoms=[]
names=[]
myvars = {}
reason=[]
threshold = None
icu_vales = list()
target_values = list()

def all_equal(it):
    """Ritorna vero se tutti gli elementi di it sono uguali"""
    g = groupby(it)
    return next(g, True) and not next(g, False)

def addedVarName(var, name):
    global atoms, names, myvars, threshold
    
    if name.startswith("occurrenceUtility"):
        # occ è il valore del predicato b, tipo: list
        occ = wasp.getTerms("occurrenceUtility", name)
        atoms.append(var)
        # i valori del predicato
        (tid, maxICU, target) = tuple(occ)

        myvars.update({
            var: (int(tid), int(maxICU), float(target.replace('"', ''))),
        })
    
    # soglia di interesse per la funzione calcolata (pearson)
    if name.startswith("utilityThreshold"):
        threshold_value = wasp.getTerms("utilityThreshold", name)[0].replace('"', '')
        threshold = float(threshold_value)


def getVariablesToFreeze():
    return atoms


def compute(answer_set):
    global threshold, icu_vales, target_values

    acc = 0
    for x in answer_set:
        if x < 0:
            continue
        if x not in myvars:
            continue
        
        (tid, maxICU, target) = myvars[x]

        acc += maxICU
        icu_vales.append(maxICU)
        target_values.append(target)

    # se uno dei due array è costante, pearson è undefined, la setto a -2.0
    # altrimenti la calcolo sui due array icu_values e target_values
    pearson_value = -2.0 if all_equal(icu_vales) or all_equal(target_values) else stats.pearsonr(icu_vales, target_values)[0]

    # se la pearson è undefined, l'answerset non è coerente
    if pearson_value == -2.0:
        return (pearson_value, True)
    
    # l'answerset è coerente se la pearson è <= -soglia oppure >= soglia
    unsat = (pearson_value > -threshold and pearson_value < threshold)
    return (pearson_value, unsat)


def checkAnswerSet(*answer_set):
    global reason
    reason = []
    answer_set = list(answer_set)
    (pearson, res) = compute(answer_set)

    # la ragione sono tutti quegli atomi che mi servirebbero per soddisfare i vincoli
    if res:
        reason.append([x for x in myvars if answer_set[x] < 0]) # il valore di answer_set[x] è negativo se l'atomo è falso
        return wasp.incoherent()
    
    print(f"Pearson = {pearson}", flush=True)
    return wasp.coherent()


def getReasonsForCheckFailure():
    global reason
    return wasp.createReasonsForCheckFailure(reason)