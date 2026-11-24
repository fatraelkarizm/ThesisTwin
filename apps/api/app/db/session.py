from collections.abc import Iterator

from sqlalchemy import Engine, create_engine, event
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import settings


class Base(DeclarativeBase):
    pass


def make_engine(url: str) -> Engine:
    engine = create_engine(url)
    if engine.dialect.name == "sqlite":
        # SQLite mengabaikan foreign key kecuali diaktifkan per koneksi.
        @event.listens_for(engine, "connect")
        def _fk_on(dbapi_conn, _):  # noqa: ANN001
            dbapi_conn.execute("PRAGMA foreign_keys=ON")

    return engine


engine = make_engine(settings.database_url)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)


def init_db(bind: Engine | None = None) -> None:
    from app.db import models  # noqa: F401  (daftarkan tabel)

    target = bind or engine
    Base.metadata.create_all(target)
    _add_missing_nullable_columns(target)


def _add_missing_nullable_columns(target: Engine) -> None:
    """Migrasi aditif minimal: kolom baru yang nullable ditambahkan ke tabel lama.

    create_all tidak mengubah tabel yang sudah ada. Ini cukup untuk perubahan aditif selama
    SQLite dipakai; perubahan lain (ubah tipe, hapus kolom) butuh Alembic.
    """
    from sqlalchemy import inspect, text

    insp = inspect(target)
    with target.begin() as conn:
        for table in Base.metadata.sorted_tables:
            if not insp.has_table(table.name):
                continue
            existing = {c["name"] for c in insp.get_columns(table.name)}
            for col in table.columns:
                if col.name in existing:
                    continue
                if not col.nullable:
                    raise RuntimeError(
                        f"Kolom wajib baru {table.name}.{col.name} butuh migrasi manual (Alembic)."
                    )
                ddl = col.type.compile(dialect=target.dialect)
                conn.execute(text(f'ALTER TABLE "{table.name}" ADD COLUMN "{col.name}" {ddl}'))


def get_session() -> Iterator[Session]:
    with SessionLocal() as session:
        yield session
