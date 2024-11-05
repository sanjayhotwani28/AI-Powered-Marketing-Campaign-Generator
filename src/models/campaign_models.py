from typing import Dict, List, Any, TypedDict
from dataclasses import dataclass
from datetime import datetime


class VisualElements(TypedDict):
    color_scheme: str
    imagery: str
    layout: str
    visual_hierarchy: str


class ChannelStrategy(TypedDict):
    primary_channels: List[str]
    secondary_channels: List[str]
    channel_specific_adaptations: Dict[str, str]


class PersonalizationElements(TypedDict):
    key_variables: List[str]
    dynamic_content: List[str]
    personalization_rules: str


class ToneGuidelines(TypedDict):
    voice: str
    style: str
    language_level: str


class CampaignMetadata(TypedDict):
    generated_at: str
    customer_segment: str
    model_version: str
    brand_guidelines_version: str


class CampaignContent(TypedDict):
    primary_message: str
    secondary_message: str
    visual_elements: VisualElements
    channel_strategy: ChannelStrategy
    personalization_elements: PersonalizationElements
    tone_guidelines: ToneGuidelines
    metadata: CampaignMetadata


@dataclass
class CustomerPersona:
    demographic: Dict[str, Any]
    behavioral: Dict[str, Any]
    psychographic: Dict[str, Any]


@dataclass
class CampaignPerformance:
    engagement_rate: float
    optimization_score: float
    personalization_score: float
    brand_alignment_score: float
    timestamp: datetime

    @property
    def overall_score(self) -> float:
        """Calculate overall campaign performance score"""
        weights = {
            'engagement': 0.3,
            'optimization': 0.25,
            'personalization': 0.25,
            'brand_alignment': 0.2
        }

        return (
                self.engagement_rate * weights['engagement'] +
                self.optimization_score * weights['optimization'] +
                self.personalization_score * weights['personalization'] +
                self.brand_alignment_score * weights['brand_alignment']
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert performance metrics to dictionary"""
        return {
            'engagement_rate': self.engagement_rate,
            'optimization_score': self.optimization_score,
            'personalization_score': self.personalization_score,
            'brand_alignment_score': self.brand_alignment_score,
            'overall_score': self.overall_score,
            'timestamp': self.timestamp.isoformat()
        }