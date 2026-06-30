from __future__ import annotations

import asyncio
from pathlib import Path
from sqlalchemy import text
from app.core.database import engine

MIGRATIONS_DIR = Path(__file__).resolve().parents[1] / "migrations" / "versions"


def split_sql_statements(sql: str) -> list[str]:
    statements: list[str] = []
    current: list[str] = []
    in_single_quote = False
    in_double_quote = False
    line_comment = False

    index = 0
    while index < len(sql):
        char = sql[index]
        next_char = sql[index + 1] if index + 1 < len(sql) else ""

        if line_comment:
            current.append(char)
            if char == "\n":
                line_comment = False
            index += 1
            continue

        if not in_single_quote and not in_double_quote and char == "-" and next_char == "-":
            line_comment = True
            current.append(char)
            current.append(next_char)
            index += 2
            continue

        if char == "'" and not in_double_quote:
            in_single_quote = not in_single_quote
            current.append(char)
            index += 1
            continue

        if char == '"' and not in_single_quote:
            in_double_quote = not in_double_quote
            current.append(char)
            index += 1
            continue

        if char == ";" and not in_single_quote and not in_double_quote:
            statement = "".join(current).strip()
            if statement:
                statements.append(statement)
            current = []
            index += 1
            continue

        current.append(char)
        index += 1

    tail = "".join(current).strip()
    if tail:
        statements.append(tail)
    return statements


async def run() -> None:
    files = sorted(MIGRATIONS_DIR.glob("*.sql"))
    if not files:
        print("No migration files found.")
        return

    async with engine.begin() as connection:
        await connection.execute(
            text(
                "CREATE TABLE IF NOT EXISTS schema_migrations "
                "(version TEXT PRIMARY KEY, applied_at TIMESTAMPTZ NOT NULL DEFAULT now())"
            )
        )
        applied = {
            row[0]
            for row in (await connection.execute(text("SELECT version FROM schema_migrations"))).all()
        }

        for file in files:
            if file.name in applied:
                print(f"Skipping {file.name}")
                continue

            print(f"Applying {file.name}")
            for statement in split_sql_statements(file.read_text(encoding="utf-8")):
                await connection.execute(text(statement))
            await connection.execute(
                text("INSERT INTO schema_migrations (version) VALUES (:version)"),
                {"version": file.name},
            )

    await engine.dispose()
    print("Migrations complete.")


if __name__ == "__main__":
    asyncio.run(run())