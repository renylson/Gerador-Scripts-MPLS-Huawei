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
        vlan_inicial = input("Digite o número da VLAN inicial: ")
        if validar_vlan(vlan_inicial):
            break
        else:
            print("VLAN inválida. Insira apenas números.")
    
    while True:
        vlan_final = input("Digite o número da VLAN final: ")
        if validar_vlan(vlan_final) and int(vlan_final) >= int(vlan_inicial):
            break
        else:
            print("VLAN final inválida. Insira um número maior ou igual à VLAN inicial.")

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
    
    return int(vlan_inicial), int(vlan_final), nome, peer_lado_a, peer_lado_b

def gerar_script_lado_a(vlan, nome, peer_lado_a):
    """Gera o script para o LADO A."""
    script_a = f"""
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
"""
    return script_a

def gerar_script_lado_b(vlan, nome, peer_lado_b):
    """Gera o script para o LADO B."""
    script_b = f"""
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
    return script_b

def salvar_script(script, nome_arquivo):
    """Salva o script em um arquivo .txt."""
    with open(nome_arquivo, 'w') as arquivo:
        arquivo.write(script)
    print(f"\nScript salvo em: {nome_arquivo}")

def main():
    vlan_inicial, vlan_final, nome, peer_lado_a, peer_lado_b = obter_input()
    
    script_completo_a = ""
    script_completo_b = ""
    
    for vlan in range(vlan_inicial, vlan_final + 1):
        script_a = gerar_script_lado_a(vlan, nome, peer_lado_a)
        script_completo_a += script_a
        
        script_b = gerar_script_lado_b(vlan, nome, peer_lado_b)
        script_completo_b += script_b
    
    nome_arquivo_a = f"script_mpls_lado_a_{nome}.txt"
    nome_arquivo_b = f"script_mpls_lado_b_{nome}.txt"
    
    salvar_script(script_completo_a, nome_arquivo_a)
    salvar_script(script_completo_b, nome_arquivo_b)

if __name__ == "__main__":
    main()
