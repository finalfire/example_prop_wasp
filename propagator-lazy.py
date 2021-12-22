from scipy import stats
import wasp

atoms=[]
myvars = {}
names = {}
reason=[]
threshold = None
icu_values = list()
target_values = list()

# questo viene chiamato una sola volta
def addedVarName(var, name):
    global atoms, myvars, threshold, names

    names[var] = name
    
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
    global threshold, icu_values, target_values

    icu_values = list()
    target_values = list()

    for x in answer_set:
        if x < 0:
            continue
        if x not in myvars:
            continue
        
        (_, maxICU, target) = myvars[x]

        icu_values.append(maxICU)
        target_values.append(target)

    # calcolo della pearson
    pearson_value = stats.pearsonr(icu_values, target_values)[0]
    
    # l'answerset è coerente se abs(pearson) >= soglia
    sat = abs(pearson_value) >= threshold
    return (pearson_value, not sat)


def checkAnswerSet(*answer_set):
    global reason, myvars, names
    reason = []

    answer_set = list(answer_set)
    (pearson, res) = compute(answer_set)

    # la ragione sono tutti quegli atomi che mi servirebbero per soddisfare i vincoli
    if res:
        l = [-x for x in myvars if answer_set[x] > 0]
        l.extend([x for x in myvars if answer_set[x] < 0])
        reason.append(l) # il valore di answer_set[x] è negativo se l'atomo è falso
        return wasp.incoherent()

    print(f"Pearson = {pearson}", flush=True)
    #print(f"Pearson = {pearson} {' '.join([names[x] for x in answer_set if x in names and answer_set[x] > 0])}", flush=True)
    return wasp.coherent()


def getReasonsForCheckFailure():
    global reason
    return wasp.createReasonsForCheckFailure(reason)