from collections import OrderedDict
from pprint import pprint
import cfg

chiaddrs = 'data/chicago_addresses.csv'
fix_chiaddrs = True
fix_tktaddrs = True

#ugly code
def fix_tktline(line, fails, fieldnames):
    changed_fields = {}
    ordered_line = [ line[field] for field in fieldnames ]

    for field,failval in fails:
        field_index = fieldnames.index(field)
        prev_fieldnames = fieldnames[:field_index+1]
        prev_vals = [ line[field] for field in prev_fieldnames ]

        prevs = dict((zip(prev_fieldnames,prev_vals)))

        if 'Issue Date' in prev_fieldnames:
            if failval in [ td['description'] for td in cfg.ticket_descripts ]:
                old_description = prevs['Violation Description']
                changed_fields['Violation Description'] = {
                    'old':old_description,
                    'new':failval,
                    'index':field_index
                }

            elif failval in [ td['code'] for td in cfg.ticket_descripts ]:
                old_code = failval
                changed_fields['Violation Code'] = {
                    'old':old_code,
                    'new':failval,
                    'index':field_index
                }
    if not changed_fields:
        return None

    address_idx = fieldnames.index('Violation Location')
    for changedkey,vals in changed_fields.iteritems():
        if vals['old'] in [ td['code'] for td in cfg.ticket_descripts ]:
            code_idx = vals['index']
            missing_distance = (code_idx - 1) - (address_idx +1)
            
            ordered_line[address_idx] += ordered_line.pop(address_idx+missing_distance)
            ordered_line.append('') #Hearing Dispo 

    return dict(zip(fieldnames,ordered_line))
