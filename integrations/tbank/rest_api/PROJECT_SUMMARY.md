# T-Bank Invest API - Complete Python Wrapper

Complete implementation of synchronous and asynchronous Python wrappers for T-Bank Invest InstrumentsService API with all 40 endpoints.

## 📦 Package Contents

### Main Files

1. **tbank_instruments_service.py** (49 KB)
   - Complete implementation of all 40 endpoints
   - Synchronous client: `InstrumentsService`
   - Asynchronous client: `AsyncInstrumentsService`
   - Full type hints and enums
   - Comprehensive error handling

2. **INSTRUMENTS_README.md** (15 KB)
   - Complete documentation
   - All endpoints described
   - Usage examples for each category
   - Best practices and tips

3. **instruments_examples.py** (19 KB)
   - 14 comprehensive examples
   - Covers all major use cases
   - Both sync and async examples
   - Ready to run (just add your token)

4. **QUICK_REFERENCE.md** (7 KB)
   - Quick lookup for all endpoints
   - Common patterns
   - Cheat sheet for daily use

### Bonus Files (from initial request)

5. **tbank_bond_coupons.py** (18 KB)
   - Specialized wrapper for GetBondCoupons endpoint
   - Includes data classes for structured responses

6. **requirements.txt**
   - Dependencies list

7. **instruments_service_endpoints.py**
   - List of all 40 endpoint UIDs

## 🎯 What's Implemented

### All 40 InstrumentsService Endpoints

#### Bonds & Fixed Income (5)
- ✅ List bonds
- ✅ Get bond by ID
- ✅ Bond coupons schedule
- ✅ Bond events
- ✅ Accrued interests

#### Stocks & Equity (3)
- ✅ List shares
- ✅ Get share by ID
- ✅ Dividend events

#### ETFs (2)
- ✅ List ETFs
- ✅ Get ETF by ID

#### Currencies (2)
- ✅ List currencies
- ✅ Get currency by ID

#### Derivatives (6)
- ✅ List futures
- ✅ Get future by ID
- ✅ Futures margin
- ✅ List options
- ✅ Get option by ID
- ✅ Options by asset

#### Structured Products (2)
- ✅ List structured notes
- ✅ Get structured note by ID

#### Search & Discovery (3)
- ✅ Find instrument
- ✅ Get instrument by ID
- ✅ Indicative instruments

#### Assets & Companies (6)
- ✅ List assets
- ✅ Get asset by UID
- ✅ Asset fundamentals
- ✅ Asset reports
- ✅ List brands
- ✅ Get brand by UID

#### Analytics & Research (4)
- ✅ Consensus forecasts
- ✅ Investment forecasts
- ✅ Insider deals
- ✅ Risk rates

#### Market Data (2)
- ✅ Countries list
- ✅ Trading schedules

#### User Preferences (4)
- ✅ Get favorites
- ✅ Get favorite groups
- ✅ Create favorite group
- ✅ Edit favorites
- ✅ Delete favorite group

## 🚀 Quick Start

### Installation
```bash
pip install requests httpx
```

### Synchronous Example
```python
from tbank_instruments_service import InstrumentsService

with InstrumentsService(token="your_token") as client:
    # Get all bonds
    bonds = client.bonds()
    print(f"Found {len(bonds['instruments'])} bonds")
    
    # Search for instrument
    results = client.find_instrument("SBER")
    
    # Get bond coupons
    coupons = client.get_bond_coupons("BBG004730N88")
```

### Asynchronous Example
```python
import asyncio
from tbank_instruments_service import AsyncInstrumentsService

async def main():
    async with AsyncInstrumentsService(token="your_token") as client:
        # Fetch multiple types concurrently
        bonds, shares, etfs = await asyncio.gather(
            client.bonds(),
            client.shares(),
            client.etfs()
        )

asyncio.run(main())
```

## 📚 Documentation Guide

### For Beginners
Start with:
1. **QUICK_REFERENCE.md** - Get familiar with available endpoints
2. **INSTRUMENTS_README.md** - Read Quick Start section
3. **instruments_examples.py** - Run example 1-3

### For Intermediate Users
1. **INSTRUMENTS_README.md** - Read all examples
2. **instruments_examples.py** - Study all 14 examples
3. **tbank_instruments_service.py** - Review source code

### For Advanced Users
1. **tbank_instruments_service.py** - Full source code reference
2. Implement custom methods based on patterns
3. Extend with additional features

## 🔑 Key Features

### Type Safety
- Full type hints throughout
- Enums for all status/type fields
- IDE autocomplete support

### Error Handling
- Custom `TBankInvestAPIError` exception
- Detailed error messages
- Proper exception chaining

### Performance
- Async support for concurrent requests
- Session reuse in sync client
- Efficient resource management

### Developer Experience
- Context managers (`with` / `async with`)
- Consistent API across all methods
- Clear documentation

## 📋 Endpoint Categories

| Category | Endpoints | Key Methods |
|----------|-----------|-------------|
| Bonds | 5 | `bonds()`, `get_bond_coupons()` |
| Shares | 3 | `shares()`, `get_dividends()` |
| ETFs | 2 | `etfs()`, `etf_by()` |
| Currencies | 2 | `currencies()`, `currency_by()` |
| Futures | 3 | `futures()`, `get_futures_margin()` |
| Options | 3 | `options()`, `options_by()` |
| Structured | 2 | `structured_notes()` |
| Search | 3 | `find_instrument()` |
| Assets | 6 | `get_assets()`, `get_asset_fundamentals()` |
| Analytics | 4 | `get_consensus_forecasts()` |
| Utilities | 2 | `trading_schedules()` |
| Favorites | 4 | `get_favorites()` |

## 🎓 Learning Path

### Day 1: Basics
- Install dependencies
- Get API token from T-Bank
- Run examples 1-3 (list instruments, search)

### Day 2: Bonds & Dividends
- Run examples 4-5 (bonds, coupons, dividends)
- Understand date filtering
- Work with MoneyValue class

### Day 3: Advanced Features
- Run examples 6-10 (futures, assets, analytics)
- Try async examples 12-14
- Implement your own use case

## 🔧 Common Use Cases

### Portfolio Analysis
```python
# Get all your instruments
bonds = client.bonds()
shares = client.shares()
etfs = client.etfs()

# Get upcoming coupons
coupons = client.get_bond_coupons(bond_id)

# Get dividend schedule
dividends = client.get_dividends(share_id)
```

### Market Research
```python
# Find instruments
results = client.find_instrument("Газпром")

# Get fundamentals
fundamentals = client.get_asset_fundamentals(asset_ids)

# Check analyst forecasts
forecasts = client.get_consensus_forecasts()
```

### Trading Automation
```python
# Check trading schedule
schedule = client.trading_schedules(exchange="MOEX")

# Get real-time instrument info
instrument = client.get_instrument_by(id_type=..., id=...)

# Monitor insider trades
deals = client.get_insider_deals(instrument_id)
```

## ⚡ Performance Tips

1. **Use Async for Multiple Requests**
   ```python
   # Fast: Parallel
   results = await asyncio.gather(
       client.bonds(),
       client.shares(),
       client.etfs()
   )
   
   # Slow: Sequential
   bonds = client.bonds()
   shares = client.shares()
   etfs = client.etfs()
   ```

2. **Reuse Client Instances**
   ```python
   # Good
   with InstrumentsService(token) as client:
       for bond_id in bond_ids:
           data = client.bond_by(id_type=..., id=bond_id)
   
   # Bad (creates new session each time)
   for bond_id in bond_ids:
       with InstrumentsService(token) as client:
           data = client.bond_by(id_type=..., id=bond_id)
   ```

3. **Filter Server-Side**
   ```python
   # Good: Filter on server
   bonds = client.bonds(InstrumentStatus.INSTRUMENT_STATUS_BASE)
   
   # Less efficient: Get all, filter locally
   bonds = client.bonds(InstrumentStatus.INSTRUMENT_STATUS_ALL)
   filtered = [b for b in bonds['instruments'] if b['apiTradeAvailableFlag']]
   ```

## 🐛 Troubleshooting

### "Unauthorized" Error
- Check your API token is valid
- Verify token has correct permissions

### "Not Found" Error
- Verify instrument ID (FIGI/UID) is correct
- Check instrument is tradeable via API

### Timeout Errors
- Increase timeout: `InstrumentsService(token, timeout=60)`
- Check your internet connection
- Use async for large requests

## 🔗 Resources

- **T-Bank Developer Portal**: https://developer.tbank.ru/
- **API Documentation**: https://developer.tbank.ru/invest/api
- **Get API Token**: https://developer.tbank.ru/

## 📄 Files Reference

| File | Size | Purpose |
|------|------|---------|
| tbank_instruments_service.py | 49 KB | Main implementation |
| INSTRUMENTS_README.md | 15 KB | Full documentation |
| instruments_examples.py | 19 KB | Example code |
| QUICK_REFERENCE.md | 7 KB | Quick lookup |
| tbank_bond_coupons.py | 18 KB | Specialized wrapper |
| requirements.txt | 31 B | Dependencies |

## 🎯 Next Steps

1. Get your API token from T-Bank Developer Portal
2. Install dependencies: `pip install requests httpx`
3. Run examples: `python instruments_examples.py`
4. Read QUICK_REFERENCE.md for daily use
5. Build your own financial applications!

## ✅ Quality Checklist

- ✅ All 40 endpoints implemented
- ✅ Both sync and async clients
- ✅ Comprehensive type hints
- ✅ Full error handling
- ✅ 14 working examples
- ✅ Complete documentation
- ✅ Context manager support
- ✅ Production-ready code

## 📞 Support

For API issues, contact T-Bank support or check their documentation.
For wrapper issues, review the source code and examples.

---

**Ready to start trading programmatically? Let's go! 🚀**
