"""Config routes — GET/POST /config"""
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class MachineConfig(BaseModel):
    group1_shot_secs: int = 28
    group2_shot_secs: int = 27
    steamer_warmup_secs: int = 8
    grinder_secs: int = 10
    assemble_secs: int = 15
    milk_whole_secs: int = 24
    milk_oat_secs: int = 32
    milk_almond_secs: int = 30
    milk_soy_secs: int = 28


class SchedulerConfig(BaseModel):
    max_concurrent_slots: int = 3
    wait_weight: float = 0.70
    complexity_weight: float = 0.20
    machine_weight: float = 0.10


class RLConfig(BaseModel):
    learning_rate: float = 0.03
    discount_factor: float = 0.95
    epsilon: float = 0.12
    live_training: bool = True


class FeatureToggles(BaseModel):
    rush_mode_auto: bool = True
    concurrent_suggestions: bool = True
    rl_live_retraining: bool = True
    demand_forecasting: bool = True
    post_rush_report: bool = True
    error_recovery: bool = False


class AppConfig(BaseModel):
    machine: MachineConfig = MachineConfig()
    scheduler: SchedulerConfig = SchedulerConfig()
    rl: RLConfig = RLConfig()
    features: FeatureToggles = FeatureToggles()


# In-memory config (replace with DB in production)
_config = AppConfig()


@router.get("/", response_model=AppConfig)
def get_config() -> AppConfig:
    return _config


@router.post("/", response_model=AppConfig)
def update_config(body: AppConfig) -> AppConfig:
    global _config
    _config = body
    return _config


@router.post("/reset", response_model=AppConfig)
def reset_config() -> AppConfig:
    global _config
    _config = AppConfig()
    return _config
