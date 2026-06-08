from scripts.seed_dream_camp import main as seed_dream_camp
from scripts.seed_groups_sections_for_dream_camp import main as seed_groups_sections


def main() -> None:
    seed_dream_camp()
    seed_groups_sections()
    print("Dream Camp reset complete.")


if __name__ == "__main__":
    main()