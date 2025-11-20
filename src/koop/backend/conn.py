# https://apidocs.koordinates.com/

import os

import requests


class KoordinatesConnection:
    """A class representing the Koordinates API."""

    def __init__(
        self,
        api_key: str | None = None,
        domain: str = "ttgroup.koordinates.com",
        api_version: str = "1.x",
    ) -> None:
        """Initialize the Koordinates API client.

        Args:
            api_key: The API key. If not provided, it will be read from the environment.
            domain: The domain of the API. Defaults to "ttgroup.koordinates.com". Use
            "data.linz.govt.nz" for querying from LINZ.
            api_version: The version of the API. Defaults to "1.x".
        """
        if api_key is None:
            # Get it from the environment
            api_key = os.environ.get("KOORDINATES_API_KEY")

        if api_key is None:
            msg = "Please set the KOORDINATES_API_KEY environment variable in the .env file."
            raise ValueError(msg)

        self.domain = domain
        self.api_key = api_key
        self.api_version = api_version
        self.session = self._create_session()

    def _create_session(self) -> requests.Session:
        """Create a session with the Koordinates API.

        Returns:
            requests.Session: The session.
        """
        session = requests.Session()

        # HeaderTokenAuthentication
        session.headers.update(
            {
                "Authorization": f"key {self.api_key}",
            }
        )

        # Authenticate the session
        response = session.get(f"https://{self.domain}/login/?next=/")
        response.raise_for_status()

        return session

    def close(self) -> None:
        """Close the session."""
        self.session.close()
