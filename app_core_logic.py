import uuid

import streamlit as st
import shutil
import zipfile
import os

from pathlib import Path
from encode import encode_known_faces
from detector import process_all_images

TRAINING_DIR = Path("training")
DETECT_DIR = Path("images_to_detect")
OUTPUT_IDENTIFIED_PATH = Path("output/identified_photos")

TRAINING_DIR.mkdir(exist_ok=True)
DETECT_DIR.mkdir(exist_ok=True)
OUTPUT_IDENTIFIED_PATH.mkdir(parents=True, exist_ok=True)

def listar_recursivo(path):
    itens = []
    for root, dirs, files in os.walk(path):
        nivel = root.replace(path, '').count(os.sep)
        indent = ' ' * 4 * nivel  # indentação visual
        itens.append(f"{indent}{os.path.basename(root)}/")
        subindent = ' ' * 4 * (nivel + 1)
        for f in files:
            itens.append(f"{subindent}{f}")
    return itens


def main_logic():
    # ===============================
    # SEÇÃO 1: Adicionar fotos de treino
    # ===============================
    st.header("1️⃣ Adicionar Fotos de Treinamento")

    nome = st.text_input("Nome do Aluno")
    uploaded_training_files = st.file_uploader(
        "Envie fotos para treinamento (uma ou mais)",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True
    )

    if st.button("Salvar Fotos de Treinamento"):
        if not nome.strip():
            st.error("Por favor, digite o nome do aluno.")
        elif not uploaded_training_files:
            st.error("Por favor, envie pelo menos uma foto.")
        else:
            pasta_aluno = TRAINING_DIR / nome.strip()
            pasta_aluno.mkdir(exist_ok=True)
            for file in uploaded_training_files:
                ext = Path(file.name).suffix  # mantém a extensão original
                random_name = f"{uuid.uuid4().hex}{ext}"
                file_path = pasta_aluno / random_name
                with open(file_path, "wb") as f:
                    f.write(file.getbuffer())
            st.success(f"{len(uploaded_training_files)} fotos salvas para o aluno {nome}.")
    # ===============================
    # SEÇÃO 2: Gerar/Atualizar codificações
    # ===============================

    if st.button('Listar pastas de treinamento'):
        training_path = 'training'
        if os.path.exists(training_path) and os.path.isdir(training_path):
            conteudo = listar_recursivo(training_path)
            if conteudo:
                # junta tudo numa única string com quebras de linha
                texto_completo = "\n".join(conteudo)
                # mostra com markdown em bloco de código para preservar indentação
                st.markdown(f"```\n{texto_completo}\n```")
            else:
                st.write("A pasta training está vazia.")
        else:
            st.write("A pasta training não foi encontrada.")

    st.header("2️⃣ Gerar/Atualizar Codificações")

    if st.button("Executar Codificação"):
        encode_known_faces()
        st.success("Codificações atualizadas com sucesso!")

    # ===============================
    # SEÇÃO 3: Detectar rostos
    # ===============================
    st.header("3️⃣ Detectar Rostos em Fotos")

    uploaded_detect_files = st.file_uploader(
        "Envie fotos para detecção",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True,
        key="detect"
    )

    if st.button("Executar Detecção"):
        # Limpar pasta anterior de resultados
        shutil.rmtree(OUTPUT_IDENTIFIED_PATH)
        OUTPUT_IDENTIFIED_PATH.mkdir(parents=True, exist_ok=True)

        # Salvar fotos enviadas
        for file in uploaded_detect_files:
            file_path = DETECT_DIR / file.name
            with open(file_path, "wb") as f:
                f.write(file.getbuffer())

        # Executar detecção
        process_all_images()

        # Criar ZIP com resultados
        zip_filename = "fotos_identificadas.zip"
        zip_filepath = Path(zip_filename)
        with zipfile.ZipFile(zip_filepath, "w") as zipf:
            for file in OUTPUT_IDENTIFIED_PATH.glob("*"):
                zipf.write(file, arcname=file.name)

        # Botão para download
        with open(zip_filepath, "rb") as f:
            st.download_button(
                label="📥 Baixar Fotos Identificadas (ZIP)",
                data=f,
                file_name=zip_filename,
                mime="application/zip"
            )

        st.success("Detecção concluída! Baixe os resultados acima.")

# testando
if __name__ == '__main__':
    main_logic()