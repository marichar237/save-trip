# SAVE-TRIP

Multi-agency Cameroon bus-travel platform written in PHP, HTML, CSS, and MySQL.

## Install

1. Create a MySQL database by importing `database/schema.sql`.
2. Edit `config/config.php` with database credentials and the deployed `APP_URL`.
3. Configure Apache/Nginx to serve `public/` as the document root; enable PHP PDO MySQL.
4. Create the developer user with a real `password_hash()` value (the SQL comment shows the query), then sign in.
5. In production, configure SMTP, Google/Apple OAuth, map provider, and official MTN MoMo/Orange Money/card provider credentials. Configure signed payment webhooks before accepting live payments.

## Security model

Agency records are assigned an `agency_id`. Agency manager pages derive it exclusively from the authenticated session (`tenant_id()`), and all agency data queries must filter by it. Developer is the only role permitted to create, activate, deactivate, or delete agencies. PDO prepared statements, CSRF tokens, password hashing, session regeneration, output escaping and activity logs are included.

## Included workflows

Customer registration/login, searchable scheduled trips, atomic seat holds, payment handoff/confirmation demo, tickets with QR verification and basic PHP-generated PDF download, agency isolation foundations, and global developer agency management.

## Update existing installations

If you imported the original schema before the agency operations update, import `database/migration_001_operations.sql` once. The application now includes email verification, reset-password completion, customer profiles, notifications, customer cancellation, agency-managed buses/drivers/employees/routes/trips, global developer listings, and a basic platform report.

## Before accepting real payments

The payment confirmation route is explicitly a demo workflow. Replace it with each provider's server-to-server signed webhook; validate the signature and provider transaction amount/reference before changing a reservation to `confirmed`. Never put production API keys in committed source code.

## Scheduled housekeeping

Run `php cron/expire_reservations.php` every five minutes through Windows Task Scheduler or a hosting cron job. It expires abandoned reservations and returns their seats to the trip inventory.
