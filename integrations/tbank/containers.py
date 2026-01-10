from dependency_injector import containers, providers

from t_tech.invest.constants import INVEST_GRPC_API, INVEST_GRPC_API_SANDBOX
from t_tech.invest import Client

from integrations.common.base_client import BaseClient
from integrations.common.utils import get_bool_env_var


class ApiClient:
    def __init__(self, api_key: str, is_sandbox: bool):
        self._api_key = api_key
        self._is_sandbox = is_sandbox
        self._invest_grpc_api = (
            INVEST_GRPC_API_SANDBOX if is_sandbox else INVEST_GRPC_API
        )
        self._api_client = self.get_new_client()

    def get_new_client(self):
        return Client(self._api_key, target=self._invest_grpc_api)

    def get_client(self):
        return self._api_client


class CustomClient(BaseClient):
    def __init__(self, api_client: ApiClient):
        self.api_client = api_client

    def get_accounts(self):
        with self.api_client.get_new_client() as client:
            return client.users.get_accounts()


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    api_client = providers.Singleton(
        ApiClient, api_key=config.api_key, is_sandbox=config.is_sandbox
    )

    custom_client = providers.Factory(CustomClient, api_client=api_client)


def get_t_custom_client_from_envs() -> CustomClient:
    container = Container()
    container.check_dependencies()
    t_is_sandbox = get_bool_env_var("T_IS_SANDBOX")
    container.config.api_key.from_env("T_INVEST_API", required=True)
    container.config.is_sandbox.from_value(t_is_sandbox)
    custom_client = container.custom_client()
    return custom_client


if __name__ == "__main__":
    from dotenv import load_dotenv

    # Load variables from .env file
    load_dotenv()
    t_custom_client = get_t_custom_client_from_envs()
    print(t_custom_client.get_accounts())
