from decimal import Decimal
from datetime import date
from sqlmodel import SQLModel, Field

class FileHash(SQLModel, table=True):
    id: int|None = Field(default=None, primary_key=True)
    hash: str = Field(default=None, nullable=False)
    filepath: str =Field(default=None, nullable=False)

class Df1(SQLModel, table=True):
    __tablename__ = "df1s"

    id: int | None = Field(default=None, primary_key=True)

    PERIOD_M: int | None = Field(
        default=None,
        description="Місяць звітного періоду"
    )

    PERIOD_Y: int | None = Field(
        default=None,
        description="Рік звітного періоду"
    )

    UKR_GROMAD: int | None = Field(
        default=None,
        description="Ознака громадянства України"
    )

    ST: int | None = Field(
        default=None,
        description="Статус"
    )

    NUMIDENT: str | None = Field(
        default=None,
        max_length=20,#real numident is exatly 10 digits, but other entities may be here
        description="Ідентифікаційний номер"
    )

    LN: str | None = Field(
        default=None,
        max_length=100,
        description="Прізвище"
    )

    NM: str | None = Field(
        default=None,
        max_length=100,
        description="Ім’я"
    )

    FTN: str | None = Field(
        default=None,
        max_length=100,
        description="По батькові"
    )

    ZO: int | None = Field(default=None)
    PAY_TP: int | None = Field(default=None)
    PAY_MNTH: int | None = Field(default=None)
    PAY_YEAR: int | None = Field(default=None)

    SUM_TOTAL: Decimal | None = Field(default=None, max_digits=16, decimal_places=2)
    SUM_MAX: Decimal | None = Field(default=None, max_digits=16, decimal_places=2)
    SUM_INS: Decimal | None = Field(default=None, max_digits=16, decimal_places=2)

    OTK: int | None = Field(default=None)
    EXP: int | None = Field(default=None)

    KD_NP: int | None = Field(default=None)
    KD_NZP: int | None = Field(default=None)
    KD_PTV: int | None = Field(default=None)
    NRM: int | None = Field(default=None)
    KD_VP: int | None = Field(default=None)

    SUM_DIFF: Decimal | None = Field(
        default=None,
        max_digits=16,
        decimal_places=2
    )

    SUM_NARAH: Decimal | None = Field(
        default=None,
        max_digits=16,
        decimal_places=2
    )

    NRC: int | None = Field(default=None)

    OZN: str | None = Field(default=None, max_length=1)
    OTD: str | None = Field(default=None, max_length=1)

    SYS_ERROR: str | None = Field(default=None, max_length=2000)

    @property
    def sum_total_display(self):
        if str(self.PAY_TP) == "3":
            return -self.SUM_TOTAL
        return self.SUM_TOTAL

    @property
    def sum_max_display(self):
        if str(self.PAY_TP) == "3":
            return -self.SUM_MAX
        return self.SUM_MAX

    @property
    def sum_narah_display(self):
        if str(self.PAY_TP) == "3":
            return -self.SUM_NARAH
        return self.SUM_NARAH

class Df4(SQLModel, table=True):
    """
    Дані таблиці dBase III Plus.

    Містить інформацію про:
    - звітний період
    - фізичну особу
    - доходи
    - податки
    - дати прийняття / звільнення
    - податкові ознаки
    """

    __tablename__ = "df4s"

    id: int | None = Field(
        default=None,
        primary_key=True,
        description="Внутрішній ID запису"
    )

    NP: int | None = Field(
        default=None,
        description="Порядковий номер запису"
    )

    PERIOD: int | None = Field(
        default=None,
        description="Місяць звітного періоду"
    )

    RIK: int | None = Field(
        default=None,
        description="Рік звітного періоду"
    )

    KOD: str = Field(
        default="",
        max_length=10,
        description="Код або службовий ідентифікатор запису"
    )

    TYP: int | None = Field(
        default=None,
        description="Тип запису"
    )

    TIN: str = Field(
        default="",
        max_length=10,
        description="РНОКПП / ІПН фізичної особи"
    )

    S_NAR: Decimal | None = Field(
        default=Decimal("0.00"),
        max_digits=12,
        decimal_places=2,
        description="Сума нарахованого доходу"
    )

    S_DOX: Decimal | None = Field(
        default=Decimal("0.00"),
        max_digits=12,
        decimal_places=2,
        description="Сума виплаченого доходу"
    )

    S_TAXN: Decimal | None = Field(
        default=Decimal("0.00"),
        max_digits=12,
        decimal_places=2,
        description="Сума нарахованого податку"
    )

    S_TAXP: Decimal | None = Field(
        default=Decimal("0.00"),
        max_digits=12,
        decimal_places=2,
        description="Сума перерахованого податку"
    )

    OZN_DOX: int | None = Field(
        default=None,
        description="Ознака доходу"
    )

    D_PRIYN: date | None = Field(
        default=None,
        description="Дата прийняття працівника"
    )

    D_ZVILN: date | None = Field(
        default=None,
        description="Дата звільнення працівника"
    )

    OZN_PILG: int | None = Field(
        default=None,
        description="Ознака податкової пільги"
    )

    OZNAKA: str = Field(
        default="",
        max_length=1,
        description="Додаткова службова ознака"
    )

    A051: Decimal | None = Field(
        default=Decimal("0.00"),
        max_digits=12,
        decimal_places=2,
        description="Додаткове числове поле A051"
    )

    A05: Decimal | None = Field(
        default=Decimal("0.00"),
        max_digits=12,
        decimal_places=2,
        description="Додаткове числове поле A05"
    )
    SYS_ERROR: str | None = Field(default=None, max_length=2000)
    
class Df5(SQLModel, table=True):
    """
    Дані про трудові відносини, професію, посаду
    та періоди роботи фізичної особи.

    Імовірно використовується у звітності ЄСВ / ПФУ /
    кадровому обліку.
    """

    __tablename__ = "df5s"

    id: int | None = Field(
        default=None,
        primary_key=True
    )

    PERIOD_M: int | None = Field(
        default=None,
        description="Звітний місяць"
    )

    PERIOD_Y: int | None = Field(
        default=None,
        description="Звітний рік"
    )

    UKR_GROMAD: int | None = Field(
        default=None,
        description="Ознака громадянства України"
    )

    NUMIDENT: str | None = Field(
        default=None,
        max_length=10,
        description="Ідентифікаційний номер особи"
    )

    LN: str | None = Field(
        default=None,
        max_length=100,
        description="Прізвище"
    )

    NM: str | None = Field(
        default=None,
        max_length=100,
        description="Ім’я"
    )

    FTN: str | None = Field(
        default=None,
        max_length=100,
        description="По батькові"
    )

    START_DT: date | None = Field(
        default=None,
        description="Дата початку трудових відносин"
    )

    END_DT: date | None = Field(
        default=None,
        description="Дата завершення трудових відносин"
    )

    ZO: int | None = Field(
        default=None,
        description="Код категорії застрахованої особи"
    )

    PID_ZV: str | None = Field(
        default=None,
        max_length=150,
        description="Підстава або ідентифікатор звільнення"
    )

    NRM_DT: date | None = Field(
        default=None,
        description="Дата наказу або нормативного документа"
    )

    DOG_CPH: int | None = Field(
        default=None,
        description="Ознака цивільно-правового договору"
    )

    PNR: str | None = Field(
        default=None,
        max_length=250,
        description="Назва професії або робіт"
    )

    PROF: str | None = Field(
        default=None,
        max_length=6,
        description="Код професії"
    )

    POS: str | None = Field(
        default=None,
        max_length=250,
        description="Назва посади"
    )

    PID: str | None = Field(
        default=None,
        max_length=250,
        description="Підстава прийняття або кадровий документ"
    )

    VZV: str | None = Field(
        default=None,
        max_length=250,
        description="Вид зайнятості або відносин"
    )

    VS: int | None = Field(
        default=None,
        description="Ознака військової служби або спецстатусу"
    )

    PIR: int | None = Field(
        default=None,
        description="Ознака пільги або спеціального режиму"
    )

    OZN: str | None = Field(
        default=None,
        max_length=1,
        description="Службова ознака запису"
    )

    SYS_ERROR: str | None = Field(default=None, max_length=2000)