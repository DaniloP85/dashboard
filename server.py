import logging
from concurrent import futures
import grpc
import loteria_pb2
import loteria_pb2_grpc
import threading
import streamlit as st

# Lista para armazenar as mensagens recebidas e os dados de progresso
mensagens = []

class LoteriaServiceServicer(loteria_pb2_grpc.LoteriaServiceServicer):
    def EnviarLoteria(self, request, context):
        mensagem = {
            "loteria": request.loteria,
            "concurso": request.concurso,
            "fluxo": request.fluxo, # "processar
            "total_concursos": request.total_concursos,
            "total_geral": request.total_geral
        }
        mensagens.append(mensagem)
        return loteria_pb2.LoteriaResponse(message="Informações recebidas com sucesso")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    loteria_pb2_grpc.add_LoteriaServiceServicer_to_server(LoteriaServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

def run_streamlit():
    st.title('Servidor gRPC - Informações Recebidas')

    progress_bars = {}

    while True:
        if mensagens:
            for msg in mensagens:
                loteria = msg["loteria"]
                concurso = msg["concurso"]
                total_concursos = msg["total_concursos"]
                progresso = concurso / total_concursos if total_concursos != 0 else 0

                if loteria not in progress_bars:
                    progress_bars[loteria] = st.progress(0, f"{loteria}")

                progress_bars[loteria].progress(progresso, f"{loteria}: {concurso}/{total_concursos} ({progresso:.2%})")
                logging.basicConfig(level=logging.INFO,
                                    format='%(loteria)s - %(concurso)s',
                                    datefmt='%Y-%m-%d %H:%M:%S')
            mensagens.clear()

if __name__ == '__main__':
    grpc_thread = threading.Thread(target=serve, daemon=True)
    grpc_thread.start()
    run_streamlit()