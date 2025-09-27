#!/bin/bash

# SSL Certificate Generation Script for Development
# Generates self-signed certificates for localhost development with HTTPS

set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR"

echo "🔐 Generating SSL certificates for localhost development..."

# Check if OpenSSL is available
if ! command -v openssl &> /dev/null; then
    echo "❌ Error: OpenSSL is not installed or not in PATH"
    echo "   Install OpenSSL and try again"
    exit 1
fi

# Remove existing certificates
echo "📁 Cleaning up existing certificates..."
rm -f localhost.key localhost.crt

# Create OpenSSL configuration if it doesn't exist
if [ ! -f "localhost.conf" ]; then
    echo "📝 Creating OpenSSL configuration..."
    cat > localhost.conf << EOF
[req]
distinguished_name = req_distinguished_name
req_extensions = v3_req
prompt = no

[req_distinguished_name]
C = US
ST = CA
L = San Francisco
O = Development
OU = LocalDev
CN = localhost

[v3_req]
keyUsage = keyEncipherment, dataEncipherment
extendedKeyUsage = serverAuth
subjectAltName = @alt_names

[alt_names]
DNS.1 = localhost
DNS.2 = 127.0.0.1
IP.1 = 127.0.0.1
IP.2 = ::1
EOF
fi

# Generate the certificate
echo "🔑 Generating SSL certificate and private key..."
openssl req -new -newkey rsa:2048 -days 365 -nodes -x509 \
    -keyout localhost.key \
    -out localhost.crt \
    -config localhost.conf

# Set appropriate permissions
chmod 600 localhost.key
chmod 644 localhost.crt

echo "✅ SSL certificates generated successfully!"
echo ""
echo "📄 Files created:"
echo "   - localhost.key (private key)"
echo "   - localhost.crt (certificate)"
echo "   - localhost.conf (OpenSSL config)"
echo ""
echo "🌐 Certificate details:"
openssl x509 -in localhost.crt -text -noout | grep -A 3 "Subject Alternative Name" || true
echo ""
echo "📅 Certificate validity:"
openssl x509 -in localhost.crt -noout -dates
echo ""
echo "🚀 Next steps:"
echo "   1. Start your HTTPS servers using VS Code tasks"
echo "   2. Accept certificate warnings in your browser"
echo "   3. Configure DigiKey OAuth with: https://localhost:3000/template-sync/callback"
echo ""
echo "⚠️  Note: These are self-signed certificates for development only"