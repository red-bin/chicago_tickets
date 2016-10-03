from collections import OrderedDict
from pprint import pprint
import cfg

ticket_types = cfg.ticket_types

#ugly code
def fix_tktline(line, fails, fieldnames):
    changed_fields = {}
    line_dict = OrderedDict([ (field,line[field]) 
                                  for field in fieldnames])

    ordered_line = line_dict.values()

    for field,failval in fails.items():
        field_index = fieldnames.index(field)
        prev_fieldnames = fieldnames[:field_index+1]
        prev_vals = [ line[field] for field in prev_fieldnames ]

        prevs = dict((zip(prev_fieldnames,prev_vals)))

        if 'Issue Date' in prev_fieldnames:
            if failval in cfg.ticket_descriptions:
                old_description = prevs['Violation Description']
                changed_fields['Violation Description'] = {
                    'old':old_description,
                    'new':failval,
                    'index':field_index
                }

            elif failval in cfg.ticket_codes:
                old_code = failval
                changed_fields['Violation Code'] = {
                    'old':old_code,
                    'new':failval,
                    'index':field_index
                }
    if not changed_fields:
        return None

    address_idx = fieldnames.index('Violation Location')
    for changedkey,vals in changed_fields.items():
        if vals['old'] in cfg.ticket_codes:
            code_idx = vals['index']
            missing_distance = (code_idx - 1) - (address_idx +1)
            
            ordered_line[address_idx] += ordered_line.pop(address_idx+missing_distance)
            ordered_line.append('') #Hearing Dispo 

    return dict(zip(fieldnames,ordered_line))
