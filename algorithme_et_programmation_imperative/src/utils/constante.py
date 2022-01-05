"""
Language elements:
    * Person/chromosome     --> A sequence
    * Population            --> The sequences to be evaluated
    * Reproduction          --> New sequence obtained by combining two others
    * Mutation              --> Removal of some genes in a sequence
    * Selection             --> Elimination of the least similar sequences
    * Gene                  --> An element of the sequence
"""
dict_const = {
    "PM": "Hello*I a^m a (tes5t phr$ase+",
    "L":   29,            # 10 <= L (verify in the input function)
    "N":  100,            # 10 <= N (verify in the input function)
    "TS": 0.3,            # 0.1 < TS <= 1 (verify in the input function)
    "TM": 0.05,           # 0.1 < TM <= 1 (verify in the input function)
    "NG": 1000,           # 1 <= NG
    "FITNESS_CHOICE": 1,  # case 1, 2, 3
    "CURVE_CHOICE": 0     # case 0, 1
}