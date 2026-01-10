from t_tech.invest import Client
from t_tech.invest.constants import INVEST_GRPC_API_SANDBOX

from dependency_injector import containers, providers

TOKEN = "t.F2ZXN0ISrPoJ9NFG5F6fEN1z8atQj6TAuqZN26R1KJXa80V41BYEm5Ro31zDbjDx9olx8ZjSrOveJGGruAt1Vg"


with Client(TOKEN, target=INVEST_GRPC_API_SANDBOX) as client:
    print(client.users.get_accounts())
