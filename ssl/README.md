# SSL Certificate Configuration for Development

This directory contains SSL certificates and configuration files for HTTPS development.

## Quick Setup

Run the certificate generation script:

```bash
./generate-certificates.sh
```

This will create:
- `localhost.key` - Private key
- `localhost.crt` - SSL certificate
- `localhost.conf` - OpenSSL configuration

## Manual Certificate Generation

If you need to regenerate certificates manually:

```bash
openssl req -new -newkey rsa:2048 -days 365 -nodes -x509 \
  -keyout localhost.key \
  -out localhost.crt \
  -config localhost.conf
```

## Certificate Details

- **Validity**: 365 days
- **Key Size**: 2048-bit RSA
- **Subject Alternative Names**: localhost, 127.0.0.1, ::1
- **Usage**: Development only - self-signed certificates

## Browser Acceptance

For development, you'll need to accept the self-signed certificate warnings in your browser:

1. Navigate to `https://localhost:3000` (frontend) and `https://localhost:8001` (backend)
2. Click "Advanced" → "Proceed to localhost (unsafe)"
3. Accept the certificate for both URLs

## DigiKey OAuth Requirement

**Important**: DigiKey OAuth integration requires HTTPS. The frontend callback URL must use HTTPS:
- Callback URL: `https://localhost:3000/template-sync/callback`
- This URL must be configured in your DigiKey API application settings

## Configuration Files

- `localhost.conf` - OpenSSL configuration with SAN entries
- `generate-certificates.sh` - Automated certificate generation script
- `README.md` - This documentation file

## Security Note

⚠️ **Development Only**: These are self-signed certificates intended for local development only. Never use self-signed certificates in production environments.