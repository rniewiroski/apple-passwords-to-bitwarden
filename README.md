# Apple Passwords to Bitwarden Migration

This tool helps Mac users migrate missing password entries from Apple Passwords CSV exports into Bitwarden's CSV import format. It assists in consolidating password vaults securely and avoiding duplicates during migration.

## Features

- Identifies Apple Passwords entries not yet in Bitwarden by comparing normalized URLs and usernames
- Outputs a Bitwarden-importable CSV with only missing entries
- Supports customizable column headers and flexible note-marking
- Simple command-line interface with helpful error messages

## Prerequisites

- Python 3.7 or higher
- [pandas](https://pandas.pydata.org/) library

Install pandas using pip if not already installed:

`pip install pandas`

## Export Your Passwords

1. Export your Bitwarden vault CSV from your Bitwarden web vault.
2. Export your passwords from Apple Passwords (iCloud Keychain) as a CSV.

## Usage

Clone this repo and navigate to it in your terminal. Then run:

`python apple_passwords_to_bitwarden.py -b path/to/bitwarden.csv -a path/to/apple_passwords.csv -o output.csv`

### Optional Arguments

- `--apple-url-col`, `--apple-user-col`, `--apple-pass-col`, `--apple-title-col`, `--apple-notes-col`, `--apple-totp-col`  
  Customize Apple CSV column names if your export differs. Defaults match typical Apple Passwords export columns.

- `--marker`  
  Specify a custom note marker to append in the output notes field. Default: `"Migrated from Apple Passwords"`. Use empty string `""` to disable.

### Example

`python apple_passwords_to_bitwarden.py -b bitwarden_export.csv -a ApplePasswords.csv -o migrated.csv –marker “Migrated on 2025-11-25”`

## Importing Back to Bitwarden

1. Go to your Bitwarden web vault.
2. Navigate to Tools > Import Data.
3. Select "Bitwarden CSV" as format.
4. Upload the generated CSV file from the script.
5. Review and confirm the import.

## Security Notes

- Always handle exported CSV files carefully; they contain plaintext passwords.
- Run this script locally; do not upload to untrusted environments.
- Delete exported CSVs from your system immediately after use.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Contributions

Contributions and improvements are welcome! Please open issues or submit pull requests on GitHub.