def check_balance_with_interaction(df):
    """
    Define the relations and interactions.
    First, we need to specify that `account_id` and `dest_account_id` refer to the same entity that we label `acc_id`.
    Then, for each column representing an entity `acc_id`, we specify the map attribute to columns.
    For instance, the attribute `balance` is represented by the column `balance` for the `account_id` but by the column `dest_balance` for the `dest_account_id`.
    """
    relations = {
        'acc_id': {
            'nameOrig': {'balance': 'newBalanceOrig'},
            'nameDest': {'balance': 'newBalanceDest'},
        }
    }
    """
    For each entity defined above, let us define a state per attribute.
    """
    entity_state = {'acc_id': {'balance': {}}}
    
    
    mask = pdDataframe({'balance': [True] * df.shape[0]}) # In the end we need to return a mask
    
    for i, r in df.iterrows():
        '''
        We need to initialize the attributes.
        In this example, we simply initialize the state with 0. but this is use-case based.
        '''
        for entity, rel_entities in relations.items():
            for col_rel, col_fields in rel_entities.items():
                for state, col in col_fields.items():
                    if r[col_rel] not in entity_state[entity][state]:
                        entity_state[entity][state][r[col_rel]] = 0.

        '''
        Let us define here if the constraints are respected.
        '''
        
        #Todo this logic is not correct. Have to re-check the rules for the PAYSIM dataset
        mask.at[i, 'newBalanceOrig'] = r['newBalanceOrig'] == entity_state['acc_id']['balance'][r['nameOrig']] + r['amount']
        mask.at[i, 'newBalanceDest'] = r['newBalanceDest'] == entity_state['acc_id']['balance'][r['nameDest']] - r['amount']
        
        '''
        Update the state for each attribute and each entity.
        '''
        for entity, rel_entities in relations.items():
            for col_rel, col_fields in rel_entities.items():
                for state, col in col_fields.items():
                    entity_state[entity][state][r[col_rel]] = df.at[i, col]
    return mask