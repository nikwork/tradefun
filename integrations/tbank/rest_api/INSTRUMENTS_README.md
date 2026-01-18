# T-Bank Invest API: InstrumentsService Complete Wrapper

Comprehensive Python wrappers (synchronous and asynchronous) for all 40 T-Bank Invest API InstrumentsService endpoints.

## 📋 Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [API Coverage](#api-coverage)
- [Detailed Documentation](#detailed-documentation)
- [Examples](#examples)

## ✨ Features

- ✅ **Complete coverage** of all 40 InstrumentsService endpoints
- ✅ **Synchronous client** using `requests`
- ✅ **Asynchronous client** using `httpx`
- ✅ **Type hints** for better IDE support
- ✅ **Enums** for instrument types, statuses, and identifiers
- ✅ **Context managers** for resource management
- ✅ **Comprehensive error handling**
- ✅ **DateTime support** with timezone handling

## 🚀 Installation

```bash
pip install requests httpx
```

## ⚡ Quick Start

### Synchronous Usage

```python
from tbank_instruments_service import InstrumentsService, InstrumentStatus

# Initialize client
with InstrumentsService(token="your_api_token") as client:
    # Get all bonds
    bonds = client.bonds(InstrumentStatus.INSTRUMENT_STATUS_BASE)
    
    # Get all shares
    shares = client.shares()
    
    # Find an instrument
    results = client.find_instrument("SBER")
    
    # Get bond coupons
    coupons = client.get_bond_coupons("BBG004730N88")
```

### Asynchronous Usage

```python
import asyncio
from tbank_instruments_service import AsyncInstrumentsService

async def main():
    async with AsyncInstrumentsService(token="your_api_token") as client:
        # Fetch multiple instrument types concurrently
        bonds, shares, currencies = await asyncio.gather(
            client.bonds(),
            client.shares(),
            client.currencies()
        )
        
        print(f"Bonds: {len(bonds.get('instruments', []))}")
        print(f"Shares: {len(shares.get('instruments', []))}")
        print(f"Currencies: {len(currencies.get('instruments', []))}")

asyncio.run(main())
```

## 📚 API Coverage

### All 40 Endpoints Implemented

#### Bonds (5 endpoints)
- `bonds()` - List of bonds
- `bond_by()` - Get bond by identifier
- `get_bond_coupons()` - Bond coupon schedule
- `get_bond_events()` - Bond events
- `get_accrued_interests()` - Accrued interest

#### Shares (3 endpoints)
- `shares()` - List of shares
- `share_by()` - Get share by identifier
- `get_dividends()` - Dividend events

#### ETFs (2 endpoints)
- `etfs()` - List of ETFs
- `etf_by()` - Get ETF by identifier

#### Currencies (2 endpoints)
- `currencies()` - List of currencies
- `currency_by()` - Get currency by identifier

#### Futures (3 endpoints)
- `futures()` - List of futures
- `future_by()` - Get future by identifier
- `get_futures_margin()` - Futures margin requirements

#### Options (3 endpoints)
- `options()` - List of options (deprecated)
- `option_by()` - Get option by identifier
- `options_by()` - Options by basic asset

#### Structured Notes (2 endpoints)
- `structured_notes()` - List of structured notes
- `structured_note_by()` - Get structured note by identifier

#### Search & Information (3 endpoints)
- `find_instrument()` - Search for instruments
- `get_instrument_by()` - Get instrument info
- `indicatives()` - Indicative instruments

#### Assets (4 endpoints)
- `get_assets()` - List of assets
- `get_asset_by()` - Get asset by UID
- `get_asset_fundamentals()` - Asset fundamentals
- `get_asset_reports()` - Asset report schedules

#### Brands (2 endpoints)
- `get_brands()` - List of brands
- `get_brand_by()` - Get brand by UID

#### Analytics (4 endpoints)
- `get_consensus_forecasts()` - Analyst forecasts
- `get_forecast_by()` - Investment house forecasts
- `get_insider_deals()` - Insider trading deals
- `get_risk_rates()` - Risk rates

#### Utilities (2 endpoints)
- `get_countries()` - List of countries
- `trading_schedules()` - Trading schedules

#### Favorites (4 endpoints)
- `get_favorites()` - List favorites
- `get_favorite_groups()` - List favorite groups
- `create_favorite_group()` - Create group
- `edit_favorites()` - Edit favorites
- `delete_favorite_group()` - Delete group

## 📖 Detailed Documentation

### Client Initialization

```python
# Synchronous
client = InstrumentsService(
    token="your_api_token",
    timeout=30.0  # Optional, default 30 seconds
)

# Asynchronous
async_client = AsyncInstrumentsService(
    token="your_api_token",
    timeout=30.0
)
```

### Enums

#### InstrumentStatus
```python
from tbank_instruments_service import InstrumentStatus

InstrumentStatus.INSTRUMENT_STATUS_UNSPECIFIED  # Default
InstrumentStatus.INSTRUMENT_STATUS_BASE         # Tradeable via API
InstrumentStatus.INSTRUMENT_STATUS_ALL          # All instruments
```

#### InstrumentIdType
```python
from tbank_instruments_service import InstrumentIdType

InstrumentIdType.INSTRUMENT_ID_TYPE_FIGI         # FIGI identifier
InstrumentIdType.INSTRUMENT_ID_TYPE_TICKER       # Ticker + class code
InstrumentIdType.INSTRUMENT_ID_TYPE_UID          # Instrument UID
InstrumentIdType.INSTRUMENT_ID_TYPE_POSITION_UID # Position UID
```

#### InstrumentType
```python
from tbank_instruments_service import InstrumentType

InstrumentType.INSTRUMENT_TYPE_BOND      # Bonds
InstrumentType.INSTRUMENT_TYPE_SHARE     # Shares
InstrumentType.INSTRUMENT_TYPE_CURRENCY  # Currencies
InstrumentType.INSTRUMENT_TYPE_ETF       # ETFs
InstrumentType.INSTRUMENT_TYPE_FUTURES   # Futures
InstrumentType.INSTRUMENT_TYPE_OPTION    # Options
```

## 💡 Examples

### Example 1: Get All Instrument Types

```python
from tbank_instruments_service import InstrumentsService, InstrumentStatus

with InstrumentsService(token="your_token") as client:
    # Get all tradeable instruments
    bonds = client.bonds(InstrumentStatus.INSTRUMENT_STATUS_BASE)
    shares = client.shares(InstrumentStatus.INSTRUMENT_STATUS_BASE)
    etfs = client.etfs(InstrumentStatus.INSTRUMENT_STATUS_BASE)
    currencies = client.currencies(InstrumentStatus.INSTRUMENT_STATUS_BASE)
    futures = client.futures(InstrumentStatus.INSTRUMENT_STATUS_BASE)
    
    print(f"Bonds: {len(bonds.get('instruments', []))}")
    print(f"Shares: {len(shares.get('instruments', []))}")
    print(f"ETFs: {len(etfs.get('instruments', []))}")
    print(f"Currencies: {len(currencies.get('instruments', []))}")
    print(f"Futures: {len(futures.get('instruments', []))}")
```

### Example 2: Search for Instruments

```python
from tbank_instruments_service import InstrumentsService, InstrumentType

with InstrumentsService(token="your_token") as client:
    # Search for Sberbank shares
    results = client.find_instrument(
        query="SBER",
        instrument_kind=InstrumentType.INSTRUMENT_TYPE_SHARE
    )
    
    for instrument in results.get('instruments', []):
        print(f"Name: {instrument.get('name')}")
        print(f"Ticker: {instrument.get('ticker')}")
        print(f"FIGI: {instrument.get('figi')}")
        print()
```

### Example 3: Get Bond Coupons

```python
from datetime import datetime
from tbank_instruments_service import InstrumentsService

with InstrumentsService(token="your_token") as client:
    # Get bond coupons for 2024
    coupons = client.get_bond_coupons(
        instrument_id="BBG004730N88",
        from_date=datetime(2024, 1, 1),
        to_date=datetime(2024, 12, 31)
    )
    
    for event in coupons.get('events', []):
        print(f"Date: {event.get('couponDate')}")
        print(f"Amount: {event.get('payOneBond')}")
        print()
```

### Example 4: Get Dividends

```python
from tbank_instruments_service import InstrumentsService

with InstrumentsService(token="your_token") as client:
    # Get dividend events
    dividends = client.get_dividends(
        instrument_id="BBG004730N88"
    )
    
    for dividend in dividends.get('dividends', []):
        print(f"Date: {dividend.get('dividendDate')}")
        print(f"Amount: {dividend.get('dividendNet')}")
        print()
```

### Example 5: Get Instrument by Different IDs

```python
from tbank_instruments_service import InstrumentsService, InstrumentIdType

with InstrumentsService(token="your_token") as client:
    # By FIGI
    bond = client.bond_by(
        id_type=InstrumentIdType.INSTRUMENT_ID_TYPE_FIGI,
        id="BBG004730N88"
    )
    
    # By Ticker + Class Code
    share = client.share_by(
        id_type=InstrumentIdType.INSTRUMENT_ID_TYPE_TICKER,
        class_code="TQBR",
        id="SBER"
    )
    
    # By UID
    instrument = client.get_instrument_by(
        id_type=InstrumentIdType.INSTRUMENT_ID_TYPE_UID,
        id="some-uid-here"
    )
```

### Example 6: Async Concurrent Fetching

```python
import asyncio
from tbank_instruments_service import AsyncInstrumentsService

async def fetch_all_instruments():
    async with AsyncInstrumentsService(token="your_token") as client:
        # Fetch all instrument types concurrently
        results = await asyncio.gather(
            client.bonds(),
            client.shares(),
            client.etfs(),
            client.currencies(),
            client.futures(),
            return_exceptions=True
        )
        
        names = ['Bonds', 'Shares', 'ETFs', 'Currencies', 'Futures']
        for name, result in zip(names, results):
            if isinstance(result, Exception):
                print(f"{name}: Error - {result}")
            else:
                count = len(result.get('instruments', []))
                print(f"{name}: {count} instruments")

asyncio.run(fetch_all_instruments())
```

### Example 7: Trading Schedules

```python
from datetime import datetime, timedelta
from tbank_instruments_service import InstrumentsService

with InstrumentsService(token="your_token") as client:
    # Get trading schedules for next week
    today = datetime.now()
    next_week = today + timedelta(days=7)
    
    schedules = client.trading_schedules(
        exchange="MOEX",
        from_date=today,
        to_date=next_week
    )
    
    for exchange in schedules.get('exchanges', []):
        print(f"Exchange: {exchange.get('exchange')}")
        for day in exchange.get('days', []):
            print(f"  Date: {day.get('date')}")
            print(f"  Is trading: {day.get('isTradingDay')}")
```

### Example 8: Get Asset Fundamentals

```python
from tbank_instruments_service import InstrumentsService

with InstrumentsService(token="your_token") as client:
    # Get fundamentals for multiple assets
    fundamentals = client.get_asset_fundamentals(
        assets=["asset-uid-1", "asset-uid-2", "asset-uid-3"]
    )
    
    for asset in fundamentals.get('fundamentals', []):
        print(f"Asset: {asset.get('assetUid')}")
        print(f"Market cap: {asset.get('marketCapitalization')}")
        print(f"P/E ratio: {asset.get('priceToEarnings')}")
        print()
```

### Example 9: Work with Favorites

```python
from tbank_instruments_service import InstrumentsService

with InstrumentsService(token="your_token") as client:
    # Get current favorites
    favorites = client.get_favorites()
    print(f"Favorites: {favorites}")
    
    # Create favorite group
    group = client.create_favorite_group(
        name="My Portfolio",
        instruments=[
            {"figi": "BBG004730N88"},
            {"figi": "BBG000BPH459"}
        ]
    )
    
    # Get all favorite groups
    groups = client.get_favorite_groups()
    print(f"Groups: {groups}")
```

### Example 10: Error Handling

```python
from tbank_instruments_service import InstrumentsService, TBankInvestAPIError

with InstrumentsService(token="your_token") as client:
    try:
        # Try to get non-existent instrument
        result = client.bond_by(
            id_type=InstrumentIdType.INSTRUMENT_ID_TYPE_FIGI,
            id="INVALID_FIGI"
        )
    except TBankInvestAPIError as e:
        print(f"API Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
```

## 🔧 Advanced Usage

### Custom Timeout

```python
# Longer timeout for slow connections
client = InstrumentsService(token="your_token", timeout=60.0)
```

### Reusing Session

```python
# Client automatically manages session
with InstrumentsService(token="your_token") as client:
    # Multiple requests reuse the same session
    bonds1 = client.bonds()
    bonds2 = client.bonds()
    shares = client.shares()
# Session closed automatically
```

### Async Context Manager

```python
async def process_instruments():
    async with AsyncInstrumentsService(token="your_token") as client:
        # All requests in this block use the same client
        bonds = await client.bonds()
        shares = await client.shares()
        # Client closed automatically on exit
```

## 📝 API Reference

### Common Parameters

- `token` (str): Bearer API token
- `timeout` (float): Request timeout in seconds (default: 30.0)
- `instrument_status` (InstrumentStatus): Filter by instrument status
- `id_type` (InstrumentIdType): Type of instrument identifier
- `instrument_id` (str): Instrument identifier (FIGI or UID)
- `from_date` (datetime): Start of date range (UTC)
- `to_date` (datetime): End of date range (UTC)

### Return Values

All methods return a dictionary with API response data. The structure varies by endpoint but typically includes:

- `instruments`: List of instruments
- `events`: List of events (coupons, dividends, etc.)
- `instrument`: Single instrument details

## 🔗 Related Links

- [T-Bank Developer Portal](https://developer.tbank.ru/)
- [InstrumentsService Documentation](https://developer.tbank.ru/invest/api/instruments-service)
- [T-Bank Invest API](https://developer.tbank.ru/invest/api)

## ⚠️ Error Handling

All methods can raise `TBankInvestAPIError` for:
- HTTP errors (4xx, 5xx)
- Network issues
- Invalid responses

Always wrap API calls in try-except blocks for production use.

## 📄 License

This is an unofficial wrapper for T-Bank Invest API. Check T-Bank's terms of service for API usage restrictions.

## 🤝 Contributing

Contributions are welcome! Please ensure all 40 endpoints remain functional when making changes.

## ⚡ Performance Tips

1. Use async client for concurrent requests
2. Reuse client instances when making multiple requests
3. Use context managers to ensure proper cleanup
4. Filter results server-side when possible (use InstrumentStatus.INSTRUMENT_STATUS_BASE)

## 🎯 Best Practices

1. Always use context managers (`with` or `async with`)
2. Handle `TBankInvestAPIError` exceptions
3. Use enums for type safety
4. Validate instrument IDs before making requests
5. Cache frequently used data to reduce API calls
