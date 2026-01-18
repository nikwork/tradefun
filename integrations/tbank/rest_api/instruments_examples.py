"""
Comprehensive examples for T-Bank InstrumentsService API wrapper.

This file demonstrates usage of all 40 endpoints with practical examples.
Replace 'YOUR_API_TOKEN' with your actual T-Bank API token.
"""

import asyncio
from datetime import datetime, timedelta
from typing import Dict, Any
from tbank_instruments_service import (
    InstrumentsService,
    AsyncInstrumentsService,
    InstrumentStatus,
    InstrumentIdType,
    InstrumentType,
    AssetType,
    TBankInvestAPIError
)


# Configuration
API_TOKEN = "YOUR_API_TOKEN"


# ============================================================================
# SYNCHRONOUS EXAMPLES
# ============================================================================

def example_01_list_all_instruments():
    """Example 1: Get lists of all instrument types"""
    print("=" * 60)
    print("EXAMPLE 1: List All Instrument Types")
    print("=" * 60)
    
    try:
        with InstrumentsService(token=API_TOKEN) as client:
            print("\nFetching instrument lists...")
            
            bonds = client.bonds(InstrumentStatus.INSTRUMENT_STATUS_BASE)
            shares = client.shares(InstrumentStatus.INSTRUMENT_STATUS_BASE)
            etfs = client.etfs(InstrumentStatus.INSTRUMENT_STATUS_BASE)
            currencies = client.currencies(InstrumentStatus.INSTRUMENT_STATUS_BASE)
            futures = client.futures(InstrumentStatus.INSTRUMENT_STATUS_BASE)
            
            print(f"\nBonds: {len(bonds.get('instruments', []))}")
            print(f"Shares: {len(shares.get('instruments', []))}")
            print(f"ETFs: {len(etfs.get('instruments', []))}")
            print(f"Currencies: {len(currencies.get('instruments', []))}")
            print(f"Futures: {len(futures.get('instruments', []))}")
            
            # Show first 3 bonds
            print("\nFirst 3 bonds:")
            for bond in bonds.get('instruments', [])[:3]:
                print(f"  - {bond.get('name')} ({bond.get('ticker')})")
                
    except TBankInvestAPIError as e:
        print(f"Error: {e}")


def example_02_search_instruments():
    """Example 2: Search for instruments"""
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Search for Instruments")
    print("=" * 60)
    
    try:
        with InstrumentsService(token=API_TOKEN) as client:
            # Search for specific ticker
            print("\nSearching for 'SBER'...")
            results = client.find_instrument(
                query="SBER",
                instrument_kind=InstrumentType.INSTRUMENT_TYPE_SHARE
            )
            
            for instrument in results.get('instruments', [])[:5]:
                print(f"\nName: {instrument.get('name')}")
                print(f"Ticker: {instrument.get('ticker')}")
                print(f"FIGI: {instrument.get('figi')}")
                print(f"Currency: {instrument.get('currency')}")
                
    except TBankInvestAPIError as e:
        print(f"Error: {e}")


def example_03_get_instrument_by_different_ids():
    """Example 3: Get instruments using different identifier types"""
    print("\n" + "=" * 60)
    print("EXAMPLE 3: Get Instruments by Different IDs")
    print("=" * 60)
    
    try:
        with InstrumentsService(token=API_TOKEN) as client:
            # By FIGI
            print("\nGetting bond by FIGI...")
            bond = client.bond_by(
                id_type=InstrumentIdType.INSTRUMENT_ID_TYPE_FIGI,
                id="BBG004730N88"
            )
            print(f"Bond: {bond.get('instrument', {}).get('name')}")
            
            # By Ticker
            print("\nGetting share by Ticker...")
            share = client.share_by(
                id_type=InstrumentIdType.INSTRUMENT_ID_TYPE_TICKER,
                class_code="TQBR",
                id="SBER"
            )
            print(f"Share: {share.get('instrument', {}).get('name')}")
            
    except TBankInvestAPIError as e:
        print(f"Error: {e}")


def example_04_bond_coupons_and_events():
    """Example 4: Get bond coupons and events"""
    print("\n" + "=" * 60)
    print("EXAMPLE 4: Bond Coupons and Events")
    print("=" * 60)
    
    try:
        with InstrumentsService(token=API_TOKEN) as client:
            instrument_id = "BBG004730N88"
            
            # Get coupons for 2024
            print(f"\nGetting coupons for {instrument_id}...")
            coupons = client.get_bond_coupons(
                instrument_id=instrument_id,
                from_date=datetime(2024, 1, 1),
                to_date=datetime(2024, 12, 31)
            )
            
            print(f"Found {len(coupons.get('events', []))} coupons")
            
            for event in coupons.get('events', [])[:3]:
                coupon_date = event.get('couponDate', '')
                pay_one = event.get('payOneBond', {})
                print(f"\nDate: {coupon_date}")
                print(f"Payment: {pay_one.get('units', 0)} {pay_one.get('currency', '')}")
            
            # Get accrued interests
            print(f"\nGetting accrued interests...")
            interests = client.get_accrued_interests(
                instrument_id=instrument_id,
                from_date=datetime(2024, 1, 1),
                to_date=datetime(2024, 12, 31)
            )
            
            print(f"Found {len(interests.get('accruedInterests', []))} records")
            
    except TBankInvestAPIError as e:
        print(f"Error: {e}")


def example_05_dividends():
    """Example 5: Get dividend information"""
    print("\n" + "=" * 60)
    print("EXAMPLE 5: Dividend Information")
    print("=" * 60)
    
    try:
        with InstrumentsService(token=API_TOKEN) as client:
            # Get dividends for a share
            print("\nGetting dividend events...")
            dividends = client.get_dividends(
                instrument_id="BBG004730N88",
                from_date=datetime(2023, 1, 1),
                to_date=datetime(2024, 12, 31)
            )
            
            print(f"Found {len(dividends.get('dividends', []))} dividend events")
            
            for div in dividends.get('dividends', [])[:5]:
                print(f"\nDeclared: {div.get('declaredDate')}")
                print(f"Payment: {div.get('dividendNet')}")
                print(f"Yield: {div.get('yieldValue')}%")
                
    except TBankInvestAPIError as e:
        print(f"Error: {e}")


def example_06_futures_and_options():
    """Example 6: Work with futures and options"""
    print("\n" + "=" * 60)
    print("EXAMPLE 6: Futures and Options")
    print("=" * 60)
    
    try:
        with InstrumentsService(token=API_TOKEN) as client:
            # Get futures list
            print("\nGetting futures list...")
            futures = client.futures(InstrumentStatus.INSTRUMENT_STATUS_BASE)
            print(f"Found {len(futures.get('instruments', []))} futures")
            
            if futures.get('instruments'):
                first_future = futures['instruments'][0]
                future_id = first_future.get('uid')
                
                # Get margin requirements
                print(f"\nGetting margin for {first_future.get('name')}...")
                margin = client.get_futures_margin(instrument_id=future_id)
                print(f"Margin: {margin}")
            
            # Get options
            print("\nGetting options list...")
            options = client.options(InstrumentStatus.INSTRUMENT_STATUS_BASE)
            print(f"Found {len(options.get('instruments', []))} options")
            
    except TBankInvestAPIError as e:
        print(f"Error: {e}")


def example_07_assets_and_fundamentals():
    """Example 7: Work with assets and fundamentals"""
    print("\n" + "=" * 60)
    print("EXAMPLE 7: Assets and Fundamentals")
    print("=" * 60)
    
    try:
        with InstrumentsService(token=API_TOKEN) as client:
            # Get assets list
            print("\nGetting assets...")
            assets = client.get_assets(AssetType.ASSET_TYPE_SECURITY)
            print(f"Found {len(assets.get('assets', []))} assets")
            
            # Get fundamentals for first few assets
            if assets.get('assets'):
                asset_uids = [a.get('uid') for a in assets['assets'][:3] if a.get('uid')]
                
                if asset_uids:
                    print(f"\nGetting fundamentals for {len(asset_uids)} assets...")
                    fundamentals = client.get_asset_fundamentals(assets=asset_uids)
                    
                    for fund in fundamentals.get('fundamentals', []):
                        print(f"\nAsset: {fund.get('assetUid')}")
                        print(f"Market Cap: {fund.get('marketCapitalization')}")
                        print(f"P/E: {fund.get('priceToEarnings')}")
                        
    except TBankInvestAPIError as e:
        print(f"Error: {e}")


def example_08_brands_and_countries():
    """Example 8: Work with brands and countries"""
    print("\n" + "=" * 60)
    print("EXAMPLE 8: Brands and Countries")
    print("=" * 60)
    
    try:
        with InstrumentsService(token=API_TOKEN) as client:
            # Get brands
            print("\nGetting brands...")
            brands = client.get_brands(paging={'limit': 10})
            
            print(f"Found {len(brands.get('brands', []))} brands")
            for brand in brands.get('brands', [])[:5]:
                print(f"  - {brand.get('name')}")
            
            # Get countries
            print("\nGetting countries...")
            countries = client.get_countries()
            
            print(f"Found {len(countries.get('countries', []))} countries")
            for country in countries.get('countries', [])[:10]:
                print(f"  - {country.get('name')} ({country.get('alfaTwo')})")
                
    except TBankInvestAPIError as e:
        print(f"Error: {e}")


def example_09_trading_schedules():
    """Example 9: Get trading schedules"""
    print("\n" + "=" * 60)
    print("EXAMPLE 9: Trading Schedules")
    print("=" * 60)
    
    try:
        with InstrumentsService(token=API_TOKEN) as client:
            # Get schedules for next week
            today = datetime.now()
            next_week = today + timedelta(days=7)
            
            print(f"\nGetting schedules from {today.date()} to {next_week.date()}...")
            schedules = client.trading_schedules(
                exchange="MOEX",
                from_date=today,
                to_date=next_week
            )
            
            for exchange in schedules.get('exchanges', []):
                print(f"\nExchange: {exchange.get('exchange')}")
                for day in exchange.get('days', []):
                    status = "Trading" if day.get('isTradingDay') else "Non-trading"
                    print(f"  {day.get('date')}: {status}")
                    
    except TBankInvestAPIError as e:
        print(f"Error: {e}")


def example_10_analytics_and_forecasts():
    """Example 10: Analytics and forecasts"""
    print("\n" + "=" * 60)
    print("EXAMPLE 10: Analytics and Forecasts")
    print("=" * 60)
    
    try:
        with InstrumentsService(token=API_TOKEN) as client:
            instrument_id = "BBG004730N88"
            
            # Get consensus forecasts
            print("\nGetting consensus forecasts...")
            forecasts = client.get_consensus_forecasts(paging={'limit': 5})
            print(f"Found {len(forecasts.get('items', []))} forecasts")
            
            # Get forecasts for specific instrument
            print(f"\nGetting forecasts for {instrument_id}...")
            instrument_forecasts = client.get_forecast_by(instrument_id=instrument_id)
            print(f"Forecasts: {instrument_forecasts}")
            
            # Get risk rates
            print(f"\nGetting risk rates for {instrument_id}...")
            risk_rates = client.get_risk_rates(instrument_id=instrument_id)
            print(f"Risk rates: {risk_rates}")
            
            # Get insider deals
            print(f"\nGetting insider deals...")
            deals = client.get_insider_deals(
                instrument_id=instrument_id,
                from_date=datetime(2023, 1, 1),
                to_date=datetime.now()
            )
            print(f"Found {len(deals.get('items', []))} deals")
            
    except TBankInvestAPIError as e:
        print(f"Error: {e}")


def example_11_favorites():
    """Example 11: Work with favorites"""
    print("\n" + "=" * 60)
    print("EXAMPLE 11: Favorites Management")
    print("=" * 60)
    
    try:
        with InstrumentsService(token=API_TOKEN) as client:
            # Get current favorites
            print("\nGetting favorites...")
            favorites = client.get_favorites()
            print(f"Current favorites: {favorites}")
            
            # Get favorite groups
            print("\nGetting favorite groups...")
            groups = client.get_favorite_groups()
            print(f"Groups: {len(groups.get('favoriteGroups', []))}")
            
            # Note: Creating/editing requires valid instrument IDs
            # Uncomment to test with real data:
            # group = client.create_favorite_group(
            #     name="Test Portfolio",
            #     instruments=[{"figi": "BBG004730N88"}]
            # )
            # print(f"Created group: {group}")
            
    except TBankInvestAPIError as e:
        print(f"Error: {e}")


# ============================================================================
# ASYNCHRONOUS EXAMPLES
# ============================================================================

async def example_12_async_concurrent_fetch():
    """Example 12: Concurrent fetching with async"""
    print("\n" + "=" * 60)
    print("EXAMPLE 12: Async Concurrent Fetching")
    print("=" * 60)
    
    try:
        async with AsyncInstrumentsService(token=API_TOKEN) as client:
            print("\nFetching multiple instrument types concurrently...")
            
            # Fetch all at once
            results = await asyncio.gather(
                client.bonds(InstrumentStatus.INSTRUMENT_STATUS_BASE),
                client.shares(InstrumentStatus.INSTRUMENT_STATUS_BASE),
                client.etfs(InstrumentStatus.INSTRUMENT_STATUS_BASE),
                client.currencies(InstrumentStatus.INSTRUMENT_STATUS_BASE),
                client.futures(InstrumentStatus.INSTRUMENT_STATUS_BASE),
                return_exceptions=True
            )
            
            labels = ['Bonds', 'Shares', 'ETFs', 'Currencies', 'Futures']
            
            for label, result in zip(labels, results):
                if isinstance(result, Exception):
                    print(f"{label}: Error - {result}")
                else:
                    count = len(result.get('instruments', []))
                    print(f"{label}: {count} instruments")
                    
    except Exception as e:
        print(f"Error: {e}")


async def example_13_async_search_multiple():
    """Example 13: Search multiple instruments concurrently"""
    print("\n" + "=" * 60)
    print("EXAMPLE 13: Async Multiple Searches")
    print("=" * 60)
    
    try:
        async with AsyncInstrumentsService(token=API_TOKEN) as client:
            # Search for multiple tickers at once
            tickers = ["SBER", "GAZP", "LKOH", "YNDX"]
            
            print(f"\nSearching for {len(tickers)} tickers concurrently...")
            
            searches = [
                client.find_instrument(ticker, InstrumentType.INSTRUMENT_TYPE_SHARE)
                for ticker in tickers
            ]
            
            results = await asyncio.gather(*searches, return_exceptions=True)
            
            for ticker, result in zip(tickers, results):
                if isinstance(result, Exception):
                    print(f"{ticker}: Error")
                else:
                    instruments = result.get('instruments', [])
                    if instruments:
                        print(f"{ticker}: {instruments[0].get('name')}")
                    else:
                        print(f"{ticker}: Not found")
                        
    except Exception as e:
        print(f"Error: {e}")


async def example_14_async_bulk_data_fetch():
    """Example 14: Fetch detailed data for multiple instruments"""
    print("\n" + "=" * 60)
    print("EXAMPLE 14: Async Bulk Data Fetch")
    print("=" * 60)
    
    try:
        async with AsyncInstrumentsService(token=API_TOKEN) as client:
            # First get list of bonds
            bonds_data = await client.bonds(InstrumentStatus.INSTRUMENT_STATUS_BASE)
            bonds = bonds_data.get('instruments', [])[:5]  # First 5 bonds
            
            if not bonds:
                print("No bonds found")
                return
            
            print(f"\nFetching detailed data for {len(bonds)} bonds...")
            
            # Fetch coupons for all bonds concurrently
            coupon_tasks = [
                client.get_bond_coupons(
                    instrument_id=bond.get('figi'),
                    from_date=datetime(2024, 1, 1),
                    to_date=datetime(2024, 12, 31)
                )
                for bond in bonds
            ]
            
            coupon_results = await asyncio.gather(*coupon_tasks, return_exceptions=True)
            
            for bond, coupons in zip(bonds, coupon_results):
                name = bond.get('name', 'Unknown')
                if isinstance(coupons, Exception):
                    print(f"{name}: Error fetching coupons")
                else:
                    count = len(coupons.get('events', []))
                    print(f"{name}: {count} coupons")
                    
    except Exception as e:
        print(f"Error: {e}")


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Run all synchronous examples"""
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "  T-Bank InstrumentsService - Complete Examples".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "═" * 58 + "╝")
    print("\n")
    
    # Synchronous examples
    example_01_list_all_instruments()
    example_02_search_instruments()
    example_03_get_instrument_by_different_ids()
    example_04_bond_coupons_and_events()
    example_05_dividends()
    example_06_futures_and_options()
    example_07_assets_and_fundamentals()
    example_08_brands_and_countries()
    example_09_trading_schedules()
    example_10_analytics_and_forecasts()
    example_11_favorites()
    
    # Asynchronous examples
    print("\n" + "=" * 60)
    print("ASYNC EXAMPLES")
    print("=" * 60)
    
    asyncio.run(example_12_async_concurrent_fetch())
    asyncio.run(example_13_async_search_multiple())
    asyncio.run(example_14_async_bulk_data_fetch())
    
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
