pattern_list = [{'ID':'0', 'Name': 'apg', 'Pattern': ['Add penalty', 'Payment']},
                            {'ID':'1', 'Name': 'cpg', 'Pattern': ['Create Fine', 'Payment']}]

ids_user_patterns = [x['ID'] for x in pattern_list]
print("ids_user_patterns = ",ids_user_patterns)