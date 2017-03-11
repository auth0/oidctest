TOOL_ISS = 'https://localhost'

FO = {'swamid': 'https://swamid.sunet.se',
      'surfnet': 'https://surfnet.nl/oidc',
      'feide': 'https://www.feide.no',
      'edugain': 'https://edugain.com'}

OA = {'sunet': 'https://sunet.se', 'uninett': 'https://uninett.no'}

IA = {}

EO = {'sunet.op': 'https://sunet.se/op'}

BASE = {'sunet.op': EO['sunet.op']}

SMS_DEF = {
    'sunet':{
        FO['swamid']: [
            {'request': {}, 'requester': OA['sunet'],
             'signer_add': {}, 'signer': FO['swamid']},
        ],
        FO['feide']: [
            {'request': {}, 'requester': OA['sunet'],
             'signer_add': {}, 'signer': FO['feide']},
        ],
        FO['surfnet']: [
            {'request': {}, 'requester': OA['sunet'],
             'signer_add': {}, 'signer': FO['surfnet']},
        ],
        FO['edugain']: [
            {'request': {}, 'requester': FO['swamid'],
             'signer_add': {}, 'signer': FO['edugain']},
            {'request': {}, 'requester': OA['sunet'],
             'signer_add': {}, 'signer': FO['swamid']}
        ]
    },
    'uninett':{
        FO['feide']: [
            {'request': {}, 'requester': OA['uninett'],
             'signer_add': {}, 'signer': FO['feide']},
        ]
    }
}

KEY_DEFS = [
    {"type": "RSA", "key": '', "use": ["sig"]},
    {"type": "EC", "crv": "P-256", "use": ["sig"]}
]