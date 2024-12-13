import pyautogui
import time
import os
from pathlib import Path
import glob
import csv
from datetime import datetime

# Configurações de segurança
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 1.0

class RegistroPartidas:
    def __init__(self):
        self.arquivo_csv = 'registro_partidas.csv'
        self.colunas = ['data', 'hora_inicio', 'duracao_segundos']
        self.criar_arquivo_se_necessario()

    def criar_arquivo_se_necessario(self):
        if not os.path.exists(self.arquivo_csv):
            with open(self.arquivo_csv, 'w', newline='') as arquivo:
                writer = csv.writer(arquivo)
                writer.writerow(self.colunas)

    def registrar_partida(self, tempo_inicio, tempo_fim):
        duracao = tempo_fim - tempo_inicio
        data_atual = datetime.now().strftime('%Y-%m-%d')
        hora_inicio = datetime.fromtimestamp(tempo_inicio).strftime('%H:%M:%S')
        
        with open(self.arquivo_csv, 'a', newline='') as arquivo:
            writer = csv.writer(arquivo)
            writer.writerow([data_atual, hora_inicio, f"{duracao:.2f}"])

class AutomacaoEmulador:
    def __init__(self):
        self.pasta_imagens = Path('imagens')
        self.confianca = 0.8
        self.registro = RegistroPartidas()

    def encontrar_e_clicar(self, nome_imagem, timeout=10):
        inicio = time.time()
        while (time.time() - inicio) < timeout:
            try:
                caminho_imagem = self.pasta_imagens / nome_imagem
                localizacao = pyautogui.locateOnScreen(
                    str(caminho_imagem),
                    confidence=self.confianca
                )
                
                if localizacao:
                    centro = pyautogui.center(localizacao)
                    pyautogui.moveTo(centro)
                    time.sleep(1)
                    pyautogui.click(centro)
                    print(f"Clicou em {nome_imagem}")
                    time.sleep(3)
                    return True
                
            except Exception as e:
                print(f"Erro ao procurar {nome_imagem}: {e}")
                
            
        print(f"Não foi possível encontrar {nome_imagem}")
        return False

    def obter_sequencia_imagens(self):
        """
        Obtém todas as imagens numeradas da pasta em ordem
        """
        padrao = self.pasta_imagens / "*.png"
        arquivos = glob.glob(str(padrao))
        # Ordena os arquivos numericamente
        arquivos.sort(key=lambda x: int(''.join(filter(str.isdigit, os.path.basename(x)))))
        return [os.path.basename(arquivo) for arquivo in arquivos]



    def jogar_partida(self):
        if not self.encontrar_e_clicar('01.iniciante.png'):
            return
        if not self.encontrar_e_clicar('02.auto-desligado.png'):
            return
        if not self.encontrar_e_clicar('04.batalhar.png'):
            return
        # esperar ate aparecer o 05.continuar.png
        while not self.encontrar_e_clicar('05.continuar.png'):
            time.sleep(1)
        if not self.encontrar_e_clicar('06.continuar.png'):
            return
        if not self.encontrar_e_clicar('07.continuar.png'):
            return
        if not self.encontrar_e_clicar('08.continuar.png'):
            return
       


    def executar_loop_infinito(self):
        """
        Executa a sequência de cliques em loop infinito
        """
        print("Iniciando automação")
        
        sequencia = self.obter_sequencia_imagens()
        print(f"Sequência detectada: {sequencia}")
        
        while True:
            inicio = time.time()
            self.jogar_partida()
            fim = time.time()
            self.registro.registrar_partida(inicio, fim)
            print("Partida finalizada")
            print(f"Tempo de duração: {fim - inicio:.2f} segundos")
            time.sleep(2)
if __name__ == "__main__":
    bot = AutomacaoEmulador()
    try:
        bot.executar_loop_infinito()
    except KeyboardInterrupt:
        print("\nPrograma interrompido pelo usuário")
