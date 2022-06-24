# QR code maker for Authenticator Plus data exports

For a long time I used a two-factor authentication (2FA) app on Android called [Authenticator Plus](https://www.authenticatorplus.com/). However, in 2019 its author vanished and it started decaying from lack of updates. First its cloud backup feature stopped working due to changes in Android, then, as of Android 11, the feature for exporting its data to plain text also broke. However, it is still possible to use the feature that copies the data to an encrypted database, and as that&rsquo;s in a standard format we can get the data out.

This small Python utility script generates QR codes from the extracted data, which you can then scan into a different 2FA app.

## 1: Get the database

Open Authenticator Plus and go to *Settings* &rarr; *Backup & Restore*. Tap *Backup to Sd Card*. Where precisely that destination is in your filesystem will vary by device, but the path is shown there.

Use a method of your choice to copy the `authplus.db` file to the computer you&rsquo;re using this script on.

## 2: Extract the data

Getting this script to be able to open an encrypted SQLite database would make it significantly more complicated for me to write, so we&rsquo;re handling that part with a separate tool.

Install [DB Browser for SQLite](https://sqlitebrowser.org/). When installing, pick the version with SQLCipher support.

Run *DB Browser (SQLCipher)*. Click *Open Database* and choose the `authplus.db` file. In *Encryption settings*, pick &ldquo;SQLCipher 3 defaults&rdquo;. Enter your Authenticator Plus password.

Put this query into the `Execute SQL` tab and click the play (▶️) button:

```sql
SELECT issuer, email AS label, secret FROM accounts
```

Click the result pane, select all (Ctrl-A), copy, paste into a text file. Save in the same directory as this script, named `export.csv`.

## 3: Clean up the data if necessary

Look at the `issuer` column in the results in DB Browser. If it&rsquo;s empty in any rows, open the CSV file in your text editor and add something on those lines. Separate it with a tab character from the label that follows, like in the other entries.

## 4: Install prerequisites for the script

In a terminal:
```sh
pip install pillow qrcode rich
```

## 5: Run the script

In a terminal:
```sh
python generate-qr-codes.py
```

You should see the names of your services and some identifying info for each printed out to the terminal. In the `qr` directory you&rsquo;ll now find PNG images with a QR code for each service. You can scan those into your new 2FA app as usual.

# Notes

The idea of extracting the data with SQL and using Python to generate the QR codes came from [this blog post by Nigel Sim](https://blog.nigelsim.org/2021-01-15-extracting-authenticator-plus/). Thanks!

I&rsquo;m not a Python programmer usually so unfortunately can&rsquo;t offer any support if something goes wrong with this script (dependency issues or the like). If you do encounter an issue and are able to fix it, please file a PR.

Good luck!
