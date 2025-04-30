import os
import httpx
from typing import Dict, List, Optional, Any, Union
import time
import base64

class InvestecClient:
    """Client for interacting with the Investec Open API."""
    
    API_BASE_URL = "https://openapi.investec.com"
    TOKEN_URL = f"{API_BASE_URL}/identity/v2/oauth2/token"
    API_URL = f"{API_BASE_URL}/za/pb/v1"
    
    def __init__(self, client_id: str, client_secret: str, api_key: str):
        """
        Initialize the Investec API client.
        
        Args:
            client_id: The client ID from the Investec Developer portal
            client_secret: The client secret from the Investec Developer portal
            api_key: The API key from the Investec Developer portal
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.api_key = api_key
        self.access_token = None
        self.token_expires_at = 0
        self.scope = "accounts balances transactions transfers beneficiarypayments documents.statements documents.taxcertificates"

    async def _get_token(self) -> None:
        """Get or refresh the OAuth token."""
        if self.access_token and time.time() < self.token_expires_at:
            return

        auth = base64.b64encode(f"{self.client_id}:{self.client_secret}".encode()).decode()
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.TOKEN_URL,
                headers={
                    "Authorization": f"Basic {auth}",
                    "x-api-key": self.api_key,
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                data={"grant_type": "client_credentials", "scope": self.scope}
            )
            
            response.raise_for_status()
            data = response.json()
            
            self.access_token = data["access_token"]
            self.token_expires_at = time.time() + data["expires_in"] - 60  # Buffer of 60 seconds

    async def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make an authenticated request to the Investec API."""
        await self._get_token()
        
        url = f"{self.API_URL}{endpoint}"
        
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "x-api-key": self.api_key,
            "Accept": "application/json"
        }
        
        if "headers" in kwargs:
            headers.update(kwargs.pop("headers"))
        
        async with httpx.AsyncClient() as client:
            response = await client.request(
                method,
                url,
                headers=headers,
                **kwargs
            )
            
            response.raise_for_status()
            return response.json()

    # Account information endpoints
    async def get_accounts(self) -> Dict[str, Any]:
        """
        Get a list of accounts with metadata regarding the account like Account name, 
        Account type and the profile it is associated to.
        
        Returns:
            Dict containing a list of accounts and associated metadata
        """
        return await self._make_request("GET", "/accounts")

    async def get_account_balance(self, account_id: str) -> Dict[str, Any]:
        """
        Get the balance for a specific account.
        
        Args:
            account_id: The ID of the account to retrieve the balance for
            
        Returns:
            Dict containing current, available, budget, straight and cash balances for the account
        """
        return await self._make_request("GET", f"/accounts/{account_id}/balance")

    async def get_account_transactions(
        self, 
        account_id: str, 
        from_date: Optional[str] = None, 
        to_date: Optional[str] = None,
        transaction_type: Optional[str] = None,
        include_pending: bool = False
    ) -> Dict[str, Any]:
        """
        Get transactions for a specific account with optional filtering.
        
        Args:
            account_id: The ID of the account to retrieve transactions for
            from_date: Optional start date in format YYYY-MM-DD
            to_date: Optional end date in format YYYY-MM-DD
            transaction_type: Optional transaction type filter
            include_pending: Whether to include pending transactions
            
        Returns:
            Dict containing transactions and metadata
        """
        params = {}
        if from_date:
            params["fromDate"] = from_date
        if to_date:
            params["toDate"] = to_date
        if transaction_type:
            params["transactionType"] = transaction_type
        if include_pending:
            params["includePending"] = "true"
            
        return await self._make_request(
            "GET", 
            f"/accounts/{account_id}/transactions", 
            params=params
        )

    async def get_pending_transactions(self, account_id: str) -> Dict[str, Any]:
        """
        Get pending transactions for a specific account.
        
        Args:
            account_id: The ID of the account to retrieve pending transactions for
            
        Returns:
            Dict containing pending transactions and metadata
        """
        return await self._make_request("GET", f"/accounts/{account_id}/pending-transactions")

    # Profile endpoints
    async def get_profiles(self) -> Dict[str, Any]:
        """
        Get a list of all profiles consented to.
        
        Returns:
            Dict containing a list of profiles and associated metadata
        """
        return await self._make_request("GET", "/profiles")
    
    async def get_profile_accounts(self, profile_id: str) -> Dict[str, Any]:
        """
        Get accounts for a specific profile.
        
        Args:
            profile_id: The ID of the profile to retrieve accounts for
            
        Returns:
            Dict containing accounts associated with the profile
        """
        return await self._make_request("GET", f"/profiles/{profile_id}/accounts")

    async def get_authorisation_setup_details(
        self, 
        profile_id: str, 
        account_id: str
    ) -> Dict[str, Any]:
        """
        Get authorisation setup details for a specific profile and account.
        
        Args:
            profile_id: The ID of the profile
            account_id: The ID of the account
            
        Returns:
            Dict containing authorisation setup details
        """
        return await self._make_request(
            "GET", 
            f"/profiles/{profile_id}/accounts/{account_id}/authorisationsetupdetails"
        )
    
    async def get_profile_beneficiaries(
        self, 
        profile_id: str, 
        account_id: str
    ) -> Dict[str, Any]:
        """
        Get beneficiaries for a specific profile and account.
        
        Args:
            profile_id: The ID of the profile
            account_id: The ID of the account
            
        Returns:
            Dict containing beneficiaries for the profile and account
        """
        return await self._make_request(
            "GET", 
            f"/profiles/{profile_id}/accounts/{account_id}/beneficiaries"
        )

    # Beneficiary endpoints
    async def get_beneficiaries(self) -> Dict[str, Any]:
        """
        Get all beneficiaries for the authenticated user.
        
        Returns:
            Dict containing a list of beneficiaries and associated metadata
        """
        return await self._make_request("GET", "/accounts/beneficiaries")
    
    async def get_beneficiary_categories(self) -> Dict[str, Any]:
        """
        Get all beneficiary categories available.
        
        Returns:
            Dict containing beneficiary categories
        """
        return await self._make_request("GET", "/accounts/beneficiarycategories")

    # Transfer and payment endpoints
    async def transfer_multiple(
        self, 
        from_account_id: str, 
        transfer_list: List[Dict[str, Union[str, float]]],
        profile_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Transfer funds to one or multiple accounts.
        
        Args:
            from_account_id: The ID of the source account
            transfer_list: List of transfers to make
            profile_id: Optional profile ID
            
        Returns:
            Dict containing transfer responses
        """
        payload = {"transferList": transfer_list}
        if profile_id:
            payload["profileId"] = profile_id
            
        return await self._make_request(
            "POST",
            f"/accounts/{from_account_id}/transfermultiple",
            json=payload,
            headers={"Content-Type": "application/json"}
        )

    async def pay_multiple(
        self, 
        account_id: str, 
        payment_list: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Pay funds to one or multiple beneficiaries.
        
        Args:
            account_id: The ID of the source account
            payment_list: List of payments to make
            
        Returns:
            Dict containing payment responses
        """
        return await self._make_request(
            "POST",
            f"/accounts/{account_id}/paymultiple",
            json={"paymentList": payment_list},
            headers={"Content-Type": "application/json"}
        )

    # Document endpoints
    async def get_documents(
        self, 
        account_id: str, 
        from_date: str, 
        to_date: str
    ) -> Dict[str, Any]:
        """
        Get a list of documents for a specific account within a date range.
        
        Args:
            account_id: The ID of the account to retrieve documents for
            from_date: Start date in format YYYY-MM-DD
            to_date: End date in format YYYY-MM-DD
            
        Returns:
            Dict containing documents and metadata
        """
        params = {"fromDate": from_date, "toDate": to_date}
        return await self._make_request(
            "GET", 
            f"/accounts/{account_id}/documents", 
            params=params
        )
    
    async def get_document(
        self, 
        account_id: str, 
        document_type: str, 
        document_date: str
    ) -> Dict[str, Any]:
        """
        Get a specific document.
        
        Args:
            account_id: The ID of the account
            document_type: The type of document
            document_date: The date of the document in format YYYY-MM-DD
            
        Returns:
            Dict containing document data
        """
        return await self._make_request(
            "GET", 
            f"/accounts/{account_id}/document/{document_type}/{document_date}"
        )

    # Convenience methods that combine or simplify the API endpoints
    async def transfer_money(
        self, from_account_id: str, to_account_id: str, amount: float, reference: str
    ) -> Dict[str, Any]:
        """
        Transfer money between accounts.
        
        Args:
            from_account_id: The ID of the source account
            to_account_id: The ID of the destination account
            amount: The amount to transfer
            reference: A reference for the transaction
            
        Returns:
            Dict containing transfer response
        """
        transfer_list = [
            {
                "beneficiaryAccountId": to_account_id,
                "amount": str(amount),
                "myReference": reference,
                "theirReference": reference
            }
        ]
        return await self.transfer_multiple(from_account_id, transfer_list)

    async def pay_beneficiary(
        self, account_id: str, beneficiary_id: str, amount: float, reference: str
    ) -> Dict[str, Any]:
        """
        Pay a saved beneficiary.
        
        Args:
            account_id: The ID of the source account
            beneficiary_id: The ID of the beneficiary to pay
            amount: The amount to pay
            reference: A reference for the payment
            
        Returns:
            Dict containing payment response
        """
        payment_list = [
            {
                "beneficiaryId": beneficiary_id,
                "amount": str(amount),
                "myReference": reference,
                "theirReference": reference
            }
        ]
        return await self.pay_multiple(account_id, payment_list)

def get_investec_api_client() -> InvestecClient:
    """Create and configure an Investec API client from environment variables."""
    client_id = os.getenv("INVESTEC_CLIENT_ID", "")
    client_secret = os.getenv("INVESTEC_CLIENT_SECRET", "")
    api_key = os.getenv("INVESTEC_API_KEY", "")
    
    if not all([client_id, client_secret, api_key]):
        raise ValueError(
            "Missing required environment variables: "
            "INVESTEC_CLIENT_ID, INVESTEC_CLIENT_SECRET, or INVESTEC_API_KEY"
        )
    
    return InvestecClient(client_id, client_secret, api_key)