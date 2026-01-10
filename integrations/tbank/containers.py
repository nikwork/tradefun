from dependency_injector import containers, providers
from decimal import Decimal

from t_tech.invest.constants import INVEST_GRPC_API, INVEST_GRPC_API_SANDBOX
from t_tech.invest import Client, AsyncClient
from t_tech.invest.utils import decimal_to_quotation, quotation_to_decimal
from t_tech.invest import MoneyValue
from t_tech.invest.sandbox.client import SandboxClient

from integrations.common.base_client import BaseClient
from integrations.common.utils import get_bool_env_var


class ApiClient(BaseClient):
    def _get_t_invest_env_info_msg(self) -> str:
        invest_grpc_api_str = str(self._invest_grpc_api)
        env_name = "SANDBOX" if self._is_sandbox else "PROD"
        return f"Client for the env: {env_name} (target: {invest_grpc_api_str})."

    def __init__(self, api_key: str, is_sandbox: bool):
        super().__init__()
        self._api_key = api_key
        self._is_sandbox = is_sandbox
        self._invest_grpc_api = (
            INVEST_GRPC_API_SANDBOX if is_sandbox else INVEST_GRPC_API
        )
        self._api_client = self.get_new_client()

    def get_new_client(self):
        self.logger.info(f"Get new client ({self._get_t_invest_env_info_msg()})")
        return Client(self._api_key, target=self._invest_grpc_api)

    def get_async_new_client(self):
        self.logger.info(f"Get new client ({self._get_t_invest_env_info_msg()})")
        return AsyncClient(self._api_key, target=self._invest_grpc_api)

    def get_client(self):
        self.logger.info(f"Get client ({self._get_t_invest_env_info_msg()})")
        return self._api_client


class CustomClient(BaseClient):

    def _get_t_invest_env_info_msg(self) -> str:
        invest_grpc_api_str = str(self.api_client._invest_grpc_api)
        env_name = "SANDBOX" if self.api_client._is_sandbox else "PROD"
        return f"Client for the env: {env_name} (target: {invest_grpc_api_str})."

    def __init__(self, api_client: ApiClient):
        super().__init__()
        self.api_client = api_client
        self.logger.info(
            f"Init for the client id done ({self._get_t_invest_env_info_msg()})."
        )

    def get_accounts(self):
        with self.api_client.get_new_client() as client:
            return client.users.get_accounts()

    def add_money_sandbox(self, account_id, money, currency="rub"):
        """Function to add money to sandbox account."""
        money = decimal_to_quotation(Decimal(money))
        with self.api_client.get_new_client() as client:
            resp = client.sandbox.sandbox_pay_in(
                account_id=account_id,
                amount=MoneyValue(
                    units=money.units, nano=money.nano, currency=currency
                ),
            )
            return resp

    # TODO: add auto sandbox setup (https://github.com/RussianInvestments/invest-python/blob/main/examples/wiseplat_set_get_sandbox_balance.py).


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
    accounts = t_custom_client.get_accounts()
    print(accounts)

    # Add some money to the account.
    account_id = accounts.accounts[0].id
    t_custom_client.add_money_sandbox(account_id, 1_000)
    accounts = t_custom_client.get_accounts()
    print(accounts)
