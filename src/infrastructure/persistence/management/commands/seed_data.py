from django.core.management.base import BaseCommand
from django.db import transaction
import json

from src.infrastructure.persistence.models import (
    Country,
    State,
    City,
    Language,
    InterestedPlatform,
    Occupation,
)


class Command(BaseCommand):
    help = "Seed initial/master data"

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING("🌱 Seeding data..."))

        self.seed_countries()
        self.seed_languages()
        self.seed_platforms()
        self.seed_occupations()

        self.stdout.write(self.style.SUCCESS("✅ Seeding completed"))

    def seed_countries(self):
        path = "src/infrastructure/persistence/data/countries_states_cities.json"

        try:
            with open(path, encoding="utf-8") as fh:
                countries = json.load(fh)
        except FileNotFoundError:
            self.stdout.write(self.style.WARNING(f"Countries JSON not found at {path}, skipping."))
            return

        for country_data in countries:
            country_title = country_data.get("name") or country_data.get("title")

            # ✅ COUNTRY (unique by iso2 OR title)
            country_lookup = {
                "iso2": country_data.get("iso2")
            } if country_data.get("iso2") else {
                "title": country_title
            }

            country_defaults = {
                "title": country_title,
                "iso2": country_data.get("iso2"),
                "iso3": country_data.get("iso3"),
            }

            country, _ = Country.objects.update_or_create(
                **country_lookup,
                defaults=country_defaults
            )

            # ---------- STATES ----------
            for state_data in country_data.get("states", []):
                state_title = state_data.get("name") or state_data.get("title")

                # ✅ must match UNIQUE(country, title)
                state_lookup = {
                    "country": country,
                    "title": state_title,
                }

                # State model has no iso2 field; only set fields that exist.
                state_defaults = {}
    
                state, _ = State.objects.update_or_create(
                    **state_lookup,
                    defaults=state_defaults
                )

                # ---------- CITIES ----------
                for city_data in state_data.get("cities", []):
                    city_title = city_data.get("name") or city_data.get("title")

                    # ✅ must match UNIQUE(state, title)
                    city_lookup = {
                        "state": state,
                        "title": city_title,
                    }

                    city_defaults = {
                        "country": country,
                        "country_name": country.title,
                        "state_name": state.title,
                    }

                    City.objects.update_or_create(
                        **city_lookup,
                        defaults=city_defaults
                    )

        self.stdout.write(self.style.SUCCESS("Countries, states, and cities seeded successfully ✔"))

    def seed_languages(self):
        for title in ["English", "हिंदी", "Gujrati", "Marathi", "Tamil (தமிழ்)", "Telugu (తెలుగు)", "Kannada (ಕನ್ನಡ)", "Malayalam (മലയാളം)"]:
            Language.objects.get_or_create(title=title)

    def seed_platforms(self):
        for title in ["YouTube", "Instagram", "Telegram"]:
            InterestedPlatform.objects.get_or_create(title=title)

    def seed_occupations(self):
        for title in ["Business Owner", "Working Professional", "House wife", "Student", "Existing Saller"]:
            Occupation.objects.get_or_create(title=title)
