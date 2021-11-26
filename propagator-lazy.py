import wasp

atoms=[]
names=[]
myvars = {1: 'false', 'false': 1}
reason=[]
threshold = None

def addedVarName(var, name):
    global atoms, names, myvars, threshold
    
    if name.startswith("b"):
        # occ è il valore del predicato b, tipo: list
        occ = wasp.getTerms("b", name)
        atoms.append(var)
        b_value = tuple(occ)

        myvars.update({
            var: b_value,
            b_value: var
        })
    
    if name.startswith("t"):
        threshold = int(wasp.getTerms("t", name)[0])


def getVariablesToFreeze():
    return atoms


def compute(answer_set):
    global threshold

    acc = 0
    for x in answer_set:
        if x < 0:
            continue
        if x not in myvars:
            continue
        
        # myvars[x] è un tupla con un solo valore, la distrutturo
        (b_value,) = myvars[x]
        acc += int(b_value)
    
    return (acc, acc < threshold)


def checkAnswerSet(*answer_set):
    global reason
    reason = []
    answer_set = list(answer_set)
    (acc, res) = compute(answer_set)

    if res:
        reason.append([x for x in myvars if answer_set[x] > 0])
        return wasp.incoherent()
    
    print("Somma = %s" % acc)
    return wasp.coherent()


def getReasonsForCheckFailure():
    global reason
    return wasp.createReasonsForCheckFailure(reason)