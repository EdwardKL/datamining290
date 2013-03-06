#!/usr/bin/python
"""Script can be used to calculate the Gini Index of a column in a CSV file.

Classes are strings."""

import fileinput
import csv

(cmte_id, cand_id, cand_nm, contbr_nm, contbr_city, contbr_st, contbr_zip,
contbr_employer, contbr_occupation, contb_receipt_amt, contb_receipt_dt,
receipt_desc, memo_cd, memo_text, form_tp, file_num, tran_id, election_tp) = range(18)


############### Set up variables

total_entries = 0
items_per_name = {}
ipn_per_zip = {}
ipn_per_contrib = {}
splits = []

############### Read through files
for row in csv.reader(fileinput.input()):
    if not fileinput.isfirstline():
        ###
        # TODO: replace line below with steps to save information to calculate
        # Gini Index
        name = row[cand_nm]
        zipc = row[contbr_zip]
        contrib = float(row[contb_receipt_amt])

        if zipc not in ipn_per_zip:
            ipn_per_zip[zipc] = {'total':0, 'ipns': {}}
        if contrib not in ipn_per_contrib:
            ipn_per_contrib[contrib] = {'total':0, 'ipns': {}}
        if name not in items_per_name:
            items_per_name[name] = 0
        if name not in ipn_per_zip[zipc]['ipns']:
            ipn_per_zip[zipc]['ipns'][name] = 0
        if name not in ipn_per_contrib[contrib]['ipns']:
            ipn_per_contrib[contrib]['ipns'][name] = 0

        items_per_name[name] += 1
        ipn_per_zip[zipc]['ipns'][name] += 1
        ipn_per_zip[zipc]['total'] += 1
        ipn_per_contrib[contrib]['ipns'][name] += 1
        ipn_per_contrib[contrib]['total'] += 1
        total_entries += 1

        splits.append(contrib)
        ##/

def get_gini(counts, total):
    '''
    Gets the gini index from a list of counts and the total number of entries.
    '''
    if (total == 0):
        return 0 # don't want it to affect weighted averages of split ginis
    return 1 - sum([(c/float(total))**2 for c in counts])

###
# TODO: calculate the values below:
gini = 0  # current Gini Index using candidate name as the class

total_entries = float(total_entries)
gini = get_gini(items_per_name.values(), total_entries)

split_gini = 0  # weighted average of the Gini Indexes using candidate names, split up by zip code

for info in ipn_per_zip.values():
    temp_total = float(info['total'])
    temp_gini = get_gini(info['ipns'].values(), temp_total)
    split_gini += temp_gini * temp_total / total_entries

##/

print "Gini Index: %s" % gini
print "Gini Index after split: %s" % split_gini


#################### Extra credit
### I will be finding the best 2-way split for donation amount.
### Best split = one with the smallest weighted average gini index
### 2-way split will be based on <= test on one number

splits = set(splits)
splits = list(splits)
splits.sort()

split1 = {'total':0, 'ipns':{}}
split2 = {'total':0, 'ipns':{}}

for info in ipn_per_contrib.values():
    split2['total'] += info['total']
    for name, count in info['ipns'].iteritems():
        if name not in split2['ipns']:
            split2['ipns'][name] = 0
        split2['ipns'][name] += count

def get_split_gini(s1, s2, total):
    split1_gini = get_gini(s1['ipns'].values(), s1['total'])
    split2_gini = get_gini(s2['ipns'].values(), s2['total'])
    wa_gini = split1_gini * s1['total'] + split2_gini * s2['total']
    wa_gini = wa_gini / float(total)
    return wa_gini

lowest_gini_so_far = get_split_gini(split1, split2, total_entries)

print(repr(splits[:20]))
best_split_so_far = float(splits[0]) - 1

for split in splits:
    # every pair that has contrib = split will be moved from split2 to split1
    total_to_move = ipn_per_contrib[split]['total']
    ipns_to_move = ipn_per_contrib[split]['ipns']
    split2['total'] -= total_to_move
    split1['total'] += total_to_move
    for name, count in ipns_to_move.iteritems():
        split2['ipns'][name] -= count
        if name not in split1['ipns']:
            split1['ipns'][name] = 0
        split1['ipns'][name] += count
    new_gini = get_split_gini(split1, split2, total_entries)
    if (new_gini < lowest_gini_so_far):
        lowest_gini_so_far = new_gini
        best_split_so_far = split

print "Best split for contribution amount: split1 has <= %(a)s and split2 has > %(a)s" % {'a':best_split_so_far}
print "This gave a gini of: %s" % lowest_gini_so_far

