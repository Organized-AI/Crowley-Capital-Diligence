#!/usr/bin/env python3
"""
Carta API Client for VC Due Diligence
Usage: python carta_client.py --firm-id <FIRM_ID> [--action investments|captable|performance]
"""

import os
import json
import requests
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class CartaConfig:
    """Carta API configuration."""
    client_id: str
    client_secret: str
    firm_id: str
    environment: str = "playground"
    
    @property
    def base_url(self) -> str:
        if self.environment == "production":
            return "https://api.carta.com/v1alpha1"
        return "https://api.playground.carta.team/v1alpha1"
    
    @property
    def token_url(self) -> str:
        if self.environment == "production":
            return "https://api.carta.com/oauth/token"
        return "https://api.playground.carta.team/oauth/token"


class CartaClient:
    """Carta API client for VC diligence workflows."""
    
    def __init__(self, config: CartaConfig):
        self.config = config
        self._access_token: Optional[str] = None
        self._token_expires: Optional[datetime] = None
    
    @property
    def access_token(self) -> str:
        """Get or refresh access token."""
        if self._access_token is None or self._is_token_expired():
            self._refresh_token()
        return self._access_token
    
    def _is_token_expired(self) -> bool:
        if self._token_expires is None:
            return True
        return datetime.now() >= self._token_expires
    
    def _refresh_token(self) -> None:
        """Refresh OAuth access token."""
        response = requests.post(
            self.config.token_url,
            data={
                "grant_type": "client_credentials",
                "client_id": self.config.client_id,
                "client_secret": self.config.client_secret,
                "scope": " ".join([
                    "read_investor_capitalizationtables",
                    "read_investor_investments",
                    "read_investor_funds",
                    "read_investor_fundperformance",
                    "read_investor_securities",
                    "read_investor_stakeholdercapitalizationtable"
                ])
            }
        )
        response.raise_for_status()
        data = response.json()
        self._access_token = data["access_token"]
        # Assume 1 hour expiry if not specified
        expires_in = data.get("expires_in", 3600)
        self._token_expires = datetime.now().timestamp() + expires_in
    
    @property
    def headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
    
    def _get(self, endpoint: str) -> Dict:
        """Make GET request to Carta API."""
        url = f"{self.config.base_url}{endpoint}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    # ============ Investor API ============
    
    def get_firm_info(self) -> Dict:
        """Get firm information."""
        return self._get(f"/investors/firms/{self.config.firm_id}")
    
    def list_funds(self) -> List[Dict]:
        """List all funds in the firm."""
        result = self._get(f"/investors/firms/{self.config.firm_id}/funds")
        return result.get("funds", [])
    
    def list_investments(self, fund_id: Optional[str] = None) -> List[Dict]:
        """List all portfolio investments."""
        if fund_id:
            result = self._get(
                f"/investors/firms/{self.config.firm_id}/funds/{fund_id}/investments"
            )
        else:
            result = self._get(f"/investors/firms/{self.config.firm_id}/investments")
        return result.get("investments", [])
    
    def get_cap_table(self, fund_id: str, company_id: str, cap_table_id: str) -> Dict:
        """Get cap table for a portfolio company."""
        return self._get(
            f"/investors/firms/{self.config.firm_id}/funds/{fund_id}"
            f"/investments/{company_id}/capitalizationTables/{cap_table_id}"
        )
    
    def get_fund_performance(self, fund_id: str) -> Dict:
        """Get fund performance metrics (TVPI, DPI, IRR)."""
        return self._get(
            f"/investors/firms/{self.config.firm_id}/funds/{fund_id}/performance"
        )
    
    def list_securities(self, fund_id: str, company_id: str) -> List[Dict]:
        """List securities for a portfolio company."""
        result = self._get(
            f"/investors/firms/{self.config.firm_id}/funds/{fund_id}"
            f"/investments/{company_id}/securities"
        )
        return result.get("securities", [])
    
    # ============ Diligence Helpers ============
    
    def pull_portfolio_summary(self) -> Dict[str, Any]:
        """Pull complete portfolio summary for diligence."""
        summary = {
            "firm": self.get_firm_info(),
            "funds": [],
            "pulled_at": datetime.now().isoformat()
        }
        
        funds = self.list_funds()
        for fund in funds:
            fund_data = {
                "fund_id": fund["id"],
                "fund_name": fund.get("name"),
                "performance": None,
                "investments": []
            }
            
            # Get fund performance
            try:
                fund_data["performance"] = self.get_fund_performance(fund["id"])
            except Exception as e:
                fund_data["performance_error"] = str(e)
            
            # Get investments
            investments = self.list_investments(fund["id"])
            for inv in investments:
                inv_data = {
                    "company_id": inv.get("companyId"),
                    "company_name": inv.get("companyName"),
                    "investment_date": inv.get("investmentDate"),
                    "cap_table": None
                }
                
                # Get cap table if available
                cap_tables = inv.get("capitalizationTables", [])
                if cap_tables:
                    try:
                        inv_data["cap_table"] = self.get_cap_table(
                            fund["id"],
                            inv["companyId"],
                            cap_tables[0]["id"]
                        )
                    except Exception as e:
                        inv_data["cap_table_error"] = str(e)
                
                fund_data["investments"].append(inv_data)
            
            summary["funds"].append(fund_data)
        
        return summary
    
    def extract_ownership_metrics(self, cap_table: Dict) -> Dict[str, Any]:
        """Extract key ownership metrics from cap table."""
        metrics = {
            "type": cap_table.get("type"),  # PRIMARY or PRO_FORMA
            "fully_diluted_shares": cap_table.get("fullyDilutedShares", 0),
            "issued_shares": cap_table.get("issuedShares", 0),
            "stakeholder_count": 0,
            "founders_pct": 0.0,
            "investors_pct": 0.0,
            "employees_pct": 0.0,
            "option_pool_pct": 0.0
        }
        
        stakeholders = cap_table.get("stakeholders", [])
        metrics["stakeholder_count"] = len(stakeholders)
        
        total_fd = metrics["fully_diluted_shares"]
        if total_fd > 0:
            for sh in stakeholders:
                shares = sh.get("fullyDilutedShares", 0)
                pct = (shares / total_fd) * 100
                
                category = sh.get("category", "").lower()
                if "founder" in category:
                    metrics["founders_pct"] += pct
                elif "investor" in category:
                    metrics["investors_pct"] += pct
                elif "employee" in category:
                    metrics["employees_pct"] += pct
                elif "pool" in category or "option" in category:
                    metrics["option_pool_pct"] += pct
        
        return metrics


def load_config_from_env() -> CartaConfig:
    """Load configuration from environment variables."""
    return CartaConfig(
        client_id=os.environ.get("CARTA_CLIENT_ID", ""),
        client_secret=os.environ.get("CARTA_CLIENT_SECRET", ""),
        firm_id=os.environ.get("CARTA_FIRM_ID", ""),
        environment=os.environ.get("CARTA_ENV", "playground")
    )


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Carta API Client")
    parser.add_argument("--firm-id", help="Carta Firm ID (overrides env)")
    parser.add_argument("--action", choices=["investments", "captable", "performance", "summary"],
                       default="summary", help="Action to perform")
    parser.add_argument("--fund-id", help="Fund ID for fund-specific actions")
    parser.add_argument("--output", default="json", choices=["json", "pretty"],
                       help="Output format")
    
    args = parser.parse_args()
    
    # Load config
    config = load_config_from_env()
    if args.firm_id:
        config.firm_id = args.firm_id
    
    if not config.client_id or not config.client_secret:
        print("Error: CARTA_CLIENT_ID and CARTA_CLIENT_SECRET must be set")
        exit(1)
    
    if not config.firm_id:
        print("Error: CARTA_FIRM_ID must be set or --firm-id provided")
        exit(1)
    
    # Create client
    client = CartaClient(config)
    
    # Execute action
    try:
        if args.action == "investments":
            result = client.list_investments(args.fund_id)
        elif args.action == "performance" and args.fund_id:
            result = client.get_fund_performance(args.fund_id)
        elif args.action == "summary":
            result = client.pull_portfolio_summary()
        else:
            result = {"error": "Invalid action or missing parameters"}
        
        # Output
        if args.output == "pretty":
            print(json.dumps(result, indent=2, default=str))
        else:
            print(json.dumps(result, default=str))
    
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        exit(1)
