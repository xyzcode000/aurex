from app.schemas.risk_engine import (
    RiskEngineRequest,
    RiskEngineResponse
)


class RiskEngineClient:
    """
    Client interface for communicating with the AUREX
    Risk / Anomaly Engine.

    The actual engine connection will be added once
    the engine endpoint/interface is provided.
    """

    def analyze(
        self,
        request: RiskEngineRequest
    ) -> RiskEngineResponse:
        raise NotImplementedError(
            "Risk Engine connection is not configured yet."
        )