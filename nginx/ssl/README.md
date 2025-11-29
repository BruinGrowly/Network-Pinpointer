# SSL Certificate Directory

Place your SSL certificates here for HTTPS support.

Required files:
- cert.pem (or fullchain.pem) - SSL certificate
- key.pem (or privkey.pem) - Private key

For Let's Encrypt certificates:
- Use certbot or similar tools
- Copy files from /etc/letsencrypt/live/your-domain/

For self-signed certificates (development only):
  openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout key.pem -out cert.pem \
    -subj '/CN=localhost'

IMPORTANT: Never commit private keys to version control!

