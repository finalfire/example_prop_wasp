occurrencesThreshold(10).
utilityThreshold("0.50").
maxCardItemset(4).

% tutti i valori degli item
usefulItem(K,V) :- item(_, K, V).



% ------------------------------
{ inCandidatePattern(K,W) } :- usefulItem(K,W).
% ------------------------------


% filtro sulle transaction utility
transactionUtilityVector(V, A) :- transactionUtilityVector(V, A, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _).

% itemset di lunghezza al più M
cardItemset(N) :- #count{ K,W: inCandidatePattern(K,W)} = N.
:- cardItemset(N), maxCardItemset(M), N > M.
:- cardItemset(N), N < 1. 

% non possono esserci due item dello stesso tipo
:- inCandidatePattern(K1,V), inCandidatePattern(K2,W), V != W, K1 = K2.

% considero solo le transaction che contengono gli item guessati e il valore target non è nan
inTransaction(Tid) :- transaction(Tid,_), not incomplete(Tid), not containsNan(Tid).
incomplete(Tid) :- transaction(Tid,_), inCandidatePattern(K,W), not contains(Tid,K,W).
contains(Tid,K,W) :- item(Tid, K, W).
containsNan(Tid) :- transaction(Tid, PatientId), objectUtilityVector(PatientId, "nan").
containsNan(Tid) :- transaction(Tid, PatientId), transactionUtilityVector(Tid, "nan"). 

% ho almeno Tho transaction
:- #count{ Tid: inTransaction(Tid) }=N, N < Tho, occurrencesThreshold(Tho).

% utility dell'occurrence è la concatenazione dei valori che ci servono
occurrenceUtility(Tid,MaxICU,Albumin) :- inTransaction(Tid), transaction(Tid, PatientId),
    objectUtilityVector(PatientId, MaxICU), transactionUtilityVector(Tid, Albumin).

% se i valori sono costanti la pearson non puo essere calcolata
:- #count{ M : occurrenceUtility(T,M,_)} = 1.
:- #count{ M : occurrenceUtility(T,_,M)} = 1.

#show utilityThreshold/1.
#show occurrenceUtility/3.
#show inCandidatePattern/2.