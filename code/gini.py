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

############### Read through files
for row in csv.reader(fileinput.input()):
    if not fileinput.isfirstline():
        ###
        # TODO: replace line below with steps to save information to calculate
        # Gini Index
        name = row[cand_nm]
        zipc = row[contbr_zip]
        if zipc not in ipn_per_zip:
            ipn_per_zip[zipc] = {'total':0, 'ipns': {}}
        if name not in items_per_name:
            items_per_name[name] = 0
        if name not in ipn_per_zip[zipc]['ipns']:
            ipn_per_zip[zipc]['ipns'][name] = 0
        items_per_name[name] += 1
        ipn_per_zip[zipc]['ipns'][name] += 1
        total_entries += 1
        ##/

###
# TODO: calculate the values below:
gini = 0  # current Gini Index using candidate name as the class

total_entries = float(total_entries)
gini = 1 - sum([(v/total_entries)**2 for v in items_per_name.values()])

split_gini = 0  # weighted average of the Gini Indexes using candidate names, split up by zip code

for info in ipn_per_zip.values():
    temp_total = float(info['total'])
    temp_gini = 1 - sum([(ipn/temp_total)**2 for ipn in info['ipns'].values()])
    split_gini += temp_gini * temp_total / total_entries

##/

print "Gini Index: %s" % gini
print "Gini Index after split: %s" % split_gini
