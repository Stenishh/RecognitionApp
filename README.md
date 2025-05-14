# Sistema de Reconhecimento Facial com Python e Tkinter

Este projeto é um **Sistema de Reconhecimento Facial** desenvolvido com a linguagem Python, utilizando bibliotecas poderosas como o **OpenCV**, **face_recognition**, e **Tkinter**. O objetivo é proporcionar uma interface gráfica simples e intuitiva para cadastro e reconhecimento de faces em tempo real.

## Funcionalidades

### 1. **Cadastro de Novas Pessoas**
   O sistema permite cadastrar novas pessoas por meio da captura de imagens da face. Após o cadastro, o sistema armazena as informações de face para futuras comparações.

### 2. **Reconhecimento Facial em Tempo Real**
   Ao iniciar o reconhecimento, a aplicação utiliza a webcam para capturar faces em tempo real. Se uma face cadastrada for detectada, o nome da pessoa é exibido na tela.

### 3. **Interface Gráfica Intuitiva**
   A interface gráfica foi criada utilizando a biblioteca **Tkinter**, proporcionando uma experiência amigável e fácil de navegar.

## Como Funciona

### 1. **Cadastro de Pessoas**
   - O usuário pode cadastrar uma nova pessoa clicando no botão **"Cadastrar Nova Pessoa"**.
   - O sistema pede para o usuário fornecer um nome para a pessoa.
   - Após a entrada do nome, a aplicação ativa a webcam e aguarda o usuário pressionar a tecla **Espaço** para capturar uma foto da face.
   - Caso a foto seja capturada com sucesso, a face é processada e registrada no banco de dados do sistema.

### 2. **Reconhecimento Facial**
   - O botão **"Iniciar Reconhecimento"** ativa a webcam e começa a buscar faces cadastradas no banco de dados.
   - Quando uma face é detectada e reconhecida, o nome da pessoa é exibido no vídeo em tempo real.
   - Caso uma face desconhecida seja detectada, o sistema exibe "Desconhecido".

### 3. **Saída**
   - O botão **"Sair"** fecha o programa e libera a câmera.

## Tecnologias Utilizadas

- **Python 3.x**
- **OpenCV** - Biblioteca para processamento de imagens e vídeos.
- **face_recognition** - Biblioteca especializada no reconhecimento facial.
- **Tkinter** - Biblioteca para criação da interface gráfica.
- **Pillow** - Biblioteca para manipulação de imagens no Tkinter.

## Pré-requisitos

Antes de executar o projeto, é necessário instalar as dependências. Você pode fazer isso utilizando o `pip`:

```bash
pip install opencv-python face_recognition numpy pillow
