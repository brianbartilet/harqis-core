# Create the empty volume first
docker volume create n8n_data

# Restore into it
docker run --rm \
  -v n8n_data:/data \
  -v "$PWD:/backup" \
  alpine sh -c "cd /data && tar xzf ../backups/n8n/$1.tgz"