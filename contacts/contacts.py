#!/usr/bin/python

"""Skript zum Erstellen einer csv-Datei mit DLLP-Adressen

Importieren von Kontakten aus Nextcloud Contact als vcard
Filtern nach Domänen, die mehr als n Adressen enthalten
manuell Hinzufügen von Domains in 'manuel_domains'
"""

import csv
from collections import Counter
import vobject

# Pfad zu deiner .vcf-Datei
VCF_PATH = './z-server-generated--system-2023-12-13.vcf'

# Pfad zur Ausgabedatei
CSV_PATH = './contacts.csv'

# Mindestanzahl der E-Mail-Adressen je Domain
MIND_ANZAHL_ADRESSEN = 13

# Manuell hinzuzufügende Domains
manual_domains = ['dllp.schule']


# Funktion zum Extrahieren der Domain aus einer E-Mail-Adresse
def get_domain(email):
    return email.split('@')[-1]


# Domains zählen
domain_counts = Counter()

with open(VCF_PATH, 'r') as vcf_file:
    for vcard in vobject.readComponents(vcf_file):
        if hasattr(vcard, 'email'):
            email = vcard.email.value
            domain = get_domain(email)
            domain_counts[domain] += 1

# CSV-Datei erstellen
with open(CSV_PATH, 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['Name', 'Email'])  # Header

    with open(VCF_PATH, 'r') as vcf_file:
        for vcard in vobject.readComponents(vcf_file):
            if hasattr(vcard, 'fn') and hasattr(vcard, 'email'):
                name = vcard.fn.value
                email = vcard.email.value
                domain = get_domain(email)
                # Schreibe nur E-Mail-Adressen in CSV, deren Domain ≥ n hat
                # oder manuell hinzugefügt wurde
                if domain_counts[domain] >= MIND_ANZAHL_ADRESSEN \
                   or domain in manual_domains:
                    writer.writerow([name, email])
