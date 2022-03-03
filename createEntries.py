#!/usr/bin/env python
# coding: utf-8

from __future__ import print_function
from lxml import etree
#from StringIO import StringIO
import pandas as pd
import csv

NSMAP = {"xml" : 'http://www.w3.org/XML/1998/namespace/'}
#mappings_id = {}
#parse input data
term_counter = 1
df = pd.read_csv ('final.csv', sep='$', encoding='UTF-8')
#print(df)
#champs : Terme allemand;Traduction proposée;Traduction alternative;Définition;Problème traduction;Auteur;Forme rejetée
for ind in df.index:
	#print("http://saintempire.hypotheses.org/publications/glossaire/"+df['URL_ID'][ind])
	#mappings_id["http://saintempire.hypotheses.org/publications/glossaire/"+df['URL_ID'][ind]] = "#"+df['URL_ID'][ind]
	#mappings_id["https://saintempire.hypotheses.org/publications/glossaire/"+df['URL_ID'][ind]] = "#"+df['URL_ID'][ind]
	
	# prepare TEI document
	tei = etree.Element('TEI', xmlns='http://www.tei-c.org/ns/1.0')
	pi1 = etree.ProcessingInstruction('xml-model', 'href="../schemaTEI/02032022/tei_mse.rng" type="application/xml" schematypens="http://relaxng.org/ns/structure/1.0"')
	tei.addprevious(pi1)
	 
	tei_header = etree.SubElement(tei, 'teiHeader')
	filedesc = etree.SubElement(tei_header, 'fileDesc')
	file_titlestmt = etree.SubElement(filedesc, 'titleStmt')
	titlemain = etree.SubElement(file_titlestmt, 'title', type='main')
	titlemain.text = str(df['Terme allemand'][ind]).upper()
	
	##respStmt
	file_respstmt = etree.SubElement(file_titlestmt, 'respStmt')
	resp_respstmt = etree.SubElement(file_respstmt, 'resp')
	resp_respstmt.text = "Notice originalement rédigée par "
	resp_respstmt.attrib['{http://www.w3.org/XML/1998/namespace}lang'] = 'fra'
	
	if not pd.isna(df['Auteur'][ind]):
		if "|" in df['Auteur'][ind]:
			ref_list = df['Auteur'][ind].split("|")
			for rej_term in ref_list:
				author = etree.SubElement(file_titlestmt, 'author')
				author.text = rej_term
				name_respstmt = etree.SubElement(file_respstmt, 'name')
				name_respstmt.text = rej_term
				
		else:
			author = etree.SubElement(file_titlestmt, 'author')
			author.text = df['Auteur'][ind]
			name_respstmt = etree.SubElement(file_respstmt, 'name')
			name_respstmt.text = df['Auteur'][ind]
	
	file_respstmt2 = etree.SubElement(file_titlestmt, 'respStmt')
	resp_respstmt2 = etree.SubElement(file_respstmt2, 'resp')
	resp_respstmt2.text = "Notice revisée et éditée par "
	resp_respstmt2.attrib['{http://www.w3.org/XML/1998/namespace}lang'] = 'fra'
	name_respstmt2 = etree.SubElement(file_respstmt2, 'name')
	name_respstmt2.text = "FB ou CD"
	
	file_publistmt = etree.SubElement(filedesc, 'publicationStmt')
	distributor_file_publistmt = etree.SubElement(file_publistmt, 'distributor')
	distributor_file_publistmt.text = "Ecole des hautes études en sciences sociales"
	availability_file_publistmt = etree.SubElement(file_publistmt, 'availability')
	licence_availability = etree.SubElement(availability_file_publistmt, 'licence')
	licence_availability.attrib['target'] = "https://creativecommons.org/licenses/by-nc-sa/4.0/"
	licence_availability.text = "Attribution-NonCommercial-ShareAlike 4.0 International (CC-BY-SA-NC)"
	date_file_publistmt = etree.SubElement(file_publistmt, 'date')
	date_file_publistmt.text = "2022"
	date_file_publistmt.attrib['when'] = "2022"

	sourcedesc = etree.SubElement(filedesc, 'sourceDesc')
	p_sourcedesc = etree.SubElement(sourcedesc, 'p')
	p_sourcedesc.attrib['{http://www.w3.org/XML/1998/namespace}lang'] = 'fra'
	p_sourcedesc.text = "Glossaire Les mots du Saint Empire"
	
	profile_desc = etree.SubElement(tei_header, 'profileDesc')
	lang_usg = etree.SubElement(profile_desc, 'langUsage')
	language2_tag = etree.SubElement(lang_usg, 'language')
	language2_tag.attrib['ident'] = 'fra'
	language_tag = etree.SubElement(lang_usg, 'language')
	language_tag.attrib['ident'] = 'deu'
	
	
	revisiondesc = etree.SubElement(tei_header, 'revisionDesc')
	list_revisiondesc = etree.SubElement(revisiondesc, 'list')
	item1 = etree.SubElement(list_revisiondesc, 'item')
	item1.text = "2021-2022: extraction et encodage en TEI automatiques à partir du site https://saintempire.hypotheses.org/publications/glossaire/les-mots-du-saint-empire-liste-des-notices"
	item1.attrib['{http://www.w3.org/XML/1998/namespace}lang'] = 'fra'
	item2 = etree.SubElement(list_revisiondesc, 'item')
	item2.text = "2022: relecture et revision des notices"
	item2.attrib['{http://www.w3.org/XML/1998/namespace}lang'] = 'fra'
	
	tei_text = etree.SubElement(tei, 'text')
	tei_body = etree.SubElement(tei_text, 'body')

	tei_entry = etree.SubElement(tei_body, 'entry')
	tei_entry.attrib['{http://www.w3.org/XML/1998/namespace}id']= df['URL_ID'][ind].lower()
	form_entry = etree.SubElement(tei_entry, 'form')
	orth_entry = etree.SubElement(form_entry, 'orth')
	orth_entry.text = df['Terme allemand'][ind]
	orth_entry.attrib['{http://www.w3.org/XML/1998/namespace}lang'] = 'deu'
	
	cit_entry = etree.SubElement(tei_entry, 'cit')
	cit_entry.attrib['type'] = 'translation'
	cit_entry.attrib['{http://www.w3.org/XML/1998/namespace}lang'] = 'fra'
	
	if not pd.isna(df['Traduction proposée'][ind]):
		quote_entry = etree.SubElement(cit_entry, 'quote')
		quote_entry.attrib['type'] = 'ppal'
		quote_entry.text = df['Traduction proposée'][ind]

	if not pd.isna(df['Traduction alternative'][ind]):
		if "|" in df['Traduction alternative'][ind]:
			ref_list = df['Traduction alternative'][ind].split("|")
			for rej_term in ref_list:
				quote_entry_alt = etree.SubElement(cit_entry, 'quote')
				quote_entry_alt.attrib['type'] = 'variante'
				quote_entry_alt.text = rej_term
		else:
			quote_entry_alt = etree.SubElement(cit_entry, 'quote')
			quote_entry_alt.attrib['type'] = 'variante'
			quote_entry_alt.text = df['Traduction alternative'][ind]
	
	sense_entry = etree.SubElement(tei_entry, 'sense')
	
	if not pd.isna(df['Définition'][ind]):
		new = "<def>"+df['Définition'][ind]+"</def>"
		tag_new = etree.fromstring(new)
		tag_new.attrib['{http://www.w3.org/XML/1998/namespace}lang'] = 'fra'
		#print(df['Définition'][ind])
		sense_entry.append(tag_new)
		
	if not pd.isna(df['Problème traduction'][ind]):
		
		new2 = "<note>"+df['Problème traduction'][ind]+"</note>"
		tag_new2 = etree.fromstring(new2)
		tag_new2.attrib['{http://www.w3.org/XML/1998/namespace}lang'] = 'fra'
		#print(df['Problème traduction'][ind])
		sense_entry.append(tag_new2)
		
	tei_tree = etree.ElementTree(tei)
	
	for elem in tei_tree.findall("//em"):
		elem.tag = "emph"
	
	for elem in tei_tree.findall("//a"):
		#elem.
		elem.tag = "ref"
		if elem.get('title') is not None:
			del elem.attrib['title']
		if elem.get('href') is not None:
			#ptr_elem = etree.SubElement(elem, 'ptr')
			#ptr_elem.text = elem.text
			elem.attrib['target'] = elem.attrib['href']#.replace("http://saintempire.hypotheses.org/publications/glossaire/", "#").replace("https://saintempire.hypotheses.org/publications/glossaire/", "#").lower()
			del elem.attrib['href']
	
	#print(mappings_id)
	tei_tree.write("notices/mse_t_"+str(term_counter)+"_"+df['URL_ID'][ind].lower()+".xml",pretty_print=True, xml_declaration=True, encoding='UTF-8')
	term_counter = term_counter + 1