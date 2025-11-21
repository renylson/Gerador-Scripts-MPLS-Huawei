import re

def validar_vlan(vlan):
    """Verifica se a VLAN é um número válido."""
    return vlan.isdigit()

def validar_nome(nome):
    """Verifica se o nome não contém espaços."""
    return " " not in nome

def validar_peer(peer):
    """Verifica se o peer é um endereço IPv4 válido."""
    ipv4_pattern = re.compile(
        r"^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\."
        r"(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\."
        r"(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\."
        r"(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
    )
    return bool(ipv4_pattern.match(peer))

def obter_input():
    """Obtém e valida as entradas do usuário."""
    while True:
        vlan = input("Digite o número da VLAN: ")
        if validar_vlan(vlan):
            break
        else:
            print("VLAN inválida. Insira apenas números.")
    
    while True:
        nome = input("Digite o nome (sem espaços): ")
        if validar_nome(nome):
            break
        else:
            print("Nome inválido. Insira um nome sem espaços.")
    
    while True:
        peer_lado_a = input("Digite o endereço IP do peer (IPv4) para o LADO A: ")
        if validar_peer(peer_lado_a):
            break
        else:
            print("Peer inválido. Insira um endereço IPv4 válido para o LADO A.")
    
    while True:
        peer_lado_b = input("Digite o endereço IP do peer (IPv4) para o LADO B: ")
        if validar_peer(peer_lado_b):
            break
        else:
            print("Peer inválido. Insira um endereço IPv4 válido para o LADO B.")
    
    return vlan, nome, peer_lado_a, peer_lado_b

def gerar_script(vlan, nome, peer_lado_a, peer_lado_b):
    """Gera o script para os dois lados baseado nos inputs fornecidos."""
    script = f"""
#### LADO A ####
#
vlan {vlan}
 description MPLS_{nome}
#
vsi vlan{vlan} static
 pwsignal ldp
  vsi-id {vlan}
  peer {peer_lado_a}
#
interface Vlanif{vlan}
 description MPLS_{nome}
 l2 binding vsi vlan{vlan}
#

#### LADO B ####
#
vlan {vlan}
 description MPLS_{nome}
#
vsi vlan{vlan} static
 pwsignal ldp
  vsi-id {vlan}
  peer {peer_lado_b}
#
interface Vlanif{vlan}
 description MPLS_{nome}
 l2 binding vsi vlan{vlan}
#
"""
    return script

def salvar_script(script, nome_arquivo):
    """Salva o script em um arquivo .txt."""
    with open(nome_arquivo, 'w') as arquivo:
        arquivo.write(script)
    print(f"\nScript salvo em: {nome_arquivo}")

def main():
    vlan, nome, peer_lado_a, peer_lado_b = obter_input()
    script = gerar_script(vlan, nome, peer_lado_a, peer_lado_b)
    nome_arquivo = f"script_mpls_{nome}.txt"
    salvar_script(script, nome_arquivo)

if __name__ == "__main__":
    main()
