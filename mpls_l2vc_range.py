import re
from datetime import datetime

# Função para validar o número da VLAN
def validar_vlan(vlan):
    return vlan.isdigit() and 1 <= int(vlan) <= 4095

# Solicitar informações ao usuário
while True:
    vlan_inicio = input("Digite o número da VLAN inicial (1-4095): ")
    vlan_fim = input("Digite o número da VLAN final (1-4095): ")
    
    if validar_vlan(vlan_inicio) and validar_vlan(vlan_fim):
        vlan_inicio = int(vlan_inicio)
        vlan_fim = int(vlan_fim)
        
        if vlan_inicio <= vlan_fim:
            break
        else:
            print("A VLAN inicial deve ser menor ou igual à VLAN final.")
    else:
        print("Número de VLAN inválido. Deve ser um número entre 1 e 4095.")

nome_circuito = input("Digite o nome do circuito: ")
lado_a = input("Digite o nome do peer do lado A: ")
lado_b = input("Digite o nome do peer do lado B: ")

# Gerar o conteúdo das VLANs
conteudo_vlan = ""
for vlan in range(vlan_inicio, vlan_fim + 1):
    conteudo_vlan += f"""#
vlan {vlan}
 description MPLS_{nome_circuito} 
#
"""

# Gerar o conteúdo do lado A
conteudo_lado_a = ""
for vlan in range(vlan_inicio, vlan_fim + 1):
    conteudo_lado_a += f"""#
# Aplicar do lado A
#
interface Vlanif{vlan}
 description MPLS_{nome_circuito} 
 mpls l2vc pw-template {lado_b} {vlan} 
#
"""

# Gerar o conteúdo do lado B
conteudo_lado_b = ""
for vlan in range(vlan_inicio, vlan_fim + 1):
    conteudo_lado_b += f"""#
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
nome_arquivo = f"MPLS_L2VC_VLAN_{vlan_inicio}-{vlan_fim}_{lado_a}_x_{lado_b}_{data_str}_{hora_str}.txt"

# Unir todo o conteúdo (VLANs primeiro, lado A e depois lado B)
conteudo_final = conteudo_vlan + conteudo_lado_a + conteudo_lado_b

# Escrever o conteúdo no arquivo .txt
with open(nome_arquivo, 'w') as arquivo:
    arquivo.write(conteudo_final)

print(f"Arquivo '{nome_arquivo}' gerado com sucesso!")
