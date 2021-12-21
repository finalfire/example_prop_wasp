occurrencesThreshold(2).
utilityThreshold("0.25").
maxCardItemset(4).


% ------------------------------
%% Con la choice rule, la combinazione di cui sotto wasp non la considera
%% la combinazione di sotto nell'output di gringo è presente
{ inCandidatePattern(K,W) } :- usefulItem(K,W).

%% Se li seleziono manualmente, wasp considera l'answerset e calcola correttamente
%inCandidatePattern("dg3", "1.0").
%inCandidatePattern("above", "0").
%inCandidatePattern("htn", "1.0").
%inCandidatePattern("gender", "1").
% ------------------------------


% tutti i valori degli item
usefulItem(K,V) :- item(_, K, V).

% filtro sulle transaction utility
transactionUtilityVector(V, A) :- transactionUtilityVector(V, A, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _).

% itemset di lunghezza al più M
cardItemset(N) :- #count{ K,W: inCandidatePattern(K,W)} = N.
:- cardItemset(N), maxCardItemset(M), N > M.
:- cardItemset(N), N < 1. 

% non possono esserci due item dello stesso tipo
:- inCandidatePattern(K1,V), inCandidatePattern(K2,W), V != W, K1 = K2.

% considero solo le transaction che contengono gli item guessati
inTransaction(Tid) :- transaction(Tid,_), not incomplete(Tid).
incomplete(Tid) :- transaction(Tid,_), inCandidatePattern(K,W), not contains(Tid,K,W).
contains(Tid,K,W) :- item(Tid, K, W).

% ho almeno Tho transaction
:- #count{ Tid: inTransaction(Tid) }=N, N < Tho, occurrencesThreshold(Tho).

% utility dell'occurrence è la concatenazione dei valori che ci servono
occurrenceUtility(Tid,MaxICU,Albumin) :- inTransaction(Tid), transaction(Tid, PatientId),
    objectUtilityVector(PatientId, MaxICU), transactionUtilityVector(Tid, Albumin).

#show utilityThreshold/1.
#show occurrenceUtility/3.
#show inCandidatePattern/2.