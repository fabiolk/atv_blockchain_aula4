import json
import os
from hashlib import sha256
import time

DIR_BLOCKCHAIN = 'blockchain/'#variavel globa para o nome do diretorio

        
def minera(ant_bloco,dificuldade):
    
    with open(DIR_BLOCKCHAIN + ant_bloco, 'rb') as bloco:#le no modo binario o ultimo bloco da blockchain
        
        conteudo_bloco = bloco.read()
            
    nonce = 0    
    
    while True:
        
        temp = str(conteudo_bloco)+str(nonce) 
	#guarda em uma variável reporária a concatenação do nonce e o conteudo do bloco anterior
        
        hash_bloco = sha256(temp.encode("ascii")).hexdigest()
	#sha256() create a hash object. You can now feed this object with bytes-like objects 
	#hexdigest() returned as a string object of double length, containing only hexadecimal digits.
        
        if hash_bloco.startswith("0" * int(dificuldade)):
	#verifica se o hash começa com a quantidade de zeros definidas
            
            return hash_bloco,nonce
        
        nonce += 1 #caso contrario soma 1 a nonce ate achar o hash que atenda a condicional
        
def check_integridade(dificuldade):
    
    arquivos = sorted(os.listdir(DIR_BLOCKCHAIN), key=lambda x: int(x))
	#sorted ordena os blocos
	#key determina como a lista será ordenada e converte para integer por meio da 'lambda x: int(x))'
    
    for i in arquivos[1:]: #checa a integridade a partir do bloco 2 pois o bloco 1 não tem predecessor
        
        with open(DIR_BLOCKCHAIN + i,'r') as bloco:#le cada bloco de forma crescente
            
            blocos = json.load(bloco)#blocos é uma variavel dicionário
            
            ant_hash = blocos.get('ant_bloco').get('hash')#acessa o hash do bloco anterior
            ant_nome_arq = blocos.get('ant_bloco').get('nome_arquivo')
                    
            hash_bloco,nonce = minera(ant_nome_arq,dificuldade)

            if ant_hash == hash_bloco:#compara o hash gravado com o recalculado
                res = 'ok'
            else:
                res = 'mudou'
                
            print(f'Bloco{ant_nome_arq}:{res}')#printa o numero do bloco e se ele foi alterado ou não
                 
        
def cria_bloco(remetente,destinatario,transacao,dificuldade):# função que cria, minera e grava um novo bloco

    conta_bloco = len(os.listdir(DIR_BLOCKCHAIN))#conta os blocos do diretorio blockchain
    ant_bloco = str(len(os.listdir(DIR_BLOCKCHAIN)))#transforma a contagem em string

    inicio = time.time()#incia o contador de tempo
    
    hash_bloco, nonce = minera(ant_bloco,dificuldade)#envia o numero e a dificuldade do bloco que se vai minerar

    print(time.time()-inicio)#printa o tempo total
    
    dado = {	
	"remetente": remetente,
	"destinatario": destinatario,
	"transacao": transacao,
	"ant_bloco": {
		"hash": hash_bloco,
                "nonce": nonce,
		"nome_arquivo": ant_bloco
	}  
    }

    bloco_atual = DIR_BLOCKCHAIN + str(conta_bloco + 1)#armazena o caminho do diretorio mais o nome arquivo/bloco

    with open(bloco_atual, 'w') as arquivo_json:#escreve no arquivo as informações de dados do novo bloco
        json.dump(dado, arquivo_json, indent=4, ensure_ascii=False)
        arquivo_json.write('\n')

def cria_prim_bloco():#função cria bloco origem
    
    dado = {	
	"remetente": "primeiro bloco",
	"destinatario": "primeiro bloco",
	"transacao": "zero",
	"ant_bloco": {
		"hash": "0",
                "nonce": "0",
		"nome_arquivo": "origem"
	}
    }
    with open('blockchain/1', 'w') as arquivo_json:# abre o arquivo como escrita e salva em 'arquivo_json'
        json.dump(dado, arquivo_json, indent=4, ensure_ascii=False)#Serialize obj as a JSON formatted stream
        #ensure_ascii=False these characters will be output as-is
        #indent=4 Using a positive integer indent indents that many spaces per level
        arquivo_json.write('\n')#sistemas unix os aqriquivos devem terminar com uma nova linha
        
def menu():
    print("\n")#função printa menu
    print("Digite 1 criar blockchain")
    print("Digite 2 adiciona bloco")
    print("Digite 3 checa integridade")
    print("Digite 0 sair\n")
        
def main():
    
    menu()#função printa menu
    op = int(input("Digite a opção: "))
    
    while op != 0:#laço de repetição para chamada das funções
        
        if op == 1:
            cria_prim_bloco()#função cria bloco origem
            print('Primeiro bloco criado')
            
        elif op == 2:#função cria blocos 
            
            remetente = input("Digite remetente: ")
            destinatario = input("Digite destinatario: ")
            transacao = input("Digite transacao: ")
            dificuldade = input("Digite a dificuldade: ")
            cria_bloco(remetente,destinatario,transacao,dificuldade)
            #cria_bloco(remetente='fa',destinatario='sop',transacao='mil', dificuldade=5)
            
        elif op == 3:
            
	    dificuldade = input("Digite a dificuldade: ")
            check_integridade(dificuldade)#função que verifica se as informações dos blocos não forma alteradas
            
        else:
            print('Opção inválida')
            break
        
        menu()
        op = int(input("Digite a opção: "))            

if __name__ == '__main__':
    main()
