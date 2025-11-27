# Apple Passwords to Bitwarden Migration

This tool helps Mac users migrate missing password entries from Apple Passwords CSV exports into Bitwarden's CSV import format. It assists in consolidating password vaults securely and avoiding duplicates during migration.

## What this tool does

If you simply export everything from Apple Passwords and import it into Bitwarden, Bitwarden will happily import every row, including entries you already have, and you can end up with a vault full of duplicate logins.

This tool compares your existing Bitwarden export with your Apple Passwords export and keeps only the Apple entries that are truly new. In plain terms: you give it your Bitwarden CSV and your Apple Passwords CSV, and it spits out a new CSV that contains only the Apple logins Bitwarden doesn’t already know about.

## When this tool is a good fit

Use this tool when:

- You already have a Bitwarden CSV export and an Apple Passwords CSV export, and you want to merge them without duplicating existing Bitwarden logins.
- You have been using Bitwarden for a while and now want to bring over the remaining Apple Passwords entries, but you do not want to manually clean up hundreds of duplicates after a blind import.
- You primarily use Apple devices but are moving your day‑to‑day password management to Bitwarden and need a one‑time or occasional sync of “leftover” Apple‑only logins.
- You are comfortable running a simple Python script locally and want a transparent, inspectable migration process that operates entirely on your machine.

## Prerequisites

- Python 3.7 or higher
- `pandas` library (see `requirements.txt`, which specifies `pandas>=1.0.0`)

Install pandas using pip if not already installed:

```
pip install pandas
```

## Export your passwords

1. Export your Bitwarden vault CSV from your Bitwarden web vault.
2. Export your passwords from Apple Passwords (iCloud Keychain) as a CSV.

## Usage

Clone this repo and navigate to it in your terminal. Then run:

```
python apple_passwords_to_bitwarden.py -b path/to/bitwarden.csv -a path/to/apple_passwords.csv -o output.csv
```

The script will print progress messages indicating loading status, number of entries processed, and how many missing entries were found and written.

### Optional arguments

- `--apple-url-col`, `--apple-user-col`, `--apple-pass-col`, `--apple-title-col`, `--apple-notes-col`, `--apple-totp-col`  
  Customize Apple CSV column names if your export differs. Defaults match typical Apple Passwords export columns (`URL`, `Username`, `Password`, `Title`, `Notes`, `OTPAuth`).

- `--marker`  
  Specify a custom note marker to append in the output notes field. Default: `"Migrated from Apple Passwords"`. Use empty string `""` to disable.

### Example

```
python apple_passwords_to_bitwarden.py -b bitwarden_export.csv -a ApplePasswords.csv -o migrated.csv --marker "Migrated on 2025-11-25"
```

## Importing back to Bitwarden

1. Go to your Bitwarden web vault.
2. Navigate to Tools > Import Data.
3. Select “Bitwarden CSV” as format.
4. Upload the generated CSV file from the script.
5. Review and confirm the import.

## Why this tool exists

Apple Passwords and Bitwarden both support CSV, but their columns, URL formats, and handling of entries differ enough that a straightforward import often results in conflicts or duplicates. Neither Apple Passwords nor Bitwarden automatically deduplicates entries when you import, so a naive “export from Apple, import into Bitwarden” workflow can leave you with a cluttered vault.

This script was built to solve that problem by normalizing domains and usernames, comparing what Bitwarden already has against what Apple Passwords contains, and then outputting only the Apple entries that are not already present in Bitwarden.

## Background

This project started as a way to solve a common pain: getting years of saved logins out of Apple’s iCloud Keychain/Safari passwords and into Bitwarden without manually copying entries or creating duplicates. Apple’s export options are limited and do not map cleanly to Bitwarden’s import format, especially when dealing with different URL forms and usernames.

## Why move off Apple Passwords?

Apple’s built‑in password storage works reasonably well inside the Apple ecosystem, but it is not designed as a portable, cross‑platform password manager. Export and import options are limited, automation is minimal, and it is harder to audit or extend your setup compared with dedicated tools.

Bitwarden focuses on password management as its core product: it is open‑source, supports multiple platforms, and provides documented import/export and advanced features like shared vaults and strong client‑side encryption. For users who care about data portability, independent security review, and long‑term flexibility, moving critical credentials into a specialized manager like Bitwarden can be a more privacy‑ and security‑aligned choice than relying solely on a vendor‑locked keychain.

## Features

- Identifies Apple Passwords entries not yet in Bitwarden by comparing normalized URLs and usernames.
- Outputs a Bitwarden‑importable CSV with only missing entries, so you can import without flooding your vault with duplicates.
- Supports customizable column headers and flexible note‑marking.
- Simple command‑line interface with helpful error messages.
- Provides basic progress messages during execution for improved user feedback.

## Security notes

- Always handle exported CSV files carefully; they contain plaintext passwords.
- Run this script locally; do not upload exports to untrusted environments.
- Delete exported CSVs from your system immediately after use.

## License

This project is licensed under the MIT License. See `LICENSE` for details.

## Contributions

Contributions and improvements are welcome. Please open issues or submit pull requests on GitHub.