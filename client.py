import grpc
import loteria_pb2
import loteria_pb2_grpc


def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = loteria_pb2_grpc.LoteriaServiceStub(channel)
        response = stub.EnviarLoteria(
            loteria_pb2.LoteriaRequest(loteria="quina", fluxo="processar", concurso=1010, total_concursos=2909, total_geral=89899))
        print("Resposta do servidor: " + response.message)


if __name__ == '__main__':
    run()
