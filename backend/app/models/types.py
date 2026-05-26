from sqlalchemy import JSON
from sqlalchemy.dialects import postgresql


json_type = JSON().with_variant(postgresql.JSONB(), "postgresql")
