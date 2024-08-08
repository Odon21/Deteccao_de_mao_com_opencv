import subprocess

def get_volume():
    # Obtém o volume atual
    result = subprocess.run(['pactl', 'get-sink-volume', '@DEFAULT_SINK@'], capture_output=True, text=True)
    output = result.stdout.strip()
    volume_str = output.split()[4]  # O volume está na quinta posição
    volume_int = int(volume_str.replace('%', ''))  # Remove '%' e converte para inteiro
    return volume_int

def set_volume(volume):
    # Define o volume, onde volume é um número inteiro
    volume_str = f'{volume}%'  # Converte o inteiro para string com '%'
    subprocess.run(['pactl', 'set-sink-volume', '@DEFAULT_SINK@', volume_str])

def main():
    # Obtém e imprime o volume atual
    current_volume = get_volume()
    #print(f'Volume atual: {current_volume}%')

    # Define um novo volume
    new_volume = 50  # Defina o volume desejado como um número inteiro
    set_volume(new_volume)
    #print(f'Volume definido para: {new_volume}%')

if __name__ == '__main__':
    main()

#set_volume(89)
