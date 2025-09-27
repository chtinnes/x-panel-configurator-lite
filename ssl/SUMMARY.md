# SSL Certificate Summary

## 📁 Files in this Directory

| File | Purpose | Status |
|------|---------|---------|
| `generate-certificates.sh` | 🔧 Automated SSL certificate generation | ✅ Executable |
| `localhost.conf` | ⚙️ OpenSSL configuration with SAN entries | ✅ Ready |
| `localhost.key` | 🔐 Private key (generated) | ⚠️ Keep secure |
| `localhost.crt` | 📜 SSL certificate (generated) | ✅ Valid 1 year |
| `README.md` | 📖 Comprehensive SSL documentation | ✅ Complete |
| `DIGIKEY_OAUTH_SETUP.md` | 🔌 DigiKey OAuth integration guide | ✅ Complete |
| `HTTPS_CONFIGURATION.md` | 🌐 HTTPS setup instructions | ✅ Complete |

## 🚀 Quick Commands

```bash
# Generate certificates
./generate-certificates.sh

# Check certificate validity
openssl x509 -in localhost.crt -noout -dates

# View certificate details
openssl x509 -in localhost.crt -text -noout
```

## ⚠️ Important Notes

- **Development Only**: These are self-signed certificates for local development
- **DigiKey Requirement**: HTTPS is mandatory for DigiKey OAuth integration
- **Browser Warnings**: You'll need to accept certificate warnings in your browser
- **Callback URL**: DigiKey OAuth callback must be `https://localhost:3000/template-sync/callback`

## 🔗 Related Files

- [`../switch-config.sh`](../switch-config.sh) - HTTP/HTTPS configuration switcher
- [`../.vscode/tasks.json`](../.vscode/tasks.json) - VS Code HTTPS server tasks
- [`../frontend/.env.local`](../frontend/.env.local) - Frontend HTTPS configuration