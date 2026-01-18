"""
T-Bank Invest API: InstrumentsService Complete Wrapper

This module provides comprehensive synchronous and asynchronous wrappers for
all T-Bank Invest API InstrumentsService endpoints.

API Documentation: https://developer.tbank.ru/invest/api/instruments-service
"""

from datetime import datetime
from typing import Optional, Dict, Any, List, Union
from enum import Enum
import httpx
import requests
from dataclasses import dataclass


# ============================================================================
# ENUMS
# ============================================================================

class InstrumentStatus(Enum):
    """Instrument status"""
    INSTRUMENT_STATUS_UNSPECIFIED = "INSTRUMENT_STATUS_UNSPECIFIED"
    INSTRUMENT_STATUS_BASE = "INSTRUMENT_STATUS_BASE"
    INSTRUMENT_STATUS_ALL = "INSTRUMENT_STATUS_ALL"


class InstrumentIdType(Enum):
    """Instrument identifier type"""
    INSTRUMENT_ID_UNSPECIFIED = "INSTRUMENT_ID_UNSPECIFIED"
    INSTRUMENT_ID_TYPE_FIGI = "INSTRUMENT_ID_TYPE_FIGI"
    INSTRUMENT_ID_TYPE_TICKER = "INSTRUMENT_ID_TYPE_TICKER"
    INSTRUMENT_ID_TYPE_UID = "INSTRUMENT_ID_TYPE_UID"
    INSTRUMENT_ID_TYPE_POSITION_UID = "INSTRUMENT_ID_TYPE_POSITION_UID"


class InstrumentType(Enum):
    """Instrument type"""
    INSTRUMENT_TYPE_UNSPECIFIED = "INSTRUMENT_TYPE_UNSPECIFIED"
    INSTRUMENT_TYPE_BOND = "INSTRUMENT_TYPE_BOND"
    INSTRUMENT_TYPE_SHARE = "INSTRUMENT_TYPE_SHARE"
    INSTRUMENT_TYPE_CURRENCY = "INSTRUMENT_TYPE_CURRENCY"
    INSTRUMENT_TYPE_ETF = "INSTRUMENT_TYPE_ETF"
    INSTRUMENT_TYPE_FUTURES = "INSTRUMENT_TYPE_FUTURES"
    INSTRUMENT_TYPE_SP = "INSTRUMENT_TYPE_SP"
    INSTRUMENT_TYPE_OPTION = "INSTRUMENT_TYPE_OPTION"


class AssetType(Enum):
    """Asset type"""
    ASSET_TYPE_UNSPECIFIED = "ASSET_TYPE_UNSPECIFIED"
    ASSET_TYPE_CURRENCY = "ASSET_TYPE_CURRENCY"
    ASSET_TYPE_COMMODITY = "ASSET_TYPE_COMMODITY"
    ASSET_TYPE_INDEX = "ASSET_TYPE_INDEX"
    ASSET_TYPE_SECURITY = "ASSET_TYPE_SECURITY"


class CouponType(Enum):
    """Bond coupon type"""
    COUPON_TYPE_UNSPECIFIED = 0
    COUPON_TYPE_CONSTANT = 1
    COUPON_TYPE_FLOATING = 2
    COUPON_TYPE_DISCOUNT = 3
    COUPON_TYPE_MORTGAGE = 4
    COUPON_TYPE_FIX = 5
    COUPON_TYPE_VARIABLE = 6
    COUPON_TYPE_OTHER = 7


# ============================================================================
# DATA CLASSES
# ============================================================================

@dataclass
class MoneyValue:
    """Monetary value representation"""
    currency: str
    units: int
    nano: int
    
    def to_decimal(self) -> float:
        """Convert to decimal representation"""
        return float(self.units) + float(self.nano) / 1_000_000_000
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MoneyValue':
        """Create from dictionary"""
        return cls(
            currency=data.get('currency', ''),
            units=int(data.get('units', 0)),
            nano=int(data.get('nano', 0))
        )


@dataclass
class Quotation:
    """Quotation value"""
    units: int
    nano: int
    
    def to_decimal(self) -> float:
        """Convert to decimal"""
        return float(self.units) + float(self.nano) / 1_000_000_000
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Quotation':
        """Create from dictionary"""
        return cls(
            units=int(data.get('units', 0)),
            nano=int(data.get('nano', 0))
        )


# ============================================================================
# EXCEPTIONS
# ============================================================================

class TBankInvestAPIError(Exception):
    """Base exception for T-Bank Invest API errors"""
    pass


# ============================================================================
# BASE CLIENT
# ============================================================================

class BaseInstrumentsClient:
    """Base client with common functionality"""
    
    BASE_URL = "https://invest-public-api.tbank.ru/rest"
    SERVICE_PATH = "/tinkoff.public.invest.api.contract.v1.InstrumentsService"
    
    @staticmethod
    def _format_datetime(dt: Optional[datetime]) -> Optional[str]:
        """Format datetime for API"""
        if dt is None:
            return None
        return dt.isoformat().replace('+00:00', 'Z')
    
    @staticmethod
    def _parse_datetime(dt_str: Optional[str]) -> Optional[datetime]:
        """Parse datetime from API"""
        if not dt_str:
            return None
        return datetime.fromisoformat(dt_str.replace('Z', '+00:00'))


# ============================================================================
# SYNCHRONOUS CLIENT
# ============================================================================

class InstrumentsService(BaseInstrumentsClient):
    """
    Synchronous client for T-Bank Invest InstrumentsService API.
    
    Provides access to all 40 InstrumentsService endpoints for working with
    financial instruments (bonds, shares, ETFs, currencies, futures, etc.)
    
    Usage:
        client = InstrumentsService(token="your_api_token")
        bonds = client.bonds()
        shares = client.shares()
        client.close()
        
    Or with context manager:
        with InstrumentsService(token="your_token") as client:
            bonds = client.bonds()
    """
    
    def __init__(self, token: str, timeout: float = 30.0):
        """
        Initialize the client.
        
        Args:
            token: Bearer API token for authorization
            timeout: Request timeout in seconds (default: 30.0)
        """
        self.token = token
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        })
    
    def _request(self, endpoint: str, payload: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Make API request.
        
        Args:
            endpoint: Endpoint name (e.g., "Bonds")
            payload: Request payload
            
        Returns:
            Response data as dictionary
            
        Raises:
            TBankInvestAPIError: If request fails
        """
        url = f"{self.BASE_URL}{self.SERVICE_PATH}/{endpoint}"
        
        try:
            response = self.session.post(
                url,
                json=payload or {},
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.HTTPError as e:
            error_msg = f"HTTP error: {e}"
            if e.response is not None:
                try:
                    error_data = e.response.json()
                    error_msg = f"API error: {error_data}"
                except ValueError:
                    error_msg = f"HTTP {e.response.status_code}: {e.response.text}"
            raise TBankInvestAPIError(error_msg) from e
        except requests.exceptions.RequestException as e:
            raise TBankInvestAPIError(f"Request failed: {e}") from e
    
    # ========================================================================
    # BONDS
    # ========================================================================
    
    def bonds(
        self,
        instrument_status: InstrumentStatus = InstrumentStatus.INSTRUMENT_STATUS_UNSPECIFIED
    ) -> Dict[str, Any]:
        """
        Get list of bonds.
        
        Args:
            instrument_status: Status of requested instruments
            
        Returns:
            Dictionary with bonds list
        """
        payload = {'instrumentStatus': instrument_status.value}
        return self._request('Bonds', payload)
    
    def bond_by(
        self,
        id_type: InstrumentIdType,
        class_code: Optional[str] = None,
        id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get bond by identifier.
        
        Args:
            id_type: Type of instrument identifier
            class_code: Class code (required for ticker type)
            id: Instrument identifier
            
        Returns:
            Dictionary with bond information
        """
        payload = {'idType': id_type.value}
        if class_code:
            payload['classCode'] = class_code
        if id:
            payload['id'] = id
        return self._request('BondBy', payload)
    
    def get_bond_coupons(
        self,
        instrument_id: str,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """
        Get bond coupon payment schedule.
        
        Args:
            instrument_id: Instrument identifier (figi or instrument_uid)
            from_date: Start of period (UTC)
            to_date: End of period (UTC)
            
        Returns:
            Dictionary with coupon events
        """
        payload = {'instrumentId': instrument_id}
        if from_date:
            payload['from'] = self._format_datetime(from_date)
        if to_date:
            payload['to'] = self._format_datetime(to_date)
        return self._request('GetBondCoupons', payload)
    
    def get_bond_events(
        self,
        instrument_id: str,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None,
        event_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get bond events.
        
        Args:
            instrument_id: Instrument identifier
            from_date: Start of period
            to_date: End of period
            event_type: Event type filter
            
        Returns:
            Dictionary with bond events
        """
        payload = {'instrumentId': instrument_id}
        if from_date:
            payload['from'] = self._format_datetime(from_date)
        if to_date:
            payload['to'] = self._format_datetime(to_date)
        if event_type:
            payload['eventType'] = event_type
        return self._request('GetBondEvents', payload)
    
    def get_accrued_interests(
        self,
        instrument_id: str,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """
        Get accrued interest on bond.
        
        Args:
            instrument_id: Instrument identifier
            from_date: Start of period
            to_date: End of period
            
        Returns:
            Dictionary with accrued interests
        """
        payload = {'instrumentId': instrument_id}
        if from_date:
            payload['from'] = self._format_datetime(from_date)
        if to_date:
            payload['to'] = self._format_datetime(to_date)
        return self._request('GetAccruedInterests', payload)
    
    # ========================================================================
    # SHARES
    # ========================================================================
    
    def shares(
        self,
        instrument_status: InstrumentStatus = InstrumentStatus.INSTRUMENT_STATUS_UNSPECIFIED
    ) -> Dict[str, Any]:
        """
        Get list of shares.
        
        Args:
            instrument_status: Status of requested instruments
            
        Returns:
            Dictionary with shares list
        """
        payload = {'instrumentStatus': instrument_status.value}
        return self._request('Shares', payload)
    
    def share_by(
        self,
        id_type: InstrumentIdType,
        class_code: Optional[str] = None,
        id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get share by identifier.
        
        Args:
            id_type: Type of instrument identifier
            class_code: Class code (required for ticker type)
            id: Instrument identifier
            
        Returns:
            Dictionary with share information
        """
        payload = {'idType': id_type.value}
        if class_code:
            payload['classCode'] = class_code
        if id:
            payload['id'] = id
        return self._request('ShareBy', payload)
    
    def get_dividends(
        self,
        instrument_id: str,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """
        Get dividend payment events.
        
        Args:
            instrument_id: Instrument identifier
            from_date: Start of period
            to_date: End of period
            
        Returns:
            Dictionary with dividend events
        """
        payload = {'instrumentId': instrument_id}
        if from_date:
            payload['from'] = self._format_datetime(from_date)
        if to_date:
            payload['to'] = self._format_datetime(to_date)
        return self._request('GetDividends', payload)
    
    # ========================================================================
    # ETFs
    # ========================================================================
    
    def etfs(
        self,
        instrument_status: InstrumentStatus = InstrumentStatus.INSTRUMENT_STATUS_UNSPECIFIED
    ) -> Dict[str, Any]:
        """
        Get list of ETFs.
        
        Args:
            instrument_status: Status of requested instruments
            
        Returns:
            Dictionary with ETFs list
        """
        payload = {'instrumentStatus': instrument_status.value}
        return self._request('Etfs', payload)
    
    def etf_by(
        self,
        id_type: InstrumentIdType,
        class_code: Optional[str] = None,
        id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get ETF by identifier.
        
        Args:
            id_type: Type of instrument identifier
            class_code: Class code (required for ticker type)
            id: Instrument identifier
            
        Returns:
            Dictionary with ETF information
        """
        payload = {'idType': id_type.value}
        if class_code:
            payload['classCode'] = class_code
        if id:
            payload['id'] = id
        return self._request('EtfBy', payload)
    
    # ========================================================================
    # CURRENCIES
    # ========================================================================
    
    def currencies(
        self,
        instrument_status: InstrumentStatus = InstrumentStatus.INSTRUMENT_STATUS_UNSPECIFIED
    ) -> Dict[str, Any]:
        """
        Get list of currencies.
        
        Args:
            instrument_status: Status of requested instruments
            
        Returns:
            Dictionary with currencies list
        """
        payload = {'instrumentStatus': instrument_status.value}
        return self._request('Currencies', payload)
    
    def currency_by(
        self,
        id_type: InstrumentIdType,
        class_code: Optional[str] = None,
        id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get currency by identifier.
        
        Args:
            id_type: Type of instrument identifier
            class_code: Class code (required for ticker type)
            id: Instrument identifier
            
        Returns:
            Dictionary with currency information
        """
        payload = {'idType': id_type.value}
        if class_code:
            payload['classCode'] = class_code
        if id:
            payload['id'] = id
        return self._request('CurrencyBy', payload)
    
    # ========================================================================
    # FUTURES
    # ========================================================================
    
    def futures(
        self,
        instrument_status: InstrumentStatus = InstrumentStatus.INSTRUMENT_STATUS_UNSPECIFIED
    ) -> Dict[str, Any]:
        """
        Get list of futures.
        
        Args:
            instrument_status: Status of requested instruments
            
        Returns:
            Dictionary with futures list
        """
        payload = {'instrumentStatus': instrument_status.value}
        return self._request('Futures', payload)
    
    def future_by(
        self,
        id_type: InstrumentIdType,
        class_code: Optional[str] = None,
        id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get future by identifier.
        
        Args:
            id_type: Type of instrument identifier
            class_code: Class code (required for ticker type)
            id: Instrument identifier
            
        Returns:
            Dictionary with future information
        """
        payload = {'idType': id_type.value}
        if class_code:
            payload['classCode'] = class_code
        if id:
            payload['id'] = id
        return self._request('FutureBy', payload)
    
    def get_futures_margin(
        self,
        instrument_id: str
    ) -> Dict[str, Any]:
        """
        Get futures margin requirements.
        
        Args:
            instrument_id: Instrument identifier
            
        Returns:
            Dictionary with margin information
        """
        payload = {'instrumentId': instrument_id}
        return self._request('GetFuturesMargin', payload)
    
    # ========================================================================
    # OPTIONS
    # ========================================================================
    
    def options(
        self,
        instrument_status: InstrumentStatus = InstrumentStatus.INSTRUMENT_STATUS_UNSPECIFIED
    ) -> Dict[str, Any]:
        """
        Get list of options (deprecated, use options_by).
        
        Args:
            instrument_status: Status of requested instruments
            
        Returns:
            Dictionary with options list
        """
        payload = {'instrumentStatus': instrument_status.value}
        return self._request('Options', payload)
    
    def option_by(
        self,
        id_type: InstrumentIdType,
        class_code: Optional[str] = None,
        id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get option by identifier.
        
        Args:
            id_type: Type of instrument identifier
            class_code: Class code (required for ticker type)
            id: Instrument identifier
            
        Returns:
            Dictionary with option information
        """
        payload = {'idType': id_type.value}
        if class_code:
            payload['classCode'] = class_code
        if id:
            payload['id'] = id
        return self._request('OptionBy', payload)
    
    def options_by(
        self,
        basic_asset_uid: Optional[str] = None,
        basic_asset_position_uid: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get list of options by basic asset.
        
        Args:
            basic_asset_uid: Basic asset UID
            basic_asset_position_uid: Basic asset position UID
            
        Returns:
            Dictionary with options list
        """
        payload = {}
        if basic_asset_uid:
            payload['basicAssetUid'] = basic_asset_uid
        if basic_asset_position_uid:
            payload['basicAssetPositionUid'] = basic_asset_position_uid
        return self._request('OptionsBy', payload)
    
    # ========================================================================
    # STRUCTURED NOTES
    # ========================================================================
    
    def structured_notes(
        self,
        instrument_status: InstrumentStatus = InstrumentStatus.INSTRUMENT_STATUS_UNSPECIFIED
    ) -> Dict[str, Any]:
        """
        Get list of structured notes.
        
        Args:
            instrument_status: Status of requested instruments
            
        Returns:
            Dictionary with structured notes list
        """
        payload = {'instrumentStatus': instrument_status.value}
        return self._request('StructuredNotes', payload)
    
    def structured_note_by(
        self,
        id_type: InstrumentIdType,
        class_code: Optional[str] = None,
        id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get structured note by identifier.
        
        Args:
            id_type: Type of instrument identifier
            class_code: Class code (required for ticker type)
            id: Instrument identifier
            
        Returns:
            Dictionary with structured note information
        """
        payload = {'idType': id_type.value}
        if class_code:
            payload['classCode'] = class_code
        if id:
            payload['id'] = id
        return self._request('StructuredNoteBy', payload)
    
    # ========================================================================
    # INDICATIVES
    # ========================================================================
    
    def indicatives(self) -> Dict[str, Any]:
        """
        Get indicative instruments (indices, commodities, etc.).
        
        Returns:
            Dictionary with indicatives list
        """
        return self._request('Indicatives', {})
    
    # ========================================================================
    # SEARCH
    # ========================================================================
    
    def find_instrument(
        self,
        query: str,
        instrument_kind: Optional[InstrumentType] = None,
        api_trade_available_flag: Optional[bool] = None
    ) -> Dict[str, Any]:
        """
        Find instrument by search query.
        
        Args:
            query: Search string
            instrument_kind: Instrument type filter
            api_trade_available_flag: Filter by API trade availability
            
        Returns:
            Dictionary with search results
        """
        payload = {'query': query}
        if instrument_kind:
            payload['instrumentKind'] = instrument_kind.value
        if api_trade_available_flag is not None:
            payload['apiTradeAvailableFlag'] = api_trade_available_flag
        return self._request('FindInstrument', payload)
    
    def get_instrument_by(
        self,
        id_type: InstrumentIdType,
        class_code: Optional[str] = None,
        id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get instrument basic information by identifier.
        
        Args:
            id_type: Type of instrument identifier
            class_code: Class code (required for ticker type)
            id: Instrument identifier
            
        Returns:
            Dictionary with instrument information
        """
        payload = {'idType': id_type.value}
        if class_code:
            payload['classCode'] = class_code
        if id:
            payload['id'] = id
        return self._request('GetInstrumentBy', payload)
    
    # ========================================================================
    # ASSETS
    # ========================================================================
    
    def get_assets(self, asset_type: Optional[AssetType] = None) -> Dict[str, Any]:
        """
        Get list of assets.
        
        Args:
            asset_type: Asset type filter
            
        Returns:
            Dictionary with assets list
        """
        payload = {}
        if asset_type:
            payload['assetType'] = asset_type.value
        return self._request('GetAssets', payload)
    
    def get_asset_by(self, asset_uid: str) -> Dict[str, Any]:
        """
        Get asset by identifier.
        
        Args:
            asset_uid: Asset UID
            
        Returns:
            Dictionary with asset information
        """
        payload = {'assetUid': asset_uid}
        return self._request('GetAssetBy', payload)
    
    def get_asset_fundamentals(self, assets: List[str]) -> Dict[str, Any]:
        """
        Get fundamental indicators for assets.
        
        Args:
            assets: List of asset UIDs
            
        Returns:
            Dictionary with fundamentals
        """
        payload = {'assets': assets}
        return self._request('GetAssetFundamentals', payload)
    
    def get_asset_reports(
        self,
        instrument_id: str,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """
        Get asset report schedules.
        
        Args:
            instrument_id: Instrument identifier
            from_date: Start of period
            to_date: End of period
            
        Returns:
            Dictionary with report schedules
        """
        payload = {'instrumentId': instrument_id}
        if from_date:
            payload['from'] = self._format_datetime(from_date)
        if to_date:
            payload['to'] = self._format_datetime(to_date)
        return self._request('GetAssetReports', payload)
    
    # ========================================================================
    # BRANDS
    # ========================================================================
    
    def get_brands(self, paging: Optional[Dict[str, int]] = None) -> Dict[str, Any]:
        """
        Get list of brands.
        
        Args:
            paging: Pagination parameters (limit, offset)
            
        Returns:
            Dictionary with brands list
        """
        payload = {}
        if paging:
            payload['paging'] = paging
        return self._request('GetBrands', payload)
    
    def get_brand_by(self, brand_uid: str) -> Dict[str, Any]:
        """
        Get brand by identifier.
        
        Args:
            brand_uid: Brand UID
            
        Returns:
            Dictionary with brand information
        """
        payload = {'brandUid': brand_uid}
        return self._request('GetBrandBy', payload)
    
    # ========================================================================
    # COUNTRIES
    # ========================================================================
    
    def get_countries(self) -> Dict[str, Any]:
        """
        Get list of countries.
        
        Returns:
            Dictionary with countries list
        """
        return self._request('GetCountries', {})
    
    # ========================================================================
    # FORECASTS & ANALYTICS
    # ========================================================================
    
    def get_consensus_forecasts(self, paging: Optional[Dict[str, int]] = None) -> Dict[str, Any]:
        """
        Get analyst consensus forecasts.
        
        Args:
            paging: Pagination parameters
            
        Returns:
            Dictionary with forecasts
        """
        payload = {}
        if paging:
            payload['paging'] = paging
        return self._request('GetConsensusForecasts', payload)
    
    def get_forecast_by(
        self,
        instrument_id: str
    ) -> Dict[str, Any]:
        """
        Get investment house forecasts for instrument.
        
        Args:
            instrument_id: Instrument identifier
            
        Returns:
            Dictionary with forecasts
        """
        payload = {'instrumentId': instrument_id}
        return self._request('GetForecastBy', payload)
    
    def get_insider_deals(
        self,
        instrument_id: str,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """
        Get insider deals for instruments.
        
        Args:
            instrument_id: Instrument identifier
            from_date: Start of period
            to_date: End of period
            
        Returns:
            Dictionary with insider deals
        """
        payload = {'instrumentId': instrument_id}
        if from_date:
            payload['from'] = self._format_datetime(from_date)
        if to_date:
            payload['to'] = self._format_datetime(to_date)
        return self._request('GetInsiderDeals', payload)
    
    def get_risk_rates(self, instrument_id: str) -> Dict[str, Any]:
        """
        Get risk rates for instrument.
        
        Args:
            instrument_id: Instrument identifier
            
        Returns:
            Dictionary with risk rates
        """
        payload = {'instrumentId': instrument_id}
        return self._request('GetRiskRates', payload)
    
    # ========================================================================
    # TRADING SCHEDULES
    # ========================================================================
    
    def trading_schedules(
        self,
        exchange: Optional[str] = None,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """
        Get trading schedules for exchanges.
        
        Args:
            exchange: Exchange name filter
            from_date: Start of period
            to_date: End of period
            
        Returns:
            Dictionary with trading schedules
        """
        payload = {}
        if exchange:
            payload['exchange'] = exchange
        if from_date:
            payload['from'] = self._format_datetime(from_date)
        if to_date:
            payload['to'] = self._format_datetime(to_date)
        return self._request('TradingSchedules', payload)
    
    # ========================================================================
    # FAVORITES
    # ========================================================================
    
    def get_favorites(self) -> Dict[str, Any]:
        """
        Get list of favorite instruments.
        
        Returns:
            Dictionary with favorites
        """
        return self._request('GetFavorites', {})
    
    def get_favorite_groups(self) -> Dict[str, Any]:
        """
        Get list of favorite instrument groups.
        
        Returns:
            Dictionary with favorite groups
        """
        return self._request('GetFavoriteGroups', {})
    
    def create_favorite_group(
        self,
        name: str,
        instruments: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        """
        Create new favorite instruments group.
        
        Args:
            name: Group name
            instruments: List of instruments to add
            
        Returns:
            Dictionary with created group
        """
        payload = {'name': name}
        if instruments:
            payload['instruments'] = instruments
        return self._request('CreateFavoriteGroup', payload)
    
    def edit_favorites(
        self,
        instruments: List[Dict[str, Any]],
        action_type: str
    ) -> Dict[str, Any]:
        """
        Edit favorite instruments list.
        
        Args:
            instruments: List of instruments
            action_type: Action type (add/remove)
            
        Returns:
            Dictionary with result
        """
        payload = {
            'instruments': instruments,
            'actionType': action_type
        }
        return self._request('EditFavorites', payload)
    
    def delete_favorite_group(self, favorite_group_id: str) -> Dict[str, Any]:
        """
        Delete favorite instruments group.
        
        Args:
            favorite_group_id: Group ID
            
        Returns:
            Dictionary with result
        """
        payload = {'favoriteGroupId': favorite_group_id}
        return self._request('DeleteFavoriteGroup', payload)
    
    # ========================================================================
    # LIFECYCLE
    # ========================================================================
    
    def close(self):
        """Close the session"""
        self.session.close()
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()


# ============================================================================
# ASYNCHRONOUS CLIENT
# ============================================================================

class AsyncInstrumentsService(BaseInstrumentsClient):
    """
    Asynchronous client for T-Bank Invest InstrumentsService API.
    
    Same interface as InstrumentsService but all methods are async.
    
    Usage:
        async with AsyncInstrumentsService(token="your_token") as client:
            bonds = await client.bonds()
            shares = await client.shares()
    """
    
    def __init__(self, token: str, timeout: float = 30.0):
        """
        Initialize the async client.
        
        Args:
            token: Bearer API token for authorization
            timeout: Request timeout in seconds (default: 30.0)
        """
        self.token = token
        self.timeout = timeout
        self._client: Optional[httpx.AsyncClient] = None
    
    @property
    def client(self) -> httpx.AsyncClient:
        """Get or create the httpx async client"""
        if self._client is None:
            self._client = httpx.AsyncClient(
                headers={
                    'Authorization': f'Bearer {self.token}',
                    'Content-Type': 'application/json'
                },
                timeout=self.timeout
            )
        return self._client
    
    async def _request(self, endpoint: str, payload: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Make async API request.
        
        Args:
            endpoint: Endpoint name
            payload: Request payload
            
        Returns:
            Response data as dictionary
            
        Raises:
            TBankInvestAPIError: If request fails
        """
        url = f"{self.BASE_URL}{self.SERVICE_PATH}/{endpoint}"
        
        try:
            response = await self.client.post(url, json=payload or {})
            response.raise_for_status()
            return response.json()
            
        except httpx.HTTPStatusError as e:
            error_msg = f"HTTP error: {e}"
            try:
                error_data = e.response.json()
                error_msg = f"API error: {error_data}"
            except ValueError:
                error_msg = f"HTTP {e.response.status_code}: {e.response.text}"
            raise TBankInvestAPIError(error_msg) from e
        except httpx.RequestError as e:
            raise TBankInvestAPIError(f"Request failed: {e}") from e
    
    # All methods follow the same pattern as sync client but with async
    
    async def bonds(
        self,
        instrument_status: InstrumentStatus = InstrumentStatus.INSTRUMENT_STATUS_UNSPECIFIED
    ) -> Dict[str, Any]:
        """Get list of bonds (async)."""
        payload = {'instrumentStatus': instrument_status.value}
        return await self._request('Bonds', payload)
    
    async def bond_by(
        self,
        id_type: InstrumentIdType,
        class_code: Optional[str] = None,
        id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get bond by identifier (async)."""
        payload = {'idType': id_type.value}
        if class_code:
            payload['classCode'] = class_code
        if id:
            payload['id'] = id
        return await self._request('BondBy', payload)
    
    async def get_bond_coupons(
        self,
        instrument_id: str,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """Get bond coupon payment schedule (async)."""
        payload = {'instrumentId': instrument_id}
        if from_date:
            payload['from'] = self._format_datetime(from_date)
        if to_date:
            payload['to'] = self._format_datetime(to_date)
        return await self._request('GetBondCoupons', payload)
    
    async def get_bond_events(
        self,
        instrument_id: str,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None,
        event_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get bond events (async)."""
        payload = {'instrumentId': instrument_id}
        if from_date:
            payload['from'] = self._format_datetime(from_date)
        if to_date:
            payload['to'] = self._format_datetime(to_date)
        if event_type:
            payload['eventType'] = event_type
        return await self._request('GetBondEvents', payload)
    
    async def get_accrued_interests(
        self,
        instrument_id: str,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """Get accrued interest on bond (async)."""
        payload = {'instrumentId': instrument_id}
        if from_date:
            payload['from'] = self._format_datetime(from_date)
        if to_date:
            payload['to'] = self._format_datetime(to_date)
        return await self._request('GetAccruedInterests', payload)
    
    async def shares(
        self,
        instrument_status: InstrumentStatus = InstrumentStatus.INSTRUMENT_STATUS_UNSPECIFIED
    ) -> Dict[str, Any]:
        """Get list of shares (async)."""
        payload = {'instrumentStatus': instrument_status.value}
        return await self._request('Shares', payload)
    
    async def share_by(
        self,
        id_type: InstrumentIdType,
        class_code: Optional[str] = None,
        id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get share by identifier (async)."""
        payload = {'idType': id_type.value}
        if class_code:
            payload['classCode'] = class_code
        if id:
            payload['id'] = id
        return await self._request('ShareBy', payload)
    
    async def get_dividends(
        self,
        instrument_id: str,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """Get dividend payment events (async)."""
        payload = {'instrumentId': instrument_id}
        if from_date:
            payload['from'] = self._format_datetime(from_date)
        if to_date:
            payload['to'] = self._format_datetime(to_date)
        return await self._request('GetDividends', payload)
    
    async def etfs(
        self,
        instrument_status: InstrumentStatus = InstrumentStatus.INSTRUMENT_STATUS_UNSPECIFIED
    ) -> Dict[str, Any]:
        """Get list of ETFs (async)."""
        payload = {'instrumentStatus': instrument_status.value}
        return await self._request('Etfs', payload)
    
    async def etf_by(
        self,
        id_type: InstrumentIdType,
        class_code: Optional[str] = None,
        id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get ETF by identifier (async)."""
        payload = {'idType': id_type.value}
        if class_code:
            payload['classCode'] = class_code
        if id:
            payload['id'] = id
        return await self._request('EtfBy', payload)
    
    async def currencies(
        self,
        instrument_status: InstrumentStatus = InstrumentStatus.INSTRUMENT_STATUS_UNSPECIFIED
    ) -> Dict[str, Any]:
        """Get list of currencies (async)."""
        payload = {'instrumentStatus': instrument_status.value}
        return await self._request('Currencies', payload)
    
    async def currency_by(
        self,
        id_type: InstrumentIdType,
        class_code: Optional[str] = None,
        id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get currency by identifier (async)."""
        payload = {'idType': id_type.value}
        if class_code:
            payload['classCode'] = class_code
        if id:
            payload['id'] = id
        return await self._request('CurrencyBy', payload)
    
    async def futures(
        self,
        instrument_status: InstrumentStatus = InstrumentStatus.INSTRUMENT_STATUS_UNSPECIFIED
    ) -> Dict[str, Any]:
        """Get list of futures (async)."""
        payload = {'instrumentStatus': instrument_status.value}
        return await self._request('Futures', payload)
    
    async def future_by(
        self,
        id_type: InstrumentIdType,
        class_code: Optional[str] = None,
        id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get future by identifier (async)."""
        payload = {'idType': id_type.value}
        if class_code:
            payload['classCode'] = class_code
        if id:
            payload['id'] = id
        return await self._request('FutureBy', payload)
    
    async def get_futures_margin(self, instrument_id: str) -> Dict[str, Any]:
        """Get futures margin requirements (async)."""
        payload = {'instrumentId': instrument_id}
        return await self._request('GetFuturesMargin', payload)
    
    async def options(
        self,
        instrument_status: InstrumentStatus = InstrumentStatus.INSTRUMENT_STATUS_UNSPECIFIED
    ) -> Dict[str, Any]:
        """Get list of options (async, deprecated)."""
        payload = {'instrumentStatus': instrument_status.value}
        return await self._request('Options', payload)
    
    async def option_by(
        self,
        id_type: InstrumentIdType,
        class_code: Optional[str] = None,
        id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get option by identifier (async)."""
        payload = {'idType': id_type.value}
        if class_code:
            payload['classCode'] = class_code
        if id:
            payload['id'] = id
        return await self._request('OptionBy', payload)
    
    async def options_by(
        self,
        basic_asset_uid: Optional[str] = None,
        basic_asset_position_uid: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get list of options by basic asset (async)."""
        payload = {}
        if basic_asset_uid:
            payload['basicAssetUid'] = basic_asset_uid
        if basic_asset_position_uid:
            payload['basicAssetPositionUid'] = basic_asset_position_uid
        return await self._request('OptionsBy', payload)
    
    async def structured_notes(
        self,
        instrument_status: InstrumentStatus = InstrumentStatus.INSTRUMENT_STATUS_UNSPECIFIED
    ) -> Dict[str, Any]:
        """Get list of structured notes (async)."""
        payload = {'instrumentStatus': instrument_status.value}
        return await self._request('StructuredNotes', payload)
    
    async def structured_note_by(
        self,
        id_type: InstrumentIdType,
        class_code: Optional[str] = None,
        id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get structured note by identifier (async)."""
        payload = {'idType': id_type.value}
        if class_code:
            payload['classCode'] = class_code
        if id:
            payload['id'] = id
        return await self._request('StructuredNoteBy', payload)
    
    async def indicatives(self) -> Dict[str, Any]:
        """Get indicative instruments (async)."""
        return await self._request('Indicatives', {})
    
    async def find_instrument(
        self,
        query: str,
        instrument_kind: Optional[InstrumentType] = None,
        api_trade_available_flag: Optional[bool] = None
    ) -> Dict[str, Any]:
        """Find instrument by search query (async)."""
        payload = {'query': query}
        if instrument_kind:
            payload['instrumentKind'] = instrument_kind.value
        if api_trade_available_flag is not None:
            payload['apiTradeAvailableFlag'] = api_trade_available_flag
        return await self._request('FindInstrument', payload)
    
    async def get_instrument_by(
        self,
        id_type: InstrumentIdType,
        class_code: Optional[str] = None,
        id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get instrument basic information (async)."""
        payload = {'idType': id_type.value}
        if class_code:
            payload['classCode'] = class_code
        if id:
            payload['id'] = id
        return await self._request('GetInstrumentBy', payload)
    
    async def get_assets(self, asset_type: Optional[AssetType] = None) -> Dict[str, Any]:
        """Get list of assets (async)."""
        payload = {}
        if asset_type:
            payload['assetType'] = asset_type.value
        return await self._request('GetAssets', payload)
    
    async def get_asset_by(self, asset_uid: str) -> Dict[str, Any]:
        """Get asset by identifier (async)."""
        payload = {'assetUid': asset_uid}
        return await self._request('GetAssetBy', payload)
    
    async def get_asset_fundamentals(self, assets: List[str]) -> Dict[str, Any]:
        """Get fundamental indicators (async)."""
        payload = {'assets': assets}
        return await self._request('GetAssetFundamentals', payload)
    
    async def get_asset_reports(
        self,
        instrument_id: str,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """Get asset report schedules (async)."""
        payload = {'instrumentId': instrument_id}
        if from_date:
            payload['from'] = self._format_datetime(from_date)
        if to_date:
            payload['to'] = self._format_datetime(to_date)
        return await self._request('GetAssetReports', payload)
    
    async def get_brands(self, paging: Optional[Dict[str, int]] = None) -> Dict[str, Any]:
        """Get list of brands (async)."""
        payload = {}
        if paging:
            payload['paging'] = paging
        return await self._request('GetBrands', payload)
    
    async def get_brand_by(self, brand_uid: str) -> Dict[str, Any]:
        """Get brand by identifier (async)."""
        payload = {'brandUid': brand_uid}
        return await self._request('GetBrandBy', payload)
    
    async def get_countries(self) -> Dict[str, Any]:
        """Get list of countries (async)."""
        return await self._request('GetCountries', {})
    
    async def get_consensus_forecasts(self, paging: Optional[Dict[str, int]] = None) -> Dict[str, Any]:
        """Get analyst consensus forecasts (async)."""
        payload = {}
        if paging:
            payload['paging'] = paging
        return await self._request('GetConsensusForecasts', payload)
    
    async def get_forecast_by(self, instrument_id: str) -> Dict[str, Any]:
        """Get forecasts for instrument (async)."""
        payload = {'instrumentId': instrument_id}
        return await self._request('GetForecastBy', payload)
    
    async def get_insider_deals(
        self,
        instrument_id: str,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """Get insider deals (async)."""
        payload = {'instrumentId': instrument_id}
        if from_date:
            payload['from'] = self._format_datetime(from_date)
        if to_date:
            payload['to'] = self._format_datetime(to_date)
        return await self._request('GetInsiderDeals', payload)
    
    async def get_risk_rates(self, instrument_id: str) -> Dict[str, Any]:
        """Get risk rates (async)."""
        payload = {'instrumentId': instrument_id}
        return await self._request('GetRiskRates', payload)
    
    async def trading_schedules(
        self,
        exchange: Optional[str] = None,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """Get trading schedules (async)."""
        payload = {}
        if exchange:
            payload['exchange'] = exchange
        if from_date:
            payload['from'] = self._format_datetime(from_date)
        if to_date:
            payload['to'] = self._format_datetime(to_date)
        return await self._request('TradingSchedules', payload)
    
    async def get_favorites(self) -> Dict[str, Any]:
        """Get favorite instruments (async)."""
        return await self._request('GetFavorites', {})
    
    async def get_favorite_groups(self) -> Dict[str, Any]:
        """Get favorite groups (async)."""
        return await self._request('GetFavoriteGroups', {})
    
    async def create_favorite_group(
        self,
        name: str,
        instruments: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        """Create favorite group (async)."""
        payload = {'name': name}
        if instruments:
            payload['instruments'] = instruments
        return await self._request('CreateFavoriteGroup', payload)
    
    async def edit_favorites(
        self,
        instruments: List[Dict[str, Any]],
        action_type: str
    ) -> Dict[str, Any]:
        """Edit favorites (async)."""
        payload = {
            'instruments': instruments,
            'actionType': action_type
        }
        return await self._request('EditFavorites', payload)
    
    async def delete_favorite_group(self, favorite_group_id: str) -> Dict[str, Any]:
        """Delete favorite group (async)."""
        payload = {'favoriteGroupId': favorite_group_id}
        return await self._request('DeleteFavoriteGroup', payload)
    
    async def close(self):
        """Close the async client"""
        if self._client is not None:
            await self._client.aclose()
            self._client = None
    
    async def __aenter__(self):
        """Async context manager entry"""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.close()
