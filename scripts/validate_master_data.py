import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
GAME_DATA_DIR = PROJECT_ROOT / "data" / "game-data"
IMAGE_DIR = PROJECT_ROOT / "data" / "img"

DATASETS = {
	"Character": ("characters.json", "characters"),
	"Weapon": ("weapons.json", "weapons"),
	"Echo": ("echoes.json", "echoes"),
}

def load_json(file_path: Path) -> list[dict]:
    try:
        with file_path.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        raise ValueError(f"JSON 파일을 찾을 수 없습니다: {file_path}")
    except json.JSONDecodeError as error:
        raise ValueError(f"JSON 형식이 올바르지 않습니다: {error}") from error

    if not isinstance(data, list):
        raise ValueError(f"JSON 최상위 구조가 배열이 아닙니다: {file_path}")

    return data

def validate_dataset(
    label: str,
    json_filename: str,
    image_directory: str,
) -> bool:
    json_path = GAME_DATA_DIR / json_filename
    image_dir = IMAGE_DIR / image_directory

    data = load_json(json_path)

    slugs: list[str] = []
    image_keys: list[str] = []
    errors: list[str] = []

    for index, item in enumerate(data, start=1):
        if not isinstance(item, dict):
            errors.append(f"{index}번째 데이터가 객체가 아닙니다.")
            continue

        slug = item.get("slug")
        image_key = item.get("imageKey")

        if not isinstance(slug, str) or not slug:
            errors.append(f"{index}번째 데이터의 slug가 올바르지 않습니다.")
        else:
            slugs.append(slug)

        if not isinstance(image_key, str) or not image_key:
            errors.append(f"{index}번째 데이터의 imageKey가 올바르지 않습니다.")
            continue

        image_keys.append(image_key)

        image_path = IMAGE_DIR / image_key

        if not image_path.is_file():
            errors.append(f"이미지 누락: {image_key}")

    duplicate_slugs = {
        slug for slug in slugs
        if slugs.count(slug) > 1
    }

    duplicate_image_keys = {
        key for key in image_keys
        if image_keys.count(key) > 1
    }

    actual_images = {
        f"{image_directory}/{path.name}"
        for path in image_dir.iterdir()
        if path.is_file()
    }

    referenced_images = set(image_keys)
    unused_images = actual_images - referenced_images

    if duplicate_slugs:
        errors.append(
            f"중복 slug: {', '.join(sorted(duplicate_slugs))}"
        )

    if duplicate_image_keys:
        errors.append(
            f"중복 imageKey: {', '.join(sorted(duplicate_image_keys))}"
        )

    for image_key in sorted(unused_images):
        errors.append(f"사용되지 않는 이미지: {image_key}")

    print(f"\n[{label}]")
    print(f"JSON records : {len(data)}")
    print(f"Image files  : {len(actual_images)}")

    if errors:
        print("Result       : FAIL")

        for error in errors:
            print(f"- {error}")

        return False

    print("Result       : PASS")
    return True

def main() -> int:
    all_passed = True

    for label, (json_filename, image_directory) in DATASETS.items():
        try:
            passed = validate_dataset(
                label,
                json_filename,
                image_directory,
            )
        except ValueError as error:
            print(f"\n[{label}]")
            print("Result       : FAIL")
            print(f"- {error}")
            passed = False

        if not passed:
            all_passed = False

    print("\n[Summary]")

    if all_passed:
        print("All master data checks passed.")
        return 0

    print("Master data validation failed.")
    return 1


if __name__ == "__main__":
    sys.exit(main())