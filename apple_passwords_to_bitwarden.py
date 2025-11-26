import argparse
import pandas as pd
from pathlib import Path

def normalize_domain(url: str) -> str:
    if not isinstance(url, str) or not url.strip():
        return ""
    u = url.strip().lower()
    for prefix in ("https://", "http://"):
        if u.startswith(prefix):
            u = u[len(prefix):]
    u = u.split("/")[0]
    if u.startswith("www."):
        u = u[4:]
    return u

def load_csv(path: Path):
    if not path.exists():
        raise FileNotFoundError(f"CSV file not found: {path}")
    return pd.read_csv(path, dtype=str).fillna("")

def add_marker(notes, marker):
    n = (notes or "").strip()
    if marker:
        if n:
            return n + "\n\n" + marker
        else:
            return marker
    else:
        return n

def main():
    parser = argparse.ArgumentParser(
        description="Migrate missing passwords from Apple Passwords CSV export to Bitwarden CSV format."
    )
    parser.add_argument(
        "-b", "--bitwarden", required=True, help="Path to Bitwarden export CSV"
    )
    parser.add_argument(
        "-a", "--apple", required=True, help="Path to Apple Passwords export CSV"
    )
    parser.add_argument(
        "-o", "--output", default="AppleToBitwarden.csv", help="Output CSV file path"
    )
    parser.add_argument("--apple-url-col", default="URL", help="Apple Passwords URL column name")
    parser.add_argument("--apple-user-col", default="Username", help="Apple Passwords username column name")
    parser.add_argument("--apple-pass-col", default="Password", help="Apple Passwords password column name")
    parser.add_argument("--apple-title-col", default="Title", help="Apple Passwords title column name")
    parser.add_argument("--apple-notes-col", default="Notes", help="Apple Passwords notes column name")
    parser.add_argument("--apple-totp-col", default="OTPAuth", help="Apple Passwords TOTP column name")
    parser.add_argument(
        "--marker",
        default="Migrated from Apple Passwords",
        help="Custom marker to append to notes (use empty string to disable)"
    )

    args = parser.parse_args()

    try:
        bw = load_csv(Path(args.bitwarden))
        apple = load_csv(Path(args.apple))
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return

    bw["__domain"] = bw["login_uri"].apply(normalize_domain)
    bw["__key"] = bw["__domain"] + "||" + bw["login_username"].str.strip().str.lower()

    apple["__domain"] = apple[args.apple_url_col].apply(normalize_domain)
    apple["__key"] = apple["__domain"] + "||" + apple[args.apple_user_col].str.strip().str.lower()

    bw_keys = set(bw["__key"])
    missing_mask = ~apple["__key"].isin(bw_keys)
    missing = apple[missing_mask].copy()

    print(f"Total Apple entries: {len(apple)}")
    print(f"Entries missing in Bitwarden: {len(missing)}")

    out = pd.DataFrame(
        columns=[
            "folder",
            "favorite",
            "type",
            "name",
            "notes",
            "fields",
            "reprompt",
            "login_uri",
            "login_username",
            "login_password",
            "login_totp",
        ]
    )

    out["folder"] = ""
    out["favorite"] = "0"
    out["type"] = "login"
    out["name"] = missing[args.apple_title_col]

    notes_series = missing.get(args.apple_notes_col, "").replace("\r\n", "\n").replace("\r", "\n")
    out["notes"] = notes_series.apply(lambda n: add_marker(n, args.marker))

    out["fields"] = ""
    out["reprompt"] = "0"
    out["login_uri"] = missing[args.apple_url_col]
    out["login_username"] = missing[args.apple_user_col]
    out["login_password"] = missing[args.apple_pass_col]
    out["login_totp"] = missing.get(args.apple_totp_col, "")

    out.to_csv(args.output, index=False)

    print(f"Wrote {len(out)} entries to {args.output}")

if __name__ == "__main__":
    main()
