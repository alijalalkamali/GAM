lookup_states = {296: {'name':'close2party', 'type':int}}
preset_states = {'economy': {'type':int, 'val':50}}

actions_trust = {
    'refuse tax': \
        {'economy': 0.7,
         'living_condition': 0.3,
         'safety': 0.3,
        },
    'vote': \
        {'economy': 0.6,
         'education': 0.7,
         'living_condition': 0.7,
         'safety': 0.7,
        },
    'demonstration': \
        {'economy': 0.6,
         'education': 0.6,
         'living_condition': 0.3,
         'safety': 0.3,
        },
    'raise_issue': \
        {'economy': 0.6,
         'education': 0.7,
         'living_condition': 0.7,
         'safety': 0.7,
        },
}

beliefs = {
    
}

actors = ['major', 'minor', 'government']

objectives = {
    
}

# states = ['economy', 'education']
# states = ['economy', 'education', 'living_condition', 'safety',
#           'trust', 'close2party']