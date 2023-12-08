

from pydantic import BaseModel, field_validator, ValidationError, Field, ValidationInfo
from contentctl.objects.mitre_attack_enrichment import MitreAttackEnrichment
from contentctl.objects.enums import StoryCategory, DataModel, KillChainPhase, SecurityContentProductName
from typing import List
from typing_extensions import Annotated
from enum import Enum

class StoryUseCase(str,Enum):
   FRAUD_DETECTION = "Fraud Detection"
   COMPLIANCE = "Compliance"
   APPLICATION_SECURITY = "Application Security"
   SECURITY_MONITORING = "Security Monitoring"
   ADVANCED_THREAD_DETECTION = "Advanced Threat Detection"

class StoryTags(BaseModel):
    category: list[StoryCategory] = Field(...,min_length=1)
    product: list[SecurityContentProductName] = Field(...,min_length=1)
    usecase: StoryUseCase = Field(...)

    # enrichment
    mitre_attack_enrichments: List[MitreAttackEnrichment] = []
    mitre_attack_tactics: List[Annotated[str, Field(pattern="^T\d{4}(.\d{3})?$")]] = []
    datamodels: List[DataModel] = []
    kill_chain_phases: List[KillChainPhase] = []
