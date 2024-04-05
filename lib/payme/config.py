from pydantic_settings import BaseSettings


class DB(BaseSettings):
    host: str
    port: int
    name: str
    user: str
    password: str


class PaymeSettings(BaseSettings):
    min_amount: float = 1
    order_model: str
    key: str
    id: int
    account: str
    call_back_url: str
    url: str


class SettingsExtractor(BaseSettings):
    DB__HOST: str
    DB__PORT: int
    DB__NAME: str
    DB__USER: str
    DB__PASSWORD: str

    PAYME_MIN_AMOUNT: float = 1
    ORDER_MODEL: str
    PAYME_KEY: str
    PAYME_ID: int
    PAYME_ACCOUNT: str
    PAYME_CALL_BACK_URL: str
    PAYME_URL: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


class Settings(BaseSettings):
    db: DB
    payme: PaymeSettings


async def get_settings() -> Settings:
    settings = SettingsExtractor()

    return Settings(
        db=DB(
            host=settings.DB__HOST,
            port=settings.DB__PORT,
            name=settings.DB__NAME,
            user=settings.DB__USER,
            password=settings.DB__PASSWORD,
        ),
        payme=PaymeSettings(
            min_amount=settings.PAYME_MIN_AMOUNT,
            ordeR_model=settings.ORDER_MODEL,
            key=settings.PAYME_KEY,
            id=settings.PAYME_ID,
            account=settings.PAYME_ACCOUNT,
            call_back_url=settings.PAYME_CALL_BACK_URL,
            url=settings.PAYME_URL
        )
    )
