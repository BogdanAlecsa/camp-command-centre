from pathlib import Path
import subprocess
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def run_script(script_name: str) -> None:
    script_path = PROJECT_ROOT / "scripts" / script_name
    subprocess.run([sys.executable, str(script_path)], check=True)


def main() -> None:
    run_script("seed_dream_camp.py")
    run_script("seed_groups_sections_for_dream_camp.py")
    run_script("seed_presence_windows.py")
    print("Dream Camp reset complete.")


if __name__ == "__main__":
    main()
