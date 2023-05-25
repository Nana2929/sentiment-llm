import re
from typing import List, Tuple
def str_2_tuples(string: str):
    pattern = r'\((.*?)\)'
    tuples = re.findall(pattern, string)
    tuples = [tuple(t.split(',')) for t in tuples]
    for i, t in enumerate(tuples):
        if len(t) < 4:
            # manually add empty string until 4 or
            # trim the tuple to 4
            t += ('',) * (4 - len(t))
        elif len(t) > 4:
            t = t[:4]
        tuples[i] = t
    return tuples

# string = "(1iej1,dfwhf,sss)"
# print(str_2_tuples(string))
def calc_single_f1(predicted:List[str], gold: List[str], idx: int):
    """
    idx: from which position's element to extract
    """
    # following https://github.com/unikcc/DiaASQ/blob/master/src/run_eval.py
    fp, fn, tp = 0, 0, 0
    tol = 1e-10
    for pred_line, gold_line in zip(predicted, gold):
        pred_quads = str_2_tuples(pred_line)
        gold_quads = str_2_tuples(gold_line)
        pred_elems = [quad[idx] for quad in pred_quads]
        gold_elems = [quad[idx] for quad in gold_quads]

        fp += len(set(pred_elems) - set(gold_elems))
        fn += len(set(gold_elems) - set(pred_elems))
        tp += len(set(pred_elems) & set(gold_elems))
    p = tp / (tp + fp + tol)
    r = tp / (tp + fn + tol)
    f1 = 2*p*r/(p+r + tol)
    return f1

def calc_pair_f1(predicted:List[str], gold: List[str], idx: Tuple[int, int]):
    """
    idx: from which 2 position's element to extract
    """
    fp, fn, tp = 0, 0, 0
    tol = 1e-10
    assert len(idx) == 2

    for pred_line, gold_line in zip(predicted, gold):
        pred_quads = str_2_tuples(pred_line)
        gold_quads = str_2_tuples(gold_line)
        pred_pairs = [(quad[idx[0]], quad[idx[1]]) for quad in pred_quads]
        gold_pairs = [(quad[idx[0]], quad[idx[1]]) for quad in gold_quads]

        fp += len(set(pred_pairs) - set(gold_pairs))
        fn += len(set(gold_pairs) - set(pred_pairs))
        tp += len(set(pred_pairs) & set(gold_pairs))
    p = tp / (tp + fp + tol)
    r = tp / (tp + fn + tol)
    f1 = 2*p*r/(p+r + tol)
    return f1

def calc_strict_f1(predicted:List[str], gold: List[str]):
    fp, fn, tp = 0, 0, 0
    tol = 1e-10
    for pred_line, gold_line in zip(predicted, gold):
        pred_quads = str_2_tuples(pred_line)
        gold_quads = str_2_tuples(gold_line)

        fp += len(set(pred_quads) - set(gold_quads))
        fn += len(set(gold_quads) - set(pred_quads))
        tp += len(set(pred_quads) & set(gold_quads))
    p = tp / (tp + fp + tol)
    r = tp / (tp + fn + tol)
    f1 = 2*p*r/(p+r + tol)
    return f1