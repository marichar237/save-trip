from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Preformatted

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='DocTitle', parent=styles['Title'], fontName='Helvetica-Bold', fontSize=23, leading=28, alignment=TA_CENTER, textColor=colors.HexColor('#123047'), spaceAfter=6))
styles.add(ParagraphStyle(name='Sub', parent=styles['Normal'], fontSize=9.5, leading=13, alignment=TA_CENTER, textColor=colors.HexColor('#52606d'), spaceAfter=14))
styles.add(ParagraphStyle(name='Section', parent=styles['Heading2'], fontName='Helvetica-Bold', fontSize=13, leading=16, textColor=colors.HexColor('#0b7285'), spaceBefore=10, spaceAfter=4))
code = ParagraphStyle(name='SQL', fontName='Courier', fontSize=7.2, leading=9.3, leftIndent=5, rightIndent=5, borderColor=colors.HexColor('#d9e2ec'), borderWidth=.5, borderPadding=6, backColor=colors.HexColor('#f8fafc'), spaceAfter=8)

sections = [
('Connect and databases', "-- Terminal\nmysql -u root -p\nmysql -u username -p database_name\n\nSHOW DATABASES;\nCREATE DATABASE IF NOT EXISTS mydb;\nUSE mydb;\nDROP DATABASE mydb;"),
('Tables', "SHOW TABLES;\nDESCRIBE users;\nSHOW CREATE TABLE users;\n\nCREATE TABLE users (\n  id INT AUTO_INCREMENT PRIMARY KEY,\n  name VARCHAR(100) NOT NULL,\n  email VARCHAR(255) UNIQUE,\n  age INT,\n  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP\n);\n\nALTER TABLE users ADD COLUMN phone VARCHAR(30);\nALTER TABLE users MODIFY COLUMN name VARCHAR(150);\nALTER TABLE users CHANGE COLUMN phone mobile VARCHAR(30);\nALTER TABLE users DROP COLUMN mobile;\nALTER TABLE users ADD INDEX idx_email (email);\nALTER TABLE users DROP INDEX idx_email;\nRENAME TABLE users TO customers;\nTRUNCATE TABLE users;\nDROP TABLE IF EXISTS users;"),
('Insert data', "INSERT INTO users (name, email, age)\nVALUES ('Ada', 'ada@example.com', 30);\n\nINSERT INTO users (name, email)\nVALUES ('Grace', 'grace@example.com'), ('Linus', 'linus@example.com');\n\nINSERT IGNORE INTO users (name, email) VALUES ('Ada', 'ada@example.com');\n\n-- MySQL upsert\nINSERT INTO users (name, email, age) VALUES ('Ada', 'ada@example.com', 31)\nON DUPLICATE KEY UPDATE age = VALUES(age);"),
('Read and filter', "SELECT * FROM users;\nSELECT id, name FROM users;\nSELECT DISTINCT age FROM users;\nSELECT * FROM users WHERE age >= 18;\nSELECT * FROM users WHERE name LIKE 'A%';\nSELECT * FROM users WHERE age BETWEEN 18 AND 65;\nSELECT * FROM users WHERE age IN (20, 25, 30);\nSELECT * FROM users WHERE email IS NULL;\nSELECT * FROM users ORDER BY created_at DESC LIMIT 10;\nSELECT * FROM users LIMIT 10 OFFSET 20;"),
('Update, delete, and aggregates', "UPDATE users SET age = 31 WHERE id = 1;\nDELETE FROM users WHERE id = 1;\n\nSELECT COUNT(*) FROM users;\nSELECT AVG(age), MIN(age), MAX(age), SUM(age) FROM users;\nSELECT age, COUNT(*) AS total FROM users GROUP BY age HAVING COUNT(*) > 1;"),
('Joins and relationships', "SELECT u.name, o.total FROM users AS u\nINNER JOIN orders AS o ON o.user_id = u.id;\n\nSELECT u.name, o.total FROM users u\nLEFT JOIN orders o ON o.user_id = u.id;\n\nCREATE TABLE orders (\n  id INT AUTO_INCREMENT PRIMARY KEY,\n  user_id INT NOT NULL,\n  total DECIMAL(10,2) NOT NULL,\n  FOREIGN KEY (user_id) REFERENCES users(id)\n    ON DELETE CASCADE ON UPDATE CASCADE\n);"),
('Views and transactions', "CREATE VIEW adult_users AS SELECT * FROM users WHERE age >= 18;\nSELECT * FROM adult_users;\nDROP VIEW adult_users;\n\nSTART TRANSACTION;\nUPDATE users SET age = age + 1 WHERE id = 1;\nCOMMIT;\nROLLBACK;"),
('Users, permissions, and tools', "CREATE USER 'appuser'@'localhost' IDENTIFIED BY 'strong_password';\nGRANT SELECT, INSERT, UPDATE, DELETE ON mydb.* TO 'appuser'@'localhost';\nFLUSH PRIVILEGES;\nREVOKE DELETE ON mydb.* FROM 'appuser'@'localhost';\nDROP USER 'appuser'@'localhost';\n\n-- Terminal backup / restore\nmysqldump -u root -p mydb > backup.sql\nmysql -u root -p mydb < backup.sql\n\nSHOW PROCESSLIST;\nSHOW VARIABLES;\nSHOW STATUS;\nEXPLAIN SELECT * FROM users WHERE email = 'ada@example.com';")]

def footer(canvas, doc):
    canvas.saveState(); canvas.setStrokeColor(colors.HexColor('#d9e2ec')); canvas.line(18*mm, 14*mm, 192*mm, 14*mm)
    canvas.setFont('Helvetica', 7.5); canvas.setFillColor(colors.HexColor('#627d98'))
    canvas.drawString(18*mm, 9*mm, 'MySQL Command Cheat Sheet'); canvas.drawRightString(192*mm, 9*mm, f'Page {doc.page}'); canvas.restoreState()

story = [Paragraph('MySQL Command Cheat Sheet', styles['DocTitle']), Paragraph('Everyday commands for creating, querying, managing, and maintaining MySQL databases.', styles['Sub'])]
for title, body in sections: story.extend([Paragraph(title, styles['Section']), Preformatted(body, code)])
doc = SimpleDocTemplate('mysql-command-cheat-sheet.pdf', pagesize=A4, rightMargin=18*mm, leftMargin=18*mm, topMargin=16*mm, bottomMargin=20*mm)
doc.build(story, onFirstPage=footer, onLaterPages=footer)
