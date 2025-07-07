from fastapi import APIRouter, HTTPException
from typing import Dict, Any
import random
from datetime import datetime, timedelta

router = APIRouter()

@router.get("/trading/overview")
def trading_overview():
    """
    Get trading overview data including portfolio value, market cap, active trades, and watchlist
    """
    try:
        # Mock data for now - in production this would come from real trading APIs
        portfolio_value = random.uniform(100000, 200000)
        market_cap = f"{random.uniform(1.5, 4.0):.1f}T"
        active_trades = random.randint(15, 35)
        watchlist_count = random.randint(100, 200)
        
        # Calculate some mock trends
        portfolio_change = random.uniform(-5.0, 8.0)
        market_cap_change = random.uniform(-3.0, 6.0)
        trades_change = random.randint(-5, 8)
        alerts_pending = random.randint(5, 20)
        
        return {
            "portfolio_value": round(portfolio_value, 2),
            "portfolio_change": round(portfolio_change, 1),
            "market_cap": market_cap,
            "market_cap_change": round(market_cap_change, 1),
            "active_trades": active_trades,
            "trades_change": trades_change,
            "watchlist_count": watchlist_count,
            "alerts_pending": alerts_pending,
            "last_updated": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch trading overview: {str(e)}")

@router.get("/trading/portfolio")
def get_portfolio():
    """
    Get detailed portfolio information
    """
    try:
        # Mock portfolio data
        holdings = [
            {"symbol": "AAPL", "shares": 150, "avg_price": 175.50, "current_price": 182.30, "change": 3.88},
            {"symbol": "GOOGL", "shares": 50, "avg_price": 2800.00, "current_price": 2950.75, "change": 5.38},
            {"symbol": "MSFT", "shares": 100, "avg_price": 320.00, "current_price": 335.20, "change": 4.75},
            {"symbol": "TSLA", "shares": 75, "avg_price": 250.00, "current_price": 265.80, "change": 6.32},
            {"symbol": "AMZN", "shares": 80, "avg_price": 3300.00, "current_price": 3450.90, "change": 4.57}
        ]
        
        total_value = sum(holding["shares"] * holding["current_price"] for holding in holdings)
        total_cost = sum(holding["shares"] * holding["avg_price"] for holding in holdings)
        total_gain_loss = total_value - total_cost
        total_gain_loss_percent = (total_gain_loss / total_cost) * 100 if total_cost > 0 else 0
        
        return {
            "holdings": holdings,
            "total_value": round(total_value, 2),
            "total_cost": round(total_cost, 2),
            "total_gain_loss": round(total_gain_loss, 2),
            "total_gain_loss_percent": round(total_gain_loss_percent, 2),
            "last_updated": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch portfolio: {str(e)}")

@router.get("/trading/watchlist")
def get_watchlist():
    """
    Get watchlist data
    """
    try:
        # Mock watchlist data
        watchlist = [
            {"symbol": "NVDA", "name": "NVIDIA Corporation", "price": 485.20, "change": 2.15, "alert": True},
            {"symbol": "META", "name": "Meta Platforms", "price": 320.45, "change": -1.23, "alert": False},
            {"symbol": "NFLX", "name": "Netflix", "price": 485.20, "change": 0.85, "alert": True},
            {"symbol": "ADBE", "name": "Adobe Inc.", "price": 485.20, "change": -0.45, "alert": False},
            {"symbol": "CRM", "name": "Salesforce", "price": 485.20, "change": 1.67, "alert": True}
        ]
        
        return {
            "watchlist": watchlist,
            "total_count": len(watchlist),
            "alerts_pending": sum(1 for item in watchlist if item["alert"]),
            "last_updated": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch watchlist: {str(e)}")

@router.get("/trading/active-trades")
def get_active_trades():
    """
    Get active trades data
    """
    try:
        # Mock active trades data
        trades = [
            {"id": 1, "symbol": "AAPL", "type": "BUY", "quantity": 10, "price": 182.30, "status": "PENDING", "time": "10:30 AM"},
            {"id": 2, "symbol": "GOOGL", "type": "SELL", "quantity": 5, "price": 2950.75, "status": "EXECUTED", "time": "09:15 AM"},
            {"id": 3, "symbol": "MSFT", "type": "BUY", "quantity": 20, "price": 335.20, "status": "PENDING", "time": "11:45 AM"},
            {"id": 4, "symbol": "TSLA", "type": "SELL", "quantity": 15, "price": 265.80, "status": "CANCELLED", "time": "08:20 AM"}
        ]
        
        return {
            "trades": trades,
            "total_count": len(trades),
            "pending_count": sum(1 for trade in trades if trade["status"] == "PENDING"),
            "executed_count": sum(1 for trade in trades if trade["status"] == "EXECUTED"),
            "cancelled_count": sum(1 for trade in trades if trade["status"] == "CANCELLED"),
            "last_updated": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch active trades: {str(e)}") 