from nlp_plantform.center.mytree import mytree
t = mytree.fromstring("(S (NP (D the) (N dog)) (VP (V chased) (NP (D the) (N cat))))")
p = t.leaf_treeposition(index=3)
print(p.position())
