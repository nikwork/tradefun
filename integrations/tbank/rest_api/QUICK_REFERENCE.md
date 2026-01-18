# T-Bank InstrumentsService API - Quick Reference

## 📋 All 40 Endpoints

### 🔵 Bonds (5 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `bonds()` | `/Bonds` | Get list of bonds |
| `bond_by()` | `/BondBy` | Get bond by identifier |
| `get_bond_coupons()` | `/GetBondCoupons` | Get bond coupon schedule |
| `get_bond_events()` | `/GetBondEvents` | Get bond events |
| `get_accrued_interests()` | `/GetAccruedInterests` | Get accrued interest |

### 📈 Shares (3 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `shares()` | `/Shares` | Get list of shares |
| `share_by()` | `/ShareBy` | Get share by identifier |
| `get_dividends()` | `/GetDividends` | Get dividend events |

### 🏦 ETFs (2 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `etfs()` | `/Etfs` | Get list of ETFs |
| `etf_by()` | `/EtfBy` | Get ETF by identifier |

### 💱 Currencies (2 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `currencies()` | `/Currencies` | Get list of currencies |
| `currency_by()` | `/CurrencyBy` | Get currency by identifier |

### 📊 Futures (3 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `futures()` | `/Futures` | Get list of futures |
| `future_by()` | `/FutureBy` | Get future by identifier |
| `get_futures_margin()` | `/GetFuturesMargin` | Get margin requirements |

### 🎯 Options (3 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `options()` | `/Options` | Get list of options (deprecated) |
| `option_by()` | `/OptionBy` | Get option by identifier |
| `options_by()` | `/OptionsBy` | Get options by basic asset |

### 📑 Structured Notes (2 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `structured_notes()` | `/StructuredNotes` | Get list of structured notes |
| `structured_note_by()` | `/StructuredNoteBy` | Get structured note by ID |

### 🔍 Search & Info (3 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `find_instrument()` | `/FindInstrument` | Search for instruments |
| `get_instrument_by()` | `/GetInstrumentBy` | Get instrument info |
| `indicatives()` | `/Indicatives` | Get indicative instruments |

### 💼 Assets (4 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `get_assets()` | `/GetAssets` | Get list of assets |
| `get_asset_by()` | `/GetAssetBy` | Get asset by UID |
| `get_asset_fundamentals()` | `/GetAssetFundamentals` | Get fundamentals |
| `get_asset_reports()` | `/GetAssetReports` | Get report schedules |

### 🏢 Brands (2 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `get_brands()` | `/GetBrands` | Get list of brands |
| `get_brand_by()` | `/GetBrandBy` | Get brand by UID |

### 📊 Analytics (4 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `get_consensus_forecasts()` | `/GetConsensusForecasts` | Get analyst forecasts |
| `get_forecast_by()` | `/GetForecastBy` | Get investment forecasts |
| `get_insider_deals()` | `/GetInsiderDeals` | Get insider deals |
| `get_risk_rates()` | `/GetRiskRates` | Get risk rates |

### 🛠️ Utilities (2 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `get_countries()` | `/GetCountries` | Get list of countries |
| `trading_schedules()` | `/TradingSchedules` | Get trading schedules |

### ⭐ Favorites (4 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `get_favorites()` | `/GetFavorites` | Get favorites list |
| `get_favorite_groups()` | `/GetFavoriteGroups` | Get favorite groups |
| `create_favorite_group()` | `/CreateFavoriteGroup` | Create group |
| `edit_favorites()` | `/EditFavorites` | Edit favorites |
| `delete_favorite_group()` | `/DeleteFavoriteGroup` | Delete group |

## 🚀 Quick Start Examples

### Get All Bonds
```python
from tbank_instruments_service import InstrumentsService, InstrumentStatus

with InstrumentsService(token="your_token") as client:
    bonds = client.bonds(InstrumentStatus.INSTRUMENT_STATUS_BASE)
    print(f"Found {len(bonds['instruments'])} bonds")
```

### Search for Instrument
```python
with InstrumentsService(token="your_token") as client:
    results = client.find_instrument("SBER")
    for inst in results['instruments']:
        print(f"{inst['name']} - {inst['ticker']}")
```

### Get Bond Coupons
```python
from datetime import datetime

with InstrumentsService(token="your_token") as client:
    coupons = client.get_bond_coupons(
        instrument_id="BBG004730N88",
        from_date=datetime(2024, 1, 1),
        to_date=datetime(2024, 12, 31)
    )
```

### Async Concurrent Requests
```python
import asyncio
from tbank_instruments_service import AsyncInstrumentsService

async def fetch_all():
    async with AsyncInstrumentsService(token="your_token") as client:
        bonds, shares, etfs = await asyncio.gather(
            client.bonds(),
            client.shares(),
            client.etfs()
        )
        return bonds, shares, etfs

results = asyncio.run(fetch_all())
```

## 📝 Common Patterns

### Pattern 1: Get Instrument by FIGI
```python
from tbank_instruments_service import InstrumentIdType

bond = client.bond_by(
    id_type=InstrumentIdType.INSTRUMENT_ID_TYPE_FIGI,
    id="BBG004730N88"
)
```

### Pattern 2: Get Instrument by Ticker
```python
share = client.share_by(
    id_type=InstrumentIdType.INSTRUMENT_ID_TYPE_TICKER,
    class_code="TQBR",
    id="SBER"
)
```

### Pattern 3: Filter by Date Range
```python
from datetime import datetime, timedelta

today = datetime.now()
next_month = today + timedelta(days=30)

events = client.get_bond_coupons(
    instrument_id="BBG004730N88",
    from_date=today,
    to_date=next_month
)
```

### Pattern 4: Batch Processing with Async
```python
async def process_bonds(bond_ids):
    async with AsyncInstrumentsService(token="your_token") as client:
        tasks = [client.bond_by(
            id_type=InstrumentIdType.INSTRUMENT_ID_TYPE_FIGI,
            id=bond_id
        ) for bond_id in bond_ids]
        
        return await asyncio.gather(*tasks, return_exceptions=True)
```

## 🔑 Authentication

All requests require Bearer token authentication:

```python
client = InstrumentsService(token="your_api_token")
```

Get your token from: https://developer.tbank.ru/

## ⚠️ Rate Limits

Be aware of API rate limits. Use async client for concurrent requests:

```python
# Good: Concurrent with async
async with AsyncInstrumentsService(token="token") as client:
    results = await asyncio.gather(
        client.bonds(),
        client.shares(),
        client.etfs()
    )

# Less efficient: Sequential
with InstrumentsService(token="token") as client:
    bonds = client.bonds()
    shares = client.shares()
    etfs = client.etfs()
```

## 🛡️ Error Handling

```python
from tbank_instruments_service import TBankInvestAPIError

try:
    with InstrumentsService(token="token") as client:
        result = client.bonds()
except TBankInvestAPIError as e:
    print(f"API Error: {e}")
except Exception as e:
    print(f"Unexpected Error: {e}")
```

## 📚 Full Documentation

- Main README: `INSTRUMENTS_README.md`
- Examples: `instruments_examples.py`
- Source Code: `tbank_instruments_service.py`

## 🔗 Links

- [T-Bank Developer Portal](https://developer.tbank.ru/)
- [API Documentation](https://developer.tbank.ru/invest/api/instruments-service)
- [Get API Token](https://developer.tbank.ru/)
