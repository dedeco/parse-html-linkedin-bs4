import csv
import os
import codecs
import chardet

from bs4 import BeautifulSoup

from os import listdir
from os.path import isfile, join

from utils import limpa_unicode

MYPATH = '/Users/dedeco/Projetos/parse-html/linkedin-profiles'

def parse_html():

	profiles = []

	files = [f for f in listdir(MYPATH) if isfile(join(MYPATH, f))]

	for file in files:

		name, extension = os.path.splitext(file)

		if extension == ".html":

			print ("lendo arquivo", file)

			with open(join(MYPATH, file), 'r', encoding='latin-1') as myfile:
				pagina = myfile.read()

			soup = BeautifulSoup(pagina, 'html.parser')
			
			nome = soup.find("h1",attrs={"id": "name"}).text
			#print (nome)

			try:
				div_des = soup.find("div", attrs={"class": "description"} )
				ps = div_des.find_all("p")
				resumo = ''
				for p in ps:
					resumo += resumo + p.text
				#print (resumo)
			except AttributeError:
				resumo = None
				pass	

			ul = soup.find("ul",attrs={"class": "positions"})
			
			experencias = []
			if ul:
				for li in ul.children:
					exps = {}
					exps[u'cargo'] = li.h4.text
					try:
						exps[u'desc_exp'] = li.p.text
					except AttributeError:
						exps[u'desc_exp'] = ''
						pass 
					experencias.append(exps)

			profiles.append((nome,resumo,experencias))

		export_to_csv(profiles)
		print (profiles)

def export_to_csv(profiles):

	print(u'Exportando para csv...')

	file = './nome_resumo.csv'	
	header = ["nome", "resumo"]
	with open(file, 'w', encoding='utf-8') as csvfile:
		outcsv = csv.writer(csvfile, delimiter=',',quotechar='"', quoting = csv.QUOTE_MINIMAL)
		outcsv.writerow(header)    

		for nome,resumo,exp in profiles:
			outcsv.writerow([nome,resumo])    

	file = './nome_experiencia.csv'	
	header = ["nome", "cargo", u"descrição"]
	with open(file, 'w', encoding='utf-8') as csvfile:
		outcsv = csv.writer(csvfile, delimiter=',',quotechar='"', quoting = csv.QUOTE_MINIMAL)
		outcsv.writerow(header)    

		for nome,resumo,experencias in profiles:
			for exp in experencias:
				outcsv.writerow([nome,exp['cargo'],exp['desc_exp']])    

if __name__ == "__main__":
	parse_html()
