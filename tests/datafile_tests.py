from re import match
from collections import defaultdict

def test_tktline(line, fieldnames):
    if len(line) != 13:
        return None

    field_results  = defaultdict(dict)
    linefields = list(line.keys())
    testfields = linefields
    testfields.append('missing') 
    testfields.append('extra')

    missing = [ f for f in fieldnames if f not in linefields]
    missing_test = True if len(missing) == 0 else False
    field_results['missing'] = missing_test

    extra = [ f for f in linefields if f not in fieldnames]
    extra_test = True if len(extra) == 0 else False
    field_results['extra'] = extra_test

    tktno_test = line['Ticket Number'].isdigit()
    field_results['Ticket Number'] = tktno_test

    plate_test = line['License Plate Number'].isalnum()
    field_results['License Plate Number'] = plate_test

    platestate = line['License Plate State']
    platestate_test = True if len(platestate) == 2 else False
    field_results['License Plate State'] = platestate_test

    platetype_test = line['License Plate Type'].isalnum()
    field_results['License Plate Type'] = platetype_test

    make_test = line['Ticket Make'].isalpha()
    field_results['Ticket Make'] = make_test

    #regex = "[01][0-9]/[0-3][0-9]/20[01][0-9] [01][0-9]:[0-5][0-9] [ap]m"
    date_test = True if len(line['Issue Date']) == 19 else False
    field_results['Issue Date'] = date_test 

    #more thorough testing comes later for perf reasons
    loc_test = True if len(line['Violation Location']) > 1 else False
    field_results['Violation Location'] = loc_test

    code = line['Violation Code']
    code_test = True if code[:-2].isdigit() and len(code) in [7,8,9] else False
    field_results['Violation Code'] = code_test

    #12 comes from the minimum tkt descr length
    descr = line['Violation Description']
    descr_test = True if len(descr) >= 12 else False
    field_results['Violation Description'] = True

    badge_test = True if line['Badge'].isdigit() else False
    field_results['Badge'] = badge_test

    unit_test = True if line['Unit'].isdigit() or line['Unit'] == '' else False
    field_results['Unit'] = unit_test

    queue_test = True if line['Ticket Queue'].istitle() else False
    field_results['Ticket Queue'] = queue_test

    hearing = line['Hearing Dispo']
    hearing_test = True if hearing.istitle or hearing == '' else False
    field_results['Hearing Dispo'] = hearing_test

    fails = ([ (key,line[key]) for key in fieldnames if not field_results[key] ])

    #if missing:
    #    print "missing: %s" % missing

    #if extra:
    #    print "extra fails: %s" % extra

    #if fails:
    #    print "fails %s" % fails

    return fails

def test_chiaddrs(line):
    if len(line) != 3:
        return False
    else:
        return True
