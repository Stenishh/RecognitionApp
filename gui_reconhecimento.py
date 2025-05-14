import tkinter as tk
from tkinter import simpledialog, messagebox
import cv2
import face_recognition
import os
import numpy as np
from PIL import Image, ImageTk

class FaceRecognitionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Reconhecimento Facial")
        self.root.geometry("800x600")  # Define o tamanho da janela
        self.root.configure(bg="#f0f0f0")  # Define a cor de fundo
        self.diretorio_pessoas = "pessoas"
        self.encodings_conhecidos = []
        self.nomes_conhecidos = []
        self.video_capture = None

        # Configurações da interface
        self.setup_ui()

        # Carrega imagens conhecidas
        self.carregar_imagens_conhecidas()

    def setup_ui(self):
        # Título
        titulo = tk.Label(self.root, text="Sistema de Reconhecimento Facial", font=("Helvetica", 20, "bold"), bg="#f0f0f0")
        titulo.pack(pady=20)

        # Botões principais
        botoes_frame = tk.Frame(self.root, bg="#f0f0f0")
        botoes_frame.pack(pady=20)

        btn_cadastrar = tk.Button(botoes_frame, text="Cadastrar Nova Pessoa", font=("Helvetica", 14), bg="#4CAF50", fg="white", width=20, command=self.cadastrar_pessoa)
        btn_cadastrar.grid(row=0, column=0, padx=10, pady=10)

        btn_reconhecer = tk.Button(botoes_frame, text="Iniciar Reconhecimento", font=("Helvetica", 14), bg="#2196F3", fg="white", width=20, command=self.iniciar_reconhecimento)
        btn_reconhecer.grid(row=0, column=1, padx=10, pady=10)

        btn_sair = tk.Button(botoes_frame, text="Sair", font=("Helvetica", 14), bg="#f44336", fg="white", width=20, command=self.sair)
        btn_sair.grid(row=0, column=2, padx=10, pady=10)

        # Área de exibição de vídeo
        self.video_label = tk.Label(self.root, bg="#000000", width=800, height=400)
        self.video_label.pack(pady=20)

    def carregar_imagens_conhecidas(self):
        if not os.path.exists(self.diretorio_pessoas):
            os.makedirs(self.diretorio_pessoas)
            messagebox.showinfo("Informação", f"Diretório '{self.diretorio_pessoas}' criado. Adicione imagens e reinicie o programa.")
            return

        for arquivo in os.listdir(self.diretorio_pessoas):
            if arquivo.endswith(('.jpg', '.jpeg', '.png', '.webp')):
                caminho_completo = os.path.join(self.diretorio_pessoas, arquivo)
                nome_pessoa = os.path.splitext(arquivo)[0]

                try:
                    imagem = face_recognition.load_image_file(caminho_completo)
                    face_locations = face_recognition.face_locations(imagem)

                    if len(face_locations) > 0:
                        encoding = face_recognition.face_encodings(imagem, [face_locations[0]])[0]
                        self.encodings_conhecidos.append(encoding)
                        self.nomes_conhecidos.append(nome_pessoa)
                except Exception as e:
                    print(f"Erro ao carregar {arquivo}: {e}")

    def cadastrar_pessoa(self):
        nome_pessoa = simpledialog.askstring("Cadastro", "Digite o nome da pessoa:")
        if not nome_pessoa:
            return

        # Inicializa a webcam para capturar a foto
        video_capture = cv2.VideoCapture(0)
        if not video_capture.isOpened():
            messagebox.showerror("Erro", "Não foi possível acessar a webcam.")
            return

        messagebox.showinfo("Instrução", "Aperte 'Espaço' para capturar a foto ou 'Esc' para cancelar.")
        while True:
            ret, frame = video_capture.read()
            if not ret:
                break

            cv2.imshow("Captura de Foto", frame)
            key = cv2.waitKey(1) & 0xFF

            if key == 27:  # Esc para cancelar
                video_capture.release()
                cv2.destroyAllWindows()
                return
            elif key == 32:  # Espaço para capturar
                caminho_arquivo = os.path.join(self.diretorio_pessoas, f"{nome_pessoa}.jpg")
                cv2.imwrite(caminho_arquivo, frame)
                video_capture.release()
                cv2.destroyAllWindows()
                break

        # Processa a imagem capturada
        imagem = face_recognition.load_image_file(caminho_arquivo)
        face_locations = face_recognition.face_locations(imagem)

        if len(face_locations) == 0:
            messagebox.showerror("Erro", "Nenhuma face detectada na imagem. Tente novamente.")
            os.remove(caminho_arquivo)
            return

        encoding = face_recognition.face_encodings(imagem, [face_locations[0]])[0]
        self.encodings_conhecidos.append(encoding)
        self.nomes_conhecidos.append(nome_pessoa)
        messagebox.showinfo("Sucesso", f"Pessoa '{nome_pessoa}' cadastrada com sucesso!")

    def iniciar_reconhecimento(self):
        if not self.encodings_conhecidos:
            messagebox.showwarning("Aviso", "Nenhuma pessoa cadastrada. Cadastre alguém primeiro.")
            return

        self.video_capture = cv2.VideoCapture(0)
        self.atualizar_video()

    def atualizar_video(self):
        ret, frame = self.video_capture.read()
        if not ret:
            return

        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(self.encodings_conhecidos, face_encoding)
            name = "Desconhecido"

            if True in matches:
                face_distances = face_recognition.face_distance(self.encodings_conhecidos, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = self.nomes_conhecidos[best_match_index]

            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 255, 255), 1)

        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        imgtk = ImageTk.PhotoImage(image=img)
        self.video_label.imgtk = imgtk
        self.video_label.configure(image=imgtk)

        self.root.after(10, self.atualizar_video)

    def sair(self):
        if self.video_capture:
            self.video_capture.release()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = FaceRecognitionApp(root)
    root.mainloop()
