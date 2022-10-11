from pandas import DataFrame as pdDataframe

def calculate_balance_with_interactions(df):
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
    
    
    
    # Our balances DF
    calculated_df = pdDataframe({'oldBalanceOrig': [0.] * df.shape[0], 
                                 'newBalanceOrig': [0.] * df.shape[0],
                                 'oldBalanceDest': [0.] * df.shape[0],
                                 'newBalanceDest': [0.] * df.shape[0],
                                 'isUnauthorizedOverdraft': [0.] * df.shape[0] 
                                })
    
    """
    The transaction logic over the origin and destination balances:
    - CASH_IN: only the origBalances are updated (+)
    - CASH_OUT: only the origBalances are updated (-)
    - PAYMENT: both balances are updated (orig - , dest +)
    - TRANSFER: both balances are updated (orig -, dest +)
    - DEBIT: only the origBalances are updated (-)
    """
    
    ops_map = {
            'CASH_IN': [1, 0],
            'CASH_OUT': [-1, 0],
            'PAYMENT': [-1, 1],
            'TRANSFER': [-1, 1],
            'DEBIT': [-1, 0]
    }
        
    for i, r in df.iterrows():
        
        '''
        We need to initialize the attributes of the entitie.
        In this example, we simply initialize the state with 0. but this is use-case based.
        '''
        for entity, rel_entities in relations.items():
            for col_rel, col_fields in rel_entities.items():
                for state, col in col_fields.items():
                    if r[col_rel] not in entity_state[entity][state]:
                        entity_state[entity][state][r[col_rel]] = 0.

        '''
        Let us define here if the transaction logic:
        We need to update the old balances.
        We need to update the balances according to the constraints. 
        We need to then update the entity state with the balances
        '''
        
        # First, let's update the old balance variables
        calculated_df.at[i, 'oldBalanceOrig'] = entity_state['acc_id']['balance'][r['nameOrig']]
        calculated_df.at[i, 'oldBalanceDest'] = entity_state['acc_id']['balance'][r['nameDest']]
        
        # Now, let's compute the new balance given the constraints
        
        # If potentially fraudulent, operation is rejected and balances stay the same
        try:
            if r.isFlaggedFraud == 1:
                calculated_df.at[i, 'newBalanceOrig'] = calculated_df.at[i, 'oldBalanceOrig'] 
                calculated_df.at[i, 'newBalanceDest'] = calculated_df.at[i, 'oldBalanceDest']    
                continue
        except AttributeError: # column does not exist
            pass
            
        # Everything else follows the transaction logic
        op = r['action']
        amount = r['amount']


        # Checking if this is a possible overdraft
        if (op in ['CASH_OUT', 'PAYMENT', 'TRANSFER', 'DEBIT']) and (amount > calculated_df.at[i, 'oldBalanceOrig']):
            calculated_df.at[i, 'isUnauthorizedOverdraft'] = 1
            calculated_df.at[i, 'newBalanceOrig'] = calculated_df.at[i, 'oldBalanceOrig'] 
            calculated_df.at[i, 'newBalanceDest'] = calculated_df.at[i, 'oldBalanceDest']
            continue
        else:
            calculated_df.at[i, 'isUnauthorizedOverdraft'] = 0
            calculated_df.at[i, 'newBalanceOrig'] = calculated_df.at[i, 'oldBalanceOrig'] + (amount*ops_map[op][0])
            calculated_df.at[i, 'newBalanceDest'] = calculated_df.at[i, 'oldBalanceDest'] + (amount*ops_map[op][1])
        
        # Finishg by updating the state of each entity 
        for entity, rel_entities in relations.items():
            for col_rel, col_fields in rel_entities.items():
                for state, col in col_fields.items():
                    entity_state[entity][state][r[col_rel]] = calculated_df.at[i, col]
     
    # Adjusting a datatype
    calculated_df.isUnauthorizedOverdraft = calculated_df.isUnauthorizedOverdraft.astype(int)
    
    return calculated_df