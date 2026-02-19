from extensions import db
from sqlalchemy import Column, String, Text, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

users_favorites = db.Table(
    "users_favorites",
    db.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("destination_id", ForeignKey("destinations.id"), primary_key=True)
)


class User(db.Model):
    __tablename__ = "users"

    id : Mapped[int] = mapped_column(primary_key=True)
    nom: Mapped[str] = mapped_column(String(100))
    prenom: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    adresse: Mapped[str] = mapped_column(String)

    favorites: Mapped[list["Destination"]] = relationship("Destination", secondary="users_favorites")


class Destination(db.Model):
    __tablename__ = "destinations"

    id : Mapped[int] = mapped_column(primary_key=True)
    city : Mapped[str] = mapped_column(String(100))
    country : Mapped[str] = mapped_column(String, nullable=False)
    description : Mapped[str] = mapped_column(Text)


class Activity(db.Model):
    __tablename__ = "activitys"

    id : Mapped[int] = mapped_column(primary_key=True)
    name : Mapped[str] = mapped_column(String, unique=False, nullable=False)
    type : Mapped[str] = mapped_column(String, unique=False, nullable=False)
    price_estimated: Mapped[float] = mapped_column(Float)
    destination_id: Mapped[int | None] = mapped_column(ForeignKey("destinations.id"), nullable=True)
    destination: Mapped["Destination | None"] = relationship("Destination", backref="activities")

