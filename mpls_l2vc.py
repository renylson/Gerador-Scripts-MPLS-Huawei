import re
from datetime import datetime

# Função para validar o número da VLAN
def validar_vlan(vlan):
    return vlan.isdigit() and 1 <= int(vlan) <= 4095

# Solicitar informações ao usuário
while True:
    vlan = input("Digite o número da VLAN (1-4095): ")
    if validar_vlan(vlan):
        break
    else:
        print("Número da VLAN inválido. Deve ser um número entre 1 e 4095.")

nome_circuito = input("Digite o nome do circuito: ")
lado_a = input("Digite o nome do peer do lado A: ")
lado_b = input("Digite o nome do peer do lado B: ")

# Gerar o conteúdo do arquivo
conteudo = f"""#
vlan {vlan}
 description MPLS_{nome_circuito} 
#
# Aplicar do lado A
#
interface Vlanif{vlan}
 description MPLS_{nome_circuito} 
 mpls l2vc pw-template {lado_b} {vlan} 
#
# Aplicar do lado B
#
interface Vlanif{vlan}
 description MPLS_{nome_circuito} 
 mpls l2vc pw-template {lado_a} {vlan} 
#
"""

# Obter data e hora atuais
data_hora_atual = datetime.now()
data_str = data_hora_atual.strftime("%Y%m%d")
hora_str = data_hora_atual.strftime("%H%M%S")

# Definir o nome do arquivo de saída
nome_arquivo = f"MPLS_L2VC_VLAN_{vlan}_{lado_a}_x_{lado_b}_{data_str}_{hora_str}.txt"

# Escrever o conteúdo no arquivo .txt
with open(nome_arquivo, 'w') as arquivo:
    arquivo.write(conteudo)

print(f"Arquivo '{nome_arquivo}' gerado com sucesso!")
